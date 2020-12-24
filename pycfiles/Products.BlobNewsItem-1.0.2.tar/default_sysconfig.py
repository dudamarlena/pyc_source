# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/PasteScript-1.7.5-py2.6.egg/paste/script/default_sysconfig.py
# Compiled at: 2012-02-27 07:41:53
"""
This module contains default sysconfig settings.

The command object is inserted into this module as a global variable
``paste_command``, and can be used inside functions.
"""

def add_custom_options(parser):
    """
    This method can modify the ``parser`` object (which is an
    ``optparse.OptionParser`` instance).  This can be used to add new
    options to the command.
    """
    pass


def default_config_filename(installer):
    """
    This function can return a default filename or directory for the
    configuration file, if none was explicitly given.

    Return None to mean no preference.  The first non-None returning
    value will be used.

    Pay attention to ``installer.expect_config_directory`` here,
    and to ``installer.default_config_filename``.  
    """
    return installer.default_config_filename


def install_variables(installer):
    """
    Returns a dictionary of variables for use later in the process
    (e.g., filling a configuration file).  These are combined from all
    sysconfig files.
    """
    return {}


def post_setup_hook(installer, config_file):
    """
    This is called at the very end of ``paster setup-app``.  You
    might use it to register an application globally.
    """
    pass