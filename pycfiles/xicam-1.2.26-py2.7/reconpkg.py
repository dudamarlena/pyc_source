# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\plugins\tomography\reconpkg.py
# Compiled at: 2018-08-27 17:21:07
import importlib
from pipeline import msg
import tomopy
PACKAGE_LIST = [
 'astra', 'dxchange', 'tomocam', 'pyF3D']
packages = {}
for name in PACKAGE_LIST:
    try:
        package = importlib.import_module(name)
        packages[name] = package
        msg.logMessage(('{} module loaded').format(name), level=20)
    except ImportError as ex:
        msg.logMessage(('{} module not available').format(name), level=30)

packages['tomopy'] = tomopy
import pipelinefunctions
packages['pipelinefunctions'] = pipelinefunctions
if 'tomocam' in packages:
    import mbir
    packages['mbir'] = mbir