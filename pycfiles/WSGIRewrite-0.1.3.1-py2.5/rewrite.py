# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-ppc/egg/wsgirewrite/rewrite.py
# Compiled at: 2007-08-10 09:18:23
"""
Implementation of a ``mod_rewrite`` compatible URL rewriter.

This WSGI middleware implements an URL rewriter that uses the same
syntax as the famous ``mod_rewrite`` module for Apache. Most of
``mod_rewrite`` features are supported, including redirecting with
a specific status code, proxying, conditional rules based on
environment variables and chained rules.

"""
import re, os.path
from datetime import datetime, timedelta
import urllib, urlparse
from paste import httpexceptions
from paste.proxy import Proxy
__author__ = 'Roberto De Almeida <roberto@dealmeida.net>'
__license__ = 'MIT'
__version__ = (0, 1, 3)

def make_filter(app, global_conf, rulesets=None, config=None):
    r"""
    Entry point for Paste Deploy.

    To create a WSGI filter middleware add the following line to
    the deployment file::

        [pipeline:main]
        pipeline = wsgirewrite myapp

        [filter:wsgirewrite]
        use = egg:WSGIRewrite
        config = /path/to/htaccess

        [app:myapp]
        ...

    Where ``config`` specifies a file with the rewriting rules
    following ``mod_rewrite``'s syntax::

        RewriteCond  %{HTTP_USER_AGENT}  ^Mozilla.*
        RewriteRule  ^/$                 /homepage.max.html  [L]

        RewriteCond  %{HTTP_USER_AGENT}  ^Lynx.*
        RewriteRule  ^/$                 /homepage.min.html  [L]

        RewriteRule  ^/$                 /homepage.std.html  [L]

    Optionally, you can also specify rules directly on the INI file
    using the ``rulesets`` variable::

        [filter:wsgirewrite]
        use = egg:WSGIRewrite
        rulesets = feed blocked

        [wsgirewrite:feed]
        # redirect /atom.xml to real feed location
        rule1 = ^/atom.xml$ /index.php?format=Atom1.0

        [wsgirewrite:blocked]
        # block host1.example.com and host2.example.com
        # this could be done by matching ``host(1|2)``; I'm
        # using these rules just to demonstrate the ``OR``
        # flag functionality.
        cond1 = %{REMOTE_HOST} ^host1\.example\.com$ [OR]
        cond2 = %{REMOTE_HOST} ^host2\.example\.com$
        # no redirection (-), Forbidden
        rule1 = ^.*$ - F

    In case both ``config`` and ``rulesets`` are specified, the
    latter are evaluated first.

    """
    rs = []
    if rulesets is not None:
        rs.extend(parse_ini(global_conf['__file__'], rulesets))
    if config is not None and os.path.exists(config):
        rs.extend(parse_htaccess(config))
    return RewriteMiddleware(app, rs)


def parse_ini(path, names):
    """
    Parse the deployment file.

    This function parses the deployment file, searching for sections
    that specify rulesets; these sections should have the name
    ``wsgirewrite:``, followed by the name of the ruleset. Eg::

        [wsgirewrite:blocked]
        cond1 = %{REMOTE_HOST} !^.*example.com$
        rule1 = ^.*$ - F

    The ruleset aboved is called "blocked", and will be applied if
    it is in the parameter ``names``. Condition and rules are sorted
    by their names, which should start with ``cond`` and ``rule``,
    respectively.

    """
    from ConfigParser import ConfigParser
    config = ConfigParser()
    config.read(path)
    names = names.split()
    sections = [ section for section in config.sections() if section.startswith('wsgirewrite:') if section.split(':')[1] in names
               ]
    rulesets = []
    for section in sections:
        conditions = []
        directives = []
        conds = [ option for option in config.options(section) if option.startswith('cond')
                ]
        conds.sort()
        rules = [ option for option in config.options(section) if option.startswith('rule')
                ]
        rules.sort()
        for cond in conds:
            line = config.get(section, cond)
            conditions.append(parse_line(line))

        for rule in rules:
            line = config.get(section, rule)
            directives.append(parse_line(line))

        rulesets.append((conditions, directives))

    return rulesets


