# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Files\Research\databrowse\databrowse\support\dummy_web_support.py
# Compiled at: 2020-02-17 22:39:45
# Size of source mod 2**32: 17230 bytes
""" support/dummy_web_support.py - Classes to encapsulate Web/WSGI functionality """
import os, cgi
from lxml import etree
try:
    from urllib import pathname2url
except ImportError:
    from urllib.request import pathname2url

import databrowse.support

class CefHttp:

    def __init__(self):
        pass


class wsgi_req:
    __doc__ = ' A simple wrapper for the wsgi request '

    def start_response(self, status, headers):
        for header in headers:
            self.response_headers[header[0]] = header[1]

    environ = {}
    filename = None
    dirname = None
    unparsed_uri = None
    form = None
    agent = 'dummy'
    status = None
    output = None
    response_headers = None
    output_done = None

    def __init__(self, filename, params):
        """ Load Values from Request """
        fs = {}
        params['path'] = filename
        resultset = [key for key, value in params.items() if key not in ('files[]', )]
        os.environ['QUERY_STRING'] = str('&'.join(['%s=%s' % (key, params[key]) for key in resultset]))
        if 'files[]' in params:
            for var in params:
                fp = CefHttp()
                if var == 'files[]':
                    for fvar in params[var]:
                        setattr(fp, fvar, params[var][fvar])

                else:
                    setattr(fp, 'value', params[var])
                fs[var] = fp

        else:
            fs = cgi.FieldStorage(keep_blank_values=1)
        self.form = fs
        self.status = '200 OK'
        self.response_headers = {}
        self.response_headers['Content-Type'] = 'text/html'
        self.output_done = False
        if 'debug' in self.form:
            self.response_headers['Content-Type'] = 'text/plain'

    def return_page(self):
        """ Send Webpage Output """
        return self.output

    def return_error(self, status=500):
        """ Return Error Message """
        if status == 400:
            self.status = 'Bad Request'
        else:
            if status == 401:
                self.status = 'Unauthorized'
            else:
                if status == 403:
                    self.status = 'Forbidden'
                else:
                    if status == 404:
                        self.status = 'Page Not Found'
                    else:
                        if status == 405:
                            self.status = 'Method Not Allowed'
                        else:
                            if status == 406:
                                self.status = 'Not Acceptable'
                            else:
                                if status == 500:
                                    self.status = 'Internal Server Error'
                                else:
                                    if status == 501:
                                        self.status = 'Not Implemented'
                                    else:
                                        if status == 503:
                                            self.status = 'Service Unavailable'
                                        else:
                                            self.status = 'Internal Server Error'
        self.response_headers = {}
        self.response_headers['Content-Type'] = 'text/html'
        self.response_headers['Content-Length'] = str(len(self.status.encode('utf-8')))
        raise Exception(self.status)


class style_support:
    __doc__ = ' Class containing support functionality for xslt stylesheet compliation '
    _style_dict = {}

    class StyleException(Exception):
        pass

    def __init__(self):
        self._style_dict = {}

    def AddStyle(self, namespace, content):
        if namespace in self._style_dict:
            if self._style_dict[namespace] != content:
                raise self.StyleException('Multiple stylesheets using the same namespace and mode exist')
        else:
            self._style_dict[namespace] = content

    def IsStyleLoaded(self, namespace):
        if namespace in self._style_dict:
            return True
        return False

    def GetStyle(self):
        stylestring = ''
        for i in self._style_dict:
            stylestring = stylestring + self._style_dict[i]

        return stylestring


class menu_support:
    __doc__ = ' Class containing support functionality for xslt stylesheet compliation '
    _menu = []

    class MenuException(Exception):
        pass

    def __init__(self, siteurl, logouturl, username):
        self._menu = []
        topmenu = etree.Element('{http://thermal.cnde.iastate.edu/databrowse}navbar', xmlns='http://www.w3.org/1999/xhtml')
        menuitem = etree.SubElement(topmenu, '{http://thermal.cnde.iastate.edu/databrowse}navelem')
        menulink = etree.SubElement(menuitem, '{http://www.w3.org/1999/xhtml}a', href=siteurl)
        menulink.text = 'Databrowse Home'
        self.AddMenu(topmenu)

    def AddMenu(self, xml):
        self._menu.append(xml)

    def GetMenu(self):
        menu = etree.XML('<db:navigation xmlns="http://www.w3.org/1999/xhtml" xmlns:db="http://thermal.cnde.iastate.edu/databrowse"/>')
        for item in self._menu:
            menu.append(item)

        return menu


