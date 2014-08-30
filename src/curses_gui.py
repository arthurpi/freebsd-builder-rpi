#!/usr/local/bin/python3.4 -tt

import time
import sys
import curses
from curses_menu_manager import menuManager
from curses_win_manager import windowManager
from curses.textpad import Textbox, rectangle

def draw_menu(menu_man, win):
  menu = menu_man.get_selected_menu()
  for index in range(len(menu)):
    win.addstr(index * 2, 0, menu[index][1], curses.color_pair(4))
  win.chgat(menu_man._cur_pos * 2, 0, -1, curses.color_pair(3))

def draw_edit_box(menu_man, win_man, build_opts):
  ## BUGGY (resize + too small windows not handled properly)
  win_man.resize_wins("edit_mode")
  win_man.refresh_all()
  curses.curs_set(1)
  # Add title of the box
  win_man._field_win.bkgd(' ', curses.color_pair(5))
  win_man._field_win.addstr(0, 0, menu_man.get_verbose_cur_field(),
                            curses.color_pair(5))
  win_man._field_win.chgat(0, 0, -1, curses.color_pair(1))
  # Create the window that will holds the text
  (YMAX, XMAX) = win_man._field_win.getmaxyx()
  (YBEG, XBEG) = win_man._field_win.getparyx()
  text_win = curses.newwin(YMAX, XMAX, YBEG + 6, XBEG + 5)
  text_win.bkgd(' ', curses.color_pair(5))
  text_win.addstr(0, 0, build_opts[menu_man._cur_field],
                   curses.color_pair(5))
  # Refresh both windows
  win_man._field_win.noutrefresh()
  text_win.noutrefresh()
  curses.doupdate()
  # Create a textbox
  box = Textbox(text_win)
  box.edit()
  build_opts[menu_man._cur_field] = box.gather()[:-1]
  del text_win
  curses.curs_set(0)
  menu_man._cur_field = ""
  win_man.resize_wins("menu_mode")

def main_event(menu_man, win_man, build_opts):
  while True:
    c = win_man._ctn_win.getch()
    if win_man._too_small or c == ord('c') or c == curses.KEY_RESIZE: # Resize
      win_man.resize_wins("menu_mode")
      if win_man._too_small:
        continue
    if c == ord('q'): # Exit
      break
    elif c == ord('j') or c == curses.KEY_DOWN: # Down
      menu_man.incr_pos()
    elif c == ord('k') or c == curses.KEY_UP: # Up
      menu_man.decr_pos()
    elif c == ord('l') or c == curses.KEY_RIGHT or c == 10: # Go in
      menu_man.enter_selected_menu()
      if menu_man._cur_field:
        draw_edit_box(menu_man, win_man, build_opts)
    elif c == ord('h') or c == curses.KEY_LEFT or \
        c == curses.KEY_BACKSPACE or c == 127: # Go back
      menu_man.to_previous_menu()
    try:
      win_man._ctn_win.clear()
      draw_menu(menu_man, win_man._ctn_win)
      win_man.refresh_all()
    except curses.error:
      win_man._too_small = True

def start_curses_gui(build_opts):
  with windowManager() as win_man:
    # Inits
    win_man.init_wins("menu_mode")
    menu_man = menuManager()
    draw_menu(menu_man, win_man._ctn_win)
    win_man.refresh_all()

    # Loop
    win_man._ctn_win.keypad(True)
    main_event(menu_man, win_man, build_opts)
