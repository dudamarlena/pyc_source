# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: insolater/__init__.py
# Compiled at: 2013-12-07 01:55:06
__all__ = [
 'Insolater',
 'cli',
 'init',
 'push',
 'pull',
 'exit',
 'cd',
 'pwd']
import version_tools
from insolater import Insolater
from run import cli
_INSOLATER = Insolater()
init = _INSOLATER.init
push = _INSOLATER.push
pull = _INSOLATER.pull
exit = _INSOLATER.exit
cd = _INSOLATER.change_branch
pwd = _INSOLATER.get_current_branch