class web_support:
    __doc__ = ' Class containing support functionality for web operations '
    req = None
    style = None
    menu = None
    req_filename = None
    webdir = None
    confstr = None
    email_sendmail = None
    email_admin = None
    email_from = None
    administrators = None
    limatix_qautils = None
    qautils = None
    sitetitle = None
    shorttitle = None
    remoteuser = None
    siteurl = None
    resurl = None
    logouturl = None
    dataroot = None
    pluginpath = None
    icondbpath = None
    hiddenfiledbpath = None
    directorypluginpath = None
    checklistpath = None
    stderr = None
    seo_urls = None
    debugging = None

    def __init__(self, filename, params):
        self.req = wsgi_req(filename, params)
        if params.get('install'):
            self.webdir = os.path.join(params['install'], 'databrowse_wsgi')
        self.style = style_support()
        scheme = params.get('scheme')
        if params.get('install'):
            try:
                conffile = file(os.path.join(params['install'], 'databrowse_wsgi/databrowse_wsgi.conf'))
                self.confstr = conffile.read()
                conffile.close()
                exec(self.confstr)
            except Exception:
                pass

        if self.dataroot is None:
            if params.get('dataroot'):
                self.dataroot = os.path.normpath(params.get('dataroot'))
            if self.dataroot is None:
                self.dataroot = '/'
        if self.checklistpath is None:
            self.checklistpath = '/SOPs'
        elif self.siteurl is None:
            if params.get('install'):
                if scheme is not None:
                    self.siteurl = '/'.join([scheme, pathname2url(self.dataroot).replace('//', '')[1:]])
                else:
                    self.siteurl = '/'.join(['http://0.0.0.0', self.dataroot])
            else:
                self.siteurl = 'http://localhost/databrowse'
        else:
            if self.resurl is None:
                if params.get('install'):
                    if scheme is not None:
                        self.resurl = '/'.join([scheme,
                         pathname2url(os.path.abspath(os.path.join(os.path.join(os.path.join(os.path.dirname(__file__), os.pardir), os.pardir), 'databrowse_wsgi/resources'))).replace('//', '')[1:]])
                    else:
                        self.resurl = '/'.join(['http://0.0.0.0',
                         pathname2url(os.path.abspath(os.path.join(os.path.join(os.path.join(os.path.dirname(__file__), os.pardir), os.pardir), 'databrowse_wsgi/resources'))).replace('//', '')[1:]])
                else:
                    self.resurl = 'http://localhost/dbres'
            if self.logouturl is None:
                if params.get('install'):
                    if scheme is not None:
                        self.logouturl = '/'.join([scheme, 'logout'])
                else:
                    self.logouturl = 'http://0.0.0.0/logout'
            else:
                self.logouturl = 'http://localhost/logout'
        if self.icondbpath is None:
            self.icondbpath = os.path.join(os.path.dirname(databrowse.support.__file__), 'iconmap.conf')
        if self.hiddenfiledbpath is None:
            self.hiddenfiledbpath = os.path.join(os.path.dirname(databrowse.support.__file__), 'hiddenfiles.conf')
        if self.directorypluginpath is None:
            self.directorypluginpath = os.path.join(os.path.dirname(databrowse.support.__file__), 'directoryplugins.conf')
        if self.email_sendmail is None:
            self.email_sendmail = '/usr/lib/sendmail -i'
        if self.email_admin is None:
            self.email_admin = 'tylerl@iastate.edu'
        if self.email_from is None:
            self.emailfrom = 'tylerl@iastate.edu'
        if self.limatix_qautils is None:
            self.limatix_qautils = params.get('limatix-qautils')
            if self.limatix_qautils is None:
                self.limatix_qautils = '/usr/local/limatix-qautils'
        if self.qautils is None:
            self.qautils = params.get('qautils')
            if self.qautils is None:
                self.qautils = '/usr/local/QAutils'
        if self.administrators is None:
            self.administrators = {'sdh4':'Steve Holland', 
             'tylerl':'Tyler Lesthaeghe'}
        if self.sitetitle is None:
            self.sitetitle = 'Databrowse Project Browser'
        if self.shorttitle is None:
            self.shorttitle = 'databrowse'
        if self.seo_urls is None:
            self.seo_urls = True
        if self.debugging is None:
            self.debugging = False
        self.menu = menu_support(self.siteurl, self.logouturl, '')
        assert self.dataroot is not None