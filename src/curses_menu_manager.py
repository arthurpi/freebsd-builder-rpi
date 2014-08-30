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
    self.kernel_menu_init()
    self.part_menu_init()
    self.pkg_menu_init()

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
    menu.append(("user", "Name of the user on the new system"))
    menu.append(("pw", "Password of the user on the new system"))
    self._menus["general"] = menu

  def build_menu_init(self):
    menu = []
    menu.append(("src_root", "Source directory of FreeBSD"))
    menu.append(("obj_root", "Object directory of FreeBSD"))
    menu.append(("clean_obj", "Clean object file when compilation is done?"))
    menu.append(("mnt_dir", "Directory where the FreeBSD image will be mount on"))
    menu.append(("do_compile", "Compile the project? (yes) Use previously built OS? (no)"))
    menu.append(("img_name", "Where the image of FreeBSD will be saved"))
    menu.append(("uboot_dir", "Directory where RPi firmware files are"))
    self._menus["build"] = menu

  def kernel_menu_init(self):
    menu = []
    menu.append(("gpu_mem", "Set how much MB is assign to the GPU"))
    menu.append(("kern_conf", "Specify a custom kernel configuration file"))
    self._menus["kernel"] = menu

  def part_menu_init(self):
    menu = []
    menu.append(("sd_card_size", "Size of SD card (manufacturer size by default)"))
    menu.append(("img_size_raw", "If set to no, use manufacturer sd card size, else use raw size"))
    menu.append(("partition_scheme", "Custom user partitions. One partition per line. Exemple: /home 1 GB"))
    menu.append(("swap", "Specify the size of the swap partition. (set to 0 if you don't want one)"))
    menu.append(("disk_tune", "Disk tuning (yes/no)"))
    self._menus["part"] = menu

  def pkg_menu_init(self):
    menu = []
    menu.append(("port_tree", "Fetch the ports tree onto the new system"))
    menu.append(("pkg_prebuilt", "List of package you want to be prebuilt. (space separated"))
    self._menus["pkg"] = menu

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
      self._cur_pos = 0
    else:
      self._cur_field = self._menus[self._cur_menu][self._cur_pos][0]

  def to_previous_menu(self):
    if self._prev_menus:
      self._cur_menu = self._prev_menus[0]
      self._prev_menus.pop(0)
      self._cur_pos = 0

  def get_verbose_cur_field(self):
    return self._menus[self._cur_menu][self._cur_pos][1]
