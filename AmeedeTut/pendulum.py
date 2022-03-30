from manim import *
import numpy as np


class Pendulum(Scene):
    def construct(self):
        time = ValueTracker(0)
        theta_max = 15 * DEGREES 
        l = 4
        g = 9.8
        w = np.sqrt(g / l)
        T = 2 * PI / w
        
        
        theta = DecimalNumber().move_to(10*RIGHT)
        theta.add_updater(lambda m: m.set_value(theta_max * np.cos(w * time.get_value())))
        
        self.add(theta)
        
        dot = always_redraw(
            lambda: Dot().scale(2).move_to(
                RIGHT * l * np.sin(theta.get_value()) + UP * l * (1 - np.cos(theta.get_value())) + DOWN
            )
        )
        line = always_redraw(
            lambda: Line(
                3 * UP,
                dot.get_center()
            )
        )
        
        self.add(line, dot)
        self.play(time.animate.set_value(7), run_time = 10, rate_func = linear)
        
        
        
        