def parse_htaccess(path):
    """
    Parse configuration from a ``.htaccess`` like file.

    This function parses the configuration from a file specifying
    the rulesets using ``mod_rewrite``'s syntax.

    """
    config = open(path)
    rulesets = []
    conds = []
    directives = []
    state = 0
    for line in config:
        line = line.strip()
        if line.startswith('RewriteCond') or not line:
            if state == 2:
                rulesets.append((conds, directives))
                conds = []
                directives = []
            state = 1
            if line:
                line = line[11:]
                conds.append(parse_line(line))
        elif line.startswith('RewriteRule'):
            state = 2
            line = line[11:]
            directives.append(parse_line(line))

    rulesets.append((conds, directives))
    return rulesets


def parse_line(line):
    """
    Parse a configuration line into tokens.

    This function converts a line to the necessary tokens::

        >>> parse_line("^/$  /homepage.max.html  [L]")
        ('^/$', '/homepage.max.html', ['L'])
        >>> parse_line("^/$  /homepage.max.html")
        ('^/$', '/homepage.max.html', [])

    """
    tokens = re.split('\\s+', line.strip())
    if len(tokens) < 2:
        raise Exception('Bogus line: %s' % line)
    if len(tokens) == 2:
        tokens.append([])
    else:
        tokens[2] = tokens[2][1:-1].split(',')
    return tuple(tokens)


