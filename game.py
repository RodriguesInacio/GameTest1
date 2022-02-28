import random
import math
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
import df_maze
from tank import Time, Tank, Turret, Keyboard
from bullet import Bullet
from spritesheet import Spritesheet
from background import Background
from collider import Wall, Domain, Rect
from score import Score
from powerups import PowerUp

CANVAS_WIDTH = 640
CANVAS_HEIGHT = 480

# Desert Beige
GAME_BG_IMG = "https://opengameart.org/sites/default/files/backgrounddetailed8.png"
# Place holder for menu backgrounds
MENU_BG_IMG = "https://i.pinimg.com/originals/b8/1a/a4/b81aa44ba47c8ebb93c4525a96904101.jpg"
POWERUP_IMG = "https://opengameart.org/sites/default/files/icon-power-prev.png"
# Army Green
# IMG = "https://opengameart.org/sites/default/files/backgrounddetailed1.png.preview.jpg"
# Ocean Blue
# IMG = "https://opengameart.org/sites/default/files/backgrounddetailed4.png"
# Camo
# IMG = "https://lpc.opengameart.org/sites/default/files/backgrounddetailed2.png"


class Menu:
    def __init__(self):
        self.frame = 2
        self.new_level = False

    def draw_main_menu(self, canvas):
        canvas.draw_text('Boom Bots', (100, 75),
                         80, 'White', 'monospace')
        canvas.draw_text('or: How I Learned to Stop Worrying and Love the Tanks', (5, 110),
                         20, 'White', 'monospace')
        canvas.draw_text('Play', (280, 180), 30, 'White', 'monospace')
        canvas.draw_text('Controls', (250, 275), 30, 'White', 'monospace')
        canvas.draw_text('Credits', (250, 365), 30, 'White', 'monospace')
        canvas.draw_polygon(
            [[220, 140], [420, 140], [420, 210], [220, 210]], 5, 'Red')
        canvas.draw_polygon(
            [[220, 230], [420, 230], [420, 300], [220, 300]], 5, 'Red')
        canvas.draw_polygon(
            [[220, 320], [420, 320], [420, 390], [220, 390]], 5, 'Red')

    def draw_controls_menu(self, canvas):
        canvas.draw_text('Controls', (190, 75), 50, 'White', 'monospace')

        # back button
        canvas.draw_polygon(
            [[10, 25], [150, 25], [150, 75], [10, 75]], 5, 'Red')
        canvas.draw_text('<-- Back', (15, 55), 20, 'White', 'monospace')

        # player 1 info
        canvas.draw_polygon(
            [[0, 100], [320, 100], [320, 480], [0, 480]], 5, 'Red')
        canvas.draw_text('Player 2', (90, 140), 30, 'White', 'monospace')
        canvas.draw_text('Movement: A: Turn Left',
                         (10, 180), 15, 'White', 'monospace')
        canvas.draw_text('          D: Turn Right',
                         (10, 200), 15, 'White', 'monospace')
        canvas.draw_text('          W: Move Forward',
                         (10, 220), 15, 'White', 'monospace')
        canvas.draw_text('          S: Move Backwards',
                         (10, 240), 15, 'White', 'monospace')
        canvas.draw_text('Actions:  C: Shoot', (10, 260),
                         15, 'White', 'monospace')

        # player 2 info
        canvas.draw_polygon(
            [[320, 100], [640, 100], [640, 480], [320, 480]], 5, 'Red')
        canvas.draw_text('Player 1', (410, 140), 30, 'White', 'monospace')
        canvas.draw_text('Movement: Left Arrow: Turn Left',
                         (330, 180), 15, 'White', 'monospace')
        canvas.draw_text('          Right Arrow: Turn Right',
                         (330, 200), 15, 'White', 'monospace')
        canvas.draw_text('          Up: Move Forward',
                         (330, 220), 15, 'White', 'monospace')
        canvas.draw_text('          Down: Move Backwards',
                         (330, 240), 15, 'White', 'monospace')
        canvas.draw_text('Actions:  Space: Shoot',
                         (330, 260), 15, 'White', 'monospace')

    def draw_credits_menu(self, canvas):
        canvas.draw_text('Credits', (200, 75), 50, 'White', 'monospace')

        # back button
        canvas.draw_polygon(
            [[10, 25], [150, 25], [150, 75], [10, 75]], 5, 'Red')
        canvas.draw_text('<-- Back', (15, 55), 20, 'White', 'monospace')

        canvas.draw_text('Created By: Group G32 - Antony Kotronakis, James Lee,',
                         (15, 140), 18, 'White', 'monospace')
        canvas.draw_text('                        Parker Reich and Inacio Rodrigues',
                         (15, 165), 18, 'White', 'monospace')

        canvas.draw_text('Artistic Source: Background - davis123 - OpenGameArt.org',
                         (15, 190), 18, 'White', 'monospace')
        canvas.draw_text('                 PowerUp - qubodup - OpenGameArt.org',
                         (15, 215), 18, 'White', 'monospace')
        canvas.draw_text('                 Player 1 and 2 Tanks, and Turrets - ',
                         (15, 240), 18, 'White', 'monospace')
        canvas.draw_text('                     aztrakatze - aztrakatze.itch.io',
                         (15, 265), 18, 'White', 'monospace')

        canvas.draw_text('Inspiration: "Tank Trouble" by Danish Mads Purup',
                         (15, 290), 18, 'White', 'monospace')
        canvas.draw_text('              https://tanktrouble.com',
                         (15, 315), 18, 'White', 'monospace')

    def draw_single_multi_menu(self, canvas):
        canvas.draw_text('Singleplayer', (240, 120), 30, 'White', 'monospace')
        canvas.draw_text('Multiplayer', (250, 230), 30, 'White', 'monospace')
        canvas.draw_polygon(
            [[180, 70], [500, 70], [500, 150], [180, 150]], 5, 'Red')
        canvas.draw_polygon(
            [[180, 180], [500, 180], [500, 260], [180, 260]], 5, 'Red')

    def frameSwitchMG(self):
        #
        # frame 1 = game
        # frame 2 = main menu
        # frame 3 = controls
        # frame 4 = credits
        #
        if self.frame == 2:
            self.new_level = True
            self.frame = 1
        elif self.frame == 1:
            self.frame = 2

    def frameSwitchMCo(self):
        if self.frame == 2:
            self.frame = 3
        elif self.frame == 3:
            self.frame = 2

    def frameSwitchMCr(self):
        if self.frame == 2:
            self.frame = 4
        elif self.frame == 4:
            self.frame = 2

    def frameSwitchMM(self):
        self.frame = 2

    def mouse_handler(self, position):
        if self.frame == 2:
            if ((position[0] < 420) and (position[0] > 220) and
                    (position[1] < 210) and (position[1] > 140)):
                self.frame = 5
                position = None
                return
            if ((position[0] < 420) and (position[0] > 220) and
                    (position[1] < 300) and (position[1] > 230)):
                self.frameSwitchMCo()
            if ((position[0] < 420) and (position[0] > 220) and
                    (position[1] < 390) and (position[1] > 320)):
                self.frameSwitchMCr()
        if self.frame == 3:
            if ((position[0] < 150) and (position[0] > 10) and
                    (position[1] < 75) and (position[1] > 25)):
                self.frameSwitchMCo()
        if self.frame == 4:
            if ((position[0] < 150) and (position[0] > 10) and
                    (position[1] < 75) and (position[1] > 25)):
                self.frameSwitchMCr()
        if self.frame == 5:
            if position:
                if ((position[0] < 500) and (position[0] > 180) and
                        (position[1] < 150) and (position[1] > 70)):
                    self.frame = 6
                    self.new_level = True
                if ((position[0] < 500) and (position[0] > 180) and
                        (position[1] < 260) and (position[1] > 180)):
                    self.frame = 1
                    self.new_level = True


