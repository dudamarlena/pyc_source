# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tw/lymon/widgets.py
# Compiled at: 2008-07-03 15:54:48
from tw.api import Widget, JSLink, CSSLink
__all__ = [
 'ColorTab',
 'ArrowListMenu',
 'Container',
 'CSSContainer',
 'StyledMenus',
 'PageIndex',
 'PopUp',
 'ListMenu']
cssPopUp = CSSLink(modname=__name__, filename='static/css/popup/popup_link.css')
cssColorTab = CSSLink(modname=__name__, filename='static/css/colortab.css')
cssArrowMenu = CSSLink(modname=__name__, filename='static/css/arrowmenu.css')
cssContainer = CSSLink(modname=__name__, filename='static/css/container.css')
cssStyledMenu = CSSLink(modname=__name__, filename='static/css/styled_menu.css')
cssStyledTable = CSSLink(modname=__name__, filename='static/css/styled_table.css')
cssPageIdex = CSSLink(modname=__name__, filename='static/css/page_index.css')

class ListMenu(Widget):
    params = [
     'items', 'current']
    current = 0
    items = [('Item 1', '#')]
    engine_name = 'genshi'
    template = '\n\t<div xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/" py:strip=\'\'> \n    \t<ul>\n    \t\t<?python\n\t\t\t\tis_current = lambda item: items.index(item) == current \n\t\t\t?>\n\t\t\t<div py:for=\'item in items\' py:strip=\'\'>\n\t\t\t\t\n\t\t\t\t<li py:if=\'not is_current(item)\'>\n\t\t\t\t\t<a py:attrs="{\'href\': item[1]}" py:content=\'item[0]\'>  </a>\n\t\t\t\t</li>\n\t\t\t\t<li py:if=\'is_current(item)\' py:attrs="{\'href\': item[1], \'class\': \'active\'}" py:content=\'item[0]\'>\n\n\t\t\t\t</li>\n\t\t\t\t\n\t\t\t</div>\n\t\t\t\n\n    \t</ul>\n    </div>\n    '


class ColorTab(Widget):
    css = [
     cssColorTab]
    params = ['elements', 'id']
    elements = [
     ('Item 1', '#')]
    id = 'bar'
    engine_name = 'genshi'
    template = '\n    <div xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/" py:strip=\'\'>\n\t<div id="invertedtabsline">&nbsp;</div>\n\t<div id="invertedtabs">\n\t\t<ul>\n\t\t\t<li py:for="element in elements" style="margin-left: 1px">\n\t\t\t\t<a py:attrs="{\'href\':element[1]}"> <span py:content="element[0]">Title</span></a>\n\t\t\t</li>\n\t\t</ul>\n\t</div>\n\t<br style="clear: left" />\n    </div>\n    '


class StyledMenus(Widget):
    css = [
     cssStyledMenu]
    params = ['elements', 'id', 'title']
    elements = [
     ('Item 1', '#')]
    title = 'New Menu:'
    engine_name = 'genshi'
    template = '\n    <div xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/" py:strip=\'\'>\n\t<div py:attrs="{\'id\':id}">\n\t\t<ul>\n\t\t\t<li><a id="current">$title</a></li>\n\t\t\t<li py:for="element in elements">\n\t\t\t\t<a py:attrs="{\'href\':element[1]}"> <span py:content="element[0]">Title</span></a>\n\t\t\t</li>\n\t\t</ul>\n\t</div>\n\t</div>\n    '


class ArrowListMenu(Widget):
    css = [
     cssArrowMenu]
    params = ['elements', 'id', 'title']
    elements = [
     ('Item 1', '#')]
    id = 'menu'
    title = 'Menu:'
    engine_name = 'genshi'
    template = '\n    <div xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/" py:strip=\'\'>\n\t<div class="arrowlistmenu">\n\t\t<h3 class="headerbar">$title</h3>\n\t\t<ul>\n\t\t\t<li py:for="element in elements">\n\t\t\t\t<a py:attrs="{\'href\':element[1]}"> <span py:content="element[0]">Title</span></a>\n\t\t\t</li>\n\t\t</ul>\n\t</div>\n\t</div>\n    '


class Container(Widget):
    css = [
     cssContainer]
    params = ['title', 'html']
    title = 'CSS Container'
    html = 'Contained HTML'
    engine_name = 'genshi'
    template = '\n\t<div class="container">\n\t\t<div class="container_head">\n\t\t\t<img src="images/sidebar_left.jpg" alt="" class="float_left"/>\n\t\t\t<img src="images/sidebar_right.jpg" alt="" class="float_right"/>\n\t\t\t<div class="container_head_text">\n\t\t\t\t$title\n\t\t\t</div>\n\t\t</div>\n\t\t<div class="container_content">\n\t\t\t$html  \n\t\t</div>\n\t</div>\n\t'


class CSSContainer(Widget):
    css = [
     cssContainer]


class PageIndex(Widget):
    params = [
     'current', 'pages', 'start', 'link', 'page_index']
    current = 1
    start = 1
    pages = 20
    link = '/index?page=%s'
    engine_name = 'genshi'
    css = [cssPageIdex]

    def update_params(self, d):
        pages = self.pages
        d['current'] = int(self.current)
        page_index = [ page + 1 for page in range(pages) ]
        d['page_index'] = page_index
        super(PageIndex, self).update_params(d)

    template = '\n\t<div xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/">\n\t\t<ul class=\'page_index\'>\n\t\t\t<li py:for="item in page_index">\n\t\t\t\t<div py:choose=\'\' py:strip=\'\'>\n\t\t\t\t\t<a py:if=\'item == 1 and (current -1) >0\' href=\'${link % (current-1)}\' class=\'page_index_next\'> <span>&lt;&lt;</span></a>\n\t\t\t\t\t<a py:when=\'item == 0\' class=\'page_index_dot\'> <span>.......</span></a>\n\t\t\t\t\t<a py:when=\'item == current\' class=\'page_index_selected\'> <span>$item</span></a>\n\t\t\t\t\t<a py:otherwise=\'\' href=\'${link % item}\' class=\'page_index_item\'> <span>$item</span> </a>\n\t\t\t\t\t<a py:if=\'item == pages and (current +1) &lt;pages\' href=\'${link % (current+1)}\' class=\'page_index_next\'> <span>&gt;&gt;</span></a>\n\t\t\t\t</div>\n\t\t\t</li>\n\t\t</ul>\n\t<br />\n\t</div>\n\t\n\t'


class PopUp(Widget):
    css = [
     cssPopUp]
    params = ['link', 'attrs', 'string', 'title', 'href']
    engine_name = 'genshi'
    link = '/'
    href = None
    title = 'Vista sin Marcos'
    attrs = {}
    defaults = {'scrollbars': 0, 'status': 'no', 
       'titlebar': 'no', 
       'toolbar': 'no', 
       'resizable': 'yes', 
       'menubar': 'no', 
       'location': 'no', 
       'width': 300, 
       'height': 200}
    template = '\n\t<div xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/" class=\'popup_link\'>\n\t<a py:attrs="{\'href\': href, \'class\': \'cursor\'}" onclick="window.open(\'$link\',\'window\', \'$string\')" > $title </a>\n\t</div>\n\t'

    def update_params(self, d):
        d['link'] = self.link
        d['href'] = self.href
        string = ''
        self.defaults.update(self.attrs)
        for (attr, value) in self.defaults.items():
            string += '%s=%s, ' % (attr, value)

        d['string'] = string
        super(PopUp, self).update_params(d)