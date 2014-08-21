#!/usr/local/bin/python3.4 -tt

import sys
import curses
import time
import event_curses
import menu_initialisation

def init_attributes(stdscr):
  curses.start_color()
  curses.noecho()
  curses.cbreak()
  curses.curs_set(0)
  stdscr.keypad(1)
  if curses.has_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE) # background
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN) # box
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK) # select line
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_CYAN) # line


def clean_up_curses(stdscr):
  stdscr.keypad(0)
  curses.nocbreak()
  curses.echo()
  curses.endwin()


def init_backgrounds(stdscr, build_opts):
  menu_win = curses.newwin(curses.LINES - 7, curses.COLS - 7, 3, 3)
  ctn_win = menu_win.subwin(curses.LINES - 11, curses.COLS - 11, 5, 5)
  stdscr.bkgd(' ', curses.color_pair(1))
  menu_win.bkgd(' ', curses.color_pair(2))
  ctn_win.bkgd(' ', curses.color_pair(2))
  stdscr.addstr(0, 1, "FreeBSD builder. Settings file: {}".\
                format(build_opts['output_conf_file']), curses.color_pair(0))
  return (menu_win, ctn_win)


def fill_menu(menu, ctn_win, pos):
  for index in range(len(menu)):
    ctn_win.addstr(index * 2, 0, menu[index][1], curses.color_pair(4))
  ctn_win.chgat(pos * 2, 0, -1, curses.color_pair(3))


def refresh_screen(stdscr, menu_win, ctn_win):
  stdscr.noutrefresh()
  menu_win.noutrefresh()
  ctn_win.noutrefresh()
  curses.doupdate()


def main_event(stdscr, menu_win, ctn_win, menus):
  pos = 0
  cur_menu = "main"
  while True:
    c = ctn_win.getkey()
    if c == "q":
      break
    if c == "j":
      pos += 1
    if c == "k":
      pos -= 1
    if c == "a" or c == curses.KEY_ENTER:
      if menus[cur_menu][pos][0] in menus:
        cur_menu = menus[cur_menu][pos][0]
        pos = 0
    ctn_win.clear()
    fill_menu(menus[cur_menu], ctn_win, pos)
    refresh_screen(stdscr, menu_win, ctn_win)

def start_curses_gui(build_opts):
  # Init
  stdscr = curses.initscr()
  init_attributes(stdscr)
  (menu_win, ctn_win) = init_backgrounds(stdscr, build_opts)

  menus = menu_initialisation.dict_menus_init()
  fill_menu(menus["main"], ctn_win, 0)
  refresh_screen(stdscr, menu_win, ctn_win)

  # Call loop
  main_event(stdscr, menu_win, ctn_win, menus)
  clean_up_curses(stdscr)
  return
