# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/shabti/templates/moinmoin/data/moin/data/plugin/theme/plsavez.py
# Compiled at: 2010-04-25 13:56:46
"""
PLSAVEZ Theme - based on modern CMS and Mentalhealth
======================

If you want to use a wiki as a tool to create a regular site easily,
this theme is for you. The wiki looks like a plain site to visitors or
users without edit rights, and a wiki to users with edits rights. 

Problems
--------
Some actions are not available for visitors:

- Show Raw Text
- Show Print Preview
- Show Like Pages
- Show Local Site Map
- Delete Cache

Most of these are not really needed for a visitor. Print style sheet is
used transparently when you print a page. Like Pages and Local Site Map
should be available, but are not really needed if you have a good
search.

Missing page will suggest visitors to create a new page, but they will
always fail because they don't have acl rights. This should be fixed in
other place.

Install
-------

1. Put in your wiki/data/plugin/theme/

2. Prevent visitors from writing using acl::

    acl_rights_before = (u"WikiAdmin:read,write,delete,revert,admin "
                         u"EditorsGroup:read,write,delete,revert ")
    acl_rights_default = u"All:read "
                          
Remember that some ACL you put on a page will override the default ACL!

3. Make it the default and only theme on your site::

    theme_default = 'plsavez'
    theme_force = True
    
    
Compatibility
--------------
Tested with release 1.5.3 and 1.5.2, should work with any 1.5 release.

Legal
-----
@copyright (c) 2006 Jure Kodzoman <jure@plsavez.hr>

@copyright (c) 2005 robin.escalation@ACM.org
@copyright (c) 2005 Nir Soffer <nirs@freeshell.org>
@copyright (c) 2006 Thomas Waldmann
@license: GNU GPL, see COPYING for details

"""
from MoinMoin.theme import modern
from MoinMoin import wikiutil
from MoinMoin.wikiutil import escape
from MoinMoin.wikiutil import link_tag as link
from MoinMoin.wikiutil import quoteWikinameURL as quoteURL

