# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\files\research\databrowse\databrowse\__init__.py
# Compiled at: 2018-06-29 17:51:46
"""
Databrowse:  An Extensible Data Management Platform
Copyright (C) 2012-2016 Iowa State University Research Foundation, Inc.

This package contains the entire Databrowse library.  Packages are namespaced
to allow the installation of third-party plugins without needing to install
them in the Databrowse library package folders - in a similar fashion to other
extensible Python frameworks.

The WSGI components of Databrowse are distributed with the source; however,
they must be installed manually.  Refer to INSTALL for detailed instructions.

This package contains three main subpackages:
    
    Lib -     Contains the components needed to use Databrowse from within 
              other python-based applications.  By extension, these components
              could be used in any other location where Python code can be 
              called.
    Support - Contains support functionality primarily used by plugins and
              Databrowse internal components.  Some support packages might be
              useful in other contexts as well.
    Plugins - Contains all plugins that are used by Databrowse to create XML
              and other representations of files.  Use help(databrowse.plugins)
              for more information.
"""