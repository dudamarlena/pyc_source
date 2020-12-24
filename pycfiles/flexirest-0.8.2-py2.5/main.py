# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/flexirest/main.py
# Compiled at: 2009-11-13 05:05:17
from __future__ import with_statement
import os, sys, optparse, imp, errno
from flexirest import rendering, defaults, meta
from flexirest.util import StdoutConsole, BufferedFile
_cmdline_options = (
 (
  '-v', '--version',
  dict(action='store_true', dest='version', default=False, help='print version and exit')),
 (
  '-t', '--template',
  dict(action='store', dest='template', default=False, help='apply source into this template')),
 (
  '-l', '--lang',
  dict(action='store', dest='lang', default='en', help='specify language (both input and output)')),
 (
  '-c', '--config',
  dict(dest='config', default=False, help='apply source into this template')),
 (
  '-w', '--writer',
  dict(dest='writer', default=False, help='use docutils writer named "writer"')),
 (
  '-r', '--list-writers',
  dict(action='store_true', dest='list_writers', default=False, help='print a list of all writers and quit')),
 (
  '-d', '--dump-parts',
  dict(action='store_true', dest='dump_parts', default=False, help='Dump docutils parts produced by specified writer')),
 (
  '-i', '--infile',
  dict(action='store', dest='infile', default=False, help='read input from this file')),
 (
  '-o', '--outfile',
  dict(action='store', dest='outfile', default=False, help='write output to this file')))
_print_and_quit_options = set(('version', 'list_writers'))

def _import(modname, onFailRaise=True):
    try:
        return __import__(modname)
    except ImportError:
        if onFailRaise:
            raise
        return imp.new_module(modname)


def parse_commandline(args):
    parser = optparse.OptionParser(usage=meta.CMDLINE_USAGE, description=meta.CMDLINE_DESC)
    for opt in _cmdline_options:
        parser.add_option(opt[0], opt[1], **opt[2])

    return parser.parse_args(args)


def commandline(args=None, console=None, source=None, destination=None):
    if console is None:
        console = StdoutConsole()
    if args is None:
        args = sys.argv[1:]
    (options, args) = parse_commandline(args)
    opts_w_vals = set((opt for (opt, val) in options.__dict__.iteritems() if val))
    if opts_w_vals & _print_and_quit_options:
        if options.version:
            console.write('flexirest version %s' % meta.VERSION)
        if options.list_writers:
            for available_writer in rendering.all_writers():
                console.write(available_writer)

        return 0
    if source is None:
        if options.infile:
            source = open(options.infile, 'r')
        else:
            source = sys.stdin
    if destination is None:
        if options.outfile:
            destination = BufferedFile(options.outfile)
        else:
            destination = sys.stdout
    writer_name = options.writer or 'html'
    if writer_name not in rendering.all_writers():
        sys.stderr.write("flexirest: '%s' is not a valid writer%s" % (
         writer_name, os.linesep))
        return errno.EINVAL
    if options.template:
        with open(options.template, 'r') as (fp):
            template = fp.read()
    else:
        template = defaults.templates[writer_name]
    sys.path.append(os.getcwd())
    if options.config:
        confmod = _import(options.config)
    else:
        confmod = _import('flexiconf', False)
    if options.dump_parts:
        rendering.dump_parts(source, destination, confmod, options, template, writer_name)
    else:
        rendering.render(source, destination, confmod, options, template, writer_name)
    return 0