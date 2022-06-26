from manim import *
import numpy as np 


class ComplexExp(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=(-0.1, 4.25), y_range=(-1.5, 1.5), z_range=(-1.5, 1.5),
            y_length=5, z_length=5,
        )
        curve = ParametricFunction(
            lambda p: axes.c2p(p, np.exp(complex(0, PI*p)).real, np.exp(complex(0, PI*p)).imag),
            t_range = (0, 2, 0.1)
        )
        curve_extension = ParametricFunction(
            lambda p: axes.c2p(p, np.exp(complex(0, PI*p)).real, np.exp(complex(0, PI*p)).imag),
            t_range = (2, 4, 0.1)
        )
        t = MathTex("z = e^{t \pi i}, \quad t \in [0, 2]")
        t.rotate(axis=OUT, angle=90*DEGREES).rotate(axis=UP, angle=90*DEGREES)
        t.next_to(curve, UP + OUT)
        
        self.set_camera_orientation(phi=90*DEGREES, theta=0, focal_distance=10000)
        self.add(axes)
        self.play(Create(curve, run_time=2), Write(t))
        self.wait()
        
        self.move_camera(phi=75*DEGREES, theta=-30*DEGREES) # altitude, azimuth
        self.wait()
        
        four = MathTex("4").rotate(axis=OUT, angle=90*DEGREES).rotate(axis=UP, angle=90*DEGREES)
        four.move_to(t[0][12])
        self.play(Create(curve_extension, run_time=2), t[0][12].animate.become(four))
        self.wait()
        
        self.move_camera(phi=0, theta=-90*DEGREES, focal_distance=10000)
        self.wait()
        
        self.move_camera(phi=75*DEGREES, theta=-30*DEGREES)
        self.wait()
        
        self.move_camera(phi=75*DEGREES, theta=-30*DEGREES)
        self.wait()
        
        self.play(FadeOut(axes, curve, curve_extension, t, shift=IN))
        self.wait()
    
        