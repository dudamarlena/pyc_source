# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sitetool/convert/rst.py
# Compiled at: 2009-05-03 11:56:19
"""A simple reStructuredText convert plugin"""
import logging, re, os, sys, StringIO
from docutils import core
from docutils.writers.html4css1 import Writer, HTMLTranslator
from sitetool.template.dreamweaver import DreamweaverTemplateInstance
from sitetool.exception import PluginError
from sitetool.convert.plugin import Plugin
log = logging.getLogger(__name__)

class CustomHTMLTranslator(HTMLTranslator):

    def __init__(self, *k, **p):
        HTMLTranslator.__init__(self, *k, **p)
        self.settings.field_name_limit = 0
        self.initial_header_level = 2


def rstify(string, path='no path'):
    """
    Turn a reSturcturedText string into HTML, capturing any errors or warnings
    and re-emitting them with this programs logging system.
    """
    err = sys.stderr
    out = sys.stdout
    error = ''
    out_msg = ''
    try:
        sys.stderr = StringIO.StringIO()
        sys.stdout = StringIO.StringIO()
        w = Writer()
        w.translator_class = CustomHTMLTranslator
        result = core.publish_parts(string, writer=w)['html_body']
        result = ('\n').join(result.split('\n')[1:-2])
        error = sys.stderr.getvalue()
        out_msg = sys.stdout.getvalue()
    finally:
        sys.stderr = err
        sys.stdout = out

    if error:
        log.warning('%s - %s', path, error.replace('\n', ' '))
    if out_msg:
        log.warning('%s - %s', path, out_msg.replace('\n', ' '))
    return result


def save(path, data):
    fp = open(path, 'w')
    fp.write(data)
    fp.close()


class PlainRstPlugin(Plugin):

    def parse_config(self, config):
        if not config:
            return
        result = {}
        if config.has_key('DEFAULT_TEMPLATE'):
            template = config['DEFAULT_TEMPLATE'].strip()
            if template.startswith(self.site_root):
                result['template'] = template
            else:
                if '..' in template:
                    raise PluginError('Template paths cannot contain .. characters')
                if template.startswith('/'):
                    raise PluginError('Template paths cannot start with /')
                result['template'] = os.path.join(self.site_root, template)
        else:
            raise PluginError('No default template could be parsed from the config file')
        return result

    def on_file(self, path):
        if not self.user_files:
            log.debug('DefaultPlugin: Skipping %r, --ignore-user-files set', path)
            return False
        filename = path
        if not filename.endswith('.rst'):
            log.debug("Don't know how to convert %r files" % filename.split('.')[(-1)])
            return False
        html_version = filename[:-4] + '.html'
        if os.path.exists(html_version):
            if not os.stat(filename).st_mtime > os.stat(html_version).st_mtime and not self.force:
                log.debug('Skipping %s since an HTML file of the same name already exists', filename)
                return True
        log.info('DefaultPlugin: Converting %r', path)
        fp = open(filename, 'r')
        rst = fp.read().decode('utf-8')
        fp.close()
        parts = rstify(rst).split('\n')
        title = parts[0][18:-5]
        content = ('\n').join(parts[1:])
        page = DreamweaverTemplateInstance(self.config['template'])
        page['doctitle'] = '<title>' + title + '</title>'
        page['heading'] = title
        page['content'] = content + '<p class="text-right">(<a href="%s">view source</a>)</p>' % os.path.split(path)[1]
        page.save_as_page(filename[:-4] + '.html')
        return True