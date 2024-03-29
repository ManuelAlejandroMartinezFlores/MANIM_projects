import numpy as np
from manim import *


class Slopes(Scene):
    def construct(self):
        
        plane = NumberPlane(
            x_range = [-3, 3],
            y_range = [-4, 14],
            y_length = 7,
            x_length = 6
        ).add_coordinates()
        
        graph1 = plane.plot(
            lambda x: x**2, 
            x_range = [-3, 3],
            color = RED
        )
        graph1_lab = (
            MathTex("f(x) = x^2")
            .next_to(graph1, UR, buff = 0.2)
            .set_color(RED)
            .scale(0.8)
        )
        
        c = ValueTracker(-4)
        
        graph2 = always_redraw(
            lambda: plane.plot(
                lambda x: x**2 + c.get_value(),
                x_range = [-3, 3],
                color = YELLOW
            )
        )
        graph2_lab = always_redraw(
            lambda: MathTex("f(x) = x^2 + c")
            .next_to(graph2, UR, buff=0.2)
            .set_color(YELLOW)
            .scale(0.8)
        )
        
        k = ValueTracker(-3)
        dot1 = always_redraw(
            lambda: Dot().move_to(
                plane.c2p(k.get_value(), graph1.underlying_function(k.get_value()))
            )
        )
        slope1 = always_redraw(
            lambda: plane.get_secant_slope_group(
                x = k.get_value(),
                graph = graph1,
                dx = 0.01,
                secant_line_length = 5
            )
        )
        
        dot2 = always_redraw(
            lambda: Dot().move_to(
                plane.c2p(k.get_value(), graph2.underlying_function(k.get_value()))
            )
        )
        slope2 = always_redraw(
            lambda: plane.get_secant_slope_group(
                x = k.get_value(),
                graph = graph2,
                dx = 0.01,
                secant_line_length = 5
            )
        )
        
        self.play(
            LaggedStart(
                DrawBorderThenFill(plane),
                Create(graph1),
                Create(graph2)
            ), run_time = 5, lag_ratio = 1
        )
        self.add(slope1, slope2, dot1, dot2, graph1_lab, graph2_lab)
        self.play(
            k.animate.set_value(3),
            c.animate.set_value(-2),
            run_time = 5,
            rate_func = linear
        )
        self.wait()
        
        

class Area(Scene):
    def construct(self):
        axes = Axes(
            x_range = [-5, 5],
            x_length = 8,
            y_range = [-10, 10],
            y_length = 7
        )
        
        graph = axes.plot(
            lambda x: 0.1 * (x - 4) * (x - 1) * (x + 3),
            x_range = [-5, 5],
            color = YELLOW
        )
        self.add(axes, graph)
        
        dx_list = [1, 0.5, 0.3, 0.1, 0.05, 0.025, 0.01]
        rectangles = VGroup(
            *[
                axes.get_riemann_rectangles(
                    graph = graph,
                    x_range = [-5, 5],
                    stroke_width = 0.1,
                    stroke_color = WHITE,
                    dx = dx
                )
                for dx in dx_list
            ]
        )
        
        first_area = rectangles[0]
        for k in range(1, len(dx_list)):
            new_area = rectangles[k]
            self.play(Transform(first_area, new_area), run_time = 3)
            self.wait(0.3)
            
        self.wait()
        
        
        