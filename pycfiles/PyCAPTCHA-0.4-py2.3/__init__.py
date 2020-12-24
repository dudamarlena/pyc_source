# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Captcha/__init__.py
# Compiled at: 2006-02-05 00:25:47
""" Captcha

This is the PyCAPTCHA package, a collection of Python modules
implementing CAPTCHAs: automated tests that humans should pass,
but current computer programs can't. These tests are often
used for security.

See  http://www.captcha.net for more information and examples.

This project was started because the CIA project, written in
Python, needed a CAPTCHA to automate its user creation process
safely. All existing implementations the author could find were
written in Java or for the .NET framework, so a simple Python
alternative was needed.
"""
__version__ = '0.3-pre'
requiredPythonVersion = (
 2, 2, 1)

def checkVersion():
    import sys, string
    if sys.version_info < requiredPythonVersion:
        raise Exception('%s requires at least Python %s, found %s instead.' % (name, string.join(map(str, requiredPythonVersion), '.'), string.join(map(str, sys.version_info), '.')))


checkVersion()
from Base import *
import File, Words