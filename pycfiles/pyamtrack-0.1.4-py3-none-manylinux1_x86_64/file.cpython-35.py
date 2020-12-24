# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/browser/file.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 1684 bytes
__doc__ = 'PyAMS_form.browser.file module\n\nThis module provides default file widget.\n'
from zope.interface import implementer_only
from zope.schema.interfaces import IBytes
from pyams_form.browser.text import TextWidget
from pyams_form.interfaces.widget import IFieldWidget, IFileWidget
from pyams_form.widget import FieldWidget
from pyams_layer.interfaces import IFormLayer
from pyams_utils.adapter import adapter_config
__docformat__ = 'restructuredtext'

@implementer_only(IFileWidget)
class FileWidget(TextWidget):
    """FileWidget"""
    klass = 'file-widget'
    css = 'file'
    headers = None
    filename = None

    def json_data(self):
        data = super(TextWidget, self).json_data()
        data['type'] = 'file'
        return data


@adapter_config(required=(IBytes, IFormLayer), provides=IFieldWidget)
def FileFieldWidget(field, request):
    """IFieldWidget factory for FileWidget."""
    return FieldWidget(field, FileWidget(request))