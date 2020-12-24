# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/template.py
# Compiled at: 2017-12-05 15:58:38
# Size of source mod 2**32: 3215 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
from abc import ABCMeta, abstractmethod
import io
from mako.template import Template
from mako.lookup import TemplateCollection
from mako.runtime import Context
from wasp_general.verify import verify_type, verify_value

class WTemplate(metaclass=ABCMeta):

    @abstractmethod
    def template(self):
        raise NotImplementedError('This method is abstract')


class WMakoTemplate(WTemplate):

    @verify_type(template=Template)
    def __init__(self, template):
        self._WMakoTemplate__template = template

    def template(self):
        return self._WMakoTemplate__template


class WTemplateText(WTemplate):

    @verify_type(text_template=str)
    def __init__(self, text_template, **kwargs):
        WTemplate.__init__(self)
        self._WTemplateText__template = Template(text=text_template, **kwargs)

    def template(self):
        return self._WTemplateText__template


class WTemplateFile(WTemplate):

    @verify_type(template_filename=str)
    @verify_value(template_filename=lambda x: len(x) > 0)
    def __init__(self, template_filename, **kwargs):
        WTemplate.__init__(self)
        self._WTemplateFile__template = Template(filename=template_filename, **kwargs)

    def template(self):
        return self._WTemplateFile__template


class WTemplateLookup(WTemplate):

    @verify_type(template_id=str, template_collection=TemplateCollection)
    def __init__(self, template_id, template_collection):
        WTemplate.__init__(self)
        self._WTemplateLookup__template_id = template_id
        self._WTemplateLookup__collection = template_collection

    def template(self):
        return self._WTemplateLookup__collection.get_template(self._WTemplateLookup__template_id)


class WTemplateRenderer:

    @verify_type(template=WTemplate, context=(None, dict))
    def __init__(self, template, context=None):
        self._WTemplateRenderer__template = template
        self._WTemplateRenderer__context = context if context is not None else {}

    def template(self):
        return self._WTemplateRenderer__template.template()

    def context(self):
        return self._WTemplateRenderer__context

    def update_context(self, **context_vars):
        self._WTemplateRenderer__context.update(context_vars)

    def render(self, **context_vars):
        template = self.template()
        buffer = io.StringIO()
        context = self.context()
        context.update(context_vars)
        context = Context(buffer, **context)
        template.render_context(context)
        return buffer.getvalue()