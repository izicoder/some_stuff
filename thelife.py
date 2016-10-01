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

    def get_cell(self, x, y):
        return self.matrix[y][x]


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
    scr.addstr(1, 1, 'hello world')
    scr.getkey()

if __name__ == '__main__':
    main()
