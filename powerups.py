try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
import random
import math
CANVAS_WIDTH = 640
CANVAS_HEIGHT = 480
pTimer = 0
img="https://opengameart.org/sites/default/files/backgrounddetailed8.png"
class PowerUp:
    def __init__(self, img, img_width, img_height): # add powerups like for instance self.giant ball
        self.pos=Vector(CANVAS_WIDTH/2, CANVAS_HEIGHT/2)
        self.powerups=['superSpeed', 'miniTank', 'giantBullets', 'machineGun', 'supersonicBullet']
        self.type = self.powerups[random.randint(0, len(self.powerups)-1)]
        self.img = simplegui.load_image(img)
        self.img_width = img_width
        self.img_height = img_height

    def draw(self, canvas):
        SOURCE_CENTRE = ((self.img_width/2), (self.img_height/2))
        SOURCE_SIZE = (self.img_width, self.img_height)
        # doesn't have to be same aspect ratio as frame!
        DEST_SIZE = (self.img_width/2, self.img_height/2)

        canvas.draw_image(self.img,
                          SOURCE_CENTRE,
                          SOURCE_SIZE,
                          self.pos.get_p(),
                          DEST_SIZE)
    
    def hasHitPowerUp(self, ball):
        sep_vec = self.pos.copy() - ball.pos
        #print(sep_vec)
        return sep_vec.length() < self.img_width/2 + ball.radius

    def check_type(self):
        return self.type

    def generate_new(self):
        global pTimer
        pTimer+=1
        if pTimer % 1500 == 0:
            index = random.randint(0, len(self.powerups)-1)
            self.type = self.powerups[index]
            self.pos = Vector(random.randint(self.img_width, CANVAS_WIDTH-self.img_width),
                              random.randint(self.img_height, CANVAS_HEIGHT-self.img_height))
         
    
    def disappear(self, ball):
        if self.hasHitPowerUp(ball):
            self.pos = Vector(-100,-100)

