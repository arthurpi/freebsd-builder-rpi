#!/usr/local/bin/python3.4 -tt

import re
import os

##
# Checks to do in the python program
# kern_conf exists
# uboot_dir set and contains the right files

def gpu_mem_check(gpu_mem):
  i = 0
  if (gpu_mem & (gpu_mem - 1)) != 0 or gpu_mem < 0:
    print("GPU_MEM={} -> Must be a positive power of two".format(gpu_mem))
    i = 1
  if gpu_mem < 32 or gpu_mem > 256:
    print("GPU_MEM={} -> Must be inside the range 32:256 (16 is too low to allow the used u-boot to run properly")
    i = 1
  return i

def compilation_folders(src_root, obj_root):
  i = 0
  if not os.path.isdir(src_root):
    print("SRC_ROOT={} -> Invalid value: it is either not a "\
          "folder or it merely does not exist".format(src_root))
    i += 1
  if not os.path.isdir(obj_root):
    print("OBJ_ROOT={} -> Invalid value: it is either not a "\
          "folder or it merely does not exist".format(obj_root))
    i += 1
  return i

def mnt_folder(mnt_dir):
  if not os.path.isdir(mnt_dir):
    print("MNT_DIR={} -> Invalid value: it is either not a "\
          "folder or it merely does not exist".format(mnt_dir))
    return 1
  return 0

def malloc_production_redefined(src_root):
  try:
    f = open(os.path.join(src_root, "contrib/jemalloc/include/jemalloc/jemalloc_FreeBSD.h"), "r")
    text = f.read()
    f.close()
    match = re.search(r'^#define[\s]+MALLOC_PRODUCTION', text)
    if match != None:
      print("Compilation might fail, MALLOC_PRODUCTION is defined twice")
      return 1
  except FileNotFoundError:
    print("Warning: it appears the source directory is not valid: "\
          "unable to find jemalloc_FreeBSD.h")
    return 1
  return 0

def check_settings(build_opts):
  nerrors = 0
  nerrors += gpu_mem_check(int(build_opts['gpu_mem']))
  nerrors += compilation_folders(build_opts['src_root'], build_opts['obj_root'])
  nerrors += malloc_production_redefined(build_opts['src_root'])
  return nerrors
