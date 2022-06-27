from manim import *
import numpy as np 


class MovingLabel(Scene):
    def construct(self):
        d = Dot(color=BLUE)
        l = Text("Hello dot!").next_to(d, UP)
        l.add_updater(
            lambda m: m.next_to(d, UP)
        )
        self.add(d, l)
        self.play(d.animate.shift(RIGHT))
        self.play(d.animate.scale(10))
        self.wait()
        
        
class UpdaterTypes(Scene):
    def construct(self):
        d = Dot(color=RED).shift(LEFT)
        pointer = Arrow(ORIGIN, RIGHT).next_to(d, LEFT)
        pointer.add_updater(
            lambda m: m.next_to(d, LEFT)
        )
        def shifter(mob, dt):
            mob.shift(2 * dt * RIGHT)
        d.add_updater(shifter)
        
        def scene_scaler(dt):
            for mob in self.mobjects:
                mob.set(width= 2 / (1 + np.linalg.norm(mob.get_center())))
        self.add_updater(scene_scaler)
        
        self.add(d, pointer)
        self.update_self(0)
        self.wait(5)
        
        
class UpdaterAnimations(Scene):
    def construct(self):
        d = Dot(color=RED).shift(LEFT)
        s = Square()
        s.add_updater(lambda mob, dt: mob.rotate(dt*PI))
        
        def shifter(mob, dt):
            mob.shift(2 * dt * RIGHT)
        d.add_updater(shifter)
        
        self.add(d, s)
        self.wait(1)
        d.suspend_updating()
        self.wait(1)
        self.play(d.animate.shift(UP), s.animate.move_to([-2, -2, 0]))
        self.wait()
        
        
class ValueTrackerMove(Scene):
    def construct(self):
        line = NumberLine(x_range=[-5, 5])
        position = ValueTracker(0)
        pointer = Vector(DOWN)
        pointer.add_updater(
            lambda mob: mob.next_to(line.number_to_point(position.get_value()), UP)
        )
        pointer.update()
        self.add(line, pointer)
        self.wait()
        self.play(position.animate.set_value(4))
        self.play(position.animate.set_value(-2))
        self.wait()
        

class ValueTrackerPlot(Scene):
    def construct(self):
        a = ValueTracker(1)
        ax = Axes(
            x_range=[-2, 2, 1], y_range=[-8.5, 8.5, 1], x_length=4, y_length=6,
        )
        parabola = ax.plot(lambda x: a.get_value() * x**2, color=RED)
        parabola.add_updater(
            lambda mob: mob.become(ax.plot(lambda x: a.get_value() * x**2, color=RED))
        )
        a_num = DecimalNumber(
            a.get_value(),
            color=RED,
            num_decimal_places=3,
            show_ellipsis=True
        )
        a_num.add_updater(
            lambda mob: mob.set_value(a.get_value()).next_to(parabola, RIGHT)
        )
        a_num.update()
        self.add(ax, parabola, a_num)
        self.wait()
        self.play(a.animate.set_value(2))
        self.play(a.animate.set_value(-2))
        self.play(a.animate.set_value(1))
        self.wait()
        