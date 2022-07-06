from manim import * 

config.disable_caching = True

def hilb():
    H = VMobject()
    
    H.set_points_as_corners([DL, UL, UR, DR])
    return H.set_color(BLUE_A)

def connect(H):
    H.add(Line(H[2].get_boundary_point(UL), H[0].get_boundary_point(DL)))
    H.add(Line(H[0].get_boundary_point(DR), H[1].get_boundary_point(DL)))
    H.add(Line(H[1].get_boundary_point(DR), H[3].get_boundary_point(UR)))
    return H

class Hilbert(Scene):
    def construct(self):
        self.n = 0
        self.H = hilb()

        for _ in range(5):
            self.upgrade()
    
    def upgrade(self):
        self.n += 1
        self.play(self.H.animate.set(width=2))
        self.H = VGroup(self.H, *[self.H.copy() for _ in range(3)])
        
        self.add(self.H)
        self.play(self.H.animate.arrange_in_grid(2, 2, buff=self.H.width / (2**self.n - 1)))
        self.play(self.H[-1].animate.rotate(PI/2), self.H[-2].animate.rotate(-PI/2))
        self.H = connect(self.H)
        self.H.set_color(BLUE_A)
        self.play(*[Create(h) for h in self.H[-3:]])
        
        self.wait()
        

        
    