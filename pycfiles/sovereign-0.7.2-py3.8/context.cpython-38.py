# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sovereign/context.py
# Compiled at: 2020-04-29 02:35:50
# Size of source mod 2**32: 624 bytes
import schedule
from sovereign import config
from sovereign.utils import crypto
from sovereign.config_loader import load
template_context = {'crypto': crypto}

def template_context_refresh():
    """ Modifies template_context in-place with new values """
    for k, v in config.template_context.items():
        template_context[k] = load(v)


template_context_refresh()
if __name__ != '__main__':
    if config.refresh_context:
        schedule.every(config.context_refresh_rate).seconds.do(template_context_refresh)