class Theme(modern.Theme):
    name = 'plsavez'

    def header(self, d, **kw):
        """ Assemble wiki header
          @param d: parameter dictionary
          @rtype: unicode
          @return: page header html
          """
        html = [
         self.emit_custom_html(self.cfg.page_header1),
         '<div class="content">',
         '    <div id="suheader">',
         '        <div id="sulogo">',
         '            <h1 class="displaynone">Bel-EPA, a leading edge in electronic publishing</h1>',
         '        </div>',
         '        <ul id="skipnav">            <li><a href="#navareatag">Skip to area navigation</a></li>',
         '            <li><a href="#contenttag">Skip to content</a></li>',
         '        </ul>',
         '    </div>',
         self.username(d),
         '<div id="header">',
         self.logo(),
         self.searchform(d),
         '<div id="locationline">',
         self.interwiki(d),
         self.title(d),
         '</div>',
         self.trail(d),
         self.navibar(d),
         '<div id="pageline"><hr style="display:none;"></div>',
         self.msg(d),
         self.editbar(d),
         '</div>',
         self.emit_custom_html(self.cfg.page_header2),
         self.startPage()]
        return ('\n').join(html)

    def shouldShowEditbar(self, page):
        """ Hide the edit bar if you can't edit """
        if self.request.user.may.write(page.page_name):
            return modern.Theme.shouldShowEditbar(self, page)
        return False

    def pageLastName(self, name):
        """ This should be in the Page class, but its not """
        return name[name.rfind('/') + 1:]

    def shortenPagename(self, name):
        """ Shorten page names
        
        This is a modified copy from theme/__init__.py. Modified to
        show only the last name of a page, even if there is room for
        the full name.
        """
        name = self.pageLastName(name)
        maxLength = self.maxPagenameLength()
        if len(name) > maxLength:
            (half, left) = divmod(maxLength - 3, 2)
            name = '%s...%s' % (name[:half + left], name[-half:])
        return name

    def footer(self, d, **keywords):
        """ same as modern footer, but no pageinfo """
        page = d['page']
        html = [
         self.endPage(),
         self.emit_custom_html(self.cfg.page_footer1),
         '<div id="footer">',
         self.editbar(d),
         self.credits(d),
         self.showversion(d, **keywords),
         '</div>',
         self.emit_custom_html(self.cfg.page_footer2),
         '</div>']
        return ('\n').join(html)

    def searchform(self, d):
        """
        assemble HTML code for the search forms
        
        @param d: parameter dictionary
        @rtype: unicode
        @return: search form html
        """
        _ = self.request.getText
        form = self.request.form
        updates = {'search_label': _('Search:'), 
           'search_value': escape(form.get('value', [''])[0], 1), 
           'search_full_label': _('Text', formatted=False), 
           'search_title_label': _('Titles', formatted=False)}
        d.update(updates)
        html = '\n<form id="searchform" method="get" action="">\n<div>\n<input type="hidden" name="action" value="fullsearch">\n<input type="hidden" name="context" value="180">\n<label for="searchinput">%(search_label)s</label>\n<input id="searchinput" type="text" name="value" value="%(search_value)s" size="15" alt="Search">\n<input id="titlesearch" name="titlesearch" type="submit"\n    value="%(search_title_label)s" alt="Search Titles">\n<input id="fullsearch" name="fullsearch" type="submit"\n    value="%(search_full_label)s" alt="Search Full Text">\n</div>\n</form>\n' % d
        return html

    def headscript(self, d):
        """ Return html head script with common functions

        TODO: put these on common.js instead, so they can be downloaded
        only once.

        TODO: actionMenuInit should be called once, from body onload,
        but currently body is not written by theme.

        @param d: parameter dictionary
        @rtype: unicode
        @return: script for html head
        """
        if self.request.form.get('action', [''])[0] == 'print':
            return ''
        _ = self.request.getText
        script = '\n<script type="text/javascript">\n<!--// common functions\n\n// We keep here the state of the search box\n\nfunction actionsMenuInit(title) {\n    // Initialize action menu\n    for (i = 0; i < document.forms.length; i++) {\n        var form = document.forms[i];\n        if (form.className == \'actionsmenu\') {\n            // Check if this form needs update\n            var div = form.getElementsByTagName(\'div\')[0];\n            var label = div.getElementsByTagName(\'label\')[0];\n            if (label) {\n                // This is the first time: remove label and do buton.\n                div.removeChild(label);\n                var dobutton = div.getElementsByTagName(\'input\')[0];\n                div.removeChild(dobutton);\n                // and add menu title\n                var select = div.getElementsByTagName(\'select\')[0];\n                var item = document.createElement(\'option\');\n                item.appendChild(document.createTextNode(title));\n                item.value = \'show\';\n                select.insertBefore(item, select.options[0]);\n                select.selectedIndex = 0;\n            }\n        }\n    }\n}\n//-->\n</script>\n' % {'search_hint': _('Search', formatted=False)}
        return script

    def editbar(self, d):
        """
        Assemble the page edit bar.

        This is rewritten here to get rid of fugly drop-down menu.
        (Obviating the need for the actionsMenu() method).

        Also I tried to reduce the number of aliases 'cause I find
        that hard to follow.
            @param d: parameter dictionary
            @rtype: unicode
            @return: iconbar html
        """
        if not self.shouldShowEditbar(d['page']):
            return ''
        _ = self.request.getText
        page = d['page']
        cacheKey = 'editbar'
        quotedname = quoteURL(page.page_name)
        cached = self._cache.get(cacheKey)
        if cached:
            return cached
        links = []
        parent = page.getParentPage()
        if parent:
            links += [parent.link_to(self.request, _('Show Parent', formatted=False))]
        choices = [
         [
          'edit', 'Edit'],
         [
          'info', 'Info'],
         [
          'refresh', 'Delete Cache'],
         [
          'quicklink', 'Quick links'],
         [
          'AttachFile', 'Attachments'],
         [
          'RenamePage', 'Rename Page'],
         [
          'DeletePage', 'Delete Page'],
         [
          'MyPages', 'My Pages'],
         [
          'ImportHtml', 'Import HTML'],
         [
          'N3Dump', 'N3Dump'],
         [
          'ShowGraph', 'ShowGraph']]
        available = wikiutil.quoteWikinameURL(page.page_name) + '?action=PageActions'
        for (action, label) in choices:
            if action == 'refresh' and not page.canUseCache():
                continue
            if action == 'edit' and not (page.isWritable() and self.request.user.may.write(page.page_name)):
                continue
            if action[0].isupper() and action not in available:
                continue
            links += [
             link(self.request, '%s?action=%s' % (quotedname, action), _(label, formatted=False))]

        links += [self.subscribeLink(page)]
        html = '<ul class="editbar">\n<li><a id="toggleCommentsButton" onClick="toggleComments();">Comments</a></li>%s\n</ul>\n' % ('\n').join([ '<li>%s</li>' % item for item in links if item != '' ])
        self._cache[cacheKey] = html
        return html


def execute(request):
    return Theme(request)