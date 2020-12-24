# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Applications/Plone/Python-2.7/lib/python2.7/site-packages/medialog/dexterityview/interfaces.py
# Compiled at: 2015-07-06 11:58:58
from zope import schema
from zope.interface import Interface
from z3c.form import interfaces
from z3c.form.interfaces import IFileWidget
from zope.interface import alsoProvides
from plone.directives import form
from plone.autoform.interfaces import IFormFieldProvider
from medialog.controlpanel.interfaces import IMedialogControlpanelSettingsProvider
from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('medialog.dexterityview')

class IDexterityViewLayer(Interface):
    """A layer specific to medialog.dexterityview
        """
    pass


class IContentPair(form.Schema):
    content_type = schema.ASCIILine(title=_('content_type', 'Content type'), required=False)
    image_scale = schema.Choice(title=_('imagesize', default='image Size'), vocabulary='medialog.dexterityview.ImageSizeVocabulary', required=True, description=_('help_imagesize', default='Set  size for image'))
    block_fields = schema.ASCIILine(title=_('block_fields', 'Fields to block'), required=False)


class IDexterityViewSettings(form.Schema):
    """Adds settings to medialog.controlpanel
        """
    form.fieldset('dexterity_view', label=_('Dexterity View'), fields=[
     'content_pairs'])
    form.widget(content_pairs=DataGridFieldFactory)
    content_pairs = schema.List(title=_('content_pairs', default='Content type and fields blocked'), value_type=DictRow(schema=IContentPair))


alsoProvides(IDexterityViewSettings, IMedialogControlpanelSettingsProvider)