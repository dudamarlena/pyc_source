# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sorno/debuggingutil.py
# Compiled at: 2019-08-09 12:21:44
# Size of source mod 2**32: 1096 bytes
"""
Utilities to help debugging python programs in a console easier
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from IPython.terminal import embed, ipapp
_embedded_shell = None

def break_here():
    import pdb
    pdb.set_trace()


def ipython_here(**kwargs):
    _my_embed(stack_depth=3, **kwargs)


def _my_embed(**kwargs):
    """
    Since we need to control the stack_depth, the only way is to
    copy-and-paste the implementation and change the stack_depth argument :(
    """
    global _embedded_shell
    config = kwargs.get('config')
    header = kwargs.pop('header', '')
    stack_depth = kwargs.pop('stack_depth', 2)
    if config is None:
        config = ipapp.load_default_config()
        config.InteractiveShellEmbed = config.TerminalInteractiveShell
        kwargs['config'] = config
    if _embedded_shell is None:
        _embedded_shell = (embed.InteractiveShellEmbed)(**kwargs)
    _embedded_shell(header=header, stack_depth=stack_depth)