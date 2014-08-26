#!/usr/local/bin/python3.4 -tt

import sys
import curses

class windowManager:
  def __init__(self):
    self._too_small = False
    self._stdscr = curses.initscr()
    (self._LINES, self._COLS) = self._stdscr.getmaxyx()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    if curses.has_colors():
      curses.start_color()
      curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE) # bkgd
      curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN) # content box bkgd
      curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK) # selected line
      curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_CYAN) # line
      curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE) # field
    try:
      self._menu_win = curses.newwin(self._LINES - 7, self._COLS - 7, 3, 3)
      self._ctn_win = self._menu_win.subwin(self._LINES - 11, self._COLS - 11, 5, 5)
      self._field_win = self._ctn_win.subwin(self._LINES // 2, self._COLS - 15, 10, 7)
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
    self._stdscr.addstr(0, 1, "FreeBSD builder for Raspberry Pi",
                        curses.color_pair(0))
    self._stdscr.addstr(LINES - 3, 0, "Press 'q' to quit and generate the "\
                        "settings file and the script", curses.color_pair(0))

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
    (self._LINES, self._COLS) = self._stdscr.getmaxyx()
    try:
      self._stdscr.resize(self._LINES, self._COLS)
      self._menu_win.resize(self._LINES - 7, self._COLS - 7)
      self._ctn_win.resize(self._LINES - 11, self._COLS - 11)
      self._field_win.resize(self._LINES // 2, self._COLS - 15)
      self.init_wins()
      self._too_small = False
    except curses.error:
      self._too_small = True

  def init_field_win(self, field_verbose, field_value):
    (LINES, COLS) = self._field_win.getmaxyx()
    #self._field_win.resize(int(LINES - 1 / 3), COLS)
    _field_win.resize(LINES // 2, COLS)
    _field_win.bkgd(' ', curses.color_pair(5))
    _field_win.addstr(0, 0, field_verbose,
                      curses.color_pair(5))
    _field_win.addstr(3, 0, field_value,
                      curses.color_pair(5))
    _field_win.noutrefresh()
