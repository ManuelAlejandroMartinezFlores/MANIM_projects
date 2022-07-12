from manim import *


class F1(Scene):
    def construct(self):
        self.add(ArrowVectorField(lambda p: [0.5, -0.5 * p[0]/(p[1] + 1e-6), 0]))
        self.add(NumberPlane())
        
class F2(Scene):
    def construct(self):
        self.add(ArrowVectorField(lambda p: [0.5, 0.1*p[0]**2 + 0.5 * p[1], 0]))
        self.add(NumberPlane())
        
class F3(Scene):
    def construct(self):
        p = NumberPlane()
        self.add(p)
        self.add(p.plot(lambda x: -2))
        self.add(p.plot(lambda x: 2))
        self.add(p.plot(lambda x: 0))
        self.add(ArrowVectorField(lambda p: [0.5, 0.5*p[1]**2 * (4 - p[1]**2), 0]))
        
   
   
def get_graph(point, plane:NumberPlane, color=BLUE):
    c = (point[1] + 0.2 * (point[0] ** 2 + 2 * point[0] + 2)) * np.exp(-point[0])
    graph = plane.plot(lambda x : -0.2 * (x**2 + 2 * x + 2) + c * np.exp(x), x_range=[point[0], point[0]])
    graph.set_color(color)
    return graph


class DrawGraph(Animation):
    def __init__(self, mobject, point, plane, color=BLUE, **kwargs):
        super().__init__(mobject, **kwargs)
        self.plane = plane
        self.color = color
        self.point = point 
        self.f = lambda x: mobject.underlying_function(x)
        
    def begin(self) -> None:
        super().begin()
        
    def clean_up_from_scene(self, scene: Scene) -> None:
        super().clean_up_from_scene(scene)
        
    def interpolate_mobject(self, alpha: float) -> None:
        alpha = self.rate_func(alpha) 
        x = self.point[0]
        xp = (7 - x) * alpha + x
        xn = -(x + 7) * alpha + x
        
        self.mobject.become(self.plane.plot(lambda x: self.f(x), x_range=[xn, xp]).set_color(self.color))
        
        
        
class PVI(Scene):
    def construct(self):
        plane = NumberPlane()
        self.add(plane)
        self.add(ArrowVectorField(lambda p: [0.5, 0.1*p[0]**2 + 0.5 * p[1], 0]))
        do = Dot().move_to([0, 1/2, 0]).set_color(ORANGE)
        db = Dot().move_to([2, -1, 0]).set_color(BLUE)
        go = get_graph(do.get_center(), plane, ORANGE)
        gb = get_graph(db.get_center(), plane, BLUE)
        self.play(Create(do))
        self.play(DrawGraph(go, do.get_center(), plane, ORANGE), run_time=2)
        self.play(Create(db))
        self.play(DrawGraph(gb, db.get_center(), plane, BLUE), run_time=2)
        
        
 
 
# Interactive
# from manim.opengl import * 

# config.write_to_movie = False
# config.renderer = "opengl"       

class PVIInter(Scene):
    def construct(self):
        self.plane = NumberPlane()
        self.add(self.plane)
        self.add(ArrowVectorField(lambda p: [0.5, 0.1*p[0]**2 + 0.5 * p[1], 0]))
        self.dot = Dot().set_color(BLUE)
        self.add(self.dot)
        self.graph = get_graph(self.dot.get_center(), self.plane)
        self.interactive_embed()
        
    def on_key_press(self, symbol, modifiers):
        from pyglet.window import key as pyglet_key
        
        if symbol == pyglet_key.P:
            x, y, z = 2 * self.mouse_point.get_center() + np.array([7, 4, 0])
            self.remove(self.graph)
            self.play(
                self.dot.animate.move_to([x, y, 0])
            )
            self.graph = get_graph(self.dot.get_center(), self.plane)
            self.play(DrawGraph(self.graph, self.dot.get_center(), self.plane), run_time=2, rate_func=linear)
            
        
        super().on_key_press(symbol, modifiers)
        
        
        
class PVI3D(ThreeDScene):
    
    def construct(self):
        axes = ThreeDAxes(
            x_range = [-7.5, 7.5],
            y_range=[-4.5, 4.5],
            x_length=10, 
            y_length=6,
            tips=True
        )
        def f(u, v):
            return -(0.2*u**2 * v + 0.5*v**2)/5
        surf = Surface(lambda u, v: axes.c2p(u, v, f(u, v)), u_range=[-7, 7], v_range=[-4, 4]).set_opacity(0.7)
        t = ValueTracker(2)
        ball = Sphere(radius=0.3).move_to(axes.c2p(2, -1, f(2, -1)) + np.array([0, 0, 0.3])).set_color(RED)
        def sol(x):
            return -0.2*(x**2 + 2*x + 2) + np.exp(x - 2)
        self.add(ball)
        self.add(axes)
        self.add(surf)
        self.move_camera(phi=45*DEGREES, theta=-135*DEGREES)
        self.wait()   
             
        def df(p):
            u, v = p[0], p[1]
            return 0.2*u**2 + v
        
        def move_ball(b, dt):
            dt *= 1e-2
            p = axes.p2c(b.get_center())
            y = dt * df(p) + p[1]
            x = dt + p[0]
            p = (x, y, f(x, y))
            bb = b.copy()
            bb.move_to(axes.c2p(x, y, f(x, y)) + np.array([0, 0, 0.3]))
            b.become(bb)
            
       
       
        def move_ball2(b):
            b.move_to(axes.c2p(t.get_value(), sol(t.get_value()), f(t.get_value(), sol(t.get_value()))) + np.array([0, 0, 0.3]))
            
        
        ball.add_updater(move_ball2)
        self.play(t.animate.set_value(5), run_time=3, rate_func=linear)
        self.wait(3)
        
        
        
        
        