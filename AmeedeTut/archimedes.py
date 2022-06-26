from manim import *
import numpy as np


class CircleVsSpiral(Scene):
    def construct(self):
        circ_plane = (
            NumberPlane(
                x_range = [-2, 2],
                y_range = [-2, 2],
                x_length = 5, 
                y_length = 5
            ).to_edge(LEFT)
            .add_coordinates()
        )
        spiral_plane = (
            NumberPlane(
                x_range = [-2, 2],
                y_range = [-2, 2],
                x_length = 5, 
                y_length = 5
            ).to_edge(RIGHT)
            .add_coordinates()
        )
        
        r = ValueTracker(1)
        e = ValueTracker(0.01)
        
        circle = always_redraw(
            lambda: circ_plane.plot_parametric_curve(
                lambda t: np.array(
                    [r.get_value()*np.cos(t), r.get_value()*np.sin(t)]
                ),
                t_range = [0, e.get_value()],
            ).set_color(RED)
        )
        circ_dot = always_redraw(
            lambda: Dot().move_to(circle.get_end())
        )
        
        spiral = always_redraw(
            lambda: spiral_plane.plot_parametric_curve(
                lambda t: np.array(
                    [(r.get_value()/(2*PI))*t*np.cos(t),
                    (r.get_value()/(2*PI))*t*np.sin(t)]
                ),
                t_range = [0, e.get_value()],
            ).set_color([RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE_E, PURPLE_A])
        )
        spiral_dot = always_redraw(
            lambda: Dot().move_to(spiral.get_end())
        )
        
        circle_eq = (
            MathTex("c(t) = [r \\cos (t), r \\sin (t)]")
            .scale(0.7)
            .next_to(circ_plane, DOWN)
        )
        spiral_eq = (
            MathTex("s(t) = [\\frac{r}{2 \\pi} t \\cos (t), \\frac{r}{2 \\pi} t \\sin (t)]")
            .scale(0.7)
            .next_to(spiral_plane, DOWN)
        )
        
        circle_title = Tex("Circle").next_to(circ_plane, UP)
        spiral_title = Tex("Spiral").next_to(spiral_plane, UP)
        
        time_text = Tex("Timer: ").scale(0.7).shift(LEFT*0.3)
        timer_num = always_redraw(
            lambda: DecimalNumber()
            .set_value(e.get_value())
            .scale(0.7)
            .next_to(time_text, RIGHT)
        )
        
        self.play(
            LaggedStart(
                DrawBorderThenFill(VGroup(spiral_plane, circ_plane)),
                Write(VGroup(spiral_eq, circle_eq)),
                Write(VGroup(spiral_title, circle_title)),
                lag_ratio = 0.75,
                run_time = 4
            )
        )
        self.wait()
        self.add(circle, circ_dot, spiral, spiral_dot, time_text, timer_num)
        
        self.play(e.animate.set_value(4*PI), run_time = 4*PI, rate_func = linear)
        self.wait()
        self.play(r.animate.set_value(0.5), run_time = 2)
        self.play(r.animate.set_value(2), run_time = 3)
        self.wait()
        