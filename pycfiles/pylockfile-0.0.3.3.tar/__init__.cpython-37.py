# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pylocker/__init__.py
# Compiled at: 2019-11-13 16:31:28
# Size of source mod 2**32: 1636 bytes
__doc__ = "\nPYthon LOCKER or pylocker package provides a pythonic way to create locking system that\ncan be used for general purposes as well as for locking files upon reading or writing.\nThe locking system works by creating and updating a general locking file anytime a lock\nis requested with a certain pass. Lock pass is used to specify the user who sets the\nlock and who can have access to whatever is locked. Any user who knows the lock pass can\naccess whatever is locked.\n\nInstallation guide:\n===================\npylocker is a pure python 2.7.x and 2.3.x module that needs no particular\ninstallation. One can either fork pylocker's `github repository <https://github.com/bachiraoun/pylocker/>`_\nand copy the package to python's site-packages or use pip as the following:\n\n\n.. code-block:: console\n\n        pip install pylocker\n\n\nPackage Functions:\n==================\n"
from .__pkginfo__ import __version__, __author__, __email__, __onlinedoc__, __repository__, __pypi__
from .Locker import Locker
from .ServerLocker import ServerLocker, SingleLocker, FACTORY

def get_version():
    """Get pylocker's version number."""
    return __version__


def get_author():
    """Get pylocker's author's name."""
    return __author__


def get_email():
    """Get pylocker's author's email."""
    return __email__


def get_doc():
    """Get pylocker's official online documentation link."""
    return __onlinedoc__


def get_repository():
    """Get pylocker's official online repository link."""
    return __repository__


def get_pypi():
    """Get pylocker pypi's link."""
    return __pypi__