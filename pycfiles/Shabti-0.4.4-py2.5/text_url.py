# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/shabti/templates/moinmoin/data/moin/data/plugin/formatter/text_url.py
# Compiled at: 2010-04-25 12:11:22
"""
    text_url formatter plugin to MoinMoin
     - Special formatting for URL:s

    @copyright: 2006 by Juhani Eronen <exec@iki.fi>
    @license: MIT <http://www.opensource.org/licenses/mit-license.php>

    Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation
    files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use, copy,
    modify, merge, publish, distribute, sublicense, and/or sell copies
    of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.

"""
from urllib import unquote as url_unquote
from MoinMoin.formatter.base import FormatterBase
from MoinMoin import wikiutil, i18n, config
from MoinMoin.Page import Page

class Formatter(FormatterBase):
    """
    Get url values, and nothing else
    """

    def __init__(self, request, **kw):
        apply(FormatterBase.__init__, (self, request), kw)

    def null(self, *args, **kw):
        return ''

    def null_list(self, *args, **kw):
        return [
         '']

    image = null_list
    set_highlight_re = null
    url = null
    smiley = null
    text = null
    strong = null
    emphasis = null
    underline = null
    highlight = null
    sup = null
    sub = null
    code = null
    preformatted = null
    small = null
    big = null
    code_area = null
    code_line = null
    code_token = null
    linebreak = null
    paragraph = null
    rule = null
    icon = null
    number_list = null
    bullet_list = null
    listitem = null
    definition_list = null
    definition_term = null
    definition_desc = null
    heading = null
    table = null
    table_row = null
    table_cell = null
    open = null
    close = null
    formatAttributes = null

    def text(self, text):
        return [
         text]

    def url(self, on, url=None, css=None, **kw):
        if url is not None and on:
            if url[0][0] == '#':
                url = '.' + self.request.request_uri.split('?')[0] + url
                kw['local'] = wikiutil.quoteWikinameURL(self.page.page_name)
            esc_url = wikiutil.mapURL(self.request, url)
            if kw.has_key('local'):
                if not isinstance(esc_url, unicode):
                    esc_url = unicode(url_unquote(esc_url), config.charset).replace('_', ' ')
                return [
                 esc_url, kw['local']]
            else:
                return [
                 esc_url]
        return []

    def pagelink(self, on, pagename='', page=None, **kw):
        """ Link to a page.

            formatter.text_python will use an optimized call with a page!=None
            parameter. DO NOT USE THIS YOURSELF OR IT WILL BREAK.

            See wikiutil.link_tag() for possible keyword parameters.
        """
        if not on:
            return []
        apply(FormatterBase.pagelink, (self, on, pagename, page), kw)
        if page is None:
            page = Page(self.request, pagename, formatter=self)
        kw['local'] = pagename
        if self.request.user.show_nonexist_qm and not page.exists():
            return page.link_to(self.request, on=1, **kw) + '?'
        else:
            return page.link_to(self.request, on=on, **kw)
        return

    def interwikilink(self, on, interwiki='', pagename='', **kw):
        if not on:
            return []
        (wikitag, wikiurl, wikitail, wikitag_bad) = wikiutil.resolve_wiki(self.request, '%s:%s' % (interwiki, pagename))
        wikiurl = wikiutil.mapURL(self.request, wikiurl)
        if wikitag == 'Self':
            import urllib
            if wikitail.find('#') > -1:
                (wikitail, kw['anchor-removed']) = wikitail.split('#', 1)
            wikitail = urllib.unquote(wikitail)
            kw['local'] = self.page.page_name
            return apply(self.pagelink, (on,
             wikiutil.AbsPageName(self.request, self.page.page_name, wikitail)), kw)
        else:
            href = wikiutil.join_wiki(wikiurl, wikitail)
            return self.url(1, href)

    def langAttr(self, lang=None):
        return {}