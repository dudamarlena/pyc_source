# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/filters/rst.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 9527 bytes
from dexy.filter import DexyFilter
from docutils import core
from docutils.frontend import OptionParser
from docutils.parsers.rst import Parser
from docutils.transforms import Transformer, frontmatter
from docutils.utils import new_document
import io, dexy.exceptions, docutils.writers, os

def default_template(writer_name):
    """
    Set the default template correctly, in case there has been a change in working dir.
    """
    writer_class = docutils.writers.get_writer_class(writer_name)
    if os.path.isdir(writer_class.default_template_path):
        return os.path.abspath(os.path.join(writer_class.default_template_path, writer_class.default_template))
    return os.path.abspath(writer_class.default_template_path)


class RestructuredTextBase(DexyFilter):
    __doc__ = ' Base class for ReST filters using the docutils library.\n    '
    aliases = []
    _settings = {'input-extensions':[
      '.rst', '.txt'], 
     'output-extensions':[
      '.html', '.tex', '.xml', '.odt'], 
     'output':True, 
     'writer':('Specify rst writer to use (not required: dexy will attempt to determine automatically from filename if not specified).',
 None), 
     'stylesheet':('Stylesheet arg to pass to rst', None), 
     'template':('Template arg to pass to rst', None)}

    def docutils_writer_name(self):
        if self.setting('writer'):
            return self.setting('writer')
        if self.ext == '.html':
            return 'html'
        if self.ext == '.tex':
            return 'latex2e'
        if self.ext == '.xml':
            return 'docutils_xml'
        if self.ext == '.odt':
            return 'odf_odt'
        raise Exception('unsupported extension %s' % self.ext)


class RestructuredText(RestructuredTextBase):
    __doc__ = "\n    A 'native' ReST filter which uses the docutils library.\n\n    Look for configuration options for writers here:\n    http://docutils.sourceforge.net/docs/user/config.html\n    "
    aliases = ['rst']
    skip_settings = 'settings-not-for-settings-overrides'
    _settings = {'allow-any-template-extension': ('Whether to NOT raise an error if template extension does not match document extension.',
 False), 
     skip_settings: (
                     'Which of the settings should NOT be passed to settings_overrides.',
                     [
                      'writer'])}

    def process(self):

        def skip_setting(key):
            in_base_filter = key in DexyFilter._settings
            in_skip = key in self.setting(self.skip_settings) or key == self.skip_settings
            return in_base_filter or in_skip

        settings_overrides = dict(((k.replace('-', '_'), v) for k, v in self.setting_values().items() if v if not skip_setting(k)))
        writer_name = self.docutils_writer_name()
        warning_stream = io.StringIO()
        settings_overrides['warning_stream'] = warning_stream
        self.log_debug('settings for rst: %r' % settings_overrides)
        self.log_debug('rst writer: %s' % writer_name)
        if 'template' in settings_overrides:
            if not self.setting('allow-any-template-extension'):
                template = settings_overrides['template']
                template_ext = os.path.splitext(template)[1]
                if not template_ext == self.ext:
                    msg = "You requested template '%s' with extension '%s' for %s, does not match document extension of '%s'"
                    args = (template, template_ext, self.key, self.ext)
                    raise dexy.exceptions.UserFeedback(msg % args)
        if 'template' not in settings_overrides:
            if hasattr(writer_name, 'default_template'):
                settings_overrides['template'] = default_template(writer_name)
        try:
            core.publish_file(source_path=(self.input_data.storage.data_file()),
              destination_path=(self.output_data.storage.data_file()),
              writer_name=writer_name,
              settings_overrides=settings_overrides)
        except ValueError as e:
            try:
                if 'Invalid placeholder in string' in e.message:
                    if 'template' in settings_overrides:
                        self.log_warn("you are using template '%s'. is this correct?" % settings_overrides['template'])
                raise
            finally:
                e = None
                del e

        except Exception:
            self.log_warn('An error occurred while generating reStructuredText.')
            self.log_warn('source file %s' % self.input_data.storage.data_file())
            self.log_warn('settings for rst: %r' % settings_overrides)
            self.log_warn('rst writer: %s' % writer_name)
            raise

        self.log_debug('docutils warnings:\n%s\n' % warning_stream.getvalue())


