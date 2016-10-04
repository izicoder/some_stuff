#!/usr/bin/env python3
import curses
from random import randint


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


# the game of life logic class
class Logic:
    def __init__(self, gamemap):
        self.map = gamemap

    def calc_next(self):
        for y in range(self.map.height):
            for x in range(self.map.width):
                cell = self.map.get_cell(x, y)
                lives = 0
                for nr in cell.neighbors:
                    if not self.map.get_cell(nr[0], nr[1]).is_dead:
                        lives += 1
                if cell.is_dead and lives == 3:
                    cell.is_dead = False
                elif not cell.is_dead and 2 <= lives <= 3:
                    cell.is_dead = False
                else:
                    cell.is_dead = True

    def all_is_dead(self):
        for y in range(self.map.height):
            for x in range(self.map.width):
                if not self.map.get_cell(x, y).is_dead:
                    return False
        return True


# map printing function
def print_map(scr, gamemap, xshf=0, yshf=0, life='#', dead=' '):
    for y in range(gamemap.height):
        for x in range(gamemap.width):
            scr.addch(
                y+yshf,
                x+xshf,
                dead if gamemap.get_cell(y, x).is_dead else life)
    scr.refresh()


# initializing map
def init_map(gamemap, *coords):
    for x, y in coords:
        gamemap.get_cell(x, y).is_dead = False


# random initializing
def rand_init(gamemap, count):
    coords = (
        (randint(0, gamemap.width-1), randint(0, gamemap.height-1))
        for i in range(count))
    init_map(gamemap, *coords)


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
    MAP_WIDTH, MAP_HEIGHT = 100, 40
    gmap = Map(MAP_WIDTH, MAP_HEIGHT)
    glogic = Logic(gmap)
    rand_init(gmap, int(MAP_HEIGHT*MAP_WIDTH/10))
    while True:
        print_map(scr, gmap)
        glogic.calc_next()
        if scr.getkey() == 'q':
            scr.addstr(MAP_HEIGHT+2, 1, 'you click "q"')
            scr.getkey()
            break
        elif glogic.all_is_dead():
            scr.addstr(MAP_HEIGHT+2, 1, 'all is dead')
            scr.getkey()
            break

if __name__ == '__main__':
    main()
