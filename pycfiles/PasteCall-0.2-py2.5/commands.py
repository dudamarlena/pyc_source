# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/paste/call/commands.py
# Compiled at: 2009-12-08 04:53:19
from paste.deploy import loadapp
from paste.script.command import Command
from pkg_resources import EntryPoint

class CallEP(Command):
    min_args = 1
    usage = 'entry.point:foo'
    summary = 'Execute the supplied entry point'
    parser = Command.standard_parser(verbose=True)
    parser.add_option('--with-config', dest='config', help='load environment described in this config file')

    def command(self):
        """Run the actual function.
        """
        ep_str = self.args[0]
        opts = self.options
        ep = EntryPoint.parse('%s=%s' % ('NA', ep_str))
        callable = ep.load(require=False)
        if self.options.config:
            self.load_config(self.options.config)
        res = callable(*self.args[1:])
        if res is not None:
            print res
        return

    def load_config(self, config):
        self.app = loadapp('config:' + config)