class World:
    def __init__(self, player1, player2, kbd, background, score, powerup):
        self.player1 = player1
        self.player2 = player2
        self.kbd = kbd
        self.background = background
        self.score = score
        self.powerUp = powerup
        # NOTE(AKotro): List of rectangle walls
        self.rects = None
        # NOTE(AKotro): Dictionary of: colliders :: bool in_collision
        self.in_collision = {}
        self.in_col1 = {}
        self.in_col2 = {}
        self.in_tank_collision = set()
        # NOTE(AKotro): Generate maze, walls, in_collision
        self.maze = self.create_maze()
        self.time = Time()
        self.turrets = []
        self.menu = Menu()

    def init_in_collision(self):
        """Initialises the in_collision dictionaries."""
        for rect in self.rects:
            self.in_collision[rect] = False
            self.in_col1[rect] = False
            self.in_col2[rect] = False

    def create_maze(self):
        """Generates a maze and creates walls."""
        # Maze dimensions (ncols, nrows)
        nx, ny = CANVAS_WIDTH//100, CANVAS_HEIGHT//100
        # Random maze entry position
        ix, iy = random.randint(0, nx-1), random.randint(0, ny-1)

        # Generate maze
        maze = df_maze.Maze(CANVAS_WIDTH, CANVAS_HEIGHT, nx, ny, ix, iy)
        maze.generate_maze()

        # Get list of rectangle walls
        self.rects = maze.create_walls()
        # Initialise in_collision dictionaries
        self.init_in_collision()

        return maze

    def new_level(self):
        if self.menu.frame == 1:
            self.new_level_multi()
        elif self.menu.frame == 6:
            self.new_level_single()

    def new_level_single(self):
        """Creates a new maze and reinitializes the player and turrets."""
        self.create_maze()
        self.player1 = init_player_1()
        if self.turrets:
            self.turrets.clear()
        self.add_turrets()

    def new_level_multi(self):
        """Creates a new maze and reinitializes the players."""
        self.create_maze()
        self.player1 = init_player_1()
        self.player2 = init_player_2()

    def move_tanks(self):
        """Responds to inputs regarding tank movement/actions."""
        # Player1
        if self.player1 and not self.player1.stopped:
            if self.kbd.right:
                self.player1.img_rot -= self.player1.rot_step
                self.player1.look_pos.rotate_rad(-self.player1.rot_step)
            if self.kbd.left:
                self.player1.img_rot += self.player1.rot_step
                self.player1.look_pos.rotate_rad(self.player1.rot_step)
            if self.kbd.up:
                self.player1.vel.add(self.player1.look_pos)
            if self.kbd.down:
                self.player1.vel.add(-self.player1.look_pos)
            if self.kbd.shoot:
                self.player1.shoot()
                self.kbd.shoot = False

        # Player2
        if self.player2 and not self.player2.stopped:
            if self.kbd.right2:
                self.player2.img_rot -= self.player2.rot_step
                self.player2.look_pos.rotate_rad(-self.player2.rot_step)
            if self.kbd.left2:
                self.player2.img_rot += self.player2.rot_step
                self.player2.look_pos.rotate_rad(self.player2.rot_step)
            if self.kbd.up2:
                self.player2.vel.add(self.player2.look_pos)
            if self.kbd.down2:
                self.player2.vel.add(-self.player2.look_pos)
            if self.kbd.shoot2:
                self.player2.shoot()
                self.kbd.shoot2 = False

    def bounce_tanks(self):
        # TODO(AKotro): This collision response needs to be changed
        # Get vector between ball centers
        sep_vec = self.player1.pos.copy() - self.player2.pos.copy()
        # Get unit vector along the line of colision
        unit = sep_vec.copy().normalize()

        # Extract parallel and perpendicular velocities
        v1_par = self.player1.vel.get_proj(unit)
        v1_perp = self.player1.vel.copy() - v1_par
        v2_par = self.player2.vel.get_proj(unit)
        v2_perp = self.player2.vel.copy() - v2_par

        # Exchange velocities
        self.player1.vel = v2_par + v1_perp
        self.player1.vel += sep_vec.normalize()
        self.player2.vel = v1_par + v2_perp
        self.player2.vel += sep_vec.normalize()

    def collide_tanks(self, col1, col2):
        if col1.hit(col2):
            col1_col2 = (col1, col2) in self.in_tank_collision
            col2_col1 = (col2, col1) in self.in_tank_collision

            if not col1_col2 and not col2_col1:
                self.bounce_tanks()
                self.in_tank_collision.add((col1, col2))
        else:
            self.in_tank_collision.discard((col1, col2))
            self.in_tank_collision.discard((col2, col1))

    def handle_tank_collision(self, player, rect, in_collision):
        """Handles tank collision with static rectangles (walls)."""
        if rect.overlaps_circle(player.collider):
            if not self.in_collision[rect]:
                if player.vel != Vector.zero():
                    normal = rect.normal(player.pos)
                    distance = rect.distance(normal, player.collider.pos)
                    player.vel += (normal * -player.vel.copy().dot(normal)
                                   + distance.normalize())
                    in_collision[rect] = True
        else:
            in_collision[rect] = False

    def handle_bullet_collision(self, player, rect, bullet):
        """Handles bullet collision with static rectangles (walls)."""
        # IMPORTANT BUG(AKotro): If the ball hits two
        # adjacent walls at the same time, the reflection
        # cancels out and the ball goes through!
        # NOTE: A potential solution: collect a set of vectors to bounce and
        # execute the bounces after the iteration.
        if rect.overlaps_circle(bullet):
            if not self.in_collision[rect]:
                normal = rect.normal(bullet.pos)
                bullet.bounce(normal)
                self.in_collision[rect] = True
                # If the ball bounces 4 times, destroy it
                if bullet.bounce_counter >= 4 and bullet in player.bullets:
                    player.bullets.remove(bullet)
        else:
            self.in_collision[rect] = False

    def handle_power_up_collisions(self, tank):
        self.powerUp.generate_new()
        if self.powerUp.hasHitPowerUp(tank.collider):
            self.powerUp.disappear(tank.collider)
            if self.powerUp.check_type() == 'superSpeed':
                tank.look_pos.multiply(1.4)
                tank.bullet_speed = tank.bullet_speed*0.5
            if self.powerUp.check_type() == 'miniTank':
                tank.spritesheet.scale = tank.spritesheet.scale * 0.5
                tank.collider.radius = tank.collider.radius*0.5
            if self.powerUp.check_type() == 'giantBullets':
                tank.bullet_size = 16
            if self.powerUp.check_type() == 'machineGun':
                tank.max_bullets = 10
            if self.powerUp.check_type() == 'supersonicBullet':
                tank.bullet_speed = 15

    def handle_collisions(self):
        """Handles all collisions."""
        for rect in self.rects:
            # NOTE(AKotro): Handle tank collisions
            if self.player1:
                self.handle_tank_collision(self.player1, rect, self.in_col1)
            if self.player2:
                self.handle_tank_collision(self.player2, rect, self.in_col2)

            # NOTE(AKotro): Handle bullet collisions
            if self.player1 and self.player1.bullets_not_empty():
                for bullet in self.player1.bullets:
                    self.handle_bullet_collision(self.player1, rect, bullet)
            if self.player2 and self.player2.bullets_not_empty():
                for bullet in self.player2.bullets:
                    self.handle_bullet_collision(self.player2, rect, bullet)

            # NOTE(AKotro): Handle turret collisions
            if self.turrets:
                for turret in self.turrets:
                    if turret.bullets_not_empty():
                        for bullet in turret.bullets:
                            self.handle_bullet_collision(turret, rect, bullet)

        if self.player1 and self.player2:
            self.collide_tanks(self.player1.collider, self.player2.collider)

        self.handle_power_up_collisions(self.player1)
        self.handle_power_up_collisions(self.player2)

    def hit_player(self, player, bullet):
        """Responds to when a player is hit by a bullet
        (explosion, score, bullet removal).
        """
        if player == self.player1:
            p = 1
            other_player = self.player2
        elif player == self.player2:
            p = 2
            other_player = self.player1

        if player and bullet.hit(player.collider):
            if not player.explosion:
                player.explode()

                # Increment correct score
                if p == 1:
                    self.score.incrementScore2()
                elif p == 2:
                    self.score.incrementScore1()

                if self.score.checkScore():
                    self.menu.frame = 2
                    self.score.resetScores()
                self.score.printScore()
            player.stopped = True
            other_player.bullets.remove(bullet)

    def add_turrets(self):
        # TODO(AKotro): Get valid spawn position
        """Creates new turret and adds it to the list."""
        valid_positions = [
            Vector(CANVAS_WIDTH*0.1, CANVAS_HEIGHT*0.1),
            # Vector(CANVAS_WIDTH*0.9, CANVAS_HEIGHT*0.9),
            Vector(CANVAS_WIDTH*0.1, CANVAS_HEIGHT*0.9),
            Vector(CANVAS_WIDTH*0.9, CANVAS_HEIGHT*0.1),
        ]
        turret1 = init_turret(valid_positions[0])
        turret2 = init_turret(valid_positions[1])
        turret3 = init_turret(valid_positions[2])
        self.turrets.append(turret1)
        self.turrets.append(turret2)
        self.turrets.append(turret3)

    def update(self):
        # Handle all collisions
        self.handle_collisions()
        self.move_tanks()

        if self.player1:
            self.player1.update()

            # Check if bullet hit other player
            if self.player1.bullets_not_empty():
                for bullet in self.player1.bullets:
                    if self.menu.frame == 1:
                        self.hit_player(self.player2, bullet)

                    # Hit turret?
                    if self.turrets:
                        for turret in self.turrets:
                            if bullet.hit(turret.collider):
                                if not turret.explosion:
                                    turret.explode()
                                    self.player1.bullets.remove(bullet)

        if self.menu.frame == 1 and self.player2:
            self.player2.update()

            # Check if bullet hit other player
            if self.player2.bullets_not_empty():
                for bullet in self.player2.bullets:
                    self.hit_player(self.player1, bullet)

        if self.turrets:
            for turret in self.turrets:
                turret.update()
                # NOTE(AKotro): If player2 is close enough, face and shoot!
                turret.target_player(self.player1)

    def draw(self, canvas):
        if self.menu.frame == 1:
            # NOTE(AKotro): Multiplayer

            # NOTE(AKotro): If menu signals to create new level, create it
            if self.menu.new_level:
                self.new_level_multi()
                self.menu.new_level = False
            self.time.tick()
            self.update()

            # Draw background
            self.background.draw(canvas)

            if self.player1:
                self.player1.draw(canvas)
                # If explosion is done, delete player and reset level
                if self.player1.is_explosion_done():
                    self.player1 = None
                    # Reset level
                    self.new_level_multi()
            if self.player2:
                self.player2.draw(canvas)
                # If explosion is done, delete player and reset level
                if self.player2.is_explosion_done():
                    self.player2 = None
                    # Reset level
                    self.new_level_multi()

            canvas.draw_text(self.score.score, (CANVAS_WIDTH-200, 20),
                             20, 'Red', 'monospace')

            for rect in self.rects:
                rect.draw(canvas)

            self.powerUp.draw(canvas)
            # NOTE(AKotro): Uncomment this to show fps
            # self.time.print_fps(canvas)
        elif self.menu.frame == 2:
            self.menu.draw_main_menu(canvas)
        elif self.menu.frame == 3:
            self.menu.draw_controls_menu(canvas)
        elif self.menu.frame == 4:
            self.menu.draw_credits_menu(canvas)
        elif self.menu.frame == 5:
            self.menu.draw_single_multi_menu(canvas)
        elif self.menu.frame == 6:
            # NOTE(AKotro): Singleplayer

            # NOTE(AKotro): If menu signals to create new level, create it
            if self.menu.new_level:
                self.new_level_single()
                self.menu.new_level = False
            self.time.tick()
            self.update()

            # Draw background
            self.background.draw(canvas)

            if self.player1:
                self.player1.draw(canvas)
                # If explosion is done, delete player and reset level
                if self.player1.is_explosion_done():
                    self.player1 = None
                    # Reset level
                    self.new_level_single()

            for rect in self.rects:
                rect.draw(canvas)

            if self.turrets:
                for turret in self.turrets:
                    turret.draw(canvas)
                    if turret.is_explosion_done():
                        self.turrets.remove(turret)
                        if not self.turrets:
                            self.new_level_single()

            self.powerUp.draw(canvas)


