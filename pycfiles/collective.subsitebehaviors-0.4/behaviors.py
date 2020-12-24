# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/psf/Home/Code/koodaamo/collective.subsitebehaviors/src/collective/subsitebehaviors/behaviors.py
# Compiled at: 2015-09-05 08:32:48
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import alsoProvides
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from . import _

class ISubSite(model.Schema):
    """Behavior interface to add a customer logo etc.
   """
    model.fieldset('appearance', label=_('fieldset_appearance', 'Appearance'), fields=['logoImage'])
    logoImage = NamedBlobImage(title=_('field_customlogo', 'Custom logo'), description=_('field_customlogo_description', 'Custom logo to be used'), required=False)


alsoProvides(ISubSite, IFormFieldProvider)