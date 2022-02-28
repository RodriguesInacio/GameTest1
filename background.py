try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

CANVAS_WIDTH = 640
CANVAS_HEIGHT = 480
#img = "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/03d6d1a5-7133-460b-a65f-b403f180281d/d5vi8b0-9925c151-97d4-4318-8a23-af91c8f561d5.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3sicGF0aCI6IlwvZlwvMDNkNmQxYTUtNzEzMy00NjBiLWE2NWYtYjQwM2YxODAyODFkXC9kNXZpOGIwLTk5MjVjMTUxLTk3ZDQtNDMxOC04YTIzLWFmOTFjOGY1NjFkNS5qcGcifV1dLCJhdWQiOlsidXJuOnNlcnZpY2U6ZmlsZS5kb3dubG9hZCJdfQ.IgdZpDZHjNU21aRONHjBtaw9TcA25WC2SYLc0FExaaw"
IMG = "https://opengameart.org/sites/default/files/backgrounddetailed8.png"


class Background:
    def __init__(self, img, img_width, img_height):
        self.img = simplegui.load_image(img)
        self.img_width = img_width
        self.img_height = img_height

    def draw(self, canvas):
        SOURCE_CENTRE = ((self.img_width/2), (self.img_height/2))
        SOURCE_SIZE = (self.img_width, self.img_height)
        # doesn't have to be same aspect ratio as frame!
        DEST_SIZE = (CANVAS_WIDTH, CANVAS_HEIGHT)

        canvas.draw_image(self.img,
                          SOURCE_CENTRE,
                          SOURCE_SIZE,
                          ((CANVAS_WIDTH/2), (CANVAS_HEIGHT/2)),
                          DEST_SIZE)

# Create a frame and assign callbacks to event handlers
# bg = Background(500,500)
# frame = simplegui.create_frame("Background", CANVAS_WIDTH, CANVAS_HEIGHT)
# frame.set_draw_handler(bg.draw)

# frame.start()
