from math import trunc
import numpy as np
from manim import *


class PrismSurf(ThreeDScene):
    def construct(self):
        l = 2
        w = 4
        h = 1
        
        rect_prism = Prism(
            dimensions = [l, w, h]
        ).to_edge(LEFT, buff = 1)
        
        kwargs = {
            'stroke_color': BLUE_D,
            'fill_color': BLUE_B, 
            'fill_opacity': 0.8
        }
        
        bottom = Rectangle(width = w, height = l, **kwargs)
        s1 = (Rectangle(height = h, width = w, **kwargs)
            .next_to(bottom, UP, buff = 0)
        )
        s2 = (Rectangle(height = h, width = w, **kwargs)
            .next_to(bottom, DOWN, buff = 0)
        )
        l1 = (Rectangle(height = l, width = h, **kwargs)
            .next_to(bottom, LEFT, buff = 0)
        )
        l2 = (Rectangle(height = l, width = h, **kwargs)
            .next_to(bottom, RIGHT, buff = 0)
        )
        top = (Rectangle(height = l, width = w, **kwargs)
            .next_to(s1, UP, buff = 0)
        )
        net = (VGroup(top, bottom, s1, s2, l1, l2)
               .rotate(-PI /2)
               .to_edge(RIGHT, buff = 1)
        )
        
        arrow = Line(
            rect_prism.get_right(),
            net.get_left(),
            buff = 0
        ).add_tip()
        
        self.begin_ambient_camera_rotation()
        self.set_camera_orientation(phi = 45*DEGREES,
                                    theta = 45*DEGREES)
        self.play(Create(rect_prism))
        self.play(
            LaggedStart(
                Create(arrow),
                Transform(rect_prism.copy(), net)
            ),
            run_time = 2,
            lag_ratio = 0.5
        )
        self.wait()
        self.play(FadeOut(Group(*self.mobjects)))
        self.stop_ambient_camera_rotation()
        self.wait()
        
        
class SurfaceArea(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi = 0*DEGREES,
                                    theta = -90*DEGREES)
        
        text = Tex('Surface Area of a Solid of Revolution')
        self.play(Write(text))
        self.wait()
        self.play(FadeOut(text))
        
        self.begin_ambient_camera_rotation()
        self.set_camera_orientation(phi = 45*DEGREES,
                                    theta = -45*DEGREES)
        
        axes = ThreeDAxes(
            x_range = [0, 4.1, 1],
            x_length = 5,
            y_range = [-4, 4, 1],
            y_length = 5,
            z_range = [-4, 4, 1],
            z_length = 5
        ).add_coordinates()
        
        func = axes.plot(
            lambda x: 0.25 * x ** 2,
            x_range = [0, 4],
            color = YELLOW
        )
        area = axes.get_area(
            graph = func,
            x_range = [0, 4],
            color = [BLUE_B, BLUE_D]
        )
        
        surface = Surface(
            lambda u, v: axes.c2p(
                v, 0.25 * v**2 * np.cos(u), 0.25 * v**2 * np.sin(u)
            ),
            u_range = [0, 2 *PI],
            v_range = [0, 4],
            checkerboard_colors = [BLUE_B, BLUE_D]
        )
        
        self.play(
            LaggedStart(
                Create(axes),
                Create(func),
                Create(area),
                Create(surface)
            ),
            run_time = 4,
            lag_ratio = 0.5
        )
        
        self.play(
            Rotating(
                VGroup(func, area),
                axis = RIGHT,
                radians = 2 *PI,
                about_point = axes.c2p(0, 0, 0)
            ),
            run_time = 5,
            rate_func = linear
        )
        self.wait(3)
        

def get_conic_approximations(
    axes, graph, x_min = 0, x_max = 1, dx = 0.05,
    color_A = RED, color_B = GREEN, opacity = 1
):
    result = VGroup()
    for x in np.arange(x_min + dx, x_max + dx, dx):
        if graph.underlying_function(x) == 0:
            k = 0
            conic_surface = VectorizedPoint()
        else:
            k = graph.underlying_function(x)/x
            conic_surface = Surface(
                lambda u, v:
                    axes.c2p(v, k*v*np.cos(u), k*v*np.cos(u)),
                u_range = [0, 2*PI],
                v_range = [x-dx, x],
                checkerboard_colors = [color_A, color_B],
                fill_opacity = opacity
            )
        result.add(conic_surface)
    return result