class RstBody(RestructuredTextBase):
    __doc__ = '\n    Returns just the body part of an ReST document.\n    '
    aliases = ['rstbody']
    _settings = {'set-title':('Whether to set document title.', True), 
     'output-extensions':[
      '.html', '.tex']}

    def process_text(self, input_text):
        warning_stream = io.StringIO()
        settings_overrides = {}
        settings_overrides['warning_stream'] = warning_stream
        writer_name = self.docutils_writer_name()
        self.log_debug("about to call publish_parts with writer '%s'" % writer_name)
        if 'template' not in settings_overrides:
            settings_overrides['template'] = default_template(writer_name)
        try:
            parts = core.publish_parts(input_text,
              writer_name=writer_name,
              settings_overrides=settings_overrides)
        except AttributeError as e:
            try:
                raise dexy.exceptions.InternalDexyProblem(str(e))
            finally:
                e = None
                del e

        if self.setting('set-title'):
            if 'title' in parts:
                if parts['title']:
                    self.update_all_args({'title': parts['title']})
        self.log_debug('docutils warnings:\n%s\n' % warning_stream.getvalue())
        return parts['body']


class RstMeta(RestructuredTextBase):
    __doc__ = '\n    Extracts bibliographical metadata and makes this available to dexy.\n    '
    aliases = ['rstmeta']
    _settings = {'output-extensions': ['.rst']}

    def process_text(self, input_text):
        warning_stream = io.StringIO()
        settings_overrides = {}
        settings_overrides['warning_stream'] = warning_stream
        settings = OptionParser(components=(Parser,)).get_default_values()
        parser = Parser()
        document = new_document('rstinfo', settings)
        parser.parse(input_text, document)
        t = Transformer(document)
        t.add_transforms([frontmatter.DocTitle, frontmatter.DocInfo])
        t.apply_transforms()
        info = {}
        single_nodes = [
         docutils.nodes.title,
         docutils.nodes.subtitle]
        for node in single_nodes:
            for doc in document.traverse(node):
                if not len(doc.children) == 1:
                    msg = 'Expected node %s to only have 1 child.'
                    raise dexy.exceptions.InternalDexyProblem(msg % node)
                info[doc.tagname] = doc.children[0].astext()

        for doc in document.traverse(docutils.nodes.docinfo):
            for element in doc.children:
                if element.tagname == 'field':
                    name, value = element.children
                    name, value = name.astext(), value.astext()
                else:
                    name, value = element.tagname, element.astext()
                info[name] = value

        self.log_debug('found info:\n%s\n' % info)
        self.update_all_args(info)
        self.log_debug('docutils warnings:\n%s\n' % warning_stream.getvalue())
        return input_text


class RstDocParts(DexyFilter):
    __doc__ = '\n    Returns key-value storage of document parts.\n    '
    aliases = ['rstdocparts']
    _settings = {'input-extensions':[
      '.rst', '.txt'], 
     'data-type':'keyvalue', 
     'output-extensions':[
      '.sqlite3', '.json'], 
     'writer':('Specify rst writer to use.', 'html')}

    def process(self):
        input_text = str(self.input_data)
        warning_stream = io.StringIO()
        settings_overrides = {}
        settings_overrides['warning_stream'] = warning_stream
        writer_name = self.setting('writer')
        if 'template' not in settings_overrides:
            settings_overrides['template'] = default_template(writer_name)
        parts = core.publish_parts(input_text,
          writer_name=writer_name,
          settings_overrides=settings_overrides)
        self.log_debug('docutils warnings:\n%s\n' % warning_stream.getvalue())
        for k, v in parts.items():
            self.output_data.append(k, v)

        self.output_data.save()