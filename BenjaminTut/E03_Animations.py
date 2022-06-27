from manim import *
from colour import Color 
import numpy as np

class BasicAnimations(Scene):
    def construct(self):
        polys = VGroup(
            *[RegularPolygon(5, radius=1, color=Color(hue=k/5, saturation=1, luminance=0.5), fill_opacity=0.7)
              for k in range(5)]
        ).arrange(RIGHT)
        self.play(DrawBorderThenFill(polys), run_time=2)
        self.play(
            Rotate(polys[0], PI, rate_func=linear),
            Rotate(polys[1], PI, rate_func=smooth),
            Rotate(polys[2], PI, rate_func=lambda t: np.sin(t*PI)),
            Rotate(polys[3], PI, rate_func=there_and_back),
            Rotate(polys[4], PI, rate_func=lambda t: 1 - abs(1-2*t)),
            run_time = 2
        )
        self.wait()
        
        
class ConflictingAnimations(Scene):
    def construct(self):
        s = Square()
        self.add(s)
        self.play(Rotate(s, PI), Rotate(s, -PI), run_time=3)
        

class LaggingGroup(Scene):
    def construct(self):
        squares = VGroup(
            *[Square(color=Color(hue=k/20, saturation=1, luminance=0.5), fill_opacity=0.7) for k in range(20)]
        ).arrange_in_grid(4, 5).scale(0.75)
        self.play(AnimationGroup(*[FadeIn(s) for s in squares], lag_ratio=0.15))
        
        
class AnimateSyntax(Scene):
    def construct(self):
        s = Square(color=GREEN, fill_opacity=0.5)
        c = Circle(color=RED, fill_opacity=0.5)
        self.add(s, c)
        self.play(s.animate.shift(UP), c.animate.shift(DOWN))
        self.play(VGroup(s, c).animate.arrange(RIGHT))
        self.play(c.animate(rate_func=linear).shift(RIGHT).scale(2))
        self.wait()
        
class AnimateProblem(Scene):
    def construct(self):
        left_s = Square()
        right_s = Square()
        VGroup(left_s, right_s).arrange(RIGHT, buff=1)
        self.add(left_s, right_s)
        self.play(left_s.animate.rotate(PI), Rotate(right_s, PI), run_time=2)
        
        
class AnimationMechanisms(Scene):
    def construct(self):
        c = Circle()
        
        c.generate_target() 
        c.target.set_fill(color=GREEN, opacity=0.5)
        c.target.shift(2*RIGHT + UP).scale(0.5)
        
        self.add(c)
        self.wait()
        self.play(MoveToTarget(c))
        self.wait()
        
        s = Square()
        s.save_state()
        self.play(FadeIn(s))
        self.play(s.animate.set_color(PURPLE).set_opacity(0.5).shift(2*LEFT).scale(3))
        self.play(s.animate.shift(DOWN).rotate(PI/4))
        self.wait()
        self.play(Restore(s), run_time=2)
        self.wait()
        
        
class SimpleCustomAnimation(Scene):
    def construct(self):
        def spiral_out(mobject, t):
            radius = 4 * t
            angle = 4 * t * PI 
            mobject.move_to(radius * (np.cos(angle)*RIGHT + np.sin(angle)*UP))
            mobject.set_color(Color(hue=t, saturation=1, luminance=0.5))
            mobject.set_opacity(1 - t)
        
        d = Dot(color=YELLOW)
        self.add(d)
        self.wait()
        self.play(UpdateFromAlphaFunc(d, spiral_out, run_time=3))
        self.wait()
        
        

class Disperse(Animation):
    def __init__(self, mobject, dot_radius=0.05, dot_number=100, **kwargs):
        super().__init__(mobject, **kwargs)
        self.dot_radius = dot_radius
        self.dot_number = dot_number
        
    def begin(self):
        dots = VGroup(
            *[Dot(radius=self.dot_radius).move_to(self.mobject.point_from_proportion(p))
              for p in np.linspace(0, 1, self.dot_number)]
        )
        for dot in dots:
            dot.initial_position = dot.get_center()
            dot.shift_vector = 2 * (dot.get_center() - self.mobject.get_center())
        dots.set_opacity(0)
        self.mobject.add(dots)
        self.dots = dots 
        super().begin() 
        
    def clean_up_from_scene(self, scene: Scene) -> None:
        super().clean_up_from_scene(scene)
        scene.remove(self.dots)
        
    def interpolate_mobject(self, alpha: float) -> None:
        alpha = self.rate_func(alpha)
        if alpha <= 0.5:
            self.mobject.set_opacity(1 - 2*alpha, family=False)
            self.dots.set_opacity(2 * alpha)
        else:
            self.mobject.set_opacity(0)
            self.dots.set_opacity(2 * (1 - alpha))
            for dot in self.dots:
                dot.move_to(dot.initial_position + 2 * (alpha - 0.5) * dot.shift_vector)
                
class CustomAnimation(Scene):
    def construct(self):
        st = Star(color=YELLOW, fill_opacity=1).scale(3)
        self.add(st)
        self.wait()
        self.play(Disperse(st, dot_number=200, run_time=4))
        self.wait()