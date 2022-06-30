from manim import *
from manim_editor import PresentationSectionType 


def make_elements():
    dots = VGroup(*[Dot() for _ in range(7)], z_index=0)
    dots.arrange(buff=0.7).scale(2).set_color(BLUE)
    dots[0].set_color(ORANGE)
    dots[-1].set_color(ORANGE)
    moving_dot = Dot(color=ORANGE, z_index=1).scale(2.5)
    moving_dot.move_to(dots[0])
    path = Line()
    path.add_updater(lambda m: m.become(Line(dots[0], moving_dot, stroke_width=10, z_index=1)))
    path.update()
    return dots, moving_dot, path 

class PresentationEx(Scene):
    def construct(self):
        dots, moving_dot, path = make_elements()
        self.add(dots, moving_dot, path)
        
        self.next_section("A", PresentationSectionType.NORMAL)
        self.play(moving_dot.animate.move_to(dots[1]), rate_func=linear)
        
        self.next_section("A.1", PresentationSectionType.SUB_NORMAL)
        self.play(moving_dot.animate.move_to(dots[2]), rate_func=linear)
        
        self.next_section("B", PresentationSectionType.SKIP)
        self.play(moving_dot.animate.move_to(dots[3]), rate_func=linear)
        
        self.next_section("C", PresentationSectionType.LOOP)
        self.play(moving_dot.animate.move_to(dots[4]), rate_func=linear)
        
        self.next_section("D", PresentationSectionType.COMPLETE_LOOP)
        self.play(moving_dot.animate.move_to(dots[5]), rate_func=linear)
        
        self.next_section("E", PresentationSectionType.NORMAL)
        self.play(moving_dot.animate.move_to(dots[6]), rate_func=linear)