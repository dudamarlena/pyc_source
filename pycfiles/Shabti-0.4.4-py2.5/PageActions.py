# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/shabti/templates/moinmoin/data/moin/data/plugin/action/PageActions.py
# Compiled at: 2009-12-05 12:37:18
import re
from MoinMoin import config, wikiutil
from MoinMoin.Page import Page
from MoinMoin import version

def execute(pagename, request):
    _ = request.getText
    from MoinMoin.formatter.text_html import Formatter
    request.formatter = Formatter(request)
    try:
        request.emit_http_headers()
    except AttributeError:
        try:
            request.http_headers()
        except AttributeError:
            pass

    request.setContentLanguage(request.lang)
    try:
        send_title = request.theme.send_title
        send_title(_('Actions for %s') % pagename, page_name=pagename)
    except AttributeError:
        wikiutil.send_title(request, _('Actions for %s') % pagename, pagename=pagename)

    request.write(request.formatter.startContent('content'))
    request.write(availableactions(request))
    request.write(request.formatter.endContent())
    try:
        request.theme.send_footer(pagename)
    except AttributeError:
        wikiutil.send_footer(request, pagename)


def actionlink(request, action, title, comment=''):
    page = request.page
    _ = request.getText
    title = Page(request, title).split_title(request)
    title = _(title, formatted=False)
    params = '%s?action=%s' % (page.page_name, action)
    if action == 'RenamePage':
        params += '&subpages_checked=1'
    link = wikiutil.link_tag(request, params, _(title))
    return ('').join(['<li>', link, comment, '</li>'])


def availableactions(request):
    page = request.page
    _ = request.getText
    html = ''
    links = []
    try:
        available = request.getAvailableActions(page)
    except AttributeError:
        from MoinMoin.action import get_available_actions
        available = get_available_actions(request.cfg, page, request.user)

    for action in available:
        links.append(actionlink(request, action, action))

    if page.isWritable() and request.user.may.write(page.page_name):
        links.append(actionlink(request, 'edit', 'EditText'))
    if request.user.valid and request.user.email:
        action = ('Subscribe', 'Unsubscribe')[request.user.isSubscribedTo([page.page_name])]
        links.append(actionlink(request, 'subscribe', action))
    if request.user.valid:
        links.append(actionlink(request, 'userform&logout=logout', 'Logout'))
    links.append(actionlink(request, 'print', 'PrintView'))
    links.append(actionlink(request, 'raw', 'ViewRawText'))
    links.append(actionlink(request, 'refresh', 'DeleteCache'))
    html = '<ul>%s</ul>' % ('').join(links)
    return html