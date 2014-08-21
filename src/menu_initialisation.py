#!/usr/local/bin/python3.4 -tt

def dict_menus_init():
  dict_menus = {}
  dict_menus["main"] = main_menu_init()
  dict_menus["general"] = general_menu_init()
  dict_menus["build"] = build_menu_init()
  return dict_menus


def main_menu_init():
  menu = []
  menu.append(("general", "General settings --->"))
  menu.append(("err", "Check for errors"))
  menu.append(("build", "Compilation settings --->"))
  menu.append(("kernel", "Kernel settings --->"))
  menu.append(("part", "Partition scheme --->"))
  menu.append(("pkg", "Packages settings --->"))
  return menu

def general_menu_init():
  menu = []
  menu.append(("output_script_file", "Change where the generated script will be written at"))
  menu.append(("output_conf_file", "Change where the generated configuration file will be written at"))
  return menu

def build_menu_init():
  menu = []
  menu.append(("src_root", "Specify the source directory of FreeBSD"))
  menu.append(("obj_root", "Specify where obj file will be stored during compilation of FreeBSD"))
  menu.append(("clean_obj", "Clean object file when compilation is done?"))
  menu.append(("mnt_dir", "Specify a directory where the FreeBSD image will be mount on"))
  menu.append(("do_compile", "Compile the project? (yes) Use previously built OS? (no)"))
  menu.append(("img_name", "Specify where the image of FreeBSD will be saved"))

  return menu

