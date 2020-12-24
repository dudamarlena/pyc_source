# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bunny1/bunny1.py
# Compiled at: 2009-02-23 22:22:59
import sys, os, re, cgi, urllib, urlparse, optparse, socket
from urllib import quote as q
from urllib import quote_plus as qp
from xml.sax.saxutils import escape
import cherrypy
from cherrypy import HTTPRedirect
from cherrypy import expose
from itertools import imap, izip, ifilter
__doc__ = '\n    bunny1 is a tool that lets you write smart bookmarks in python and then\n    share them across all your browsers and with a group of people or the\n    whole world. It was developed at Facebook and is widely used there.\n'
__author__ = 'ccheever'
__date__ = 'Mon Oct 22 02:27:47 PDT 2007'
YUBNUB_URL = 'http://yubnub.org/parser/parse?command='
GOOGLE_SEARCH_URL = 'http://www.google.com/search?q='
GOOGLE_LUCKY_SEARCH_URL = 'http://www.google.com/search?btnI&q='
DEFAULT_FALLBACK_URL = YUBNUB_URL
DEFAULT_COMMAND = 'help'
DEFAULT_PORT = 9084
BUNNY1_HOME_URL = 'http://www.bunny1.org/'
DONT_LIST_AS_POPULAR = (
 'echo', 'url', '_setpasswd')
COMMAND_QUERY_STRING_VAR = '___'

class ServerModes(object):
    """enum for different modes that the server can operate in"""
    __module__ = __name__
    CHERRYPY = 'CHERRYPY'
    CGI = 'CGI'
    COMMAND_LINE = 'COMMAND_LINE'


class Bunny1Decorators(object):
    """bunny1 decorators manipulate URLs after they are returned"""
    __module__ = __name__

    def default_url(self):
        """the default URL to go to if nothing is entered except a decorator"""
        return BUNNY1_HOME_URL


