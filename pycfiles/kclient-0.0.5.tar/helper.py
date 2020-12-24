# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/a11960/p-project/k-client/kclient/helper.py
# Compiled at: 2018-03-08 09:42:59
import os, urlparse

def detect_filename(url):
    return os.path.basename(urlparse.urlparse(url).path)