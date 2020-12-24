# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/site-packages/dismagic.py
# Compiled at: 2016-04-01 10:55:49
# Size of source mod 2**32: 430 bytes
from dis import dis
from IPython.core.magic import Magics, magics_class, line_cell_magic

@magics_class
class DisMagics(Magics):

    @line_cell_magic
    def dis(self, line, cell=None):
        """ %dis magic command for ipython """
        dis(cell or self.shell.user_ns.get(line, line))


def load_ipython_extension(ip):
    """Load the extension in IPython."""
    dis_magic = DisMagics(ip)
    ip.register_magics(dis_magic)