class Bunny1(object):
    __module__ = __name__

    def __init__(self, commands, decorators=None, server_mode=ServerModes.CHERRYPY):
        commands._b1 = self
        decorators._b1 = self
        self.commands = commands
        if decorators:
            self.decorators = decorators
        else:
            self.decorators = Bunny1Decorators()
        self.base_url = BUNNY1_HOME_URL
        self._server_mode = server_mode

    def server_mode(self):
        """returns what mode the server is in (CHERRYPY or CGI)"""
        return self._server_mode

    def auth(self):
        """returns True if the user is authorized to use this bunny1 instance"""
        return True

    def unauthorized(self):
        """what to show when the user isn't authorized to use this instance"""
        raise cherrypy.HTTPError(404)

    def error(self, error_message):
        """call this when there is an error"""
        return "<span style='color: red; font-family: Courier New, Courier, Fixed-width; font-weight: bold;'>%s</span>" % error_message

    @expose
    def default(self, *a, **k):
        raw = None
        for raw in k:
            break

        if raw == COMMAND_QUERY_STRING_VAR:
            raw = k[COMMAND_QUERY_STRING_VAR]
        return self.do_command(raw, a, k)

    def do_command(self, raw, a=(), k={}):
        """does the specified command"""
        self.commands.history.append(raw)
        if not raw:
            raw = DEFAULT_COMMAND
        cherrypy.request.bunny1 = {'decorators': []}
        while True:
            try:
                (method, arg) = raw.split(None, 1)
            except ValueError:
                method = raw
                arg = ''

            if method.startswith('@') and method != '@':
                try:
                    d = getattr(self.decorators, method[1:])
                    if d.exposed:
                        cherrypy.request.bunny1['decorators'].append(d)
                    else:
                        raise DoesNotExist(method)
                    raw = arg
                except (AttributeError, DoesNotExist):
                    return self.error('no decorator named %s %s' % (escape(method), repr(self.decorators)))

            else:
                break

        try:
            method = cherrypy.request.cookie[('alias.' + method)].value
        except KeyError:
            pass

        if method == '@':
            try:
                (method, arg) = arg.split(None, 1)
            except ValueError:
                method = arg
                arg = ''

        if method == '':
            method = 'url'
            arg = self.decorators.default_url()
        if urlparse.urlsplit(method)[0]:
            method = 'url'
            arg = raw
        if method == '_debug':
            try:
                return self.do_command(arg)
            except HTTPRedirect, redir:
                url = redir.urls[0]
                return "<code><b>bunny1</b> DEBUG: redirect to <a href='%s'>%s</a></code>" % (url, url)

        if method.startswith('__'):
            return self.error("commands can't start with a double underscore")
        try:
            try:
                cmd = getattr(self.commands, method)
                if hasattr(cmd, 'dont_expose') and cmd.dont_expose:
                    raise Fallback('method not exposed')
                if not callable(cmd):
                    raise Fallback('method not callable')
            except AttributeError:
                raise Fallback('no method')

            if not self.auth() and not getattr(cmd, 'no_auth_required', False):
                return self.unauthorized()
            cherrypy.response.headers['X-Bunny1-Host'] = cherrypy.server.socket_host
            try:
                if method:
                    popularity = self.commands.popularity
                    popularity[method] = popularity.get(method, 0) + 1
                preprocessor = getattr(cmd, 'preprocessor', None)
                if callable(preprocessor):
                    arg = preprocessor(arg)
                url = cmd(arg)
                if url is None:
                    return 'done.'
                for decorator_method in cherrypy.request.bunny1['decorators'][::-1]:
                    url = decorator_method(url)

                raise HTTPRedirect(url)
            except Content, content:
                cherrypy.response.headers['Content-Type'] = content.content_type
                return content.html

        except Fallback:
            return self.fallback(raw, *a, **k)

        return

    def fallback(self, raw, *a, **k):
        return self.commands.fallback(raw)

    @expose
    def favicon_ico(self, *args, **kwargs):
        """favicon.ico file.  blobbunny made by julie zhuo :)"""
        cherrypy.response.headers['Content-Type'] = 'image/x-icon'
        return bunny1_file('favicon.ico')

    @expose
    def blobbunny_gif(self, *args, **kwargs):
        """blobbunny.gif logo, made by julie zhuo"""
        cherrypy.response.headers['Content-Type'] = 'image/gif'
        return bunny1_file('blobbunny.gif')

    def start(self, port=None, host=None, errorlogfile=None, accesslogfile=None):
        if port:
            cherrypy.server.socket_port = port
        if errorlogfile:
            cherrypy.config['log.error_file'] = errorlogfile
        if accesslogfile:
            cherrypy.config['log.access_file'] = accesslogfile
        if not host:
            from socket import gethostname
            cherrypy.server.socket_host = gethostname()
        return cherrypy.quickstart(self)


class Content(Exception):
    """raise when returning content instead of redirecting"""
    __module__ = __name__

    def __init__(self, html='', content_type='text/html'):
        self.content_type = content_type
        self.html = html


class HTML(Content):
    """raise when returning an HTML repsonse instead of redirecting"""
    __module__ = __name__

    def __init__(self, html=''):
        self.content_type = 'text/html'
        self.html = html


class PRE(HTML):
    """preformatted HTML"""
    __module__ = __name__

    def __init__(self, html):
        HTML.__init__(self, '<pre>%s</pre>' % html)


class ErrorMesage(Content):
    """raise when returning an error"""
    __module__ = __name__

    def __init__(self, error_message):
        Content.__init__(self)
        self.html = "<span style='color: red; font-family: Courier New, Courier, Fixed-width; font-weight: bold;'>%s</span>" % escape(error_message)


class Fallback(Exception):
    """raise when we want to go to the fallback"""
    __module__ = __name__


def dont_expose(fun):
    """decorator for methods that shouldn't be exposed to the web"""
    fun.dont_expose = True
    return fun


def preprocessor(fun):
    """decorator that defines a preprocessor"""

    def decorator(cmd):
        cmd.preprocessor = fun
        return cmd

    return decorator


def unlisted(fun):
    """decorator for methods that shouldn't be listed with list"""
    fun.unlisted = True
    return fun


def no_auth_required(fun):
    """decorator for methods that don't require auth"""
    fun.no_auth_required = True
    return fun


