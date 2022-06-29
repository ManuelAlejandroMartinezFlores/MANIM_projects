from manim import *
from manim_physics import *

class ObjectFalling(SpaceScene):
    def construct(self):
        circle = Circle().shift(RIGHT).set_fill(RED, 1)
        square = Square().shift(UP * 3).rotate(PI / 4).set_fill(YELLOW_A, 1).scale(0.5)
        
        ground = Line([-4, -3.5, 0], [4, -3.5, 0])
        wall1 = Line([-4, -3.5, 0], [-4, 3.5, 0])
        wall2 = Line([4, -3.5, 0], [4, 3.5, 0])
        walls = VGroup(ground, wall1, wall2)
        self.add(walls)
        
        self.play(DrawBorderThenFill(circle), DrawBorderThenFill(square))
        self.make_rigid_body(square, circle)
        self.make_static_body(walls)
        self.wait(5)
        
        
class TexFalling(SpaceScene):
    def construct(self):
        ground = Line(LEFT*5, RIGHT*5, color = ORANGE).shift(DOWN)
        self.add(ground)
        self.make_static_body(ground)
        forms = [
            "e^{i \pi} + 1 = 0",
            "\cos (x + y) = \cos x \cos y - \sin x \sin y",
            "\displaystyle \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}"
        ]
        cols = [RED, BLUE, YELLOW]
        for f, col in zip(forms, cols):
            tex = MathTex(f, color=col).shift(UP)
            self.add(tex)
            self.make_rigid_body(tex)
            self.wait(2)