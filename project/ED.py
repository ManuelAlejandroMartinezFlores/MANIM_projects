from manim import *


class F1(Scene):
    def construct(self):
        self.add(ArrowVectorField(lambda p: [0.5, -0.5 * p[0]/(p[1] + 1e-6), 0]))
        self.add(NumberPlane())
        
class F2(Scene):
    def construct(self):
        self.add(ArrowVectorField(lambda p: [0.5, 0.1*p[0]**2 + 0.5 * p[1], 0]))
        self.add(NumberPlane())
   
   
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
from manim.opengl import * 

config.write_to_movie = False
config.renderer = "opengl"       

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
        
        
        
        
        
        
        
        