class Bunny1Commands(object):
    """the default commands used by bunny1"""
    __module__ = __name__

    def __init__(self):
        self.history = []
        self.fallback_url = YUBNUB_URL
        self.popularity = {}

    @dont_expose
    def _base_url(self):
        if hasattr(self, '_b1'):
            return self._b1.base_url
        else:
            return BUNNY1_HOME_URL

    @dont_expose
    def _opensearch_link(self):
        m = self._opensearch_metadata()
        return '<link rel="search" type="application/opensearchdescription+xml" title="%s" href="/?_opensearch" />' % m['short_name']

    @dont_expose
    def _help_html(self):
        return '<html><head><title>bunny1</title>' + self._opensearch_link() + "</head><body><form><input type='text' name='" + COMMAND_QUERY_STRING_VAR + "' value='list'><input type='submit' value='try me'></form><pre>" + escape(bunny1_file('README')) + '</pre></body></html>'

    def help(self, arg):
        """gets help with a specific command or shows the README for general help"""
        if arg:
            raise Content('<b>' + escape(arg) + '</b><br />' + str(getattr(self, arg).__doc__))
        else:
            raise Content(self._help_html())

    man = help

    def readme(self, arg):
        """shows the README for this tool"""
        raise Content(self._help_html())

    def _info(self, arg):
        """shows some info about this instance of bunny1"""
        raise Content('<code>' + repr({'_info': {'base_url': self._b1.base_url}, 'os_env': os.environ}) + '</code>')

    @dont_expose
    def history(self, arg):
        """show the history of queries made to this server"""
        html = '<pre><b>history</b>\n'
        for entry in self.history[:-50:-1]:
            html += '<a href="/?%(url)s">%(label)s</a>\n' % {'url': entry, 'label': entry}

        html += '</pre>'
        raise Content(html)

    h = history

    def popular(self, arg):
        """shows the most popular commands"""
        raise Content(self._popularity_html())

    @dont_expose
    def _popularity_html(self, num=None):
        p = self.popularity
        pairs = [ (val, key) for (key, val) in p.items() if key not in DONT_LIST_AS_POPULAR ]
        pairs.sort()
        pairs.reverse()
        html = '<b><i>'
        if num:
            html += '%d ' % num
        html += 'Most Popular Commands</i></b><br />'
        if num:
            pairs = pairs[:num]
        for (times, method) in pairs:
            m = getattr(self, method)
            doc = m.__doc__
            if not getattr(m, 'unlisted', False):
                if doc:
                    doc_str = ' (%s)' % escape(doc)
                else:
                    doc_str = ''
                html += '<b>%s</b> used %d times%s<br />\n' % (escape(method), times, doc_str)

        return html

    def list(self, arg):
        """show the list of methods you can use or search that list"""

        def is_exposed_method((name, method)):
            return not name.startswith('__') and callable(method) and method.__doc__ and not getattr(method, 'dont_expose', False) and not getattr(method, 'unlisted', False)

        arg_lower = None
        if arg:
            arg_lower = arg.lower()
            html = ''
            search_predicate = lambda (name, method): is_exposed_method((name, method)) and (arg_lower in name.lower() or arg_lower in method.__doc__)
        else:
            html = self._popularity_html(10) + '<hr ><b><i>All Commands</i></b><br />'
            search_predicate = is_exposed_method
        attr_names = dir(self)

        def attr_getter(name):
            return getattr(self, name)

        html += '<table>'
        html += ('').join([ '<tr><td><b>%s</b></td><td>%s</td></tr>' % (name, escape(method.__doc__)) for (name, method) in ifilter(search_predicate, izip(attr_names, imap(attr_getter, attr_names)))
                          ])
        html += '<table>'
        raise Content(html)
        return

    ls = list
    commands = list

    def echo(self, arg):
        """returns back what you give to it"""
        raise Content(escape(arg))

    def html(self, arg):
        """returns back the literal HTML you give it"""
        raise Content(arg)

    def g(self, arg):
        """does a google search.  we could fallback to yubnub, but why do an unnecessary roundtrip for something as common as a google search?"""
        return GOOGLE_SEARCH_URL + q(arg)

    @unlisted
    def _hostname(self, arg):
        """shows the hostname of this server"""
        import socket
        raise Content(socket.gethostname())

    def _cookies(self, arg):
        """show the cookies set on this server or search through them"""
        cookie = cherrypy.request.cookie
        html = ''
        for name in cookie.keys():
            val = cookie[name].value
            if not arg or arg in name or arg in val:
                html += '<b>%s</b><br />%s<br /><br />' % (escape(str(name)), escape(str(val)))

        raise Content(html)

    def alias(self, arg):
        """aliases one shortcut to another.  ex: alias p profile.  alias p will show what p is aliased to.  alias with no args will show all aliases."""
        words = arg.split()
        cookie = cherrypy.response.cookie
        try:
            alias = words[0]
            real = words[1]
            cookie['alias.' + alias] = real
            raise Content('aliased <b>%s</b> to <b>%s</b>' % (escape(alias), escape(real)))
        except IndexError:
            try:
                alias = words[0]
                try:
                    raise Content('<b>%s</b> is aliased to <b>%s</b>' % (escape(alias), escape(cherrypy.request.cookie[('alias.' + alias)].value)))
                except KeyError:
                    raise Content('<b>%s</b> is not aliased to anything.' % escape(arg))

            except IndexError:
                html = 'usage:<br />alias <i>alias</i> <i>real-command</i><br />or<br />alias <i>alias</i><br /><hr />'
                cookie = cherrypy.request.cookie
                for name in cookie.keys():
                    if str(name).startswith('alias.'):
                        html += '<b>%s</b> is aliased to <b>%s</b><br />' % (escape(name[6:]), escape(cookie[name].value))

                raise Content(html)

    def unalias(self, arg):
        """unaliases an alias.  ex: unalias p"""
        if not arg:
            raise Content('usage:<br />unalias <i>alias</i>')
        cherrypy.response.cookie['alias.' + arg] = ''
        cherrypy.response.cookie[('alias.' + arg)]['expires'] = 0
        raise Content('unaliased <b>%s</b>' % escape(arg))

    def _source(self, arg):
        """goes to the source code for bunny1 (this utility)"""
        return 'http://github.com/ccheever/bunny1/tree/master'

    def _test(self, arg):
        """tests a command on a different bunny1 host.  usage: _test [fully-qualified-bunny1-url] [command]"""
        (bunny1_url, arg) = arg.split(None, 1)
        if not bunny1_url.endswith('?'):
            bunny1_url += '?'
        save('bunny1testurl', bunny1_url)
        raise HTTPRedirect(bunny1_url + q(arg))
        return

    def _t(self, arg):
        """tests a command on the most recently used bunny1 host.  usage: _t [command]"""
        bunny1_url = load('bunny1testurl')
        raise HTTPRedirect(bunny1_url + q(arg))

    def url(self, arg):
        """goes to the URL that is specified"""
        if arg:
            if ':' not in arg:
                return 'http://%s' % arg
            else:
                return arg
        else:
            raise Content('no url specified')

    @dont_expose
    def _my_url(self):
        """the URL of this server"""
        if cherrypy.request.base:
            return cherrypy.request.base + cherrypy.request.path_info
        else:
            return self._my_home_url()

    @dont_expose
    def _my_home_url(self):
        """the configured URL of this server"""
        return BUNNY1_HOME_URL

    @dont_expose
    def _opensearch_metadata(self):
        """metadata about this server"""
        return {'short_name': 'bunny1', 'description': 'bunny1', 'template': self._my_url() + '?{searchTerms}'}

    def _opensearch(self, arg):
        """returns the OpenSearch description for this server"""
        m = self._opensearch_metadata()
        raise Content('<?xml version="1.0" encoding="UTF-8" ?>\n    <OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">\n    <ShortName>' + m['short_name'] + '</ShortName>\n    <Description>' + m['description'] + '</Description>\n    <InputEncoding>UTF-8</InputEncoding>\n    <Url type="text/html" template="' + escape(m['template']) + '" />\n  </OpenSearchDescription>\n  ', 'application/xml')

    def keywurl(self, arg):
        """goes to the Keywurl Safari extension homepage"""
        return 'http://purefiction.net/keywurl/'

    @dont_expose
    def fallback(self, raw):
        raise HTTPRedirect(self.fallback_url + q(raw))


