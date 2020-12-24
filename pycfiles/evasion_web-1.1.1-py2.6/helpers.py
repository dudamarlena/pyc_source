# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: e:\nmdev\src\branches\loyalty\evasion-web\evasion\web\lib\helpers.py
# Compiled at: 2010-05-18 09:51:54
"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
siteversion = '1.0.0'
from routes import url_for
from authdetails import auth_details
from authdetails import is_authenticated