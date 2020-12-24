# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/Captcha/__init__.py
# Compiled at: 2006-02-05 00:25:47
__doc__ = " Captcha\n\nThis is the PyCAPTCHA package, a collection of Python modules\nimplementing CAPTCHAs: automated tests that humans should pass,\nbut current computer programs can't. These tests are often\nused for security.\n\nSee  http://www.captcha.net for more information and examples.\n\nThis project was started because the CIA project, written in\nPython, needed a CAPTCHA to automate its user creation process\nsafely. All existing implementations the author could find were\nwritten in Java or for the .NET framework, so a simple Python\nalternative was needed.\n"
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