from manim import *
from manim_physics import *


class ElectricFieldEx(Scene):
    def construct(self):
        c1 = Charge(-1, DL)
        c2 = Charge(2, DR)
        c3 = Charge(-1, UP)
        field = ElectricField(c1, c2, c3)
        self.add(c1, c2, c3)
        self.add(field)
        
class MagnetismEx(Scene):
    def construct(self):
        magnet1 = BarMagnet().shift(2.5 * LEFT)
        magnet2 = Current(2.5*RIGHT, direction=IN)
        field = MagneticField(magnet1, magnet2)
        self.add(field, magnet1, magnet2)