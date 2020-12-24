# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/tw/yui/base.py
# Compiled at: 2010-01-27 10:56:54
import os, tw
from tw.api import Widget, JSLink, CSSLink, Link
from tw.core.resources import registry, working_set, Requirement
from defaults import __DEFAULT_LINK_IS_EXTERNAL__, __YUI_URL_BASE__, __YUI_VERSION__, __DEFAULT_SUFFIX__

class YUILinkMixin(Link):
    params = {'basename': '(string) basename for the given file.  if you want yuitest-min.js, the base is yuitest/yuitest', 'suffix': '(string) "", min, beta-min, or beta.  Default is "min"', 
       'version': '(string) select the yui version you would like to use. Default version is: ' + __YUI_VERSION__, 
       'external': '(boolean) default:False True if you would like to grab the file from YAHOO! instead of locally', 
       'yui_url_base': 'The base url for fetching the YUI library externally'}
    version = __YUI_VERSION__
    external = __DEFAULT_LINK_IS_EXTERNAL__
    yui_url_base = __YUI_URL_BASE__
    modname = 'tw.yui'
    extension = 'js'
    default_suffix = __DEFAULT_SUFFIX__
    _suffix = ''

    def __init__(self, *args, **kw):
        super(Link, self).__init__(*args, **kw)
        if not self.is_external:
            modname = self.modname or self.__module__
            (self.webdir, self.dirname, self.link) = registry.register(self, modname, self.filename)
        if 'suffix' in kw:
            self.suffix = kw['suffix']
        else:
            self.suffix = self.default_suffix

    def _get_suffix(self):
        if self._suffix == '':
            return ''
        return '-' + self._suffix

    def _set_suffix(self, value):
        self._suffix = value

    suffix = property(_get_suffix, _set_suffix)

    @property
    def external_link(self):
        link = ('/').join((self.yui_url_base, self.version, 'build', self.basename + self.suffix + '.' + self.extension))
        return link

    def _get_link(self):
        if self.is_external:
            return self.external_link
        return tw.framework.url(self._link or '')

    def _set_link(self, link):
        self._link = link

    link = property(_get_link, _set_link)

    def abspath(self, filename):
        return os.sep.join((os.path.dirname(__file__), filename))

    def try_filename(self, filename):
        abspath = self.abspath(filename)
        if os.path.exists(abspath):
            return filename
        return False

    @property
    def filename(self):
        basename = self.basename.replace('/', os.sep)
        basename = self.basename.replace('\\', os.sep)
        basename = os.sep.join(('static', self.version, 'build', basename))
        filename = basename + self.suffix + '.' + self.extension
        if self.try_filename(filename):
            return filename
        else:
            if self.default_suffix == '':
                filename = basename + self.suffix + '.' + self.extension
                if self.try_filename(filename):
                    return filename
            if self.default_suffix == 'min':
                filename = basename + '.' + self.extension
                if self.try_filename(filename):
                    return filename
            filename = basename + '-debug' + '.' + self.extension
            if self.try_filename(filename):
                return filename
            filename = basename + '-beta-min' + '.' + self.extension
            if self.try_filename(filename):
                return filename
            filename = basename + '-beta' + '.' + self.extension
            if self.try_filename(filename):
                return filename
            filename = basename + '-beta-debug' + '.' + self.extension
            if self.try_filename(filename):
                return filename
            return

    @property
    def is_external(self):
        return self.external


class YUIJSLink(JSLink, YUILinkMixin):
    pass


class YUICSSLink(YUILinkMixin, CSSLink):
    extension = 'css'