import time
import math
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
from bullet import Bullet
from spritesheet import Spritesheet
from collider import Rect

# Explosion data
SHEET_URL = "http://www.cs.rhul.ac.uk/courses/CS1830/sprites/" \
            "explosion-spritesheet.png"
SHEET_WIDTH = 900
SHEET_HEIGHT = 900
SHEET_COLUMNS = 9
SHEET_ROWS = 9
SHEET_FRAMES = 74


class Time:
    def __init__(self):
        self.time = 0
        self.time_ns = 0
        self.start_time = time.time()
        self.start_time_ns = time.time_ns()
        self.fps = ""

    def tick(self):
        self.time += 1

    def get_time(self):
        return time.time()

    def delta_time(self):
        self.time_ns = time.time_ns()
        # Delta time in ms
        dt = int((self.time_ns - self.start_time_ns) / 1000000)
        self.start_time_ns = self.time_ns
        return dt

    def print_fps(self, canvas):
        if self.get_time() - self.start_time > 1:
            self.fps = str(int(self.time / (self.get_time()-self.start_time)))
            self.time = 0
            self.start_time = self.get_time()
        canvas.draw_text(self.fps, (5, 10), 12, "black")


class Tank:
    def __init__(self, pos, spritesheet, bullet_color="gray"):
        self.pos = pos
        self.vel = Vector()
        self.look_pos = Vector(0, -1)
        self.rot_step = -0.07
        self.img_rot = 0

        # NOTE(AKotro): Ball collider
        self.collider = Bullet(self.pos, Vector(), 30, "red")

        self.spritesheet = spritesheet
        self.time = Time()
        # NOTE(AKotro): Load explosion at startup
        self.explosion = Spritesheet(SHEET_URL, SHEET_COLUMNS, SHEET_ROWS,
                                     SHEET_FRAMES-30, 1,
                                     self.pos.copy().get_p())
        self.explosion = None
        self.bullets = []
        self.max_bullets = 3
        self.bullet_size = 8
        self.bullet_color = bullet_color
        self.bullet_speed = 8
        self.stopped = False

    def explode(self):
        """Initialize the explosion spritesheet."""
        self.explosion = Spritesheet(SHEET_URL, SHEET_COLUMNS, SHEET_ROWS,
                                     SHEET_FRAMES-30, 1,
                                     self.pos.copy().get_p(), 0.85)

    def bullets_not_empty(self):
        """Returns True if the bullet list is not empty."""
        if len(self.bullets) == 0:
            return False
        return True

    def is_explosion_done(self):
        """Returns True if the explosion animation has completed."""
        if self.explosion:
            if self.explosion.done():
                self.explosion = None
                return True
        return False

    def shoot(self):
        """Adds a bullet to the bullet list."""
        if len(self.bullets) < self.max_bullets:
            bullet = Bullet(self.pos.copy(), self.look_pos.copy()*self.bullet_speed,
                            self.bullet_size, self.bullet_color)
            self.bullets.append(bullet)

    def draw(self, canvas):
        self.time.tick()
        if self.spritesheet:
            # Update spritesheet position and rotation
            self.spritesheet.dest_centre = self.pos.get_p()
            self.spritesheet.img_rot = self.img_rot
            # Draw spritesheet
            self.spritesheet.draw(canvas, self.spritesheet.frame_index)
            if self.spritesheet.transition(self.time.time):
                self.spritesheet.next_frame()

        # Draw bullet if not None
        if self.bullets_not_empty():
            for bullet in self.bullets:
                bullet.draw(canvas)
        # Draw explosion if not None
        if self.explosion:
            self.explosion.draw(canvas, self.explosion.frame_index)
            if self.explosion.transition(self.time.time):
                self.explosion.next_frame()

    def update(self):
        self.vel.multiply(0.85)
        self.pos.add(self.vel)
        if self.bullets_not_empty():
            for bullet in self.bullets:
                bullet.update()


