# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/Plone-4.3.7-was-4.2.1/zeocluster/src/Products.ATSuccessStory/Products/ATSuccessStory/content/ATSuccessStory.py
# Compiled at: 2015-12-17 03:21:31
__author__ = 'Franco Pellegrini <frapell@menttes.com>'
__docformat__ = 'plaintext'
from BTrees.OOBTree import OOBTree
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.ATSuccessStory.content.ATSuccessStoryFolder import ATSuccessStoryFolder
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.ATSuccessStory.config import *
from Products.ATSuccessStory import _
schema = Schema((
 TextField(name='Story', allowable_content_types=('text/plain', 'text/structured', 'text/html',
                                                 'application/msword'), widget=RichWidget(label=_('Story')), default_output_type='text/html', required=1),
 ImageField(name='Image', widget=ImageField._properties['widget'](label=_('Image')), required=1, storage=AttributeStorage(), sizes={'large': (768, 768), 'preview': (400, 400), 'mini': (200, 200), 'atss': (185, 185), 'thumb': (128, 128), 'tile': (64, 64), 'icon': (32, 32), 'listing': (16, 16)})))
ATSuccessStory_schema = BaseSchema.copy() + getattr(ATSuccessStoryFolder, 'schema', Schema(())).copy() + schema.copy()

class ATSuccessStory(BaseContent, ATSuccessStoryFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IATSuccessStory)
    meta_type = 'ATSuccessStory'
    _at_rename_after_creation = True
    schema = ATSuccessStory_schema
    _tree = OOBTree()

    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        return self.getField('Image').tag(self, **kwargs)


registerType(ATSuccessStory, PROJECTNAME)