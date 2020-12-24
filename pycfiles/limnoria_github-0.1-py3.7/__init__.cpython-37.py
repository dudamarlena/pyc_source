# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/limnoria_github/__init__.py
# Compiled at: 2020-05-08 12:52:23
# Size of source mod 2**32: 2872 bytes
"""
This plugin provides access to the GitHub API, and can announce pushes on
channels.
"""
import supybot
import supybot.world as world
__version__ = '0.1'
if not hasattr(supybot.authors, 'progval'):
    supybot.authors.progval = supybot.Author('Valentin Lorentz', 'ProgVal', 'progval@gmail.com')
__author__ = supybot.authors.progval
__contributors__ = {}
__url__ = ''
from . import config
from . import plugin
from imp import reload
reload(config)
reload(plugin)
if world.testing:
    from . import test
Class = plugin.Class
configure = config.configure