# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/__init__.py
# Compiled at: 2018-10-18 17:35:13
from brasil.gov.portal import patches
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('brasil.gov.portal')
patches.run()