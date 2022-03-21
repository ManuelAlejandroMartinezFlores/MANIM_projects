import numpy as np
from manim import *


class Mobject_1(Scene):
    def construct(self):
        box = Rectangle(stroke_color=GREEN_C, stroke_opacity=0.7,
                        fill_color=RED_B, fill_opacity=0.5,
                        height=1, width=1)
        
        n_p = NumberPlane()
        
        dot = Dot(box.get_center())
        dot.add_updater(lambda d: d.move_to(box.get_center()))
        
        self.add(box, n_p, dot)
        self.play(box.animate.shift(RIGHT*2), run_time=2)
        self.play(box.animate.shift(UP*3), run_time=2)
        self.play(box.animate.shift(DOWN*5 + LEFT*5), run_time=2)
        self.play(box.animate.shift(UP*1.5 + RIGHT), run_time=2)
        self.wait()
        
        
class FittingObjects(Scene):
    def construct(self):
        axes = Axes(x_range=[-3, 3, 1], y_range=[-3, 3, 1],
                    x_length=6, y_length=6)
        axes.to_edge(LEFT, buff=0.5)
        
        circle = Circle(stroke_width=6, stroke_color=YELLOW,
                        fill_color=RED_C, fill_opacity=0.8)
        circle.set_width(2).to_edge(DR, buff=0)
        
        triangle = Triangle(stroke_color=ORANGE, stroke_width=10,
                            fill_color=GREY).set_height(2).shift(DOWN*3+RIGHT*3)
        
        self.play(Write(axes))
        self.play(DrawBorderThenFill(circle))
        self.play(circle.animate.set_width(1))
        self.play(Transform(circle, triangle), run_time=3)
        self.wait()
        
        
class Updaters(Scene):
    def construct(self):
        rect = RoundedRectangle(
            stroke_width = 8,
            stroke_color = WHITE,
            fill_color = BLUE,
            width = 4.5,
            height = 2
        ).shift(UP*2 + LEFT*3)
        
        mt = MathTex('\\frac{3}{4}=0.75'
                     ).set_color_by_gradient(GREEN, PINK).set(height=1.5)
        mt.move_to(rect.get_center())
        mt.add_updater(
            lambda x: x.move_to(rect.get_center())
        )
        
        self.play(FadeIn(rect))
        self.play(Write(mt))
        self.play(rect.animate.shift(RIGHT*1.5 + DOWN*4), run_time=6)
        self.wait()
        mt.clear_updaters()
        self.play(rect.animate.shift(LEFT*2 + UP), run_time=6)
        self.wait()
        
        
class Updater2(Scene):
    def construct(self):
        r = ValueTracker(0.5)
        
        circle = always_redraw(
            lambda :
                Circle(radius = r.get_value(), stroke_color=YELLOW,
                       stroke_width = 5)
        )
        
        line_radius = always_redraw(
            lambda :
                Line(circle.get_center(), circle.get_bottom(),
                     stroke_color=RED_B, stroke_width=10)
        )
        
        line_circ = always_redraw(
            lambda :
                Line(stroke_color=YELLOW, stroke_width=5,
                     ).set_length(2 * r.get_value() * PI).next_to(circle, DOWN, buff=0.2)
        )
        
        triangle = always_redraw(
            lambda :
                Polygon(circle.get_top(),
                        circle.get_left(),
                        circle.get_right(),
                        fill_color=GREEN_C)
        )
        
        self.play(LaggedStart(
            Create(circle), DrawBorderThenFill(line_radius), 
            DrawBorderThenFill(triangle), run_time=4, lag_ratio=0.75
        ))
        self.play(ReplacementTransform(circle.copy(), line_circ), run_time=2)
        self.play(r.animate.set_value(2), run_time=5)
        self.wait()
        
        

class GraphingMovement(Scene):
    def construct(self):
        axes = Axes(
            x_range = [0, 5, 1],
            y_range = [0, 3, 1],
            x_length = 5,
            y_length = 3,
            axis_config = {'include_tip': True,
                           'numbers_to_exclude': [0]}
        ).add_coordinates()
        
        axes.to_edge(UR)
        axis_labels = axes.get_axis_labels(x_label = 'x',
                                           y_label = 'f(x)')
        
        graph = axes.plot(lambda x : x**0.5, color = YELLOW)
        graphing_stuff = VGroup(axes, graph, axis_labels)
        
        self.play(DrawBorderThenFill(axes),
                  Write(axis_labels))
        self.play(Create(graph))
        self.play(graphing_stuff.animate.shift(DOWN*3))
        self.play(axes.animate.shift(LEFT*3), run_time = 3)
        self.wait()
        
