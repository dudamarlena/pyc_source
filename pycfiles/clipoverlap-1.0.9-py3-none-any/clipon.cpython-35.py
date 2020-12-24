# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/clipon/clipon.py
# Compiled at: 2016-06-17 03:52:51
# Size of source mod 2**32: 7518 bytes
from __future__ import absolute_import
from docopt import docopt
import sys, client
from helper import INT_MAX
from defines import CLIPON_VERSION
__version__ = CLIPON_VERSION
__author__ = 'Jin Xu <jinuxstyle@hotmail.com>'
main_doc = "\nA lightweight clipboard manager\n\nUsage:\n  clipon <command> [<options>...]\n\nGeneral Options:\n  -h, --help    Show help\n  --version     Show version and exit\n\nCommands:\n start          Start clipon daemon\n list           List clipboard history\n clear          Clear history\n size           Total number of items\n config         Configure clipon\n info           Summary about clipon configuration and history\n pause          Pause tracking clipboard\n resume         Resume tracking clipboard\n stop           Stop and quit clipon daemon\n status         Status of clipon daemon\n\nSee 'clipon <command> -h' for more information on a specific command.\n"
list_doc = '\nusage: clipon list [options]\n\nList clipboard history tracked by clipon\n\nOptions:\n  --number=<number> -n  Number of entries to be listed. Defaults to\n                        total if not given\n  --start=<start>       Starting entry number to list\n  --reverse -r          List history entries in reverse order\n  --short=<number>      Print at most given number of characters for each\n                        entry to be listed. Defaults to all if not given\n  --raw                 List history entries in raw format. Information\n                        added by clipon are excluded.\n  --before=<date time>  List history entries added before the given time\n\nExamples:\n\n  list all entries in raw and short format:\n    $ clipon list --raw --short=80\n  list the latest 10 entries:\n    $ clipon list -n 10\n  list the oldest 10 entries:\n    $ clipon list -n 10 --start=0\n\n'

def do_list(args):
    num_entry = args['--number']
    start_entry = args['--start']
    reverse = args['--reverse']
    short = args['--short']
    raw = args['--raw']
    if num_entry is None:
        num_entry = INT_MAX
    else:
        num_entry = int(num_entry)
        if num_entry <= 0:
            print('Invalid value for option --number. Shall be greater than 0')
            return
        if start_entry is None:
            start_entry = -num_entry
        else:
            start_entry = int(start_entry)
    if short is None:
        short = INT_MAX
    else:
        short = int(short)
    if short <= 0:
        print('Invalid value for option --short. Shall be greater than 0')
        return
    client.print_history(start_entry, num_entry, raw, short, reverse)


delete_doc = '\nusage: clipon delete [options]\n\nDelete a number of entries in clip history\n\nOptions:\n  --start=<number> -s   Starting from which one\n  --number=<number> -n  Number of entries to be deleted [default: 1]\n\n'

def do_delete(args):
    start_entry = args['--start']
    num_entry = int(args['--number'])
    if num_entry <= 0:
        print('Invalid value for option --number. Shall be greater than 0')
        return
    if start_entry is None:
        print('Value not specified for option --start')
        return
    start_entry = int(start_entry)
    if start_entry < 0:
        print('Invalid value for option --start. Shall be greater or equal than 0')
        return
    client.delete_history(start_entry, num_entry)


config_doc = "\nusage: clipon config [options]\n\nConfigure additional options\n\nOptions:\n  --autosave=<string>       Save history to file automatically\n  --max-entry=<number>      Maximum number of history entries, no limit\n                            by default. Note that if there has already\n                            more than the given number of entries, older\n                            ones will be deleted.\n  --max-length=<number>     Maximum number of characters for each entry,\n                            no limit by default. Note that if the length\n                            of a clip is longer than the given value, it\n                            will be truncated to the given length. But it\n                            doesn't apply to existing clips.\n\nExamples:\n\n  Do not save history to file\n    $ clipon config --autosave false\n\n"

def do_config(args):
    autosave = args['--autosave']
    max_entry = args['--max-entry']
    max_length = args['--max-length']
    cfg = {}
    if autosave is not None:
        if autosave == 'False' or autosave == 'false':
            autosave = False
    else:
        if autosave == 'True' or autosave == 'true':
            autosave = True
        else:
            print('Invalid value for option --autosave, shall be true or false')
            return
        cfg['autosave'] = autosave
    if max_entry is not None:
        max_entry = int(max_entry)
        if max_entry <= 0:
            print('Invalid value for --max_entry, shall be greater than zero')
            return
        cfg['max_entry'] = max_entry
    if max_length is not None:
        max_length = int(max_length)
        if max_length < 0:
            print('Invalid value for --max_length, shall be greater than zero')
            return
        cfg['max_length'] = max_length
    if len(cfg) > 0:
        client.config_clipon(cfg)


start_doc = '\nusage: clipon start\n\nStart clipon daemon\n'

def do_start(args):
    client.start_daemon()


stop_doc = '\nusage: clipon stop\n\nStop clipon daemon\n'

def do_stop(args):
    client.stop_daemon()


pause_doc = '\nusage: clipon pause\n\nPause clipon daemon\n'

def do_pause(args):
    client.pause_daemon()


resume_doc = '\nusage: clipon resume\n\nPause clipon daemon\n'

def do_resume(args):
    client.resume_daemon()


size_doc = '\nusage: clipon size\n\nGet the total number of clips\n'

def do_size(args):
    size = client.get_size()
    print(size)


clear_doc = '\nusage: clipon clear\n\nClear the clip history\n'

def do_clear(args):
    client.clear_history()


save_doc = '\nusage: clipon save\n\nSave clip history if autosave is not enabled\n'

def do_save(args):
    client.save_history()


def do_help(argv):
    if len(argv) == 0:
        docopt(main_doc, argv='-h')
    else:
        cmd = argv[0]
        cmd_doc = cmd + '_doc'
    try:
        print(globals()[cmd_doc])
    except KeyError:
        exit("%r is not a clipon command. See 'clipon -h|--help'." % cmd)


info_doc = '\nusage: clipon info\n\nPrint summary info of clipon\n'

def do_info(args):
    client.print_info()


status_doc = '\nusage: clipon status\n\nPrint status of clipon\n'

def do_status(args):
    client.print_status()


def main(argv=None):
    args = docopt(main_doc, version='clipon version %s' % __version__, options_first=True, argv=argv or sys.argv[1:])
    cmd = args['<command>']
    argv = [args['<command>']] + args['<options>']
    if cmd == 'help':
        do_help(argv)
        return
    try:
        cmd_doc_name = cmd + '_doc'
        cmd_doc = globals()[cmd_doc_name]
        args = docopt(cmd_doc, argv)
        method_name = 'do_' + cmd
        method = globals()[method_name]
        assert callable(method)
        method(args)
    except (KeyError, AssertionError):
        exit("%r is not a clipon command. See 'clipon help or clipon -h'." % cmd)


if __name__ == '__main__':
    main()