from manim import *
from manim_physics import *



class LinearWaveEx(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)
        wave = LinearWave()
        self.play(Create(wave))
        wave.start_wave()
        self.wait(3)
        wave.stop_wave()
        
        
class RadialWaveEx(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)
        wave = RadialWave(
            2*LEFT + 5*DOWN,
            2*RIGHT + 5*DOWN,
            stroke_width = 0
        )
        self.add(wave)
        wave.start_wave()
        self.wait(3)
        wave.stop_wave()
        
class StandingWaveEx(Scene):
    def construct(self):
        waves = VGroup(*[StandingWave(n) for n in range(1, 5)])
        waves.arrange(DOWN).move_to(ORIGIN)
        self.add(waves)
        for w in waves:
            w.start_wave()
            
        self.wait(3)