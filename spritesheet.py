try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector


class Spritesheet:
    def __init__(self, url, columns, rows, num_frames,
                 frame_duration=1, dest_centre=None, scale=1):
        self.img = simplegui.load_image(url)

        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.columns = columns
        self.rows = rows

        self.num_frames = num_frames
        self.frame_number = 1
        self.frame_duration = frame_duration

        self.frame_width = self.width / columns
        self.frame_height = self.height / rows
        self.frame_center = Vector(self.frame_width/2, self.frame_height/2)

        self.dest_centre = dest_centre
        self.img_rot = 0
        self.scale = scale
        # self.scale = random.uniform(0.5, 2)

        self.frame_index = [0, 0]

    def draw(self, canvas, frame_index):
        source_center = (
            self.frame_width * frame_index[0] + self.frame_center.x,
            self.frame_height * frame_index[1] + self.frame_center.y
        )
        source_size = (self.frame_width, self.frame_height)

        # if self.dest_centre is None:
        #     self.dest_centre = (CANVAS_WIDTH/2,
        #                         CANVAS_HEIGHT-(self.frame_height/2.1))
        dest_size = (self.scale * self.frame_width,
                     self.scale * self.frame_height)

        canvas.draw_image(
            self.img, source_center, source_size,
            self.dest_centre, dest_size, self.img_rot
        )

    def transition(self, time):
        return bool(time % self.frame_duration == 0)

    def done(self):
        return bool(self.frame_number == self.num_frames)

    def next_frame(self):
        self.frame_number += 1
        if (self.frame_index[0] < self.columns-1 and
                self.frame_number <= self.num_frames):
            # Next column
            self.frame_index[0] += 1
        elif self.frame_index[1] < self.rows-1:
            # Next row
            self.frame_index[0] = 0
            self.frame_index[1] += 1
        else:
            # Restart
            self.frame_index = [0, 0]
            self.frame_number = 1
