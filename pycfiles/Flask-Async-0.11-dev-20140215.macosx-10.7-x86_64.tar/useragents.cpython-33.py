# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mrdon/dev/flask-async/venv/lib/python3.3/site-packages/werkzeug/useragents.py
# Compiled at: 2014-01-20 15:46:16
# Size of source mod 2**32: 5300 bytes
"""
    werkzeug.useragents
    ~~~~~~~~~~~~~~~~~~~

    This module provides a helper to inspect user agent strings.  This module
    is far from complete but should work for most of the currently available
    browsers.

    :copyright: (c) 2013 by the Werkzeug Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
import re

class UserAgentParser(object):
    __doc__ = 'A simple user agent parser.  Used by the `UserAgent`.'
    platforms = (('iphone|ios', 'iphone'), ('ipad', 'ipad'), ('darwin|mac|os\\s*x', 'macos'),
                 ('win', 'windows'), ('android', 'android'), ('x11|lin(\\b|ux)?', 'linux'),
                 ('(sun|i86)os', 'solaris'), ('nintendo\\s+wii', 'wii'), ('irix', 'irix'),
                 ('hp-?ux', 'hpux'), ('aix', 'aix'), ('sco|unix_sv', 'sco'), ('bsd', 'bsd'),
                 ('amiga', 'amiga'), ('blackberry|playbook', 'blackberry'))
    browsers = (('googlebot', 'google'), ('msnbot', 'msn'), ('yahoo', 'yahoo'), ('ask jeeves', 'ask'),
                ('aol|america\\s+online\\s+browser', 'aol'), ('opera', 'opera'),
                ('chrome', 'chrome'), ('firefox|firebird|phoenix|iceweasel', 'firefox'),
                ('galeon', 'galeon'), ('safari', 'safari'), ('webkit', 'webkit'),
                ('camino', 'camino'), ('konqueror', 'konqueror'), ('k-meleon', 'kmeleon'),
                ('netscape', 'netscape'), ('msie|microsoft\\s+internet\\s+explorer', 'msie'),
                ('lynx', 'lynx'), ('links', 'links'), ('seamonkey|mozilla', 'seamonkey'))
    _browser_version_re = '(?:%s)[/\\sa-z(]*(\\d+[.\\da-z]+)?(?i)'
    _language_re = re.compile('(?:;\\s*|\\s+)(\\b\\w{2}\\b(?:-\\b\\w{2}\\b)?)\\s*;|(?:\\(|\\[|;)\\s*(\\b\\w{2}\\b(?:-\\b\\w{2}\\b)?)\\s*(?:\\]|\\)|;)')

    def __init__(self):
        self.platforms = [(b, re.compile(a, re.I)) for a, b in self.platforms]
        self.browsers = [(b, re.compile(self._browser_version_re % a)) for a, b in self.browsers]

    def __call__(self, user_agent):
        for platform, regex in self.platforms:
            match = regex.search(user_agent)
            if match is not None:
                break
        else:
            platform = None

        for browser, regex in self.browsers:
            match = regex.search(user_agent)
            if match is not None:
                version = match.group(1)
                break
        else:
            browser = version = None

        match = self._language_re.search(user_agent)
        if match is not None:
            language = match.group(1) or match.group(2)
        else:
            language = None
        return (
         platform, browser, version, language)


class UserAgent(object):
    __doc__ = 'Represents a user agent.  Pass it a WSGI environment or a user agent\n    string and you can inspect some of the details from the user agent\n    string via the attributes.  The following attributes exist:\n\n    .. attribute:: string\n\n       the raw user agent string\n\n    .. attribute:: platform\n\n       the browser platform.  The following platforms are currently\n       recognized:\n\n       -   `aix`\n       -   `amiga`\n       -   `android`\n       -   `bsd`\n       -   `hpux`\n       -   `iphone`\n       -   `ipad`\n       -   `irix`\n       -   `linux`\n       -   `macos`\n       -   `sco`\n       -   `solaris`\n       -   `wii`\n       -   `windows`\n\n    .. attribute:: browser\n\n        the name of the browser.  The following browsers are currently\n        recognized:\n\n        -   `aol` *\n        -   `ask` *\n        -   `camino`\n        -   `chrome`\n        -   `firefox`\n        -   `galeon`\n        -   `google` *\n        -   `kmeleon`\n        -   `konqueror`\n        -   `links`\n        -   `lynx`\n        -   `msie`\n        -   `msn`\n        -   `netscape`\n        -   `opera`\n        -   `safari`\n        -   `seamonkey`\n        -   `webkit`\n        -   `yahoo` *\n\n        (Browsers maked with a star (``*``) are crawlers.)\n\n    .. attribute:: version\n\n        the version of the browser\n\n    .. attribute:: language\n\n        the language of the browser\n    '
    _parser = UserAgentParser()

    def __init__(self, environ_or_string):
        if isinstance(environ_or_string, dict):
            environ_or_string = environ_or_string.get('HTTP_USER_AGENT', '')
        self.string = environ_or_string
        self.platform, self.browser, self.version, self.language = self._parser(environ_or_string)

    def to_header(self):
        return self.string

    def __str__(self):
        return self.string

    def __nonzero__(self):
        return bool(self.browser)

    __bool__ = __nonzero__

    def __repr__(self):
        return '<%s %r/%s>' % (
         self.__class__.__name__,
         self.browser,
         self.version)


from werkzeug.wrappers import UserAgentMixin