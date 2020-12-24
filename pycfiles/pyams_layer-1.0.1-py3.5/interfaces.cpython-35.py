# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_layer/interfaces.py
# Compiled at: 2020-02-21 07:39:56
# Size of source mod 2**32: 4619 bytes
"""PyAMS_layer.interfaces module

This module provides all layers and skins related interfaces.
"""
from pyramid.interfaces import IRequest
from zope.configuration.fields import GlobalInterface
from zope.interface import Attribute, Interface, implementer, invariant
from zope.interface.interfaces import IObjectEvent, Invalid, ObjectEvent
from zope.schema import Bool, Choice, TextLine
from pyams_file.schema import FileField
__docformat__ = 'restructuredtext'
from pyams_layer import _

class IResources(Interface):
    __doc__ = 'Get list of CSS and Javascript resources associated with given context'
    resources = Attribute('Resources to include')


PYAMS_BASE_SKIN_NAME = 'PyAMS base skin'

class IBaseLayer(IRequest):
    __doc__ = 'Base layer marker interface'


class IFormLayer(Interface):
    __doc__ = 'Custom layer for forms management'


class IPyAMSLayer(IBaseLayer, IFormLayer):
    __doc__ = 'PyAMS default layer'


class IPyAMSUserLayer(IPyAMSLayer):
    __doc__ = 'PyAMS custom user layer\n\n    This layer is the base for all custom skins.\n    Any component should provide a look and feel for this layer.\n    '


BASE_SKINS_VOCABULARY_NAME = 'pyams_layer.skins'
USER_SKINS_VOCABULARY_NAME = 'pyams_layer.skin.user'

class ISkin(Interface):
    __doc__ = 'Skin interface\n\n    Skins are registered as utilities implementing this interface\n    and defining request layer as attribute.\n    '
    label = TextLine(title='Skin name')
    layer = GlobalInterface(title='Request layer', description='This interface will be used to tag request layer', required=True)


class ISkinChangedEvent(IObjectEvent):
    __doc__ = 'Skin changed event'


@implementer(ISkinChangedEvent)
class SkinChangedEvent(ObjectEvent):
    __doc__ = 'Request skin changed event'


class ISkinnable(Interface):
    __doc__ = 'Skinnable content interface'
    can_inherit_skin = Attribute('Check if skin can be inherited')
    inherit_skin = Bool(title=_('Inherit parent skin?'), description=_('Should we reuse parent skin?'), required=True, default=False)
    no_inherit_skin = Bool(title=_("Don't inherit parent skin?"), description=_('Should we override parent skin?'), required=True, default=True)
    skin_parent = Attribute('Skin parent (local or inherited)')
    skin = Choice(title=_('Custom graphic theme'), description=_('This theme will be used to handle graphic design (colors and images)'), vocabulary=USER_SKINS_VOCABULARY_NAME, required=False)

    @invariant
    def check_skin(self):
        """Check for required skin if not inherited"""
        if self.no_inherit_skin and not self.skin:
            raise Invalid(_('You must select a custom skin or inherit from parent!'))

    def get_skin(self, request=None):
        """Get skin matching this content"""
        pass

    custom_stylesheet = FileField(title=_('Custom stylesheet'), description=_('This custom stylesheet will be used to override selected theme styles'), required=False)
    editor_stylesheet = FileField(title=_('Editor stylesheet'), description=_('Styles defined into this stylesheet will be available into HTML editor'), required=False)
    custom_script = FileField(title=_('Custom script'), description=_('This custom javascript file will be used to add dynamic features to selected theme'), required=False)


class IUserSkinnable(ISkinnable):
    __doc__ = 'User skinnable content interface'