# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/KA/KAXdMSFEHom0r8QU1jW-Jk+++TI/-Tmp-/zest.specialpaste-1.2-zFurOw/gitclone/zest/__init__.py
# Compiled at: 2011-11-04 10:44:31
try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)