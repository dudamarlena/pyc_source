# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bigdata/bd.py
# Compiled at: 2019-05-24 11:58:12
# Size of source mod 2**32: 2765 bytes
from __future__ import print_function
from IPython.core.magic import Magics, magics_class, line_magic, cell_magic, line_cell_magic
import pexpect

@magics_class
class bdMagic(Magics):

    def __init__(self, shell):
        super(bdMagic, self).__init__(shell)
        self.CLI_start = {'hive':'hive  ', 
         'pig':'pig '}
        self.CLI_prompt = {'hive':'hive> ', 
         'pig':'grunt>'}
        self.CLI_cont = {'hive':'    > ', 
         'pig':'>> '}
        self.CLI_quit = {'hive':'quit;', 
         'pig':'quit'}
        self.app = {'hive':None, 
         'pig':None}
        self.timeout = 30

    @line_magic
    def timeout(self, line):
        self.timeout = int(line)

    @line_magic
    def pig_start(self, line):
        return self.start('pig', line)

    @line_magic
    def hive_start(self, line):
        return self.start('hive', line)

    def start(self, appname, line):
        if self.app[appname] is not None:
            self.app[appname].close()
        self.app[appname] = pexpect.spawn((self.CLI_start[appname] + ' ' + line), timeout=(self.timeout))
        self.app[appname].expect((self.CLI_prompt[appname]), timeout=(self.timeout))

    @cell_magic
    def pig(self, line, cell):
        return self.run('pig', line, cell)

    @cell_magic
    def hive(self, line, cell):
        return self.run('hive', line, cell)

    def run(self, appname, line, cell):
        if self.app[appname] is None:
            self.start(appname, line)
        x = cell.split('\n')
        for row in x:
            if row.strip() != '':
                self.app[appname].sendline(row)
                self.app[appname].expect(['\r\n' + self.CLI_cont[appname],
                 '\r\n' + self.CLI_prompt[appname]],
                  timeout=(self.timeout))
                print(self.app[appname].before.decode())

    @line_magic
    def hive_quit(self, line):
        self.quit('hive', line)

    @line_magic
    def pig_quit(self, line):
        self.quit('pig', line)

    def quit(self, appname, line):
        self.app[appname].close()
        self.app[appname] = None


def load_ipython_extension(ip):
    bdmagic = bdMagic(ip)
    ip.register_magics(bdmagic)