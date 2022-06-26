from manim import *
import numpy as np 

def get_spanning_vectors(plane):
    result = VGroup()
    x = -7
    y = -4
    while x <= 7:
        for y in np.arange(-4, 5):
            if x <= 0:
                point = (
                    Dot(fill_color = [ORANGE, YELLOW], fill_opacity=0.75)
                    .scale(0.5).move_to(plane.c2p(x, y))
                )
                vec = (
                    Line(ORIGIN, point.get_center(), tip_length=0.2, stroke_color=[BLUE, PINK])
                    .add_tip().set_opacity(0.8)
                )
            else:
                point = (
                    Dot(fill_color = [YELLOW, ORANGE], fill_opacity=0.75)
                    .scale(0.5).move_to(plane.c2p(x, y))
                )
                vec = (
                    Line(ORIGIN, point.get_center(), tip_length=0.2, stroke_color=[PINK, BLUE])
                    .add_tip().set_opacity(0.8)
                )
            result.add(point, vec)
        x += 1
    return result 



class VectorSpan(Scene):
    def construct(self):
        plane1 = NumberPlane()
        self.add(plane1)
        
        span1 = get_spanning_vectors(plane1)
        self.play(Create(span1), run_time=2)
        self.wait()
        