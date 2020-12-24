# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tags/cookie.py
# Compiled at: 2015-09-01 07:17:44
from __future__ import unicode_literals
from ..elements import Attribute
from ..elements.elementbase import LogicElement
from ..context.expressiontime import to_seconds

class CookieJar(dict):
    """A container for cookies"""

    def __init__(self, *args, **kwargs):
        self.deleted_cookies = set()
        super(CookieJar, self).__init__(*args, **kwargs)

    def __moyaconsole__(self, console):
        console.text(b'These are pending cookies that Moya will send with the response')
        from ..console import Cell
        table = [
         [Cell(b'name'),
          Cell(b'value'),
          Cell(b'path'),
          Cell(b'domain'),
          Cell(b'secure?')]]
        for cookie in self.itervalues():
            if isinstance(cookie, Cookie):
                table += [cookie.name,
                 cookie.value,
                 cookie.path,
                 cookie.domain,
                 b'Y' if cookie.secure else b'N']

        console.table(table)

    def __delitem__(self, key):
        self.deleted_cookies.add(key)
        super(self, b'__delitem__')(key)


class Cookie(object):
    """Stores incoming cookies"""

    def __init__(self, name, value, max_age, path, domain, secure, httponly, comment, overwrite):
        self.name = name
        self.value = value
        self.max_age = max_age
        self.path = path
        self.domain = domain
        self.secure = secure
        self.httponly = httponly
        self.comment = comment
        self.overwrite = overwrite

    def __repr__(self):
        return (b'<cookie {} {!r}>').format(self.name, self.value)

    def set(self, response):
        response.set_cookie(self.name, self.value, max_age=self.max_age, path=self.path, domain=self.domain, secure=self.secure, httponly=self.httponly, comment=self.comment, overwrite=self.overwrite)


class SetCookie(LogicElement):
    """Set a new cookie."""

    class Help:
        synopsis = b'set a cookie'
        example = b'\n            <set-cookie name="session" value="${session.key}" overwrite="yes" />\n        '

    name = Attribute(b'Cookie name')
    value = Attribute(b'Value', required=True)
    maxage = Attribute(b'Max age of cookie (in seconds or as timespan)', metavar=b'AGE', type=b'timespan', required=False, example=b'60m')
    path = Attribute(b'Path', required=False, default=b'/', metavar=b'PATH')
    domain = Attribute(b'Domain', required=False, default=None, metavar=b'DOMAIN')
    secure = Attribute(b'Secure', type=b'boolean', default=False)
    httponly = Attribute(b'HTTP Only?', type=b'boolean', required=False, default=False)
    comment = Attribute(b'Comment', required=False, default=None)
    overwrite = Attribute(b'Overwrite?', required=False, default=False)

    def logic(self, context):
        params = self.get_parameters(context)
        cookie = Cookie(params.name, params.value, to_seconds(params.maxage), params.path, params.domain, params.secure, params.httponly, params.comment, params.overwrite)
        context.root[b'cookiejar'][params.name] = cookie


class DeleteCookie(LogicElement):
    """Delete a previously set cookie."""

    class Help:
        synopsis = b'delete a cookie'
        example = b'\n            <delete-cookie name="authsession" />\n        '

    name = Attribute(b'Cookie name')

    def logic(self, context):
        try:
            context.root[b'cookiejar'][self.name(context)]
        except KeyError:
            pass