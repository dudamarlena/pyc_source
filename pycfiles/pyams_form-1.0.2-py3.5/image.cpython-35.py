# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/browser/image.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 2273 bytes
"""PyAMS_form.browser.image module

This module provides form's image button widget.
"""
from zope.interface import implementer_only
from zope.schema.fieldproperty import FieldProperty
from pyams_form.browser.button import ButtonWidget
from pyams_form.browser.interfaces import IHTMLImageWidget
from pyams_form.interfaces.button import IImageButton
from pyams_form.interfaces.widget import IFieldWidget, IImageWidget
from pyams_form.util import to_unicode
from pyams_form.widget import FieldWidget
from pyams_layer.interfaces import IFormLayer
from pyams_utils.adapter import adapter_config
from pyams_utils.interfaces.form import NO_VALUE
__docformat__ = 'restructuredtext'

@implementer_only(IImageWidget)
class ImageWidget(ButtonWidget):
    __doc__ = 'Form image button widget.'
    src = FieldProperty(IHTMLImageWidget['src'])
    klass = 'image-widget'
    css = 'image'

    def extract(self, default=NO_VALUE):
        """See pyams_form.interfaces.IWidget."""
        params = self.request.params
        if self.name + '.x' not in params:
            return default
        return {'x': int(params[(self.name + '.x')]), 
         'y': int(params[(self.name + '.y')]), 
         'value': params[self.name]}

    def json_data(self):
        data = super(ImageWidget, self).json_data()
        data['type'] = 'image'
        data['src'] = self.src
        return data


@adapter_config(required=(IImageButton, IFormLayer), provides=IFieldWidget)
def ImageFieldWidget(field, request):
    """Form image button widget factory adapter"""
    image = FieldWidget(field, ImageWidget(request))
    image.value = field.title
    image.src = to_unicode(field.image)
    return image