class RewriteMiddleware(object):
    """
    WSGI middleware for rewriting URLs.

    This middleware rewrites URLs according to Apache's ``mod_rewrite``
    syntax. To redirect the user from page ``/page.html`` to
    ``new_page.html`` just give it the following ruleset::

        >>> app = RewriteMiddleware(some_app, [
        ...     ([], # conditions (none, in this case)
        ...      [   # rules
        ...          ("^/page.html$", "/new_page.html", []),
        ...      ]
        ...     )
        ... ])

    """

    def __init__(self, app, rulesets):
        """
        Create the middleware.

        To instantiate the middleware, pass a WSGI app ``app`` to
        be filtered, and a group of rulesets. The parameter
        ``rulesets`` should be a list of tuples, each tuple consisting
        of a list of conditions and a list of directives (rewrites)
        to be applied.

        """
        self.app = app
        self.rulesets = rulesets

    def __call__(self, environ, start_response):
        """
        Process the request.

        The middleware follows the algorithm used by ``mod_rewrite``,
        where first the path is checked and, in case of a match,
        the conditions are checked to see if the replacement should
        be done.

        This method will return either the original app with
        ``PATH_INFO`` modified (and possibly ``QUERY_STRING``), a
        Proxy object proxying a request to another location, or an
        ``httpexception`` middleware for redirects or Forbidden/Gone
        pages.

        """
        environ = update_environ(environ)
        additional_headers = []

        def new_start_response(status, headers, exc_info=None):
            """Modified start response with additional headers."""
            headers = headers + additional_headers
            start_response(status, headers, exc_info)

        for (conds, directives) in self.rulesets:
            cskip = False
            nskip = 0
            for (pattern, repl, flags) in directives:
                path_info = environ['PATH_INFO']
                if nskip > 0:
                    nskip -= 1
                    continue
                if cskip:
                    if 'C' not in flags:
                        if 'chain' not in flags:
                            cskip = False
                        continue
                    internal = path_info in environ.get('paste.recursive.old_path_info', [])
                    environ['IS_SUBREQ'] = ['false', 'true'][internal]
                    if internal and 'nosubreq' in flags or 'NS' in flags:
                        continue
                    if pattern.startswith('!'):
                        pattern = pattern[1:]
                        invert = True
                    else:
                        invert = False
                    if 'NC' in flags or 'nocase' in flags:
                        pattern = re.compile(pattern, re.IGNORECASE)
                    else:
                        pattern = re.compile(pattern)
                    match = pattern.search(path_info)
                    if invert:
                        match = not match
                elif match:
                    path_pattern = hasattr(match, 'groups') and match.groups() or ()
                    cond_pattern = self.check(conds, environ, path_pattern)
                    if cond_pattern is False:
                        continue
                    cookies = [ flag for flag in flags if flag.startswith('CO') or flag.startswith('cookie')
                              ]
                    for cookie in cookies:
                        additional_headers.append(cookie_header(cookie))

                    envs = [ flag for flag in flags if flag.startswith('E') or flag.startswith('env')
                           ]
                    for env in envs:
                        m = re.match('(?:E|env)=(.*)', env)
                        (k, v) = m.group(1).split(':', 1)
                        v = re.sub('(?<!\\\\)\\$(\\d)', lambda m: path_pattern[(int(m.group(1)) - 1)], v)
                        v = v.replace('\\$', '$')
                        v = re.sub('(?<!\\\\)%(\\d)', lambda m: cond_pattern[(int(m.group(1)) - 1)], v)
                        v = v.replace('\\%', '%')
                        environ.setdefault(k, v)

                    mimes = [ flag for flag in flags if flag.startswith('T') or flag.startswith('type')
                            ]
                    if mimes:
                        mime = re.match('(?:T|type)=(.*)', mimes[(-1)]).group(1)
                        h = ('Content-type', mime)
                        additional_headers.append(h)
                    if 'F' in flags or 'forbidden' in flags:
                        e = httpexceptions.HTTPForbidden()
                        return e.wsgi_application(environ, new_start_response)
                    if 'G' in flags or 'gone' in flags:
                        e = httpexceptions.HTTPGone()
                        return e.wsgi_application(environ, new_start_response)
                    new_path_info = pattern.sub(repl, path_info)
                    new_path_info = re.sub('(?<!\\\\)\\$(\\d)', lambda m: path_pattern[(int(m.group(1)) - 1)], new_path_info)
                    new_path_info = re.sub('(?<!\\\\)%(\\d)', lambda m: cond_pattern[(int(m.group(1)) - 1)], new_path_info)
                    new_path_info = new_path_info.replace('\\%', '%')
                    if 'noescape' in flags or 'NE' in flags:
                        new_path_info = urllib.unquote(new_path_info)
                    old_qs = environ.get('QUERY_STRING', '')
                    new_qs = urlparse.urlsplit(new_path_info)[3]
                    new_path_info = new_path_info.split('?', 1)[0]
                    if 'QSA' in flags or 'qsappend' in flags:
                        if old_qs:
                            new_qs = old_qs + '&' + new_qs
                    environ['QUERY_STRING'] = new_qs
                    if 'P' in flags or 'proxy' in flags:
                        proxy = Proxy(new_path_info)
                        return proxy(environ, new_start_response)
                    redir = [ flag for flag in flags if flag.startswith('R') or flag.startswith('redirect')
                            ]
                    if redir:
                        status = re.match('(?:R|redirect)(?:=(\\d+))?', redir[(-1)]).group(1) or '302'
                        exception = status_code_to_exception(status)
                        if environ['QUERY_STRING']:
                            new_path_info = '%s?%s' % (new_path_info, environ['QUERY_STRING'])
                        e = exception(new_path_info)
                        return e.wsgi_application(environ, new_start_response)
                    if repl != '-':
                        environ['PATH_INFO'] = new_path_info
                    if 'N' in flags or 'next' in flags:
                        return self(environ, new_start_response)
                    skip = [ flag for flag in flags if flag.startswith('S') or flag.startswith('skip')
                           ]
                    if skip:
                        nskip = int(re.match('(?:S|skip)=(\\d+)', skip[(-1)]).group(1))
                    if 'L' in flags or 'last' in flags:
                        break
                elif 'C' in flags or 'chain' in flags:
                    cskip = True

        return self.app(environ, new_start_response)

    def check(self, conds, environ, path_pattern):
        """
        Check if conditions apply.

        This method checks the conditions in the rulesets to see
        if the replacement should be performed. The conditions take
        the form::

            TestString CondPattern [optional-flags]

        And usually expand variables from the environment for the
        checks. Not all forms of expansion from ``mod_rewrite`` are
        supported, though.

        """
        out = True
        skip = False
        for (string, pattern, flags) in conds:
            if skip:
                if 'OR' not in flags:
                    skip = False
                continue
            string = re.sub('(?<!\\\\)%{(.*?)}', lambda m: environ.get(m.group(1), ''), string)
            string = string.replace('\\%', '%')
            string = re.sub('(?<!\\\\)\\$(\\d)', lambda m: path_pattern[(int(m.group(1)) - 1)], string)
            string = string.replace('\\$', '$')
            if pattern.startswith('!'):
                pattern = pattern[1:]
                invert = True
            else:
                invert = False
            if pattern.startswith('>'):
                m = string > pattern[1:]
            elif pattern.startswith('<'):
                m = string < pattern[1:]
            elif pattern.startswith('='):
                m = string == pattern[1:]
            elif 'NC' in flags:
                m = re.search(pattern, string, re.IGNORECASE)
            else:
                m = re.search(pattern, string)
            if invert:
                m = not m
            if not m:
                if 'OR' not in flags:
                    return False
                else:
                    out = False
            elif m:
                out = hasattr(m, 'groups') and m.groups() or ()
                if 'OR' in flags:
                    skip = True

        return out