def get_riemann_truncated_cones(
    axes, graph, x_min = 0, x_max = 1,
    dx = 0.5, color_A = RED, color_B = GREEN, 
    stroke_color = WHITE, stroke_width = 1,
    opacity = 1, theta = 45
):
    result = VGroup()
    for x in np.arange(x_min, x_max, dx):
        p1 = axes.c2p(x + dx, 0)
        p2 = axes.c2p(x + dx, graph.underlying_function(x + dx))
        p3 = axes.c2p(x, graph.underlying_function(x))
        p4 = axes.c2p(x, 0)
        truncated_conic = ArcPolygon(
            p1,
            p2,
            p3,
            p4,
            stroke_color = stroke_color,
            stroke_width = stroke_width,
            fill_color = [color_A, color_B],
            fill_opacity = opacity,
            arc_config = [
                {'angle':theta*DEGREES, 'color':stroke_color},
                {'angle':0, 'color':stroke_color},
                {'angle':-theta*DEGREES, 'color':stroke_color},
                {'angle':0, 'color':stroke_color},
            ]
        )
        result.add(truncated_conic)
    return result


class ConicSurf(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range = [0, 4.1, 1],
            x_length = 5,
            y_range = [-4, 4.1, 1],
            y_length = 5,
            z_range = [-4, 4, 1],
            z_length = 5,
            axis_config = {
                'decimal_number_config': {'num_decimal_places':0}
            }
        ).to_edge(LEFT)
        axes.add_coordinates()
        
        graph = axes.plot(
            lambda x: 0.25 * x ** 2, 
            x_range = [0, 4],
            color = YELLOW
        )
        
        surface = Surface(
            lambda u, v : axes.c2p(
                v, 0.25*v**2*np.cos(u), 0.25*v**2*np.sin(u)
            ),
            u_range = [0, 2*PI],
            v_range = [0, 4],
            checkerboard_colors = [BLUE_B, BLUE_D]
        )
        
        dx = ValueTracker(1)
        conic_approx = always_redraw(
            lambda: get_conic_approximations(
                axes=axes, graph=graph, x_min=0, x_max=4,
                dx = dx.get_value()
            )
        )
        
        num_text = MathTex('dx=').next_to(axes, UP, buff=0.5)
        num = always_redraw(
            lambda: DecimalNumber()
            .set_value(dx.get_value())
            .next_to(num_text, RIGHT, buff=0.1)
        )
        
        axes2 = Axes(
            x_range = [0, 4, 1],
            x_length = 5,
            y_range = [0, 60, 10],
            y_length = 6
        ).to_edge(UR)
        
        def sa_func(x):
            return 0.2832*x*(1+(x**2/4))**0.5
        
        graph2 = axes2.plot(sa_func, x_range=[0,4], color = BLUE)
        graph2_lab = (
            Tex("SA function")
            .next_to(axes2, UP, buff = 0.2)
        )
        
        t = ValueTracker(45)
        
        truncated_area = always_redraw(
            lambda: get_riemann_truncated_cones(
                axes=axes2,
                graph=graph2,
                x_min=0,
                x_max=4,
                dx=dx.get_value(),
                theta=t.get_value()
            )
        )
        
        self.set_camera_orientation(
            phi = 0 *DEGREES, theta = -90 *DEGREES
        )
        self.add(axes, graph, surface, conic_approx, num_text, num)
        self.move_camera(
            phi = 30*DEGREES, theta = -100 *DEGREES
        )
        self.begin_ambient_camera_rotation(rate=0.01)
        self.play(LaggedStart(
            Create(conic_approx),
            Write(VGroup(num_text, num)),
            DrawBorderThenFill(axes2),
            run_time = 1,
            lag_ratio = 0.25
        ))
        self.play(ReplacementTransform(conic_approx.copy(),
                                       truncated_area), run_time = 3),
        self.play(
            dx.animate.set_value(0.1), t.animate.set_value(5),
            run_time = 3
        )
        self.add(graph2, graph2_lab)
        self.wait
        