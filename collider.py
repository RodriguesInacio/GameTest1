import math
from vector import Vector


class Wall:
    """A line collider defined by 2 points: pos1, pos2."""

    def __init__(self, direction, pos1, pos2, border, color):
        self.direction = direction
        self.pos1 = pos1
        self.pos2 = pos2
        self.border = border
        self.color = color

    def draw(self, canvas):
        canvas.draw_line((self.pos1.x, self.pos1.y),
                         (self.pos2.x, self.pos2.y),
                         self.border*2,
                         self.color)

    def normal(self, ball):
        """Returns the normal Vector of the wall depending on direction."""

        if self.direction == "l":
            result = Vector(1, 0)
        elif self.direction == "r":
            result = Vector(-1, 0)
        elif self.direction == "t":
            result = Vector(0, 1)
        elif self.direction == "b":
            result = Vector(0, -1)
        else:
            print("Error: Direction ({}) not valid".format(self.direction))
        return result

    def collided(self, ball):
        """Returns True if collided with Ball"""

        # BUG(AKotro): Collision in corners of walls is weird!

        # Find closest point on the line segment to the circle
        line = self.pos2 - self.pos1
        line_length = line.length()
        line_norm = (1/line_length)*line
        segment_to_circle = ball.pos - self.pos1
        closest_point_on_segment = segment_to_circle.dot(line) / line_length

        # Special cases where the closest point is the end points
        closest = Vector()
        if closest_point_on_segment <= 0:
            closest = self.pos1
        elif closest_point_on_segment >= line_length:
            closest = self.pos2
        else:
            closest = self.pos1 + closest_point_on_segment*line_norm

        # Get distance
        distance = ball.pos - closest
        if distance.length()+self.border > ball.radius+ball.border:
            return False
        return True, distance


class Domain:
    def __init__(self, pos, radius, border, color, border_color):
        self.pos = pos
        self.radius = radius
        self.border = border
        self.color = color
        self.border_color = border_color
        self.edge = self.radius + self.border

    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(),
                           self.radius,
                           self.border,
                           self.border_color,
                           self.color)

    def normal(self, ball):
        perpendicular = self.pos.copy() - ball.pos
        return perpendicular.normalize()

    def hit(self, ball):
        distance = (self.pos.copy() - ball.pos).length()
        return distance <= self.edge


