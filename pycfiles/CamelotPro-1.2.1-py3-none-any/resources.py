# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/core/resources.py
# Compiled at: 2013-04-11 17:47:52
__doc__ = "wrapper around pkg_resources, with fallback to using directories specified\nin the settings file if pkg_resources cannot be used.\n\nto allow fallback to the settings file, specify the settings_attribute method,\nthis is the attribute in the settings file that contains the folder with the\nresources as opposed to the folder containing the module itself.\n\nthis mechanism will probably be rewritten to support the loading of resources\nfrom zip files instead of falling back to settings.\n\nwhen running from a bootstrapper, we'll try to use pgk_resources, even when\nrunnin from within a zip file.\n"
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