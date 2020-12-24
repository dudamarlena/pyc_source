# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.5/site-packages/bookshelf/api_v2/debug.py
# Compiled at: 2016-08-21 18:37:21
# Size of source mod 2**32: 1287 bytes
import inspect
from IPython.terminal.embed import InteractiveShellEmbed
from IPython.config.loader import Config
cfg = Config()
prompt_config = cfg.PromptManager
prompt_config.in_template = 'N.In <\\#>: '
prompt_config.in2_template = '   .\\D.: '
prompt_config.out_template = 'N.Out<\\#>: '
banner_msg = '\n**Nested Interpreter:\nHit Ctrl-D to exit interpreter and continue program.\nNote that if you use %kill_embedded, you can fully deactivate\nThis embedded instance so it will never turn on again'
exit_msg = '**Leaving Nested interpreter'

def ipsh():
    ipshell = InteractiveShellEmbed(config=cfg, banner1=banner_msg, exit_msg=exit_msg)
    frame = inspect.currentframe().f_back
    msg = 'Stopped at {0.f_code.co_filename} at line {0.f_lineno}'.format(frame)
    ipshell(msg, stack_depth=2)