class DoesNotExist(Exception):
    __module__ = __name__


def save(key, val):
    cherrypy.response.cookie[key] = val
    cherrypy.response.cookie[key]['path'] = '/'
    cherrypy.response.cookie[key]['max-age'] = 50 * 365 * 24 * 60 * 60


def load(key):
    return cherrypy.request.cookie[key].value


def bunny1_file(name):
    """the binary contents of a file in the same directory as bunny1"""
    return file(os.path.dirname(__file__) + os.path.sep + name).read()


class Bunny1OptionParser(optparse.OptionParser):
    """a class for getting bunny1 options"""
    __module__ = __name__

    def __init__(self):
        optparse.OptionParser.__init__(self)
        self.add_basic_options()

    def add_basic_options(self):
        """adds the basic bunny1 options to the parser"""
        self.add_option('--daemonize', '-d', dest='daemonize', action='store_true', help='run this as a daemon')
        self.add_option('--host', dest='host', help='host to run on (default is the result of socket.gethostname())')
        self.add_option('--port', '-p', dest='port', help='port to run on (default %s)' % DEFAULT_PORT)
        self.add_option('--pidfile', dest='pidfile', help='pidfile to write to')
        self.add_option('--errorlogfile', dest='errorlogfile', help='file to write error logs to (defaults to stdout)')
        self.add_option('--accesslogfile', dest='accesslogfile', help='file to write access logs to (defaults to stdout)')
        self.add_option('--test-command', '-t', dest='test_command', help='test some command at the command line')
        self.add_option('--base-url', '-u', dest='base_url', help='the base URL of the bunny1 server')


