#!/usr/local/bin/python3.4 -tt

import sys
import settings_init
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

def main():
  (cli_opts, cli_args) = get_cli_opts() # Todo: error handling
  build_opts = settings_init.set_defaults_opts()
  if cli_opts.config_file != None:
    settings_init.read_conf(cli_opts.config_file, build_opts) # Todo: error handling
  if cli_opts.gui == True:
    None # Start GUI

  # Create final script
  f = open("./template/script", "r") # Todo: error handling
  template_script = Template(f.read())
  f.close()
  output_script = template_script.safe_substitute(build_opts)
  print(output_script)
  sys.exit(0)

if __name__ == '__main__':
  main()
