# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/makina/pasteStage/pasteFunBot/Paste-1.7.2-py2.6.egg/paste/__init__.py
# Compiled at: 2009-07-20 09:44:04
try:
    import pkg_resources
    pkg_resources.declare_namespace(__name__)
except ImportError:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)

try:
    import modulefinder
except ImportError:
    pass
else:
    for p in __path__:
        modulefinder.AddPackagePath(__name__, p)