# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\view\genshisupport.py
# Compiled at: 2011-07-14 06:18:47
"""Template support for Genshi template engine.

This module implements a sub-class of
``genshi.template.plugin.MarkupTemplateEnginePlugin``, to support our extension
to the Buffet templating API that allows to pass additional template engine
options as keyword arguments to the ``render()`` method of engines.

This is necessary, for example, to allow us to pass different doctypes to
Genshi when rendering to different XML-based formats, i.e. HTML, XHML, XML, RSS,
etc. or to omit the doctype all together.

"""
from genshi.output import DocType
from genshi.template.plugin import MarkupTemplateEnginePlugin

class TGGenshiTemplatePlugin(MarkupTemplateEnginePlugin):
    """Custom Genshi template engine plugin supporting Buffet API extensions."""
    __module__ = __name__

    def __init__(self, extra_vars_func=None, options=None):
        default_doctype = options.pop('genshi.default_doctype', None)
        MarkupTemplateEnginePlugin.__init__(self, extra_vars_func, options)
        self.default_doctype = default_doctype
        return

    def render(self, info, format='html', fragment=False, template=None, **options):
        """Render the template to a string using the provided info."""
        kwargs = self._get_render_options(format=format, fragment=fragment, **options)
        return self.transform(info, template).render(**kwargs)

    def _get_render_options(self, format=None, fragment=False, **options):
        """Return options dict for rendering the given format."""
        if format is None:
            format = self.default_format
        kwargs = {'method': format}
        if self.default_encoding:
            kwargs['encoding'] = self.default_encoding
        doctype = options.pop('doctype', self.default_doctype)
        kwargs.update(options)
        if doctype and not fragment:
            if isinstance(doctype, dict):
                doctype = doctype.get(format)
            if doctype:
                doctype = DocType.get(doctype)
                if doctype is None:
                    raise ConfigurationError('Unknown doctype %r' % doctype)
                kwargs['doctype'] = doctype
        return kwargs