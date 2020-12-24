# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/__init__.py
# Compiled at: 2018-10-18 17:35:13
from brasil.gov.portal import patches
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('brasil.gov.portal')
patches.run()