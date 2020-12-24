# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/data.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 3944 bytes
"""PyAMS_utils.data module

The *IObjectData* interface is a generic interface which can be used to assign custom data to any
object. This object data may be any object which can be serialized to JSON, and assigned to any
HTML *data* attribute. It can typically be used to set a *data-ams-data* attribute to objects,
which is afterwards converted to classic *data-* attributes by **MyAMS.js** framework.

For example, for a custom widget in a form:

.. code-block:: python

    def updateWidgets(self):
        super(MyForm, self).updateWidgets()
        widget = self.widgets['mywidget']
        alsoProvides(widget, IObjectData)
        widget.object_data = {'ams-colorpicker-position': 'top left'}

You can then set an attribute in a TAL template like this:

.. code-block:: xml

    <div tal:attributes="data-ams-data extension:object_data(widget)">...</div>

After data initialization by **MyAMS.js**, the following code will be converted to:

.. code-block:: html

    <div data-ams-colorpicker-position="top left">...</div>
"""
import json
from pyramid.interfaces import IRequest
from zope.interface import Interface
from pyams_utils.adapter import ContextAdapter, ContextRequestViewAdapter, adapter_config
from pyams_utils.interfaces.data import IObjectData, IObjectDataRenderer
from pyams_utils.interfaces.tales import ITALESExtension
__docformat__ = 'restructuredtext'

@adapter_config(context=IObjectData, provides=IObjectDataRenderer)
class ObjectDataRenderer(ContextAdapter):
    __doc__ = 'Object data JSON renderer'

    def get_object_data(self):
        """See :py:class:`IObjectDataRenderer
        <pyams_utils.interfaces.data.IObjectDataRenderer>` interface
        """
        data = IObjectData(self.context)
        if data is not None:
            return json.dumps(data.object_data)


@adapter_config(name='object_data', context=(Interface, Interface, Interface), provides=ITALESExtension)
class ObjectDataExtension(ContextRequestViewAdapter):
    __doc__ = 'extension:object_data TALES extension\n\n    This TALES extension is to be used in Chameleon templates to define a custom data attribute\n    which stores all object data (see :py:class:`IObjectData\n    <pyams_utils.interfaces.data.IObjectData>` interface), like this:\n\n    .. code-block:: xml\n\n        <div tal:attributes="data-ams-data extension:object_data(context)">...</div>\n    '

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
    __doc__ = 'extension:request_data TALES extension for Pyramid request\n\n    This TALES extension can be used to get a request data, previously stored in the request via\n    an annotation.\n\n    For example:\n\n    .. code-block:: xml\n\n        <div tal:content="extension:request_data(\'my.annotation.key\')">...</div>\n    '

    def render(self, params=None):
        """See :py:class:`ITALESExtension <pyams_utils.interfaces.tales.ITALESExtension>`
        interface
        """
        return self.request.annotations.get(params)