def update_environ(environ):
    """
    Update environ with ``mod_rewrite`` specific values.

    """
    environ.setdefault('PATH_INFO', '/')
    now = datetime.now()
    environ['TIME_YEAR'] = now.year
    environ['TIME_MON'] = now.month
    environ['TIME_DAY'] = now.day
    environ['TIME_HOUR'] = now.hour
    environ['TIME_MIN'] = now.minute
    environ['TIME_SEC'] = now.second
    environ['TIME_WDAY'] = now.weekday()
    environ['TIME'] = now.strftime('%Y%m%d%H%M%S')
    environ['API_VERSION'] = ('.').join((str(_) for _ in __version__))
    environ['THE_REQUEST'] = '%s %s%s %s' % (
     environ['REQUEST_METHOD'],
     environ.get('SCRIPT_PATH', ''),
     environ['PATH_INFO'],
     environ['SERVER_PROTOCOL'])
    environ['REQUEST_URI'] = '%s%s' % (
     environ.get('SCRIPT_PATH', ''),
     environ['PATH_INFO'])
    environ['REQUEST_FILENAME'] = environ['SCRIPT_FILENAME'] = 'Not supported'
    environ['HTTPS'] = ['off', 'on'][(environ['wsgi.url_scheme'] == 'https')]
    return environ


def status_code_to_exception(status):
    """
    Retrieve an ``httpexceptions`` app from a given status code.

    """
    exception = {'300': httpexceptions.HTTPMultipleChoices, '301': httpexceptions.HTTPMovedPermanently, 
       'permanent': httpexceptions.HTTPMovedPermanently, 
       '302': httpexceptions.HTTPFound, 
       'temp': httpexceptions.HTTPFound, 
       '303': httpexceptions.HTTPSeeOther, 
       'seeother': httpexceptions.HTTPSeeOther, 
       '304': httpexceptions.HTTPNotModified, 
       '305': httpexceptions.HTTPUseProxy, 
       '307': httpexceptions.HTTPTemporaryRedirect}[status]
    return exception


def cookie_header(cookie):
    """
    Build a cookie header from the ``CO|cookie`` flag.

    """
    m = re.match('(?:CO|cookie)=(.*)', cookie)
    c = m.group(1).split(':')
    if len(c) >= 4:
        expires = datetime.utcnow() + timedelta(minutes=int(c[3]))
        c[3] = expires.strftime('%a, %d-%b-%Y %H:%M:%S GMT')
    k = [
     c[0], 'domain', 'expires', 'path']
    v = c[1:]
    h = ('Set-Cookie', ('; ').join(('%s=%s' % pair for pair in zip(k, v))))
    return h