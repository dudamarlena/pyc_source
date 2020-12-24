# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/slab/formats/template.py
# Compiled at: 2016-01-08 05:49:58
# Size of source mod 2**32: 4756 bytes
from ..utils import argtype_dir_input, get_module_imports
from .base import MetaFormatBase
from .apidoc import ApidocReSTFormat
__all__ = ('TemplateMetaFormat', 'TemplateApidocFormat')

class TemplateMetaFormat(MetaFormatBase):

    def configure(self, options):
        try:
            import jinja2
        except ImportError as err:
            raise ImportError("Can't find the jinja2 package, please install it to use {}".format(self.__class__.__name__)) from err

        override = not options.no_override
        template_extension = options.template_extension
        templates_dir = options.templates_dir
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=templates_dir))
        module_template = env.get_template(options.module_template.format(TEMPLATE_EXT=template_extension))
        package_template = env.get_template(options.package_template.format(TEMPLATE_EXT=template_extension))
        toc_template = env.get_template(options.toc_template.format(TEMPLATE_EXT=template_extension))

        def __maker(default_template):

            def __get_template(node):
                if not override:
                    return default_template
                try:
                    return env.get_template(node.qualname + '.' + template_extension)
                except jinja2.TemplateNotFound:
                    return default_template

            return _TemplateMetaFormat__get_template

        self._TemplateMetaFormat__get_module_template = _TemplateMetaFormat__maker(module_template)
        self._TemplateMetaFormat__get_package_template = _TemplateMetaFormat__maker(package_template)
        self._TemplateMetaFormat__get_toc_template = lambda items, default_template=toc_template: default_template

    def __get_values(self, item):
        return {'content': self.format.render(item), 
         'name': item.name, 
         'qualname': item.qualname, 
         'path': item.path, 
         'root': item.root}

    def package(self, package):
        return self._TemplateMetaFormat__get_package_template(package).render(self._TemplateMetaFormat__get_values(package))

    def module(self, module):
        values = self._TemplateMetaFormat__get_values(module)
        imports = [
         'from {} import *'.format(module.qualname)]
        values['imports'] = imports
        return self._TemplateMetaFormat__get_module_template(module).render(values)

    def toc(self, items):
        return self._TemplateMetaFormat__get_toc_template(items).render(content=self.format.toc(items))

    @classmethod
    def add_arguments(cls, parser):
        group = parser.add_argument_group('Template options')
        group.add_argument('-X', '--templates-dir', metavar='TEMPLATES_DIR', dest='templates_dir', type=argtype_dir_input, default='.', help='The directory to be searched for template files.')
        group.add_argument('-K', '--template-extension', metavar='TEMPLATE_EXT', dest='template_extension', default='rst', help='The extension to be used when looking for override files.')
        group.add_argument('-P', '--package-template', dest='package_template', default='package.{TEMPLATE_EXT}', help='The template file to be used for all package files generation. If a relative path is provided, the file name will be searched in TEMPLATES_DIR.')
        group.add_argument('-D', '--module-template', dest='module_template', default='module.{TEMPLATE_EXT}', help='The template file to be used for all module files generation. If a relative path is provided, the file name will be searched in TEMPLATES_DIR.')
        group.add_argument('-C', '--toc-template', dest='toc_template', default='toc.{TEMPLATE_EXT}', help='The template file to be used for all TOC files generation. If a relative path is provided, the file name will be searched in TEMPLATES_DIR.')
        group.add_argument('-W', '--no-override', dest='no_override', action='store_true', default=False, help='Disables the template overriding behaviour. When specified, only common templates will be used for generation of each file type.')


class TemplateApidocFormat(TemplateMetaFormat):

    def __init__(self, options):
        super().__init__(options, ApidocReSTFormat)