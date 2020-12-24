# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/espenmoe-nilssen/Plone/zinstance/src/collective.js.supersized/collective/js/supersized/interfaces.py
# Compiled at: 2014-09-17 10:19:30
from zope import schema
from zope.interface import Interface
from z3c.form import interfaces
from zope.interface import alsoProvides
from plone.directives import form
from plone.autoform.interfaces import IFormFieldProvider
from medialog.controlpanel.interfaces import IMedialogControlpanelSettingsProvider
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('collective.js.supersized')

class ISupersizedSettings(form.Schema):
    """Adds supersized settings to medialog.controlpanel
        """
    form.fieldset('supersized', label=_('supersized'), fields=[
     'min_width',
     'min_height',
     'vertical_center',
     'horizontal_center',
     'fit_always',
     'fit_portrait',
     'fit_landscape',
     'imagesize',
     'transition'])
    min_width = schema.Int(title=_('min_width', default='min_width'), description=_('help_min_width', default='Minimum width in pixels'))
    min_height = schema.Int(title=_('min_height', default='min_height'), description=_('help_min_height', default='Minimum height in pixels'))
    vertical_center = schema.Bool(title=_('vertical_center', default='vertical_center'), description=_('help_vertical_center', default='Should the images center vertically'))
    horizontal_center = schema.Bool(title=_('horizontal_center', default='horizontal_center'), description=_('help_horizontal_center', default='Should the images center horizontally'))
    fit_always = schema.Bool(title=_('fit_always', default='fit_always'), description=_('help_fit_always', default='Should all images fit.'))
    fit_portrait = schema.Bool(title=_('fit_portrait', default='fit_portrait'), description=_('help_fit_portrait', default='Should portrait images fit.'))
    fit_landscape = schema.Bool(title=_('fit_landscape', default='fit_landscape'), description=_('help_fit_landscape', default='Should the landscape images fit'))
    imagesize = schema.Choice(title=_('label_imagesize', default='Size for image'), description=_('help_imagesize', default='Choose Size'), vocabulary='collective.js.supersized.ImageSizeVocabulary')
    transition = schema.Choice(title=_('label_transition', default='Transition'), default=1, vocabulary='collective.js.supersized.TransitionVocabulary')


alsoProvides(ISupersizedSettings, IMedialogControlpanelSettingsProvider)