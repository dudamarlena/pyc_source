# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/core/resources.py
# Compiled at: 2013-04-11 17:47:52
"""wrapper around pkg_resources, with fallback to using directories specified
in the settings file if pkg_resources cannot be used.

to allow fallback to the settings file, specify the settings_attribute method,
this is the attribute in the settings file that contains the folder with the
resources as opposed to the folder containing the module itself.

this mechanism will probably be rewritten to support the loading of resources
from zip files instead of falling back to settings.

when running from a bootstrapper, we'll try to use pgk_resources, even when
runnin from within a zip file.
"""
import pkg_resources, logging
logger = logging.getLogger('camelot.core.resources')

def resource_filename(module_name, filename):
    """Return the absolute path to a file in a directory
    using pkg_resources
    """
    return pkg_resources.resource_filename(module_name, filename.encode('utf-8'))


def resource_string(module_name, filename):
    """load a file as a string using pkg_resources"""
    return pkg_resources.resource_string(module_name, filename.encode('utf-8'))