# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/browser/image.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 2273 bytes
__doc__ = "PyAMS_form.browser.image module\n\nThis module provides form's image button widget.\n"
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
    """ImageWidget"""
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