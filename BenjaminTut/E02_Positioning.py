from manim import *
import numpy as np



from manim.utils.unit import Percent, Pixels

class UsefulUnits(Scene):
    def construct(self):
        for perc in range(5, 51, 5):
            self.add(Circle(radius=perc * Percent(X_AXIS)))
            
        d = Dot()
        d.shift(100 * Pixels * RIGHT)
        self.add(d)
        
        
config.format = "gif"

class GIF(Scene):
    def construct(self):
        c = Circle()
        self.play(Create(c), run_time=2)