def init_player_1():
    # Get player 1 spritesheet
    sheet = Spritesheet("https://i.imgur.com/54ZAzF7.png", 8, 1,
                        8, 2, Vector(), 0.85)
    # Initialise tank
    player1 = Tank(Vector(CANVAS_WIDTH*0.9, CANVAS_HEIGHT*0.9), sheet,
                   "#5742B7")
    return player1


def init_player_2():
    # Get player 2 spritesheet
    sheet = Spritesheet("https://i.imgur.com/7WRDdVS.png", 9, 1,
                        9, 2, Vector(), 0.85)
    # Initialise tank
    player2 = Tank(Vector(CANVAS_WIDTH*0.1, CANVAS_HEIGHT*0.1), sheet,
                   "#449832")
    return player2


def init_turret(pos):
    # Get turret spritesheet
    sheet = Spritesheet("https://i.imgur.com/n1wKKOO.png", 8, 1,
                        8, 2, Vector(), 0.85)
    # Initialise tank
    turret = Turret(pos, sheet, "#ffa327")
    return turret


def main():
    frame = simplegui.create_frame("Boom Bots", CANVAS_WIDTH, CANVAS_HEIGHT)
    player1 = init_player_1()
    player2 = init_player_2()

    kbd = Keyboard()

    background = Background(GAME_BG_IMG, 500, 500)
    score = Score()
    powerup = PowerUp(POWERUP_IMG, 64, 64)
    world = World(player1, player2, kbd, background, score, powerup)

    # Exit/Keyboard stuff {{{
    def exit_game():
        # timer.stop()
        print("Stopping timers...")
        frame.stop()
        print("Closing frame...")
        print("Exiting...")

    def dummy():
        print("")

    def keydown_handler(key):
        kbd.keydown(key)

        # if key == simplegui.KEY_MAP['p']:
        #     if world.menu.frame == 2:
        #         world.menu.frameSwitchMG()
        # if key == simplegui.KEY_MAP['t']:
        #     world.add_turret()
        if key == simplegui.KEY_MAP['r']:
            world.new_level()
        if key == simplegui.KEY_MAP['q']:
            exit_game()

    frame.set_keydown_handler(keydown_handler)
    frame.set_keyup_handler(kbd.keyup)
    # frame.add_button("Green: C to shoot", dummy)
    # frame.add_button("Blue: SPACE to shoot", dummy)
    # frame.add_button("Click or press R to reset level", world.create_maze)
    frame.add_button("Click to exit to menu", world.menu.frameSwitchMM)
    frame.add_button("Click or press Q to exit game", exit_game)
    # frame.add_button("Test, Click to Switch M to G", world.menu.frameSwitchMG)
    frame.set_mouseclick_handler(world.menu.mouse_handler)
    # }}}

    frame.set_draw_handler(world.draw)

    frame.start()


if __name__ == "__main__":
    main()
