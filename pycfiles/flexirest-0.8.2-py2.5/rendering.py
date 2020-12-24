# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/flexirest/rendering.py
# Compiled at: 2009-11-13 06:06:07
import itertools, os, sys
from docutils import writers
from docutils.parsers.rst import roles
from docutils.core import publish_parts
from flexirest import tex
__docformat__ = 'reStructuredText'
pseudo_writers = {'latex2pdf': 'latex2e'}
all_writers = lambda : sorted(set(itertools.chain(writers._writer_aliases.keys(), writers._writer_aliases.values(), pseudo_writers)))

def _register_roles(conf):
    """
    Registers roles to be used in this run.

    `conf` - configuration module.
    """
    for (rolecand, rolename) in ((getattr(conf, role), role) for role in dir(conf) if role.startswith('role_')):
        if callable(rolecand):
            roles.register_canonical_role(rolename[5:], rolecand)


class Render(object):

    def __init__(self, conf, options, template, writer_name):
        self.conf = conf
        self.options = options
        self.template = template
        self._writer = writer_name

    def _build_settings(self):
        _register_roles(self.conf)
        return getattr(self, '_build_%s_settings' % self.writer, lambda : {})()

    def dump_parts(self, source, destination):
        """
        Writes a mini-report on what parts where created by the specified
        `docutils` writer (intended for human consumption).

        `parts` - parts `dict` created by `docutils.core.publish_parts()`
        `out` - output stream to write to.
        """
        title = "Parts created by the docutils writer '%s'" % self.writer
        destination.write(title + os.linesep)
        destination.write(len(title) * '-')
        destination.write(2 * os.linesep)
        destination.write('Part keys: ' + 2 * os.linesep)
        parts = self.publish_parts(source)
        destination.write(os.linesep.join(sorted(parts.keys())))
        destination.write(2 * os.linesep)
        for part in parts:
            destination.write("Value of part '%s':%s" % (part, os.linesep))
            destination.write(parts[part] + os.linesep)
            destination.write(80 * '-' + os.linesep)
            destination.write(os.linesep)

    @property
    def writer(self):
        if self._writer in pseudo_writers:
            return pseudo_writers[self._writer]
        return self._writer

    def publish_parts(self, source):
        parts = publish_parts(source=source.read().decode('utf8'), writer_name=self.writer, settings_overrides=self._build_settings())
        parts['lang'] = self.options.lang
        return parts

    def default_writer(self, stage_one, destination):
        """
        The default writer just writes out the template applied output
        from publich_parts().
        """
        destination.write(stage_one.encode('utf-8'))

    def render(self, source, destination):
        parts = self.publish_parts(source)
        getattr(self, '_write_%s' % self._writer, self.default_writer)(self.template % parts, destination)
        destination.flush()

    def _build_html_settings(self):
        return {}

    def _build_latex_settings(self):
        return {'output_encoding': 'utf-8', 'language_code': self.options.lang}

    _build_latex2e_settings = _build_latex_settings
    _build_latex2pdf_settings = _build_latex_settings

    def _write_latex2pdf(self, latex, destination):
        pdf = tex.latex2pdf(latex)
        destination.write(pdf)


def render(source, destination, conf, options, template, writer_name):
    """API entry point (helper for the most obvious case).

    A call expected to succed must provide all parameters. See
    flexirest.main.commandline() to find sensible defaults.

    `source` - file-like object to read input from.
    `destination` - file-like object (needs at least `.write()` and `.flush()`
                  methods.
    `conf` - configuration module.
    `options` - commandline options
    `template` - the template to enter the results of `publish_parts()` into.
               (needs to support formatting with the '..' % {} technique.)
    `writer_name` - name of the `docutils` writer to use.
    """
    renderer = Render(conf, options, template, writer_name)
    renderer.render(source, destination)


def dump_parts(source, destination, conf, options, template, writer_name):
    """API entry point for the `dump_parts` option.

    A call expected to succed must provide all parameters. See
    flexirest.main.commandline() to find sensible defaults.

    `source` - file-like object to read input from.
    `destination` - file-like object (needs at least `.write()` and `.flush()`
                  methods.
    `conf` - configuration module.
    `options` - commandline options
    `template` - the template to enter the results of `publish_parts()` into.
               (needs to support formatting with the '..' % {} technique.)
    `writer_name` - name of the `docutils` writer to use.
    """
    renderer = Render(conf, options, template, writer_name)
    renderer.dump_parts(source, destination)