class Graphing(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range = [-6, 6],
            x_length = 5,
            y_range = [-10, 10],
            y_length = 5
        )
        
        func = plane.plot(lambda x: 0.1*(x-5)*x*(x+5),
                          x_range = [-5, 5],
                          color = GREEN_B)
        
        area = plane.get_area(graph = func,
                              x_range = [-5, 5],
                              color = [BLUE, YELLOW])
        label = MathTex("f(x)=0.1x(x-5)(x+5)")
        label.next_to(plane, UP, buff=0.2)
        
        hor_line = Line(
            plane.c2p(0, func.underlying_function(-2)),
            plane.c2p(-2, func.underlying_function(-2)),
            stroke_color = YELLOW
        )
        
        self.play(DrawBorderThenFill(plane))
        self.play(Create(func), Write(label))
        self.play(FadeIn(area))
        self.play(Create(hor_line))
        self.wait()
        
        
class CoordinateSystem(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range = [-4, 4, 1],
            x_length = 4,
            y_range = [0, 20, 5],
            y_length = 4
        ).add_coordinates()
        plane.shift(LEFT * 3 + DOWN * 1.5)
        plane_graph = plane.plot(lambda x: x**2,
                                 x_range= [-4, 4],
                                 color = GREEN)
        area = plane.get_riemann_rectangles(graph = plane_graph,
                                            x_range = [-2, 2],
                                            dx = 0.05)
        
        axes = Axes(
            x_range = [-4, 4, 1],
            x_length = 4,
            y_range = [-20, 20, 5],
            y_length = 4,
        ).add_coordinates()
        axes.shift(RIGHT * 3 + DOWN * 1.5)
        axes_graph = axes.plot(lambda x: 2*x,
                               x_range = [-4, 4],
                               color = YELLOW)
        v_lines = axes.get_vertical_lines_to_graph(
            graph = axes_graph,
            x_range = [-3, 3],
            num_lines = 12
        )
        
        self.play(Write(plane), Create(axes))
        self.play(Create(plane_graph),
                  Create(axes_graph),
                  run_time = 2)
        self.play(Create(v_lines),
                  Create(area))
        self.wait()
        
        
class PolarGraph(Scene):
    def construct(self):
        e = ValueTracker(0.01)
        
        plane = PolarPlane(radius_max = 3).add_coordinates()
        plane.shift(LEFT*2)
        graph1 = always_redraw(
            lambda :
                ParametricFunction(lambda t: plane.polar_to_point(2*np.sin(3*t), t),
                                   t_range = [0, e.get_value()],
                                   color = GREEN)                
        )
        
        dot = always_redraw(
            lambda :
                Dot(fill_color = GREEN,
                    fill_opacity = 0.8).scale(
                        0.5
                    ).move_to(
                        graph1.get_end()
                    )
        )
        
        axes = Axes(
            x_range = [0, 4, 1],
            x_length = 3,
            y_range = [-3, 3, 1],
            y_length = 3
        ).shift(RIGHT*4).add_coordinates()
        graph2 = always_redraw(
            lambda :
                axes.plot(lambda x: 2*np.sin(3*x),
                          x_range = [0, e.get_value()],
                          color = GREEN)
        )
        dot2 = always_redraw(
            lambda :
                Dot(fill_color = GREEN,
                    fill_opacity = 0.8).scale(
                        0.5
                    ).move_to(
                        graph2.get_end()
                    )
        )
        
        title = MathTex(
            'f(\\theta) = 2 \\sin (3\\theta)',
            color = GREEN
        ).next_to(
            axes,
            UP,
            buff = 0.2
        )
        
        self.play(LaggedStart(
            Write(plane), 
            Create(axes),
            Write(title),
            run_time = 3, 
            lag_ratio = 0.5
        ))
        self.play(
            Create(graph1),
            Create(graph2),
            Create(dot),
            Create(dot2)
        )
        self.play(e.animate.set_value(PI),
                  run_time = 10, 
                  rate_func = linear)
        self.wait()
        
    