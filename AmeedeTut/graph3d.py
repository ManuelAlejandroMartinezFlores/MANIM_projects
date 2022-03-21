from manim import *
import numpy as np

class Graph3D1(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range = [-6, 6, 1],
            y_range = [-6, 6, 1],
            z_range = [-6, 6, 1],
            x_length = 8,
            y_length = 6, 
            z_length = 6
        )
        
        graph = axes.plot(
            lambda x: x**2, x_range = [-2, 2, 1], color = YELLOW
        )
        rects = axes.get_riemann_rectangles(
            graph = graph, x_range = [-2, 2], 
            dx = 0.1, stroke_color = WHITE
        )
        
        graph2 = ParametricFunction(
            lambda t: np.array([np.cos(t), np.sin(t), t]),
            t_range=[-2 * PI, 2 * PI],
            color=RED,
        )
        
        self.add(axes, graph)
        self.wait()
        self.move_camera(phi = 60*DEGREES)
        self.wait()
        self.move_camera(theta = -45*DEGREES)
        
        self.begin_ambient_camera_rotation(
            rate = PI/10,
            about = 'theta'
        )
        self.wait()
        self.play(Create(rects), run_time = 3)
        self.play(Create(graph2))
        self.wait()
        self.stop_ambient_camera_rotation()
        self.wait()
        self.begin_ambient_camera_rotation(
            rate = PI/10,
            about = 'phi'
        )
        self.wait(2)
        
        
class ParamSurface(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(
            phi = 60 * DEGREES,
            theta = -45 * DEGREES,
        )
        
        axes = ThreeDAxes()
        graph = axes.plot(lambda x: x**2,
                          x_range = [-2, 2])
        surface = Surface(
            lambda u, v: axes.c2p(v * np.cos(u),
                                  v * np.sin(u),
                                  v ** 2),
            u_range = [0, 2*PI],
            v_range = [0, 3],
            checkerboard_colors = [GREEN, RED]
        )
        
        stuff = VGroup(axes, graph, surface)
        
        self.play(Create(axes), Create(graph))
        self.begin_ambient_camera_rotation(rate = PI/20)
        self.wait()
        self.play(Create(surface))
        self.play(stuff.animate.shift(LEFT * 3))
        self.wait()
        
        
class ParamUpdater(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(
            phi = 45 * DEGREES,
            theta = - 45 * DEGREES
        )
        axes = ThreeDAxes(
            y_range = [-3, 10, 3],
            y_length = 7
        ).add_coordinates()
        
        graph = axes.plot(
            lambda x: x,
            x_range = [0, 3],
            color = RED_B
        )
        
        area_ref = axes.get_area(
            graph = graph, 
            x_range = [0, 3]
        )
        
        e = ValueTracker(0)
        
        area = always_redraw(
            lambda : area_ref.copy().rotate(
                axis = RIGHT,
                angle = e.get_value(),
                about_point = axes.c2p(0,0,0)
            )
        ) 
        
        surface = always_redraw(
            lambda : Surface(
                lambda u, v: axes.c2p(v, v * np.cos(u), v * np.sin(u)),
                u_range = [0, e.get_value()],
                v_range = [0, 3],
                checkerboard_colors = [GREEN, PURPLE]
            )
        )
        
        self.add(axes, surface)
        self.begin_ambient_camera_rotation(rate = PI/15)
        self.play(LaggedStart(
            Create(graph),
            Create(area)
        ))
        self.play(
            # Rotating(
            #     area,
            #     axis = RIGHT,
            #     radians = 2 * PI,
            #     about_point = axes.c2p(0,0,0)
            # ),
            e.animate.set_value(2 * PI),
            run_time = 6,
            rate_func = linear
        )
        self.stop_ambient_camera_rotation()
        self.wait()
        
