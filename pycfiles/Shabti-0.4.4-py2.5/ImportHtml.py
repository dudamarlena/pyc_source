# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/shabti/templates/moinmoin/data/moin/data/plugin/action/ImportHtml.py
# Compiled at: 2010-04-25 14:23:30
"""
    MoinMoin - ImportHtml action

"""
import mimetypes, string, sys, time, HTMLParser
from MoinMoin import config, user, util, wikiutil
from MoinMoin.util import web
from MoinMoin.Page import Page
from MoinMoin.PageEditor import PageEditor

def show_form(pagename, request):
    request.write('\n<form action="%(baseurl)s/%(pagename)s" method="POST" enctype="multipart/form-d\x07ta">\n<input type="hidden" name="action" value="ImportHtml">\n<input type="radio" name="do" value="markup">Show markup<br>\n<input type="radio" name="do" value="wiki">Show as wiki page<br>\n<input type="radio" name="do" value="import">Append to page<br>\nURL: <input type="text" name="url" size="50">\n<input type="submit" value="Get">\n</form>\n' % {'baseurl': request.getBaseURL(), 
       'pagename': wikiutil.quoteWikinameURL(pagename)})


def get_content(request):
    if request.form.has_key('url'):
        try:
            return urllib.urlopen(request.form['url'][0]).read()
        except IOError:
            return ''

    else:
        return ''


def get_parsed(request):
    from MoinMoin.converter.text_html_text_moin_wiki import convert
    return convert(request, 'Imported Page', get_content(request))


def show_markup(pagename, request):
    request.http_headers(['Content-type: text/plain'])
    request.write(get_parsed(request))


def show_as_wiki_page(pagename, request):
    page = Page(pagename)
    page.set_raw_body(get_parsed(request), 1)
    page.send_page(request)


def append_to_page(pagename, request):
    page = PageEditor(request, pagename)
    page.set_raw_body(page.get_raw_body() + get_parsed(request))
    page.sendEditor()


def error_msg(pagename, request, msg):
    Page(pagename).send_page(request, msg=msg)


def execute(pagename, request):
    """ Main dispatcher for the 'ImportHtml' action.
    """
    _ = request.getText
    msg = None
    if not request.form.has_key('do'):
        show_form(pagename, request)
    elif request.form['do'][0] == 'markup':
        show_markup(pagename, request)
    elif request.form['do'][0] == 'wiki':
        show_as_wiki_page(pagename, request)
    elif request.form['do'][0] == 'import':
        append_to_page(pagename, request)
    else:
        msg = _('<b>Unsupported action: %s</b>') % (request.form['do'][0],)
    if msg:
        error_msg(pagename, request, msg)
    return