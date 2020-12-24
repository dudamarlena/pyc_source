# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xix/__init__.py
# Compiled at: 2006-08-28 15:06:32
from xix.utils.config import configFactory
import os
pj = os.path.join
dir = os.path.dirname
try:
    from pkg_resources import resource_filename
except:
    import os, sys

    def resource_filename(name, relname):
        root = os.path.split(sys.modules[name].__file__)[0]
        fname = os.path.abspath(os.path.join(root, relname))
        return fname


from commands import getoutput
if os.sys.platform in ('win32', 'nt'):

    def getoutput(cmd):
        output = os.popen2(cmd)[1]
        return output.read()


configFactory.addResource('app.cfg', resource_filename(__name__, '__app__.cfg'))
_cfg = configFactory.getConfig('app.cfg')
configFactory.addResource('xix.utils.rules', config=_cfg.xix.utils.rules)