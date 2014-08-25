#!/usr/local/bin/python3.4 -tt

import sys
import curses
from curses.textpad import Textbox, rectangle
import time
import curses_menu_init
from curses_menu_init import menuManager
from curses_win_manager import windowManager

def draw_menu(menu_man, win):
  menu = menu_man.get_selected_menu()
  for index in range(len(menu)):
    win.addstr(index * 2, 0, menu[index][1], curses.color_pair(4))
  win.chgat(menu_man._cur_pos * 2, 0, -1, curses.color_pair(3))


def main_event(menu_man, win_man):
  while True:
    # Chars handled: arrows, return, q, resize
    c = win_man._ctn_win.getch()
    if win_man._too_small or c == ord('c') or c == curses.KEY_RESIZE: # Resize
      win_man.resize_wins()
      if win_man._too_small:
        continue
    elif c == ord('q'): # Exit
      break
    elif c == ord('j') or c == curses.KEY_DOWN: # Down
      menu_man.incr_pos()
    elif c == ord('k') or c == curses.KEY_UP: # Up
      menu_man.decr_pos()
    elif c == ord('l') or c == curses.KEY_RIGHT or c == 10: # Go in
      menu_man.enter_selected_menu()
      if menu_man._cur_field:
        pass
        # Edit field mode then empty _cur_field
    elif c == ord('h') or c == curses.KEY_LEFT or c == curses.KEY_BACKSPACE or c == 127: # Go back
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
    win_man.init_wins()
    menu_man = menuManager()
    draw_menu(menu_man, win_man._ctn_win)
    win_man.refresh_all()
    win_man._ctn_win.keypad(True)
    main_event(menu_man, win_man)
