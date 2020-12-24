# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysmvt/templates.py
# Compiled at: 2010-05-30 13:30:03
from os import path
import logging
from pysutils import case_cw2us
from pysmvt import ag, settings, appfilepath
from pysmvt.exceptions import ProgrammingError
from pysmvt.utils import safe_strftime
from jinja2 import FileSystemLoader, Environment, TemplateNotFound
from jinja2.loaders import split_template_path
log = logging.getLogger(__name__)

class JinjaBase(object):

    def __init__(self, endpoint):
        self.templateName = None
        self.tpl_extension = None
        self._templateValues = {}
        app_mod_name = endpoint.split(':')[0]
        self.setOptions()
        if hasattr(ag, 'templateEnv'):
            self.jinjaTemplateEnv = ag.templateEnv
        else:
            ag.jinjaTemplateEnv = self.templateEnv = Environment(**self._jinjaEnvOptions)
            ag.jinjaTemplateEnv.filters['strftime'] = safe_strftime
        self.templateEnv.loader = AppTemplateLoader(app_mod_name)
        return

    def setOptions(self):
        self._jinjaEnvOptions = {'block_start_string': '<%', 
           'block_end_string': '%>', 
           'variable_start_string': '<{', 
           'variable_end_string': '}>', 
           'comment_start_string': '<#', 
           'comment_end_string': '#>'}

    def render(self):
        template = self.templateEnv.get_template(self.templateName + '.' + self.tpl_extension)
        return template.render(self._templateValues)

    def assign(self, key, value):
        self._templateValues[key] = value


class JinjaHtmlBase(JinjaBase):

    def __init__(self, modulePath):
        JinjaBase.__init__(self, modulePath)
        self.tpl_extension = 'html'


class AppTemplateLoader(FileSystemLoader):
    """
        A modification of Jinja's FileSystemLoader to take into account how
        pysmvt apps can inherit from other apps
    """

    def __init__(self, modname, encoding='utf-8'):
        self.encoding = encoding
        self.modname = modname

    def get_source(self, environment, template):
        if ':' in template:
            (modname, template) = template.split(':', 1)
        else:
            modname = self.modname
        pieces = split_template_path(template)
        modppath = path.join('modules', modname, 'templates', *pieces)
        apppath = path.join('templates', *pieces)
        log.debug('template modpath: %s', modppath)
        log.debug('template apppath: %s', apppath)
        try:
            fpath = appfilepath(modppath, apppath)
        except ProgrammingError, e:
            if 'could not locate' in str(e):
                log.debug('could not locate template file, trying underscore version')
                utemplate = case_cw2us(template)
                if utemplate == template:
                    log.debug('underscore version was the same')
                    raise TemplateNotFound(template)
                pieces = split_template_path(utemplate)
                modppath = path.join('modules', self.modname, 'templates', *pieces)
                apppath = path.join('templates', *pieces)
                log.debug('utemplate modpath: %s', modppath)
                log.debug('utemplate apppath: %s', apppath)
                try:
                    fpath = appfilepath(modppath, apppath)
                except ProgrammingError, e:
                    if 'could not locate' in str(e):
                        raise TemplateNotFound(template)
                    raise

        f = file(fpath)
        try:
            contents = f.read().decode(self.encoding)
        finally:
            f.close()

        old = path.getmtime(fpath)
        return (contents, fpath, lambda : path.getmtime(fpath) == old)