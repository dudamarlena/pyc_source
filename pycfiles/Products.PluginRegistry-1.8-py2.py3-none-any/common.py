# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/pluggablecatalog/tests/common.py
# Compiled at: 2008-07-23 15:36:19


def setupPloneSite():
    from Products.PloneTestCase import PloneTestCase
    PloneTestCase.installProduct('pluggablecatalog')
    PloneTestCase.setupPloneSite()