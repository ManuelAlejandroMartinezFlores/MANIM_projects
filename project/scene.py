from manim import *
import numpy as np

class CreateCircle(Scene):
    def construct(self):
        # create circle
        circle = Circle()
        # fill circle
        circle.set_fill(PINK, opacity=0.5)
        # show circle
        self.play(Create(circle))
        

class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)
        # create square
        square = Square()
        # rotate square
        square.rotate(PI/4)
        # show square
        self.play(Create(square))
        # transforma square into circle
        self.play(Transform(square, circle))
        # fade out figure
        self.play(FadeOut(square))


class SquareAndCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)

        square = Square()
        square.set_fill(BLUE, opacity=0.5)
        # set square next to circle
        square.next_to(circle, RIGHT, buff=0.5)
        self.play(Create(circle), Create(square))

class AnimatedSquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        
        self.play(Create(square))
        self.play(square.animate.rotate(PI/4))
        self.play(ReplacementTransform(square, circle))
        self.play(circle.animate.set_fill(PINK, opacity=0.5))


class DifferentRotations(Scene):
    def construct(self):
        left_square = Square(color=BLUE, fill_opacity=0.7).shift(2 * LEFT)
        right_square = Square(color=GREEN, fill_opacity=0.7).shift(2 * RIGHT)
        self.play(
            left_square.animate.rotate(PI),
            Rotate(right_square, angle=PI),
            run_time=2
        )

class CreatingObjects(Scene):
    def construct(self):
        circle = Circle()
        self.add(circle)
        self.wait(1)
        self.remove(circle)
        self.wait(1)

