# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pyrep/__init__.py
# Compiled at: 2019-11-12 15:49:17
# Size of source mod 2**32: 1694 bytes
__doc__ = "\nPYthon REPository or pyrep package provides a pythonic way to organize dumping and pulling\npython objects and other type of files to a folder or a directory that is called\nrepository. A Repository can be created in any directory or folder, it suffices to\ninitialize a Repository instance in a directory to start dumping and pulling objects into\nit. Any directory or a folder that contains a .pyrepinfo binary file in it, is\ntheoretically a pyrep Repository. By default dump and pull methods use pickle to\nserialize storing python objects. Practically any other method can be used simply by\nproviding the means and the required libraries in a simple form of string.\n\n\nInstallation guide:\n===================\npyrep is a pure python 2.7.x module that needs no particular installation. One can either\nfork pyrep's `github repository <https://github.com/bachiraoun/pyrep/>`_ and copy the\npackage to python's site-packages or use pip as the following:\n\n\n.. code-block:: console\n\n\n        pip install pyrep\n\n\nPackage Functions:\n==================\n"
from .__pkginfo__ import __version__, __author__, __email__, __onlinedoc__, __repository__, __pypi__
from .Repository import Repository

def get_version():
    """Get pyrep's version number."""
    return __version__


def get_author():
    """Get pyrep's author's name."""
    return __author__


def get_email():
    """Get pyrep's author's email."""
    return __email__


def get_doc():
    """Get pyrep's official online documentation link."""
    return __onlinedoc__


def get_repository():
    """Get pyrep's official online repository link."""
    return __repository__


def get_pypi():
    """Get pyrep pypi's link."""
    return __pypi__