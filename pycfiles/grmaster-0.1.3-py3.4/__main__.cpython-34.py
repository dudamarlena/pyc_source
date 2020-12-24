# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/grmaster/__main__.py
# Compiled at: 2015-05-28 11:03:40
# Size of source mod 2**32: 2424 bytes
"""
grmaster - tool for dividing students into groups.

Copyright (C) 2015  Lutov V. S. <vslutov@yandex.ru>
"""
from grmaster import Manager, data, rules, server
import sys, os, pytest
USAGE = 'Usage: {0} COMMAND\n\nPlease, read the doc: <https://vslutov.github.io/grmaster/>\n\nAvailable commands:\n  divide file     Run dividing process\n  help            Show this help and exit\n  license         Show license and exit\n  server          Run http server (see setting.py)\n  template        Print csv template on stdout\n  test            Run internal tests'

def printfile(filename, file):
    """Load file from data folder and print it."""
    with data.openfile(filename) as (txtfile):
        txt = txtfile.readlines()
    file.writelines(txt)


def main(argv=tuple(sys.argv), file=sys.stdout, grmaster_http_app=server.APP):
    """Print usage and exec simple commands."""
    if len(argv) == 2 and argv[1] == 'license':
        printfile('LICENSE.txt', file=file)
    else:
        if len(argv) == 2 and argv[1] == 'template':
            printfile('template.csv', file=file)
        else:
            if len(argv) == 3 and argv[1] == 'divide':
                with open(argv[2], 'r') as (input_file):
                    manager = Manager(input_file)
                rules.apply_all(manager)
                print(manager.get_result().to_csv(), file=file)
            else:
                if len(argv) == 2 and argv[1] == 'server':
                    server.run(app=grmaster_http_app)
                else:
                    if len(argv) == 2 and argv[1] == 'test':
                        path = os.path.abspath(os.path.dirname(__file__))
                        sys.argv[1] = path
                        pytest.main()
                    else:
                        print(USAGE.format(argv[0]), file=file)