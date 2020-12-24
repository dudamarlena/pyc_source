# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ilazarev/dev/wakie/.env/lib/python2.7/site-packages/ipython2slack/__init__.py
# Compiled at: 2016-09-01 05:10:10
from slackclient import SlackClient
from IPython.core.magic import cell_magic, line_magic, Magics, magics_class
from IPython.utils import io

def load_ipython_extension(ipython):
    ipython.register_magics(Slack)


@magics_class
class Slack(Magics):

    def __init__(self, shell):
        super(Slack, self).__init__(shell)
        self.channel = None
        self.token = None
        self.client = None
        return

    def parse_line(self, line):
        parts = line.split()
        if len(parts) > 1:
            return parts
        else:
            return (
             None, parts[0])

    @line_magic
    def slack_setup(self, line, cell=None):
        self.channel, self.token = self.parse_line(line)
        self.client = SlackClient(self.token)

    @cell_magic
    def slack(self, line, cell):
        with io.capture_output() as (captured):
            res = self.shell.run_cell(cell)
        print captured
        if not captured and not line:
            return
        self.client.api_call('chat.postMessage', channel=self.channel, text=('{}\n```\n{}```').format(str(line), str(captured)), parse='full')