#!/usr/bin/env python3
# pylint: disable=missing-docstring
import curses
import random
import time

KANA = [chr(c) for c in range(0xff67, 0xff9e)]  # half-width katakana
PUNCTUATION = ['-', '*', '&', '#', '@']
NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']


class Matrix(object):
    def __init__(self, chance_on=0.98, chance_off=0.90, delay=0.075):
        self.charset = KANA + PUNCTUATION + NUMBERS
        self.delay = delay
        self.is_live = []
        self.chance_on = chance_on
        self.chance_off = chance_off

    def enter(self, stdscr):
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.curs_set(0)
        stdscr.idlok(1)
        while True:
            start = time.time()
            self.rain(stdscr)
            stdscr.refresh()
            elapsed = time.time() - start
            time.sleep(max([0, self.delay - elapsed]))

    def new_line(self, stdscr):
        color = curses.color_pair(1) | curses.A_DIM
        for column, live in enumerate(self.is_live):
            roll = random.random()
            if not live and roll > self.chance_on:
                self.is_live[column] = True
                stdscr.attrset(curses.A_BOLD)
            if live and roll > self.chance_off:
                self.is_live[column] = False
            if self.is_live[column]:
                stdscr.addch(random.choice(self.charset), color)
            else:
                stdscr.addch(' ')
            stdscr.attroff(curses.A_BOLD)

    def rain(self, stdscr):
        (dummy, columns) = stdscr.getmaxyx()
        if len(self.is_live) != columns:
            self.is_live = [False] * columns
        stdscr.move(0, 0)
        stdscr.insertln()
        self.new_line(stdscr)


def main():
    matrix = Matrix()
    curses.wrapper(matrix.enter)

if __name__ == '__main__':
    main()