class PasswordProtectionCommands(object):
    """commands for password protection"""
    __module__ = __name__

    @no_auth_required
    def _setpasswd(self, arg):
        """sets the password for password protected instances of bunny1"""
        args = arg.split()
        passwd = args[0]
        if not arg:
            return
        if len(args) > 1:
            next = (' ').join(args[1:])
        else:
            next = None
        save('b1passwd', passwd)
        if next:
            return next
        raise Content('password set.')
        return


class PasswordProtectedBunny1(Bunny1):
    """a password protected instance of bunny1"""
    __module__ = __name__

    def auth(self):
        if self.server_mode() == ServerModes.COMMAND_LINE:
            return True
        try:
            password = cherrypy.request.cookie['b1passwd'].value
        except (AttributeError, KeyError), e:
            return False

        return password == self.password()

    def password(self):
        return 'xyzzy'


def main(b1, b1op=Bunny1OptionParser()):
    """uses command line options and runs the server given an instance of the Bunny1 class"""
    if os.environ.get('GATEWAY_INTERFACE', '').startswith('CGI'):
        main_cgi(b1)
    else:
        (options, args) = b1op.parse_args()
        if options.test_command is not None:
            try:
                b1._server_mode = 'COMMAND_LINE'
                print b1.do_command(options.test_command)
            except HTTPRedirect, redir:
                print '\x1b[33m%s:\x1b[0m %s' % (redir.__class__.__name__, redir)

        else:
            if options.port:
                port = int(options.port)
            else:
                port = DEFAULT_PORT
            if options.host:
                host = options.host
            else:
                host = socket.gethostname()
            if options.base_url:
                b1.base_url = options.base_url
            else:
                protocol = 'http'
                b1.base_url = '%s://%s:%s/' % (protocol, host, port)
            if options.daemonize:
                import daemonize
                daemonize.daemonize(options.pidfile)
            b1.start(port=port, host=options.host, errorlogfile=options.errorlogfile, accesslogfile=options.accesslogfile)
    return


def main_cgi(b1):
    """for running bunny1 as a cgi"""
    try:
        form = cgi.FieldStorage()
        cmd = form.getvalue(COMMAND_QUERY_STRING_VAR)
        if not cmd:
            try:
                cmd = urllib.unquote_plus(os.environ['QUERY_STRING'])
            except KeyError:
                cmd = DEFAULT_COMMAND

        response = b1.do_command(cmd)
        if cherrypy.response.headers['Content-type']:
            content_type = cherrypy.response.headers['Content-type']
        else:
            content_type = 'text/html'
        print 'Content-type: %s\n' % content_type
        print response
    except cherrypy.HTTPRedirect, redir:
        url = redir.urls[0]
        print 'Location: ' + url + '\n\n'


if __name__ == '__main__':
    main(Bunny1(Bunny1Commands(), Bunny1Decorators()))