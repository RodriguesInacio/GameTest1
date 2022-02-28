import random
from vector import Vector
from collider import Wall, Rect

# NOTE(AKotro): Create a maze using the depth-first algorithm described at:
# https://en.wikipedia.org/wiki/Maze_generation_algorithm
# https://medium.com/swlh/solving-mazes-with-depth-first-search-e315771317ae
# https://scipython.com/blog/making-a-maze/
# http://www.migapro.com/depth-first-search/


class Cell:
    """A cell in the maze.

    A maze "Cell" is a point in the grid which may be surrounded by walls to
    the north, east, south or west.

    """

    # NOTE(AKotro): A wall separates a pair of cells
    # in the N-S or W-E directions.
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y):
        """Initialize the cell at (x,y). At first it is surrounded by walls."""

        # NOTE(AKotro): Initial position
        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}

    def has_all_walls(self):
        """Does this cell still have all its walls?"""

        return all(self.walls.values())

    def create_path(self, other, wall):
        """Knock down the wall between cells self and other."""

        self.walls[wall] = False
        other.walls[Cell.wall_pairs[wall]] = False


class Maze:
    """A Maze, represented as a grid of cells."""

    def __init__(self, width, height, nx, ny, ix=0, iy=0):
        """Initialize the maze grid.
        The maze consists of nx : ny cells and will be constructed starting
        at the cell indexed at (ix, iy).
        """

        # NOTE(AKotro): Height and width of the canvas maze in pixels
        self.width = width
        self.height = height

        self.nx, self.ny = nx, ny
        self.ix, self.iy = ix, iy
        self.maze = [[Cell(x, y) for y in range(ny)] for x in range(nx)]

    def cell_at(self, x, y):
        """Return the Cell object at (x,y)."""

        return self.maze[x][y]

    def __str__(self):
        """Return a (crude) string representation of the maze."""

        rows = ['-' * self.nx * 2]
        for y in range(self.ny):
            row = ['|']
            for x in range(self.nx):
                if self.maze[x][y].walls['E']:
                    row.append(' |')
                else:
                    row.append('  ')
            rows.append(''.join(row))
            row = ['|']
            for x in range(self.nx):
                if self.maze[x][y].walls['S']:
                    row.append('-+')
                else:
                    row.append(' +')
            rows.append(''.join(row))
        return '\n'.join(rows)

    def create_walls(self):
        """
        Create walls from maze.

        Returns a list of wall pairs, eg. [["l", "r"], ["t", "b"]].
        """

        # NOTE(AKotro): List of created rectangles
        created_rects = []
        # NOTE(AKotro): Scaling factors mapping maze coordinates
        # to image coordinates
        y_scale, x_scale = self.height / self.ny, self.width / self.nx

        def create_wall(x1, y1, x2, y2):
            if x1 == x2:
                # NOTE(AKotro): Wall is vertical
                rect = Rect(Vector(x1-1, y1), Vector(2, y2-y1))
                created_rects.append(rect)
            elif y1 == y2:
                # NOTE(AKotro): Wall is horizontal
                rect = Rect(Vector(x1, y1-1), Vector(x2-x1, 2))
                created_rects.append(rect)

        # NOTE(AKotro): Draw the "South" and "East" walls of each cell,
        # if present (these are the "North" and "West" walls of a
        # neighbouring cell in general, of course).
        for x in range(self.nx):
            for y in range(self.ny):
                if self.cell_at(x, y).walls['S']:
                    x1, y1 = x * x_scale, (y + 1) * y_scale
                    x2, y2 = (x + 1) * x_scale, (y + 1) * y_scale

                    create_wall(x1, y1, x2, y2)
                if self.cell_at(x, y).walls['E']:
                    x1, y1 = (x + 1) * x_scale, y * y_scale
                    x2, y2 = (x + 1) * x_scale, (y + 1) * y_scale

                    create_wall(x1, y1, x2, y2)
        # NOTE(AKotro): Draw the North and West maze border, which won't
        # have been drawn by the procedure above.
        create_wall(0, -1, self.width-1, -1)
        create_wall(-1, 0, -1, self.height)

        return created_rects

    def write_svg(self, filename):
        """Write an SVG image of the maze to filename."""

        # NOTE(AKotro): Pad the maze all around by this amount.
        padding = 10
        # NOTE(AKotro): Scaling factors mapping maze coordinates
        # to image coordinates
        y_scale, x_scale = self.height / self.ny, self.width / self.nx

        def write_wall(ww_f, ww_x1, ww_y1, ww_x2, ww_y2):
            """Write a single wall to the SVG image file handle f."""

            print('<line x1="{}" y1="{}" x2="{}" y2="{}"/>'
                  .format(ww_x1, ww_y1, ww_x2, ww_y2), file=ww_f)

        # NOTE(AKotro): Write the SVG image file for maze
        with open(filename, 'w') as f:
            # NOTE(AKotro): SVG preamble and styles.
            print('<?xml version="1.0" encoding="utf-8"?>', file=f)
            print('<svg xmlns="http://www.w3.org/2000/svg"', file=f)
            print('    xmlns:xlink="http://www.w3.org/1999/xlink"', file=f)
            print('    width="{:d}" height="{:d}" viewBox="{} {} {} {}">'
                  .format(self.width + 2 * padding, self.height + 2 * padding,
                          -padding, -padding, self.width + 2 * padding, self.height + 2 * padding),
                  file=f)
            print('<defs>\n<style type="text/css"><![CDATA[', file=f)
            print('line {', file=f)
            print('    stroke: #000000;\n    stroke-linecap: square;', file=f)
            print('    stroke-width: 5;\n}', file=f)
            print(']]></style>\n</defs>', file=f)
            # NOTE(AKotro): Draw the "South" and "East" walls of each cell,
            # if present (these are the "North" and "West" walls of a
            # neighbouring cell in general, of course).
            for x in range(self.nx):
                for y in range(self.ny):
                    if self.cell_at(x, y).walls['S']:
                        x1, y1 = x * x_scale, (y + 1) * y_scale
                        x2, y2 = (x + 1) * x_scale, (y + 1) * y_scale
                        write_wall(f, x1, y1, x2, y2)
                    if self.cell_at(x, y).walls['E']:
                        x1, y1 = (x + 1) * x_scale, y * y_scale
                        x2, y2 = (x + 1) * x_scale, (y + 1) * y_scale
                        write_wall(f, x1, y1, x2, y2)
            # NOTE(AKotro): Draw the North and West maze border, which won't
            # have been drawn by the procedure above.
            print('<line x1="0" y1="0" x2="{}" y2="0"/>'.format(self.width), file=f)
            print('<line x1="0" y1="0" x2="0" y2="{}"/>'.format(self.height), file=f)
            print('</svg>', file=f)

    def get_valid_neighbours(self, cell):
        """Return a list of unvisited neighbours to cell."""

        delta = [('W', (-1, 0)),
                 ('E', (1, 0)),
                 ('S', (0, 1)),
                 ('N', (0, -1))]
        neighbours = []
        for direction, (dx, dy) in delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.nx) and (0 <= y2 < self.ny):
                neighbour = self.cell_at(x2, y2)
                if neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
        return neighbours

    def generate_maze(self):
        # NOTE(AKotro): Total number of cells.
        n = self.nx * self.ny
        # NOTE(AKotro): Stack of cells
        cell_stack = []
        current_cell = self.cell_at(self.ix, self.iy)
        # NOTE(AKotro): Total number of visited cells during maze construction.
        nv = 1

        while nv < n:
            # NOTE(AKotro): Get unvisited neighbouring cells
            neighbours = self.get_valid_neighbours(current_cell)

            if not neighbours:
                # NOTE(AKotro): We've reached a dead end: backtrack.
                current_cell = cell_stack.pop()
                continue

            # NOTE(AKotro): Choose a random neighbouring cell and move to it.
            direction, next_cell = random.choice(neighbours)
            current_cell.create_path(next_cell, direction)
            cell_stack.append(current_cell)
            current_cell = next_cell
            nv += 1
