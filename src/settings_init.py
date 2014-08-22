#!/usr/local/bin/python3.4 -tt

def set_defaults_opts():
  """
  Set default values for all options
  """

  def_opts = {}

  # General settings
  def_opts['output_script_file'] = 'freebsd-builder-rpi.sh'
  def_opts['output_conf_file'] = 'settings.sh'

  # Compilation settings
  def_opts['gpu_mem'] = '128'
  def_opts['kern_conf'] = 'RPI-B' # Todo: allow user to choose important settings through this tool
  def_opts['src_root'] = '/usr/src/freebsd'
  def_opts['obj_root'] = '/usr/obj/freebsd'
  def_opts['mnt_dir'] = '/mnt'
  def_opts['img_name'] = '/usr/obj/freebsd/fbsd-rpi.img'
  def_opts['do_compile'] = "yes"
  def_opts['clean_obj'] = "no"

  # Partition settings
  def_opts['user'] = 'pi'
  def_opts['pw'] = 'raspberry'
  def_opts['sd_card_size'] = '1 GB'
  def_opts['img_size_raw'] = '0' # Default to zero if sd_card_size is specified to compute optimal size
  def_opts['partition_scheme'] = {'/': 'rest'}
  def_opts['swap'] = '0 GB' # If equals 0, do not create swap partition
  def_opts['disk_tune'] = "yes"# Todo: allow user to specify more options

  # Pre-built packages settings
  def_opts['port_tree'] = "no"
  def_opts['pkg_prebuilt'] = []

  # Firmware files
  # Todo: path.join etc
  def_opts['uboot_dir'] = './firmware' # Folder where uboot files are located

  return def_opts


def read_conf(config_file, build_opts):
  """
  Read configuration file. Ignore lines starting with #,
  and ignore trailing whitespaces, then set the specified values
  """

  f = open(config_file) # Todo: error handling
  conf = []
  for line in f:
    if (line[0] != '#'):
      conf.append(" ".join((line.strip()).split()))
  f.close()
  for opt in conf:
    word_list = opt.split()
    if len(word_list) > 1:
      build_opts[word_list[0]] = word_list[1] # Todo: error handling (dic range) + multi args
  return build_opts
