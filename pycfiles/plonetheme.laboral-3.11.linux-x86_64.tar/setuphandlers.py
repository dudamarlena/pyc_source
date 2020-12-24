# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/plone4_dev/Python-2.6/lib/python2.6/site-packages/plonetheme/laboral/setuphandlers.py
# Compiled at: 2011-05-20 07:51:01


def setupVarious(context):
    if context.readDataFile('plonetheme.laboral_various.txt') is None:
        return
    else:
        return