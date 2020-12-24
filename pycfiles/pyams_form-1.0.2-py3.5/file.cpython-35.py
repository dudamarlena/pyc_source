# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/browser/file.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 1684 bytes
"""PyAMS_form.browser.file module

This module provides default file widget.
"""
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
    __doc__ = 'File input widget implementation'
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