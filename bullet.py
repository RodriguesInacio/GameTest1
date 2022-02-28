try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector


class Bullet:
    def __init__(self, pos, vel, radius, color):
        self.pos = pos
        self.vel = vel
        self.radius = radius
        self.border = 1
        self.color = color
        self.bounce_counter = 0

    def hit(self, ball):
        """Returns True if ball has hit this bullet."""
        sep_vec = self.pos.copy() - ball.pos
        return sep_vec.length() < self.radius + ball.radius

    def update(self):
        self.pos.add(self.vel)

    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(),
                           self.radius,
                           self.border,
                           self.color,
                           self.color)

    def bounce(self, normal):
        """Bounces the bullet along the normal."""
        self.vel.reflect(normal)
        self.bounce_counter += 1
