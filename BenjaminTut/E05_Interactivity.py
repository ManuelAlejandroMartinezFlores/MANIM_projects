import manim.utils.opengl as opengl
from manim import * 
from manim.opengl import * 
import numpy as np

config.renderer = "opengl"
config.write_to_movie = False 
        


class OpenGLIntro(Scene):
    def construct(self):
        
        hello_world = Tex("Hello World!").scale(3)
        self.play(Write(hello_world))
        self.play(
            self.camera.animate.set_euler_angles(
                theta=-10*DEGREES,
                phi=50*DEGREES
            )
        )
        self.play(FadeOut(hello_world))
        surface = OpenGLSurface(
            lambda u, v: (u, v, u*np.sin(v) + v*np.cos(u)),
            u_range=(-3, 3),
            v_range=(-3, 3)
        )
        surface_mesh = OpenGLSurfaceMesh(surface)
        self.play(Create(surface_mesh))
        self.play(FadeTransform(surface_mesh, surface))
        self.wait()
        light = self.camera.light_source
        self.play(light.animate.shift([0, 0, -20]))
        self.play(light.animate.shift([0, 0, 10]))
        self.play(self.camera.animate.set_euler_angles(theta=60*DEGREES))
        
        

        self.play(self.camera.animate.set_euler_angles(theta=0*DEGREES))
        self.play(FadeOut(surface, shift=np.array([0, 0, -2])))

        red_sphere = OpenGLSurface(
            lambda u, v: (np.cos(u) * np.sin(v), np.sin(u) * np.sin(v), -np.cos(v)),
            u_range=(0, TAU),
            v_range=(0, PI),
            color=RED,
        )
        self.play(Create(red_sphere))
        self.play(red_sphere.animate.scale(3))

        sphere_mesh = OpenGLSurfaceMesh(red_sphere)
        self.play(FadeTransform(red_sphere, sphere_mesh))  

        self.play(self.camera.animate.set_euler_angles(phi=0, theta=0))
        
        self.interactive_embed()
        
        

class SurfaceExample(Scene):
    def construct(self):
        
        torus1 = OpenGLSurface(
            lambda u, v: ((1 - np.cos(v)) * np.cos(u), (1 - np.cos(v)) * np.sin(u), np.sin(v)),
            u_range=(0, TAU),
            v_range=(0, TAU),
        )
        torus2 = OpenGLSurface(
            lambda u, v: ((3 - np.cos(v)) * np.cos(u), (3 - np.cos(v)) * np.sin(u), np.sin(v)),
            u_range=(0, TAU),
            v_range=(0, TAU),
        )
        sphere = OpenGLSurface(
            lambda u, v: (np.cos(u) * np.sin(v), np.sin(u) * np.sin(v), -np.cos(v)),
            u_range=(0, TAU),
            v_range=(0, PI),
            resolution=torus1.resolution,
        ) 
        
        day_texture = "day.jpeg"
        night_texture = "night.jpeg"
        
        surfaces = [
            OpenGLTexturedSurface(surf, day_texture, night_texture) 
            for surf in [sphere, torus1, torus2]
        ]
        
        for mob in surfaces:
            mob.shift(IN)
            mob.mesh = OpenGLSurfaceMesh(mob)
            mob.mesh.set_stroke(BLUE, 1, opacity=0.2)
            
        frame = self.renderer.camera
        frame.set_euler_angles(theta = -30*DEGREES, phi = 70*DEGREES)
        
        surface = surfaces[0]
        
        self.play(FadeIn(surface), Create(surface.mesh, lag_ratio=0.01), run_time=3)
        
        for mob in surfaces:
            mob.add(mob.mesh)
        
        surface.save_state()
        
        self.play(Rotate(surface, PI/2), run_time=2)
        
        for mob in surfaces[1:]:
            mob.rotate(PI/2)
            
        self.play(Transform(surface, surfaces[1]), run_time=3)
        
        self.play(
            Transform(surface, surfaces[2]),
            frame.animate.increment_phi(-10*DEGREES),
            frame.animate.increment_theta(-20*DEGREES),
            run_time=3,
        )
        
        frame.add_updater(lambda m, dt: m.increment_theta(-0.1*dt))
        
        light = self.camera.light_source
        self.add(light)
        light.save_state()
        self.wait(3)
        self.play(light.animate.move_to(5 * IN), run_time=5)
        self.wait()
        # self.interactive_embed()


class InteractiveRadius(Scene):
    def construct(self):
        plane = NumberPlane()
        cursor_dot = Dot().move_to(3*RIGHT + 2*UP)
        red_circle = Circle(
            radius=np.linalg.norm(cursor_dot.get_center()),
            color=RED
        )
        red_circle.add_updater(
            lambda mob: mob.become(
                Circle(
                    radius=np.linalg.norm(cursor_dot.get_center()),
                    color=RED
                )
            )
        )
        self.play(Create(plane), Create(red_circle), FadeIn(cursor_dot))
        self.cursor_dot = cursor_dot
        self.interactive_embed() 

    def on_key_press(self, symbol, modifiers):
        from pyglet.window import key as pyglet_key
        if symbol == pyglet_key.G:
            self.play(
                self.cursor_dot.animate.move_to(2 * self.mouse_point.get_center() + np.array([7, 4, 0]))
            )
        super().on_key_press(symbol, modifiers)
        
        
class NewtonIteration(Scene):
    def construct(self):
        self.axes = Axes()
        self.f = lambda x: (x + 6) * (x - 3) * (x - 6) * x * (x + 3) / 300 
        curve = self.axes.plot(self.f, color=RED)
        
        self.cursor_dot = Dot(color=YELLOW)
        self.play(Create(self.axes), Create(curve), FadeIn(self.cursor_dot))
        self.interactive_embed()
        
    def on_key_press(self, symbol, modifiers):
        from pyglet.window import key as pyglet_key
        from scipy.misc import derivative
        
        if symbol == pyglet_key.P:
            x, y = self.axes.p2c(2 * self.mouse_point.get_center() + np.array([7, 4, 0]))
            self.play(
                self.cursor_dot.animate.move_to(self.axes.c2p(x, self.f(x)))
            )
            
        if symbol == pyglet_key.I:
            x, y = self.axes.p2c(self.cursor_dot.get_center())
            x_new = x - self.f(x) / derivative(self.f, x, dx=0.01)
            curve_point = self.cursor_dot.get_center()
            axes_point = self.axes.c2p(x_new, 0)
            tangent = Line(
                curve_point + (curve_point - axes_point) * 0.25,
                axes_point - (curve_point - axes_point) * 0.25,
                color = YELLOW, stroke_width = 2,
            )
            self.play(Create(tangent))
            self.play(self.cursor_dot.animate.move_to(self.axes.c2p(x_new, 0)))
            self.play(
                self.cursor_dot.animate.move_to(self.axes.c2p(x_new, self.f(x_new))),
                FadeOut(tangent),
            )
        
        super().on_key_press(symbol, modifiers)