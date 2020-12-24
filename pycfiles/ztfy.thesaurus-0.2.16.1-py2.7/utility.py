# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/thesaurus/extension/gps/utility.py
# Compiled at: 2012-06-04 04:56:46
from ztfy.thesaurus.extension.gps.interfaces import IThesaurusTermGPSExtensionTarget
from ztfy.thesaurus.interfaces.extension import IThesaurusTermExtension
from zope.interface import implements
from ztfy.thesaurus import _

class ThesaurusTermGPSExtension(object):
    """Thesaurus term GPS extension"""
    implements(IThesaurusTermExtension)
    label = _('GPS coordinates')
    target_interface = IThesaurusTermGPSExtensionTarget
    target_view = '@@gps.html'
    icon = '/--static--/ztfy.thesaurus/img/gps.png'