class Turret(Tank):
    def __init__(self, pos, spritesheet, bullet_color):
        super().__init__(pos, spritesheet, bullet_color)
        self.active_distance = 250
        # NOTE(AKotro): Time interval to shoot, in seconds
        self.shoot_interval = 2

    def shoot(self):
        """Adds a bullet to the bullet list on a time interval,
        determined by self.shoot_interval.
        """
        if self.time.get_time() - self.time.start_time > self.shoot_interval:
            super().shoot()
            self.time.start_time = self.time.get_time()

    def look_angle(self):
        """Gets the angle of self.look_pos"""
        angle = math.atan2(self.look_pos.y, self.look_pos.x)
        return angle

    def get_player_angle(self, player):
        """Gets the angle between the turret and player."""
        angle = math.atan2(player.pos.y-self.pos.y, player.pos.x-self.pos.x)
        return angle

    def player_is_close(self, player):
        """Returns True if the player is closer than self.active_distance."""
        distance = (self.pos - player.pos).length()
        if distance > self.active_distance:
            return False
        return True

    def face_player(self, player):
        """Rotates the turret to face the player if they are close enough."""
        if self.player_is_close(player):
            look_angle = self.look_angle()
            target = self.get_player_angle(player)
            buffer = self.rot_step
            if target + buffer < look_angle:
                self.img_rot += self.rot_step
                self.look_pos.rotate_rad(self.rot_step)
            elif target + buffer > look_angle:
                self.img_rot -= self.rot_step
                self.look_pos.rotate_rad(-self.rot_step)

    def target_player(self, player):
        """If player is close, the turret tracks them and starts shooting."""
        if self.player_is_close(player):
            self.face_player(player)
            self.shoot()
            # Hit player?
            if self.bullets_not_empty():
                for bullet in self.bullets:
                    if player and bullet.hit(player.collider):
                        if not player.explosion:
                            player.stopped = True
                            player.explode()
                            self.bullets.remove(bullet)


class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False
        self.up = False
        self.down = False
        self.shoot = False

        self.right2 = False
        self.left2 = False
        self.up2 = False
        self.down2 = False
        self.shoot2 = False

    def keydown(self, key):
        # NOTE(AKotro): Player1
        if key == simplegui.KEY_MAP['right']:
            self.right = True
        if key == simplegui.KEY_MAP['left']:
            self.left = True
        if key == simplegui.KEY_MAP['up']:
            self.up = True
        if key == simplegui.KEY_MAP['down']:
            self.down = True
        if key == simplegui.KEY_MAP['space']:
            self.shoot = True

        # NOTE(AKotro): Player2
        if key == simplegui.KEY_MAP['d']:
            self.right2 = True
        if key == simplegui.KEY_MAP['a']:
            self.left2 = True
        if key == simplegui.KEY_MAP['w']:
            self.up2 = True
        if key == simplegui.KEY_MAP['s']:
            self.down2 = True
        if key == simplegui.KEY_MAP['c']:
            self.shoot2 = True

    def keyup(self, key):
        # NOTE(AKotro): Player1
        if key == simplegui.KEY_MAP['right']:
            self.right = False
        if key == simplegui.KEY_MAP['left']:
            self.left = False
        if key == simplegui.KEY_MAP['up']:
            self.up = False
        if key == simplegui.KEY_MAP['down']:
            self.down = False
        if key == simplegui.KEY_MAP['space']:
            self.shoot = False

        # NOTE(AKotro): Player2
        if key == simplegui.KEY_MAP['d']:
            self.right2 = False
        if key == simplegui.KEY_MAP['a']:
            self.left2 = False
        if key == simplegui.KEY_MAP['w']:
            self.up2 = False
        if key == simplegui.KEY_MAP['s']:
            self.down2 = False
        if key == simplegui.KEY_MAP['c']:
            self.shoot2 = False
