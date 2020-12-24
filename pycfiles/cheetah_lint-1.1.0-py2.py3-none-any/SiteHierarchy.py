# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Tools/SiteHierarchy.py
# Compiled at: 2019-09-22 10:12:27
__doc__ = 'Create menus and crumbs from a site hierarchy.\n\nYou define the site hierarchy as lists/tuples.  Each location in the hierarchy\nis a (url, description) tuple.  Each list has the base URL/text in the 0\nposition, and all the children coming after it.  Any child can be a list,\nrepresenting further depth to the hierarchy.  See the end of the file for an\nexample hierarchy.\n\nUse Hierarchy(contents, currentURL), where contents is this hierarchy, and\ncurrentURL is the position you are currently in.\nThe menubar and crumbs methods give you the HTML output.\n\nThere are methods you can override to customize the HTML output.\n'
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class Hierarchy:

    def __init__(self, hierarchy, currentURL, prefix='', menuCSSClass=None, crumbCSSClass=None):
        """
        hierarchy is described above, currentURL should be somewhere in
        the hierarchy.  prefix will be added before all of the URLs (to
        help mitigate the problems with absolute URLs), and if given,
        cssClass will be used for both links *and* nonlinks.
        """
        self._contents = hierarchy
        self._currentURL = currentURL
        if menuCSSClass:
            self._menuCSSClass = ' class="%s"' % menuCSSClass
        else:
            self._menuCSSClass = ''
        if crumbCSSClass:
            self._crumbCSSClass = ' class="%s"' % crumbCSSClass
        else:
            self._crumbCSSClass = ''
        self._prefix = prefix

    def menuList(self, menuCSSClass=None):
        """An indented menu list"""
        if menuCSSClass:
            self._menuCSSClass = ' class="%s"' % menuCSSClass
        stream = StringIO()
        for item in self._contents[1:]:
            self._menubarRecurse(item, 0, stream)

        return stream.getvalue()

    def crumbs(self, crumbCSSClass=None):
        """The home>where>you>are crumbs"""
        if crumbCSSClass:
            self._crumbCSSClass = ' class="%s"' % crumbCSSClass
        path = []
        pos = self._contents
        while True:
            foundAny = False
            path.append(pos[0])
            for item in pos[1:]:
                if self._inContents(item):
                    if isinstance(item, tuple):
                        path.append(item)
                        break
                    else:
                        pos = item
                        foundAny = True
                        break

            if not foundAny:
                break

        if len(path) == 1:
            return self.emptyCrumb()
        return self.crumbSeperator().join(map(lambda x, self=self: self.crumbLink(x[0], x[1]), path)) + self.crumbTerminator()

    def menuLink(self, url, text, indent):
        if url == self._currentURL or self._prefix + url == self._currentURL:
            return '%s<B%s>%s</B> <BR>\n' % ('&nbsp;&nbsp;' * indent,
             self._menuCSSClass, text)
        else:
            return '%s<A HREF="%s%s"%s>%s</A> <BR>\n' % (
             '&nbsp;&nbsp;' * indent, self._prefix, url,
             self._menuCSSClass, text)

    def crumbLink(self, url, text):
        if url == self._currentURL or self._prefix + url == self._currentURL:
            return '<B%s>%s</B>' % (self._crumbCSSClass, text)
        else:
            return '<A HREF="%s%s"%s>%s</A>' % (
             self._prefix, url, self._crumbCSSClass, text)

    def crumbSeperator(self):
        return '&nbsp;&gt;&nbsp;'

    def crumbTerminator(self):
        return ''

    def emptyCrumb(self):
        """When you are at the homepage"""
        return ''

    def _menubarRecurse(self, contents, indent, stream):
        if isinstance(contents, tuple):
            url, text = contents
            rest = []
        else:
            url, text = contents[0]
            rest = contents[1:]
        stream.write(self.menuLink(url, text, indent))
        if self._inContents(contents):
            for item in rest:
                self._menubarRecurse(item, indent + 1, stream)

    def _inContents(self, contents):
        if isinstance(contents, tuple):
            return self._currentURL == contents[0]
        for item in contents:
            if self._inContents(item):
                return True

        return False


if __name__ == '__main__':
    hierarchy = [('/', 'home'),
     ('/about', 'About Us'),
     [
      ('/services', 'Services'),
      [
       ('/services/products', 'Products'),
       ('/services/products/widget', 'The Widget'),
       ('/services/products/wedge', 'The Wedge'),
       ('/services/products/thimble', 'The Thimble')],
      ('/services/prices', 'Prices')],
     ('/contact', 'Contact Us')]
    for url in ['/', '/services', '/services/products/widget', '/contact']:
        print (
         '<p>', '=' * 50)
        print '<br> %s: <br>\n' % url
        n = Hierarchy(hierarchy, url, menuCSSClass='menu', crumbCSSClass='crumb', prefix='/here')
        print n.menuList()
        print ('<p>', '-' * 50)
        print n.crumbs()