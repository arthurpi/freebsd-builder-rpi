#!/usr/local/bin/python3.4 -tt

import sys
import curses
from curses.textpad import Textbox, rectangle
import time
import curses_menu_init
from curses_menu_init import menuManager
from curses_win_manager import windowManager

def init_attributes(stdscr):
  curses.noecho()
  curses.cbreak()
  curses.curs_set(0)
  if curses.has_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE) # background
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN) # box
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK) # select line
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_CYAN) # line

def clean_up_curses(stdscr):
  curses.curs_set(1)
  curses.nocbreak()
  curses.echo()
  curses.endwin()

def init_backgrounds(stdscr, build_opts):
  print(curses.LINES, curses.COLS, file=sys.stderr)
  menu_win = curses.newwin(curses.LINES - 7, curses.COLS - 7, 3, 3)
  ctn_win = menu_win.subwin(curses.LINES - 11, curses.COLS - 11, 5, 5)
  stdscr.bkgd(' ', curses.color_pair(1))
  menu_win.bkgd(' ', curses.color_pair(2))
  ctn_win.bkgd(' ', curses.color_pair(2))
  stdscr.addstr(0, 1, "FreeBSD builder for Raspberry Pi", curses.color_pair(0))
  stdscr.addstr(curses.LINES - 2, 0, "Press 'q' to quit and generate the settings file and the script", curses.color_pair(0))
  return (menu_win, ctn_win)

def adjust_wins_size(stdscr, menu_win, ctn_win):
  try:
    (maxy, maxx) = stdscr.getmaxyx()
    curses.resizeterm(maxy, maxx)
    print(maxy, maxx, file=sys.stderr)
    menu_win.resize(maxy - 7, maxx - 7, 3, 3)
    ctn_win.resize(maxy- 11, maxx - 11, 5, 5)
    stdscr.bkgd(' ', curses.color_pair(1))
    menu_win.bkgd(' ', curses.color_pair(2))
    ctn_win.bkgd(' ', curses.color_pair(2))
    stdscr.addstr(0, 1, "FreeBSD builder for Raspberry Pi", curses.color_pair(0))
    stdscr.addstr(maxy - 2, 0, "Press 'q' to quit and generate the settings file and the script", curses.color_pair(0))
    return True
  except:
    return False

def fill_menu(menu, ctn_win, pos):
  for index in range(len(menu)):
    ctn_win.addstr(index * 2, 0, menu[index][1], curses.color_pair(4))
  ctn_win.chgat(pos * 2, 0, -1, curses.color_pair(3))

def refresh_screen(windows):
  for window in windows:
    window.noutrefresh()
  curses.doupdate()

def browse_menu(c, pos, menus, cur_menu, ctn_win):
  if c == ord('q'):
    return (-1, cur_menu, False)
  elif c == ord('j') or c == curses.KEY_DOWN:
    pos += 1
  elif c == ord('k') or c == curses.KEY_UP:
    pos -= 1
  elif c == 127:
    pos = 0
    cur_menu = "main"
  elif  c == 10:
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
  if key == 127: # delete
    return 8
  elif key == 10:
    return 0
  return key

def edit_field(c, menus, cur_menu, pos, ctn_win, build_opts):
  curses.curs_set(1)
  ctn_win.clear()
  ctn_win.addstr(0, 0, menus[cur_menu][pos][1] + "\n", curses.color_pair(4))
  txt_win = ctn_win.subwin(curses.LINES - 15, curses.COLS - 15, 7, 7)
  txt_win.addstr(0, 0, build_opts[menus[cur_menu][pos][0]], curses.color_pair(4))
  refresh_screen([ctn_win, txt_win])
  textbox = Textbox(txt_win)
  textbox.edit(validator)
  value = textbox.gather()
  curses.curs_set(0)
  build_opts[menus[cur_menu][pos][0]] = value
  return (0, "main", False)

def main_event(stdscr, menu_win, ctn_win, menus, build_opts):
  pos = 0
  cur_menu = "main"
  editing = False
  while True:
    c = ctn_win.getch()
    if c == curses.KEY_RESIZE or c == ord('c'):
      adjust_wins_size(stdscr, menu_win, ctn_win)
    if not editing:
      (pos, cur_menu, editing) = browse_menu(c, pos, menus, cur_menu, ctn_win)
      if pos == -1:
        break
    if editing:
      (pos, cur_menu, editing) = edit_field(c, menus, cur_menu, pos, ctn_win, build_opts)
    stdscr.clear()
    menu_win.clear()
    ctn_win.clear()
    fill_menu(menus[cur_menu], ctn_win, pos)
    refresh_screen([stdscr, menu_win, ctn_win])

def oop_main_event():
  pass

def start_curses_gui(build_opts):
  # Init
  stdscr = curses.initscr()
  init_attributes(stdscr)
  (menu_win, ctn_win) = init_backgrounds(stdscr, build_opts)

  menu_manager = menuManager()
  fill_menu(menu_manager._menus["main"], ctn_win, 0)

  menus = menu_manager._menus
  refresh_screen([stdscr, menu_win, ctn_win])

  # Call loop
  ctn_win.keypad(True)
  main_event(stdscr, menu_win, ctn_win, menus, build_opts)
  ctn_win.keypad(False)
  clean_up_curses(stdscr)
