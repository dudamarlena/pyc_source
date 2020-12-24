# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/google/apputils/resources.py
# Compiled at: 2015-02-20 20:25:16
"""Wrapper around setuptools' pkg_resources with more Google-like names.

This module is not very useful on its own, but many Google open-source projects
are used to a different naming scheme, and this module makes the transition
easier.
"""
__author__ = 'dborowitz@google.com (Dave Borowitz)'
import atexit, pkg_resources

def _Call(func, name):
    """Call a pkg_resources function.

  Args:
    func: A function from pkg_resources that takes the arguments
          (package_or_requirement, resource_name); for more info,
          see http://peak.telecommunity.com/DevCenter/PkgResources
    name: A name of the form 'module.name:path/to/resource'; this should
          generally be built from __name__ in the calling module.

  Returns:
    The result of calling the function on the split resource name.
  """
    pkg_name, resource_name = name.split(':', 1)
    return func(pkg_name, resource_name)


def GetResource(name):
    """Get a resource as a string; see _Call."""
    return _Call(pkg_resources.resource_string, name)


def GetResourceAsFile(name):
    """Get a resource as a file-like object; see _Call."""
    return _Call(pkg_resources.resource_stream, name)


_extracted_files = False

def GetResourceFilename(name):
    """Get a filename for a resource; see _Call."""
    global _extracted_files
    if not _extracted_files:
        atexit.register(pkg_resources.cleanup_resources)
        _extracted_files = True
    return _Call(pkg_resources.resource_filename, name)