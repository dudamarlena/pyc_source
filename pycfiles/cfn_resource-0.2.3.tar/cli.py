# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cfn_pyplates/cli.py
# Compiled at: 2015-03-14 14:35:19
__doc__ = "CLI Entry points for handy bins\n\nDocumentation for CLI methods defined in this file will be that method's\nusage information as seen on the command-line.\n\n"
import sys, yaml
from docopt import docopt
from schema import Schema, Use, Or
from cfn_pyplates import core
from cfn_pyplates.options import OptionsMapping

def _open_outfile(outfile_name):
    """Helper function for Schema to open the outfile"""
    if outfile_name == '-':
        return sys.stdout
    else:
        return open(outfile_name, 'w')


def _open_optionfile(optionfile_name):
    """Helper function for Schema to open the option file"""
    if optionfile_name == '-':
        return sys.stdin
    else:
        return open(optionfile_name)


def generate():
    """Generate CloudFormation JSON Template based on a Pyplate

Usage:
  cfn_py_generate <pyplate> [<outfile>] [-o/--options=<options_mapping>]
  cfn_py_generate (-h|--help)
  cfn_py_generate --version

Arguments:
  pyplate
    Input pyplate file name

  outfile
    File in which to place the compiled JSON template
    (if omitted or '-', outputs to stdout)

Options:
  -o --options=<options_mapping>
    Input JSON or YAML file for options mapping
    exposed in the pyplate as "options_mapping"
    (if '-', accepts input from stdin)

  -h --help
    This usage information

WARNING!

  Do not use pyplates that you haven't personally examined!

  A pyplate is a crazy hybrid of JSON-looking python.
  exec is used to read the pyplate, so any code in there is going to
  run, even potentailly harmful things.

  Be careful.

    """
    from pkg_resources import require
    version = require('cfn-pyplates')[0].version
    args = docopt(generate.__doc__, version=version)
    scheme = Schema({'<pyplate>': Use(open), 
       '<outfile>': Or(None, Use(_open_outfile)), 
       '--options': Or(None, Use(_open_optionfile)), 
       '--help': Or(True, False), 
       '--version': Or(True, False)})
    args = scheme.validate(args)
    options_file = args['--options']
    if options_file:
        options = yaml.load(options_file)
    else:
        options = {}
    output = core.generate_pyplate(args['<pyplate>'], OptionsMapping(options))
    if not output:
        return 1
    else:
        if not args['<outfile>'] or args['<outfile>'] == '-':
            print output
        else:
            args['<outfile>'].write(output)
        return 0