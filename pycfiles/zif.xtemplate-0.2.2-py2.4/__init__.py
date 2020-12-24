# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zif/__init__.py
# Compiled at: 2007-08-25 13:41:36
"""
$Id: __init__.py 9 2006-12-16 04:22:32Z fairwinds $

zif.xtemplate
Copyright (c) 2006, Virginia Polytechnic Institute and State University
All rights reserved. Refer to LICENSE.txt for details of distribution and use.

Namespace package
 
"""
try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError, e:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)