class Rect:
    """A 2d rectangle with a pos vector which represents the top-left corner
    and a size vector which represents the width/height.
    """
    def __init__(self, pos=None, size=None, points=None,
                 line_width=None, line_color=None):
        if pos and size:
            # NOTE(AKotro): Define rectangle from pos and size

            # NOTE(AKotro): Top left corner of rect
            self.pos = pos
            # NOTE(AKotro): Width/height of rect
            self.size = size
            p1 = (self.pos.x, self.pos.y)
            p2 = (self.pos.x + self.size.x, self.pos.y)
            p3 = (self.pos.x + self.size.x, self.pos.y+self.size.y)
            p4 = (self.pos.x, self.pos.y + self.size.y)
            self.points = [p1, p2, p3, p4]
        else:
            # NOTE(AKotro): Define rectangle from points
            self.pos = Vector(points[0][0], points[0][1])
            self.size = Vector(points[2][0] - self.pos.x,
                               points[2][0] - self.pos.y)
            self.points = points
        if line_width:
            self.line_width = line_width
        else:
            self.line_width = 2
        if line_color:
            self.line_color = line_color
        else:
            self.line_color = "brown"

        self.width = self.pos.x + self.size.x
        self.height = self.pos.y + self.size.y

    def draw(self, canvas):
        canvas.draw_polygon(self.points, self.line_width, self.line_color)

    def __hash__(self):
        return id(self)

    def __str__(self):
        return "Pos: ({}, {}), Size: ({}, {})".format(self.pos.x, self.pos.y,
                                                      self.size.x, self.size.y)

    def __eq__(self, rect):
        return self.pos == rect.pos and self.size == rect.size

    def __ne__(self, rect):
        return not self.__eq__(rect)

    def center(self):
        """Returns the center of the rectangle."""
        return (self.width/2, self.height/2)

    def scale(self, s):
        """Scales the rectangle by a scalar value."""
        self.pos *= s
        self.size *= s
        return self

    def normal(self, pos):
        """Returns the normal of the rectangle side depending on pos."""
        result = Vector(0, 0)
        if pos.x < self.pos.x:
            # Left
            result = Vector(-1, 0)
        elif pos.x > self.width:
            # Right
            result = Vector(1, 0)
        elif pos.y < self.pos.y:
            # Top
            result = Vector(0, -1)
        elif pos.y > self.height:
            # Bottom
            result = Vector(0, 1)
        return result

    def distance(self, normal, pos):
        """Returns the distance of pos from the normal of the rectangle."""
        def get_distance_from_side(pos1, pos2, pos):
            # Find closest point on the line segment to the circle
            line = pos2 - pos1
            line_length = line.length()
            line_norm = (1/line_length)*line
            segment_to_circle = pos - pos1
            closest_point_on_segment = (segment_to_circle.dot(line) /
                                        line_length)

            # Special cases where the closest point is the end points
            closest = Vector()
            if closest_point_on_segment <= 0:
                closest = pos1
            elif closest_point_on_segment >= line_length:
                closest = pos2
            else:
                closest = pos1 + closest_point_on_segment*line_norm

            # Get distance
            distance = pos - closest
            return distance

        p1 = Vector(self.pos.x, self.pos.y)
        p2 = Vector(self.pos.x + self.size.x, self.pos.y)
        p3 = Vector(self.pos.x + self.size.x, self.pos.y+self.size.y)
        p4 = Vector(self.pos.x, self.pos.y + self.size.y)
        if normal == Vector(-1, 0):
            distance = get_distance_from_side(p1, p4, pos)
        elif normal == Vector(1, 0):
            distance = get_distance_from_side(p2, p3, pos)
        elif normal == Vector(0, -1):
            distance = get_distance_from_side(p1, p2, pos)
        elif normal == Vector(0, 1):
            distance = get_distance_from_side(p3, p4, pos)
        return distance

    def contains(self, pt):
        """Returns True if point pt is inside the rectangle."""
        return (self.pos.x < pt.x < self.width and
                self.pos.y < pt.y < self.height)
        # return (pt.x >= self.pos.x and pt.x < self.pos.x + self.size.x and
        #         pt.y >= self.pos.y and pt.y < self.pos.y + self.size.y)

    def overlaps(self, rect):
        """Returns True if rect overlaps with this rectangle."""
        distance = rect.center() - self.pos
        return (self.pos.x + self.size.x >= rect.pos.x and
                self.pos.y + self.size.y >= rect.pos.y and
                self.pos.x < rect.pos.x + rect.size.x and
                self.pos.y < rect.pos.y + rect.size.y, distance)

    def line_circle(self, pos1, pos2, ball):
        """Returns True if ball has collided with line segment pos1,pos2"""
        # Find closest point on the line segment to the circle
        line = pos2 - pos1
        line_length = line.length()
        line_norm = (1/line_length)*line
        segment_to_circle = ball.pos - pos1
        closest_point_on_segment = segment_to_circle.dot(line) / line_length

        # Special cases where the closest point is the end points
        closest = Vector()
        if closest_point_on_segment <= 0:
            closest = pos1
        elif closest_point_on_segment >= line_length:
            closest = pos2
        else:
            closest = pos1 + closest_point_on_segment*line_norm

        # Get distance
        distance = ball.pos - closest
        if distance.length() > ball.radius+ball.border:
            return False
        return True

    def overlaps_circle(self, ball):
        """Returns True if ball overlaps with this rectangle."""
        p1 = Vector(self.pos.x, self.pos.y)
        p2 = Vector(self.pos.x + self.size.x, self.pos.y)
        p3 = Vector(self.pos.x + self.size.x, self.pos.y+self.size.y)
        p4 = Vector(self.pos.x, self.pos.y + self.size.y)
        return (self.contains(ball.pos) or
                self.line_circle(p1, p2, ball) or
                self.line_circle(p2, p3, ball) or
                self.line_circle(p3, p4, ball) or
                self.line_circle(p4, p1, ball))
