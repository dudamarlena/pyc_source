# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/bayesdb/bql.py
# Compiled at: 2015-02-12 15:25:14
from bayesdb.client import Client
from cmd2 import Cmd
import sys

class BayesDBApp(Cmd):
    """Provides "interactive mode" features."""
    Cmd.redirector = '>>>'

    def __init__(self, client):
        self.client = client
        self.prompt = 'bql> '
        Cmd.__init__(self, 'tab')

    def do_show(self, line):
        self.client('show ' + str(line))

    def do_list(self, line):
        self.client('list ' + str(line))

    def do_analyze(self, line):
        self.client('analyze ' + str(line))

    def do_execute(self, line):
        self.client('execute ' + str(line))

    def do_drop(self, line):
        self.client('drop ' + str(line))

    def do_initialize(self, line):
        self.client('initialize ' + str(line))

    def do_create(self, line):
        self.client('create ' + str(line))

    def do_infer(self, line):
        self.client('infer ' + str(line))

    def do_select(self, line):
        self.client('select ' + str(line))

    def do_simulate(self, line):
        self.client('simulate ' + str(line))

    def do_save(self, line):
        self.client('save ' + str(line))

    def do_load(self, line):
        self.client('load ' + str(line))

    def do_estimate(self, line):
        self.client('estimate ' + str(line))

    def do_update(self, line):
        self.client('update ' + str(line))

    def do_help(self, line):
        self.client('help ' + str(line))

    def default(self, line):
        self.client(str(line))


def run_command_line():
    hostname = None
    port = None
    if len(sys.argv) > 1:
        input = sys.argv[1].split(':')
        hostname = input[0]
        if len(input) == 1:
            client = Client(hostname)
            print 'Using hostname %s.' % hostname
        if len(input) == 2:
            port = int(input[1])
            client = Client(hostname, port)
            print 'Using hostname %s, port %d' % (hostname, port)
        elif len(input) > 2:
            print "Run with 'python bql [hostname[:port]]'"
    else:
        client = Client()
    print "Welcome to BayesDB. You may enter BQL commands directly into this prompt. Type 'help' for help, and 'quit' to quit."
    app = BayesDBApp(client)
    app.cmdloop()
    return


if __name__ == '__main__':
    run_command_line()