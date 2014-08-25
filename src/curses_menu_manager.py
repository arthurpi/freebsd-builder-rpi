#!/usr/local/bin/python3.4 -tt

class menuManager:
  def __init__(self):
    self._menus = {}
    self._cur_menu = "main"
    self._cur_field = ""
    self._prev_menus = []
    self._entries_pos = []
    self._cur_pos = 0
    self.dict_menus_init()

  def dict_menus_init(self):
    dict_menus = {}
    self.main_menu_init()
    self.general_menu_init()
    self.build_menu_init()

  def main_menu_init(self):
    menu = []
    menu.append(("general", "General settings --->"))
    menu.append(("err", "Check for errors"))
    menu.append(("build", "Compilation settings --->"))
    menu.append(("kernel", "Kernel settings --->"))
    menu.append(("part", "Partition scheme --->"))
    menu.append(("pkg", "Packages settings --->"))
    self._menus["main"] = menu

  def general_menu_init(self):
    menu = []
    menu.append(("output_script_file", "Name of the generated script file"))
    menu.append(("output_conf_file", "Name of the generated configuration file"))
    self._menus["general"] = menu

  def build_menu_init(self):
    menu = []
    menu.append(("src_root", "Source directory of FreeBSD"))
    menu.append(("obj_root", "Object directory of FreeBSD"))
    menu.append(("clean_obj", "Clean object file when compilation is done?"))
    menu.append(("mnt_dir", "Directory where the FreeBSD image will be mount on"))
    menu.append(("do_compile", "Compile the project? (yes) Use previously built OS? (no)"))
    menu.append(("img_name", "Where the image of FreeBSD will be saved"))
    self._menus["build"] = menu

  def is_editbox(self):
    if self._menus[self._cur_menu][self._cur_pos][0] in _menus:
      return True
    return False

  def incr_pos(self):
    self._cur_pos += 1
    if self._cur_pos > len(self._menus[self._cur_menu]) - 1:
      self._cur_pos = 0

  def decr_pos(self):
    self._cur_pos -= 1
    if self._cur_pos < 0:
      self._cur_pos = len(self._menus[self._cur_menu]) - 1

  def get_selected_menu(self):
    return self._menus[self._cur_menu]

  def enter_selected_menu(self):
    if self._menus[self._cur_menu][self._cur_pos][0] in self._menus:
      self._prev_menus.insert(0, self._cur_menu)
      self._cur_menu = self._menus[self._cur_menu][self._cur_pos][0]
    else:
      self._cur_field = self._menus[self._cur_menu][self._cur_pos][0]

  def to_previous_menu(self):
    if self._prev_menus:
      self._cur_menu = self._prev_menus[0]
      self._prev_menus.pop(0)
