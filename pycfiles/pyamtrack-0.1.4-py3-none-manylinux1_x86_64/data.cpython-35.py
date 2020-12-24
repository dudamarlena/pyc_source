# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/data.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 3944 bytes
__doc__ = 'PyAMS_utils.data module\n\nThe *IObjectData* interface is a generic interface which can be used to assign custom data to any\nobject. This object data may be any object which can be serialized to JSON, and assigned to any\nHTML *data* attribute. It can typically be used to set a *data-ams-data* attribute to objects,\nwhich is afterwards converted to classic *data-* attributes by **MyAMS.js** framework.\n\nFor example, for a custom widget in a form:\n\n.. code-block:: python\n\n    def updateWidgets(self):\n        super(MyForm, self).updateWidgets()\n        widget = self.widgets[\'mywidget\']\n        alsoProvides(widget, IObjectData)\n        widget.object_data = {\'ams-colorpicker-position\': \'top left\'}\n\nYou can then set an attribute in a TAL template like this:\n\n.. code-block:: xml\n\n    <div tal:attributes="data-ams-data extension:object_data(widget)">...</div>\n\nAfter data initialization by **MyAMS.js**, the following code will be converted to:\n\n.. code-block:: html\n\n    <div data-ams-colorpicker-position="top left">...</div>\n'
import json
from pyramid.interfaces import IRequest
from zope.interface import Interface
from pyams_utils.adapter import ContextAdapter, ContextRequestViewAdapter, adapter_config
from pyams_utils.interfaces.data import IObjectData, IObjectDataRenderer
from pyams_utils.interfaces.tales import ITALESExtension
__docformat__ = 'restructuredtext'

@adapter_config(context=IObjectData, provides=IObjectDataRenderer)
class ObjectDataRenderer(ContextAdapter):
    """ObjectDataRenderer"""

    def get_object_data(self):
        """See :py:class:`IObjectDataRenderer
        <pyams_utils.interfaces.data.IObjectDataRenderer>` interface
        """
        data = IObjectData(self.context)
        if data is not None:
            return json.dumps(data.object_data)


@adapter_config(name='object_data', context=(Interface, Interface, Interface), provides=ITALESExtension)
class ObjectDataExtension(ContextRequestViewAdapter):
    """ObjectDataExtension"""

    def render(self, context=None):
        """See :py:class:`ITALESExtension `pyams_utils.interfaces.tales.ITALESExtension`
        interface
        """
        if context is None:
            context = self.context
        renderer = IObjectDataRenderer(context, None)
        if renderer is not None:
            return renderer.get_object_data()


@adapter_config(name='request_data', context=(Interface, IRequest, Interface), provides=ITALESExtension)
class PyramidRequestDataExtension(ContextRequestViewAdapter):
    """PyramidRequestDataExtension"""

    def render(self, params=None):
        """See :py:class:`ITALESExtension <pyams_utils.interfaces.tales.ITALESExtension>`
        interface
        """
        return self.request.annotations.get(params)