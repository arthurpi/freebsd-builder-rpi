#!/usr/local/bin/python3.4 -tt

import sys
import curses

class windowManager:
  def __init__(self):
    self._too_small = False
    self._stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    if curses.has_colors():
      curses.start_color()
      curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE) # background
      curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN) # box
      curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK) # select line
      curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_CYAN) # line
    try:
      self._menu_win = curses.newwin(curses.LINES - 7, curses.COLS - 7, 3, 3)
      self._ctn_win = self._menu_win.subwin(curses.LINES - 11, curses.COLS - 11, 5, 5)
    except curses.error:
      print("Windows is too small. Exiting...", file=sys.stderr)


  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    curses.echo()
    curses.nocbreak()
    curses.curs_set(1)
    curses.endwin()

  def init_wins(self):
    (LINES, COLS) = self._stdscr.getmaxyx()
    self._stdscr.bkgd(' ', curses.color_pair(1))
    self._menu_win.bkgd(' ', curses.color_pair(2))
    self._ctn_win.bkgd(' ', curses.color_pair(2))
    self._stdscr.addstr(0, 1, "FreeBSD builder for Raspberry Pi", curses.color_pair(0))
    self._stdscr.addstr(LINES - 3, 0, "Press 'q' to quit and generate the settings file and the script", curses.color_pair(0))

  def clear_all(self):
    self._stdscr.clear()
    self._menu_win.clear()
    self._ctn_win.clear()

  def refresh_all(self):
    self._stdscr.noutrefresh()
    self._menu_win.noutrefresh()
    self._ctn_win.noutrefresh()
    curses.doupdate()

  def resize_wins(self):
    self.clear_all()
    (LINES, COLS) = self._stdscr.getmaxyx()
    try:
      self._stdscr.resize(LINES, COLS)
      self._menu_win.resize(LINES - 7, COLS - 7)
      self._ctn_win.resize(LINES - 11, COLS - 11)
      self.init_wins()
      self._too_small = False
    except curses.error:
      self._too_small = True
      print("Windows is too small. Exiting...", file=sys.stderr)
