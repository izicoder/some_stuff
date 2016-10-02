#!/usr/bin/env python3
import curses


# cell class
class Cell:
    def __init__(self, x, y):
        # cell status
        self.is_dead = True

        # read only cell coordinates
        self.x, self.y = x, y

        # cell neighbors
        self.neighbors = (
            (x-1, y-1),
            (x,   y-1),
            (x+1, y-1),
            (x-1, y),
            (x+1, y),
            (x-1, y+1),
            (x,   y+1),
            (x+1, y+1))


# global map class
class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = []
        for y in range(height):
            self.matrix.append([])
            for x in range(width):
                self.matrix[y].append(Cell(x, y))

    def calc_coord(self, x, y):
        x = (
            self.width-abs(x)
            if x < 0
            else
            self.width-x
            if x >= self.width
            else x)

        y = (
            self.height-abs(y)
            if y < 0
            else
            self.height-y
            if y >= self.height
            else
            y)

        if 0 <= x < self.width and 0 <= y < self.height:
            return x, y
        else:
            return self.calc_coord(x, y)

    def get_cell(self, x, y):
        x, y = self.calc_coord(x, y)
        return self.matrix[y][x]


# map printing function
def print_map(scr, gamemap, xshf=0, yshf=0, life='#', dead=' '):
    for y in range(gamemap.height):
        for x in range(gamemap.width):
            scr.addch(
                y+yshf,
                x+xshf,
                dead if gamemap.get_cell(y, x).is_dead else life)
    scr.refresh()


# curses exception decorator
def excwrap(fun):
    def wrapped(*v, **kv):
        try:
            return fun(*v, **kv)
        except Exception as exc:
            raise exc
        finally:
            curses.endwin()
    return wrapped


# main function
@excwrap
def main():
    scr = curses.initscr()
    gmap = Map(5, 5)

    for y in range(-1, 2):
        for x in range(-1, 2):
            gmap.get_cell(x, y).is_dead = False

    print_map(scr, gmap, dead='.')
    scr.getkey()

if __name__ == '__main__':
    main()
