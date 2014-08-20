#!/usr/local/bin/python3.4 -tt

import sys
import settings_init
import settings_check
from string import Template
from optparse import OptionParser

def get_cli_opts():
  """
  Retrieve command lines arguments.
  ./freebsd-rpi-builder.py -h for usage informations.
  """

  optparser = OptionParser()
  optparser.add_option("-q", "--quiet",
                       action="store_false", dest="verbose", default=True,
                       help="don't print status messages to stdout")

  optparser.add_option("-n", "--no-gui",
                       action="store_false", dest="gui", default=True,
                       help="start program without the ncurses gui. "\
                       "If --no-gui is provided, a configuration file "\
                       "must be provided via the --config option, and the"\
                       "bash script will be generated instantly")

  optparser.add_option("-c", "--config",
                       dest="config_file",
                       help="provide a custom configuration file FILE",
                       metavar="FILE")

  dict_opts = optparser.parse_args()
  return dict_opts


def read_templ_files():
  try:
    f = open("./template/script.sh", "r")
    templ_script = Template(f.read())
    f.close()
    f = open("./template/settings.sh", "r")
    templ_settings = Template(f.read())
    f.close()
  except FileNotFoundError:
    print("Missing template file(s) in template/. Try to restore the git repo"\
          " Exiting program...")
    sys.exit(1)
  return (templ_script, templ_settings)


def main():
  # Set defaults
  (cli_opts, cli_args) = get_cli_opts() # Todo: error handling + -n depends -c
  build_opts = settings_init.set_defaults_opts()
  (templ_script, templ_settings) = read_templ_files()

  # Read provided setting file
  if cli_opts.config_file != None:
    settings_init.read_conf(cli_opts.config_file, build_opts) # Todo: error handling

  if cli_opts.gui == True:
    # Start GUI
    None 

  # Error checking
  nerrors = settings_check.check_settings(build_opts)
  if nerrors != 0:
    print("/!\\ {} warning(s) were generated concerning your configuration "\
          "setup".format(nerrors))

  # Create final script and settings
  output_script = templ_script.safe_substitute(build_opts)
  output_settings = templ_settings.safe_substitute(build_opts)
  print(output_script)
  print(output_settings)
  sys.exit(0)

if __name__ == '__main__':
  main()
