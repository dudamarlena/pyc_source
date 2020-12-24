# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /var/plone4_dev/Python-2.6/lib/python2.6/site-packages/plonetheme/laboral/setuphandlers.py
# Compiled at: 2011-05-20 07:51:01


def setupVarious(context):
    if context.readDataFile('plonetheme.laboral_various.txt') is None:
        return
    else:
        return