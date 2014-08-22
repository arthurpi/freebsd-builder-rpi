#!/usr/local/bin/python3.4 -tt

import sys
import curses
from curses.textpad import Textbox
import time
import curses_menu_init

def init_attributes(stdscr):
  curses.start_color()
  curses.noecho()
  curses.cbreak()
  curses.curs_set(0)
  stdscr.keypad(True)
  if curses.has_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE) # background
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN) # box
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK) # select line
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_CYAN) # line

def clean_up_curses(stdscr):
  stdscr.keypad(False)
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

def refresh_screen(windows):
  for window in windows:
    window.noutrefresh()
  curses.doupdate()

def browse_menu(c, pos, menus, cur_menu, ctn_win):
  if c == 'q':
    return (-1, cur_menu, False)
  elif c == ord('j') or c == curses.KEY_DOWN:
    pos += 1
  elif c == 'k':
    pos -= 1
  elif c == 'a':
    if menus[cur_menu][pos][0] in menus:
      cur_menu = menus[cur_menu][pos][0]
      pos = 0
    else:
      return (pos, cur_menu, True) # (pos, editing)
  if pos < 0:
    pos = len(menus[cur_menu]) - 1
  elif pos > len(menus[cur_menu]) - 1:
    pos = 0
  return (pos, cur_menu, False) # (pos, editing)

def validator(key):
  if key == "c" or key == 'c' or key == ord('c'):
    return None
  else:
    return key

def edit_field(c, menus, cur_menu, pos, ctn_win, build_opts):
  ctn_win.clear()
  ctn_win.addstr(0, 0, menus[cur_menu][pos][1] + "\naa", curses.color_pair(4))
  refresh_screen([ctn_win])
  global textbox
  textbox = Textbox(ctn_win)
  textbox.do_command(curses.KEY_BACKSPACE)
  textbox.edit(validator)
  value = textbox.gather()
  build_opts[menus[cur_menu][pos][0]] = value
  return (0, "main", False)

def main_event(stdscr, menu_win, ctn_win, menus, build_opts):
  pos = 0
  cur_menu = "main"
  field = ""
  editing = False
  while True:
    c = ctn_win.getch()
    print(c, file=sys.stderr)
    if not editing:
      (pos, cur_menu, editing) = browse_menu(c, pos, menus, cur_menu, ctn_win)
      if pos == -1:
        break
    if editing:
      (pos, cur_menu, editing) = edit_field(c, menus, cur_menu, pos, ctn_win, build_opts)
    ctn_win.clear()
    fill_menu(menus[cur_menu], ctn_win, pos)
    refresh_screen([ctn_win])

def start_curses_gui(build_opts):
  # Init
  stdscr = curses.initscr()
  init_attributes(stdscr)
  (menu_win, ctn_win) = init_backgrounds(stdscr, build_opts)

  menus = curses_menu_init.dict_menus_init()
  fill_menu(menus["main"], ctn_win, 0)
  refresh_screen([stdscr, menu_win, ctn_win])

  # Call loop
  main_event(stdscr, menu_win, ctn_win, menus, build_opts)
  clean_up_curses(stdscr)