class Shapes(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        triangle = Triangle()

        circle.shift(LEFT)
        square.shift(UP)
        triangle.shift(RIGHT)

        self.add(circle, square, triangle)
        self.wait(1)

class MobjectPlacement(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        triangle = Triangle()

        # move 2 units
        circle.move_to(LEFT *2)
        # put square next to circle
        square.next_to(circle, LEFT)
        # align triangle to circle
        triangle.align_to(circle, LEFT)

        self.wait(1)
        self.add(circle, square, triangle)
        self.wait(1)

class MobjectStyling(Scene):
    def construct(self):
        circle = Circle().shift(LEFT)
        square = Square().shift(UP)
        triangle = Triangle().shift(RIGHT)

        circle.set_stroke(color=GREEN, width=20)
        square.set_fill(YELLOW, opacity=1.0)
        triangle.set_fill(PINK, opacity=0.5)

        # first added shows in the back
        self.add(circle, square, triangle)
        self.wait(1)

class SomeAnimations(Scene):
    def construct(self):
        square = Square()
        
        self.play(FadeIn(square))
        self.play(Rotate(square, PI/4))
        self.play(FadeOut(square))
        self.wait(1)


class AnimateExample(Scene):
    def construct(self):
        square = Square().set_fill(RED, opacity=1.0)
        self.add(square)

        self.play(square.animate.set_fill(WHITE))
        self.wait(1)
        
        self.play(square.animate.shift(UP).rotate(PI/3))
        self.wait(1)


class RunTime(Scene):
    def construct(self):
        square = Square()
        self.add(square)
        self.play(square.animate.shift(UP), run_time=3)
        self.wait(1)
    
## Custom Animation
class Count(Animation):
    def __init__(self, number: DecimalNumber, start: float, end: float, **kwargs) -> None:
        super().__init__(number, **kwargs)
        self.start = start
        self.end = end
    
    def interpolate_mobject(self, alpha: float) -> None:
        value = self.start + alpha * (self.end - self.start)
        self.mobject.set_value(value)
        
class CountingScene(Scene):
    def construct(self):
        number = DecimalNumber().set_color(WHITE).scale(5)
        # add updater to keep it centered
        number.add_updater(lambda number: number.move_to(ORIGIN))
        
        self.add(number)
        self.wait()
        
        self.play(Count(number, 0, 100), run_time=4, rate_func=linear)
        self.wait()
        

class MobjectExample(Scene):
    def construct(self):
        p1 = [-1, -1, 0]
        p2 = [1, -1, 0]
        p3 = [1, 1, 0]
        p4 = [-1, 1, 0]
        
        a = Line(p1, p2).append_points(Line(p2, p3).points).append_points(Line(p3, p4).points)
        point_start = a.get_start()
        point_end = a.get_end()
        point_center = a.get_center()
        
        self.add(Text(f"a.get_start() = {np.round(point_start, 2)}", font_size=24).to_edge(UR).set_color(YELLOW))
        self.add(Text(f"a.get_end() = {np.round(point_end, 2)}", font_size=24).next_to(self.mobjects[-1], DOWN).set_color(RED))
        self.add(Text(f"a.get_center() = {np.round(point_center, 2)}", font_size=24).next_to(self.mobjects[-1], DOWN).set_color(BLUE))
        
        self.add(Dot(a.get_start()).set_color(YELLOW).scale(2))
        self.add(Dot(a.get_end()).set_color(RED).scale(2))
        self.add(Dot(a.get_center()).set_color(BLUE).scale(2))
        self.add(Dot(a.get_top()).set_color(GREEN_A).scale(2))
        self.add(Dot(a.get_bottom()).set_color(GREEN_D).scale(2))
        self.add(Dot(a.point_from_proportion(0.5)).set_color(ORANGE).scale(2))
        self.add(*[Dot(x) for x in a.points])
        self.add(a)
        
        
class ExampleTransform(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        m1 = Square().set_color(RED)
        m2 = Rectangle().set_color(RED).rotate(0.2)
        self.play(Transform(m1, m2))
        
class ExampleRotation(Scene):
    def construct(self):
        m1a = Square().set_color(RED).shift(LEFT)
        m2a = Square().set_color(BLUE).shift(RIGHT)
        
        m1b = Circle().set_color(RED).shift(LEFT)
        m2b = Circle().set_color(BLUE).shift(RIGHT)
        
        points = m2a.points
        points = np.roll(points, int(len(points)/4), axis=0)
        m2a.points = points
        
        self.play(Transform(m1a, m1b), Transform(m2a, m2b), run_time=1)
        
class TextT2cExample(Scene):
    def construct(self):
        t2ind = Text('Hello', t2c={'[1:-1]':BLUE}).move_to(LEFT)
        t2w = Text('World', t2c={'rl':RED}).next_to(t2ind, RIGHT)
        self.add(t2ind, t2w)
        
class GradientExample(Scene):
    def construct(self):
        t = Text('Hello World', gradient=(RED, BLUE, GREEN))
        self.add(t)
        
        
class t2gExample(Scene):
    def construct(self):
        t2gind = Text('Hello', t2g={'[1:-1]':(BLUE,GREEN)}).move_to(LEFT)
        t2gw = Text('World', t2g={'orl':(RED,BLUE)}).next_to(t2gind, RIGHT)
        self.add(t2gind, t2gw)
        
class LineSpacing(Scene):
    def construct(self):
        a = Text('Hello\nWorld', line_spacing=1)
        b = Text('Hello\nWorld', line_spacing=4)
        self.add(Group(a, b).arrange(LEFT, buff=5))
        
class IterateColor(Scene):
    def construct(self):
        t = Text('Colors', font_size=96)
        for letter in t:
            letter.set_color(random_bright_color())
        self.add(t)
        
class MarkupTest(Scene):
    def construct(self):
        text = MarkupText(
            f'<span underline="double" underline_color="green">double green underline</span> in red text<span fgcolor="{YELLOW}"> except this</span>',
            color=RED,
            font_size=34
        )
        self.add(text)
        
class HelloLaTeX(Scene):
    def construct(self):
        t = Tex(r"\LaTeX", font_size=144)
        self.add(t)
        
class MathTeXDemo(Scene):
    def construct(self):
        mt = MathTex(r'\xrightarrow{x^6y^8}', font_size=96)
        t = Tex(r'$\xrightarrow{x^6y^8}$', font_size=96)
        self.add(VGroup(mt, t).arrange(DOWN))
        
class AddPackageLatex(Scene):
    def construct(self):
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"\usepackage{mathrsfs}")
        tex = Tex(
            r"$\mathscr{H} \rightarrow \mathbb{H}$}",
            tex_template=myTemplate,
            font_size=144,
        )
        self.add(tex)
        
class LaTeXSubstringColoring(Scene):
    def construct(self):
        eq1 = MathTex(
            r"e^x = x^0 + x^1 + \frac{1}{2} x^2 + \frac{1}{6} x^3 + \cdots + \frac{1}{n!} x^n + \cdots",
        )
        eq2 = MathTex(
            r"e^x = x^0 + x^1 + \frac{1}{2} x^2 + \frac{1}{6} x^3 + \cdots + \frac{1}{n!} x^n + \cdots",
            substrings_to_isolate="x"
        )
        eq1.set_color_by_tex("x", YELLOW)
        eq2.set_color_by_tex("x", YELLOW)
        self.add(VGroup(eq1, eq2).arrange(DOWN))
        
class IndexLabelsMathTex(Scene):
    def construct(self):
        text = MathTex(r'\binom{2n}{n+2}', font_size=96)
        self.add(index_labels(text[0]))
        
        text[0][1:3].set_color(YELLOW)
        text[0][3:6].set_color(RED)
        self.add(text)
        
class LatesMathFonts(Scene):
    def construct(self):
        tex = Tex(
            r'$x^2 + y^2 = z^2$',
            tex_template=TexFontTemplates.french_cursive,
            font_size=144
        )
        self.add(tex)
        
class LatexAlignEnv(Scene):
    def construct(self):
        tex = MathTex(r'f(x) & = 3 + 2+1\\ &=5+1 \\ &=6', font_size=96)
        self.add(tex)


