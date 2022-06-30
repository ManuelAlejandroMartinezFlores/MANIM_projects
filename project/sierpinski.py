from manim import *

config.disable_caching = True


class Sierpinski(Scene):
    def construct(self):
        t = Triangle(color=BLUE_A, fill_opacity=0.7)
        self.add(t)
        for _ in range(6):
            t = self.upgrade(t)
        
    def upgrade(self, base):
        S = VGroup()
        S_ = VGroup()
        S_.add(base.copy(), base.copy()).arrange(RIGHT, buff=0)
        S.add(S_, base.copy()).arrange(UP, buff=0).move_to(ORIGIN)
        
        self.play(base.animate.move_to(S[1].get_center()))
        self.play(FadeTransform(base, S[1]), FadeIn(S[0]))
        if S.width > 8:
            self.play(S.animate.set(width=8))
        else:
            self.wait()
        return S
    
    
# Interactive
# from manim.opengl import * 

# config.write_to_movie = False
# config.renderer = "opengl"

class SierpinskiInter(Scene):
    def construct(self):
        t = Triangle(color=BLUE_A, fill_opacity=0.7)
        self.add(t)
        self.base = t
        self.interactive_embed()
        
    def upgrade(self):
        base = self.base
        S = VGroup()
        S_ = VGroup()
        S_.add(base.copy(), base.copy()).arrange(RIGHT, buff=0)
        S.add(S_, base.copy()).arrange(UP, buff=0).move_to(ORIGIN)
        
        self.play(base.animate.move_to(S[1].get_center()))
        self.play(FadeTransform(base, S[1]), FadeIn(S[0]))
        if S.width > 8:
            self.play(S.animate.set(width=8))
        else:
            self.wait()
        self.base =  S
    
    def on_key_press(self, symbol, modifiers):
        from pyglet.window import key as pyglet_key
        if symbol == pyglet_key.I:
            self.upgrade()
        super().on_key_press(symbol, modifiers)