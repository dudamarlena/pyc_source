# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/shabti/templates/moinmoin/data/moin/data/plugin/theme/bplus.py
# Compiled at: 2010-04-22 17:25:58
"""
    MoinMoin - modern theme

    @copyright: 2003-2005 Nir Soffer, Thomas Waldmann
    @license: GNU GPL, see COPYING for details.
"""
from MoinMoin.theme import ThemeBase
from MoinMoin import wikiutil
from MoinMoin.Page import Page

class Theme(ThemeBase):
    name = 'bplus'
    _ = lambda x: x
    icons = {'attach': ('%(attach_count)s', 'moin-attach.png', 16, 16), 
       'info': ('[INFO]', 'moin-info.png', 16, 16), 
       'attachimg': (
                   _('[ATTACH]'), 'attach.png', 32, 32), 
       'rss': (
             _('[RSS]'), 'moin-rss.png', 16, 16), 
       'deleted': (
                 _('[DELETED]'), 'moin-deleted.png', 16, 16), 
       'updated': (
                 _('[UPDATED]'), 'moin-updated.png', 16, 16), 
       'renamed': (
                 _('[RENAMED]'), 'moin-renamed.png', 16, 16), 
       'conflict': (
                  _('[CONFLICT]'), 'moin-conflict.png', 16, 16), 
       'new': (
             _('[NEW]'), 'moin-new.png', 16, 16), 
       'diffrc': (
                _('[DIFF]'), 'moin-diff.png', 16, 16), 
       'www': ('[WWW]', 'moin-www.png', 16, 16), 
       'bottom': (
                _('[BOTTOM]'), 'moin-bottom.png', 16, 16), 
       'top': (
             _('[TOP]'), 'moin-top.png', 16, 16), 
       'mailto': ('[MAILTO]', 'moin-email.png', 16, 16), 
       'news': ('[NEWS]', 'moin-news.png', 16, 16), 
       'telnet': ('[TELNET]', 'moin-telnet.png', 16, 16), 
       'ftp': ('[FTP]', 'moin-ftp.png', 16, 16), 
       'file': ('[FILE]', 'moin-ftp.png', 16, 16), 
       'searchbutton': ('[?]', 'moin-search.png', 16, 16), 
       'interwiki': ('[%(wikitag)s]', 'moin-inter.png', 16, 16), 
       'X-(': ('X-(', 'angry.png', 16, 16), 
       ':D': (':D', 'biggrin.png', 16, 16), 
       '<:(': ('<:(', 'frown.png', 16, 16), 
       ':o': (':o', 'redface.png', 16, 16), 
       ':(': (':(', 'sad.png', 16, 16), 
       ':)': (':)', 'smile.png', 16, 16), 
       'B)': ('B)', 'smile2.png', 16, 16), 
       ':))': (':))', 'smile3.png', 16, 16), 
       ';)': (';)', 'smile4.png', 16, 16), 
       '/!\\': ('/!\\', 'alert.png', 16, 16), 
       '<!>': ('<!>', 'attention.png', 16, 16), 
       '(!)': ('(!)', 'idea.png', 16, 16), 
       ':-?': (':-?', 'tongue.png', 16, 16), 
       ':\\': (':\\', 'ohwell.png', 16, 16), 
       '>:>': ('>:>', 'devil.png', 16, 16), 
       '|)': ('|)', 'tired.png', 16, 16), 
       ':-(': (':-(', 'sad.png', 16, 16), 
       ':-)': (':-)', 'smile.png', 16, 16), 
       'B-)': ('B-)', 'smile2.png', 16, 16), 
       ':-))': (':-))', 'smile3.png', 16, 16), 
       ';-)': (';-)', 'smile4.png', 16, 16), 
       '|-)': ('|-)', 'tired.png', 16, 16), 
       '(./)': ('(./)', 'checkmark.png', 16, 16), 
       '{OK}': ('{OK}', 'thumbs-up.png', 16, 16), 
       '{X}': ('{X}', 'icon-error.png', 16, 16), 
       '{i}': ('{i}', 'icon-info.png', 16, 16), 
       '{1}': ('{1}', 'prio1.png', 15, 13), 
       '{2}': ('{2}', 'prio2.png', 15, 13), 
       '{3}': ('{3}', 'prio3.png', 15, 13), 
       '{*}': ('{*}', 'star_on.png', 16, 16), 
       '{o}': ('{o}', 'star_off.png', 16, 16)}
    del _

    def header(self, d, **kw):
        """ Assemble wiki header

        @param d: parameter dictionary
        @rtype: unicode
        @return: page header html
        """
        html = [
         self.emit_custom_html(self.cfg.page_header1),
         '<div id="header">',
         self.searchform(d),
         self.logo(),
         self.username(d),
         '<br/>',
         '<h1 id="locationline">',
         self.title(d),
         self.interwiki(d),
         '</h1>',
         self.trail(d),
         self.navibar(d),
         '<div id="pageline"><hr style="display:none;"></div>',
         self.msg(d),
         self.editbar(d),
         '</div>',
         self.emit_custom_html(self.cfg.page_header2),
         self.startPage()]
        return ('\n').join(html)

    def editorheader(self, d, **kw):
        """ Assemble wiki header for editor

        @param d: parameter dictionary
        @rtype: unicode
        @return: page header html
        """
        html = [
         self.emit_custom_html(self.cfg.page_header1),
         '<div id="header">',
         '<h1 id="locationline">',
         self.title(d),
         '</h1>',
         self.msg(d),
         '</div>',
         self.emit_custom_html(self.cfg.page_header2),
         self.startPage()]
        return ('\n').join(html)

    def footer(self, d, **keywords):
        """ Assemble wiki footer

        @param d: parameter dictionary
        @keyword ...:...
        @rtype: unicode
        @return: page footer html
        """
        page = d['page']
        html = [
         self.pageinfo(page),
         self.endPage(),
         self.emit_custom_html(self.cfg.page_footer1),
         '<div id="footer">',
         self.editbar(d),
         self.credits(d),
         self.showversion(d, **keywords),
         '</div>',
         self.emit_custom_html(self.cfg.page_footer2)]
        return ('\n').join(html)

    def title(self, d):
        """ Assemble the title (now using breadcrumbs)

        @param d: parameter dictionary
        @rtype: string
        @return: title html
        """
        _ = self.request.getText
        content = []
        if d['title_text'] == d['page'].split_title():
            curpage = ''
            segments = d['page_name'].split('/')
            for s in segments[:-1]:
                curpage += s
                thisp = Page(self.request, curpage)
                content.append(thisp.link_to(self.request, thisp.split_title().split('/')[(-1)]))
                curpage += '/'

            link_text = d['page'].split_title().split('/')[(-1)]
            link_title = _('Click to do a full-text search for this title')
            link_query = {'action': 'fullsearch', 
               'value': 'linkto:"%s"' % d['page_name'], 
               'context': '180'}
            link = d['page'].link_to(self.request, link_text, querystr=link_query, title=link_title, css_class='backlink', rel='nofollow')
            content.append(link)
        else:
            content.append(wikiutil.escape(d['title_text']))
        location_html = ('<span class="sep"> / </span>').join(content)
        html = '<div id="pagelocation">%s</div>' % location_html
        return html

    def username(self, d):
        """ Assemble the username / userprefs link

        @param d: parameter dictionary
        @rtype: unicode
        @return: username html
        """
        request = self.request
        _ = request.getText
        userlinks = []
        if request.user.valid and request.user.name:
            interwiki = wikiutil.getInterwikiHomePage(request)
            name = request.user.name
            aliasname = request.user.aliasname
            if not aliasname:
                aliasname = name
            title = '%s @ %s' % (aliasname, interwiki[0])
            homelink = request.formatter.interwikilink(1, title=title, id='userhome', generated=True, *interwiki) + request.formatter.text(name) + request.formatter.interwikilink(0, title=title, id='userhome', *interwiki)
            userlinks.append(homelink)
            if 'userprefs' not in self.request.cfg.actions_excluded:
                userlinks.append(d['page'].link_to(request, text=_('Settings'), querystr={'action': 'userprefs'}, id='userprefs', rel='nofollow'))
        if request.user.valid:
            if request.user.auth_method in request.cfg.auth_can_logout:
                userlinks.append(d['page'].link_to(request, text=_('Logout'), querystr={'action': 'logout', 'logout': 'logout'}, id='logout', rel='nofollow'))
        else:
            query = {'action': 'login'}
            if request.cfg.auth_login_inputs == ['special_no_input']:
                query['login'] = '1'
            if request.cfg.auth_have_login:
                userlinks.append(d['page'].link_to(request, text=_('Login'), querystr=query, id='login', rel='nofollow'))
        userlinks_html = ('<span class="sep"> | </span>').join(userlinks)
        html = '<div id="username">%s</div>' % userlinks_html
        return html

    def trail(self, d):
        """ Assemble page trail

        @param d: parameter dictionary
        @rtype: unicode
        @return: trail html
        """
        request = self.request
        user = request.user
        html = ''
        if not user.valid or user.show_page_trail:
            trail = user.getTrail()
            if trail:
                items = []
                for pagename in trail:
                    try:
                        (interwiki, page) = wikiutil.split_interwiki(pagename)
                        if interwiki != request.cfg.interwikiname and interwiki != 'Self':
                            link = self.request.formatter.interwikilink(True, interwiki, page) + self.shortenPagename(page) + self.request.formatter.interwikilink(False, interwiki, page)
                            items.append(link)
                            continue
                        else:
                            pagename = page
                    except ValueError:
                        pass

                    page = Page(request, pagename)
                    title = page.split_title()
                    title = self.shortenPagename(title)
                    link = page.link_to(request, title)
                    items.append(link)

                html = '<div id="pagetrail">%s</div>' % ('<span class="sep"> &raquo; </span>').join(items)
        return html

    def interwiki(self, d):
        """ Assemble the interwiki name display, linking to page_front_page

        @param d: parameter dictionary
        @rtype: string
        @return: interwiki html
        """
        if self.request.cfg.show_interwiki:
            page = wikiutil.getFrontPage(self.request)
            text = self.request.cfg.interwikiname or 'Self'
            link = page.link_to(self.request, text=text, rel='nofollow')
            html = '<span id="interwiki">%s<span class="sep">: </span></span>' % link
        else:
            html = ''
        return html


def execute(request):
    """
    Generate and return a theme object

    @param request: the request object
    @rtype: MoinTheme
    @return: Theme object
    """
    return Theme(request)