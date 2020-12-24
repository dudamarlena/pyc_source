# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.5/site-packages/pyjamas/Cookies.py
# Compiled at: 2008-09-03 09:02:13
from Cookie import SimpleCookie
from pyjamas.__pyjamas__ import doc
import urllib, datetime
from string import strip

def getCookie(key):
    return getCookie2(key)
    JS('\n    var cookies = Cookies_loadCookies();\n    var value = cookies[key];\n    return (value == null) ? null : value;\n    ')


def getCookie2(cookie_name):
    cookiestr = doc().props.cookie
    c = SimpleCookie(cookiestr)
    cs = c.get(cookie_name, None)
    print 'getCookie2', cookiestr, 'name', cookie_name, 'val', cs
    if cs:
        return cs.value
    return None
    JS("\n    var results = document.cookie.match ( '(^|;) ?' + cookie_name + '=([^;]*)(;|$)' );\n\n    if ( results )\n        return ( decodeURIComponent ( results[2] ) );\n    else\n        return null;\n\n    ")


def setCookie(name, value, expires, domain=None, path=None, secure=False):
    cookiestr = doc().props.cookie
    c = SimpleCookie(cookiestr)
    c[name] = value
    m = c[name]
    d = datetime.datetime.now() + datetime.timedelta(0, expires / 1000)
    d = d.strftime('%a, %d %b %Y %H:%M:%S GMT')
    m['expires'] = '"%s"' % d
    if domain:
        m['domain'] = domain
    if path:
        m['path'] = path
    if secure:
        m['secure'] = ''
    c = c.output(header='').strip()
    print 'set cookies', c
    doc().props.cookie = c
    return
    JS("\n    if (expires instanceof Date) expires = expires.getTime();\n    if (pyjslib_isUndefined(domain)) domain = null;\n    if (pyjslib_isUndefined(path)) path = null;\n    if (pyjslib_isUndefined(secure)) secure = false;\n    \n    var today = new Date();\n    var expiration = new Date();\n    expiration.setTime(today.getTime() + expires)\n\n    var c = encodeURIComponent(name) + '=' + encodeURIComponent(value);\n    c += ';expires=' + expiration.toGMTString();\n\n    if (domain)\n        c += ';domain=' + domain;\n    if (path)\n        c += ';path=' + path;\n    if (secure)\n        c += ';secure';\n\n    $doc.cookie = c;\n    ")


def get_crumbs():
    docCookie = doc().props.cookie
    c = SimpleCookie(docCookie)
    c = c.output(header='')
    return map(strip, c.split('\n'))


def loadCookies():
    JS("\n    var cookies = {};\n\n    var docCookie = $doc.cookie;\n\n    if (docCookie && docCookie != '') {\n        var crumbs = docCookie.split(';');\n        for (var i = 0; i < crumbs.length; ++i) {\n            alert(crumbs.length);\n            var name, value;\n\n            var eqIdx = crumbs[i].indexOf('=');\n            if (eqIdx == -1) {\n                name = crumbs[i];\n                value = '';\n            } else {\n                name = crumbs[i].substring(0, eqIdx);\n                value = crumbs[i].substring(eqIdx + 1);\n            }\n\n            alert(name);\n            alert(value);\n\n        cookies[decodeURIComponent(name)] = decodeURIComponent(value);\n        }\n    }\n\n    return cookies;\n    ")