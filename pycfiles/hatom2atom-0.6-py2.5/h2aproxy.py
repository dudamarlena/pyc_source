# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hatom2atom/h2aproxy.py
# Compiled at: 2008-12-18 22:31:30
"""h2aproxy - WSGI app proxy for hAtom2Atom.xsl transformations.

this file is part of the hatom2atom package.

created and maintained by luke arno <luke.arno@gmail.com>

copyright (c) 2006  Luke Arno  <luke.arno@gmail.com>

this program is free software; you can redistribute it and/or
modify it under the terms of the gnu general public license
as published by the free software foundation; either version 2
of the license, or (at your option) any later version.

this program is distributed in the hope that it will be useful,
but without any warranty; without even the implied warranty of
merchantability or fitness for a particular purpose.  see the
gnu general public license for more details.

you should have received a copy of the gnu general public license
along with this program; if not, write to:

the free software foundation, inc., 
51 franklin street, fifth floor, 
boston, ma  02110-1301, usa.

luke arno can be found at http://lukearno.com/
"""
from cgi import parse_qs
import urllib2
from kid import Template
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
from hatom2atom import settings, util

def h2a_proxy(environ, start_response):
    """WSGI app to proxy hAtom2Atom transformations of any URL."""
    messages = []
    response_status = '200 OK'
    qs = parse_qs(environ['QUERY_STRING'])
    url = qs.get('url', [''])[0]
    tidyme = qs.get('tidy', ['yes'])[0].lower()
    ctype = qs.get('ctype', [settings.default_ctype])[0]
    if url:
        try:
            f = util.url_opener(environ).open(url)
            url = f.geturl()
            response_text = f.read()
            try:
                if tidyme:
                    soup = BeautifulSoup(response_text, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
                    soup.html['xmlns'] = 'http://www.w3.org/1999/xhtml'
                    response_text = str(soup.prettify()).split('\n', 1)[1]
                file('/tmp/foo.xml', 'w').write(response_text)
                atom = util.easy_transform(settings.stylesheet, response_text, {'source-uri': "'%s'" % url})
                start_response(response_status, [
                 (
                  'Content-Type',
                  '%s; charset=utf-8' % ctype)])
                return [atom]
            except Exception, e:
                response_status = '502 Bad Gateway'
                messages.append(str(e))

        except Exception, e:
            response_status = '500 Internal Server Error'
            messages.append(str(e))

    start_response(response_status, [('Content-Type', 'text/html')])
    t = Template(file=settings.kid_template, url=url, messages=messages, settings=settings)
    return t.generate()


def run(host='', port=9000):
    """Run the proxy on wsgiref."""
    from wsgiref.simple_server import make_server
    try:
        make_server(host, port, h2a_proxy).serve_forever()
    except KeyboardInterrupt, ki:
        print 'Peace out!'


def cmd():
    import sys
    run(sys.argv[1], int(sys.argv[2]))


if __name__ == '__main__':
    cmd()