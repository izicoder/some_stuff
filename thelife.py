#!/usr/bin/env python3
import curses
from random import randint


# cell class
class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y

        # True - alive, False - dead
        self.state = False
        self.next_state = False  # state for next generation

        # cell neighbors
        self.neighbors = (
            (x-1, y-1),  # left top
            (x,   y-1),  # top
            (x+1, y-1),  # right top
            (x-1, y),    # left
            (x+1, y),    # right
            (x-1, y+1),  # left bottom
            (x,   y+1),  # bottom
            (x+1, y+1))  # right bottom


# cell map class
class CellMap:
    def __init__(self, width, height):
        self.width, self.height = width, height

        # cell matrix
        self.matrix = [
            [Cell(x, y) for x in range(width)]
            for y in range(height)]

    def calc_coord(self, x, y):
        if x < 0:
            x = self.width - abs(x)
        elif x >= self.width:
            x = abs(self.width - x)

        if y < 0:
            y = self.height - abs(y)
        elif y >= self.height:
            y = abs(self.height - y)

        return x, y

    def get_cell(self, x, y):
        x, y = self.calc_coord(x, y)
        return self.matrix[y][x]


# game logic class
class Logic:
    def __init__(self, cmap):
        self.map = cmap

    # calculate next generation
    def calc_next(self):
        for y in range(self.map.height):
            for x in range(self.map.width):
                cell = self.map.get_cell(x, y)
                around = 0
                for nx, ny in cell.neighbors:
                    if self.map.get_cell(nx, ny).state:
                        around += 1
                if (not cell.state) and around == 3:
                    cell.next_state = True
                elif cell.state and 2 <= around <= 3:
                    cell.next_state = True
                else:
                    cell.next_state = False

    # accept next generation
    def accept_next(self):
        for y in range(self.map.height):
            for x in range(self.map.width):
                cell = self.map.get_cell(x, y)
                cell.state = cell.next_state

    # if all cell is dead
    def all_is_dead(self):
        for y in range(self.map.height):
            for x in range(self.map.width):
                cell = self.map.get_cell(x, y)
                if cell.state:
                    return False
        return True

    # if nothing happens
    def nothing_happens(self):
        for y in range(self.map.height):
            for x in range(self.map.width):
                cell = self.map.get_cell(x, y)
                if cell.state == cell.next_state:
                    return True
        return False


# random map init
def rand_init(cmap, count):
    coords = [
        (randint(0, cmap.width-1), randint(0, cmap.height-1))
        for c in range(count)]
    for x, y in coords:
        cmap.get_cell(x, y).state = True


# map printing function
def print_map(scr, cmap, xshf=0, yshf=0, life='#', dead=' '):
    for y in range(cmap.height):
        for x in range(cmap.width):
            scr.addch(
                y+yshf,
                x+xshf,
                life if cmap.get_cell(x, y).state else dead)
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


# test function
@excwrap
def test():
    scr = curses.initscr()
    curses.curs_set(0)
    scr.nodelay(1)

    WIN_HEIGHT, WIN_WITDH = scr.getmaxyx()

    cm = CellMap(WIN_WITDH-1, WIN_HEIGHT)

    logic = Logic(cm)

    rand_init(cm, int(WIN_HEIGHT*WIN_WITDH/10))

    while True:
        print_map(scr, cm)

        logic.calc_next()

        if logic.all_is_dead():
            scr.nodelay(0)
            scr.addstr(1, 1, 'all cell is dead')
            scr.getkey()
            break

        elif logic.nothing_happens():
            scr.nodelay(0)
            scr.addstr(1, 1, 'nothing happens here')
            scr.getkey()
            break

        logic.accept_next()


if __name__ == '__main__':
    test()
