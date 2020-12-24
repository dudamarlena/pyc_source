# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/linkexchange/formatters.py
# Compiled at: 2010-09-06 17:57:23
from xml.sax import saxutils

class BaseFormatter(object):

    def __init__(self, count, client=None):
        """
        @param count: links count in the block (0 or None - catch all)
        @keyword client: catch links only from client
        """
        self.count = count
        self.client = client

    def format(self, tags, links):
        """
        Perform links formatting. tags is a list of unicode strings that don't
        contains '<a '. links is a list of unicode strings that contains links
        HTML code.

        @param tags: list of special tags
        @param links: list of links
        @return: HTML code
        """
        pass

    def _add_prefix(self, link, prefix):
        i = 0
        while not (prefix[:i] + link).startswith(prefix):
            i += 1

        link = prefix[:i] + link
        return link

    def _add_suffix(self, link, suffix):
        i = len(suffix)
        while not (link + suffix[i:]).endswith(suffix):
            i -= 1

        link += suffix[i:]
        return link

    def _format_container(self, tag, id, class_, content):
        html = '<' + tag
        if id:
            html += ' id="%s"' % saxutils.escape(id)
        if class_:
            html += ' class="%s"' % saxutils.escape(class_)
        html += '>'
        html += content
        html += '</%s>' % tag
        return html


class InlineFormatter(BaseFormatter):

    def __init__(self, count, client=None, delimiter='', prefix='', suffix='', prolog='', epilog='', id=None, class_=None, class_for_empty=None, strip=False):
        """
        @param count: links count in the block (None - catch all)
        @keyword client: catch links only from client
        @keyword delimiter: links delimiter
        @keyword prefix: links prefix
        @keyword suffix: links suffix
        @keyword prolog: text before links
        @keyword epilog: text after links
        @keyword id: value for id attribute
        @keyword class_: CSS class for nonempty block
        @keyword class_for_empty: CSS class for empty block
        @keyword strip: skip DIV tag
        """
        super(InlineFormatter, self).__init__(count, client=client)
        self.delimiter = delimiter
        self.prefix = prefix
        self.suffix = suffix
        self.prolog = prolog
        self.epilog = epilog
        self.id = id
        self.class_ = class_
        self.class_for_empty = class_for_empty
        self.strip = strip

    def format(self, tags, links):

        def format_link(link):
            if self.prefix:
                link = self._add_prefix(link, self.prefix)
            if self.suffix:
                link = self._add_suffix(link, self.suffix)
            return link

        if links:
            css_class = self.class_
            content = self.prolog + self.delimiter.join(map(format_link, links)) + self.epilog
        else:
            css_class = self.class_for_empty
            content = ''
        if self.strip:
            html = content
        else:
            html = self._format_container('div', self.id, css_class, content)
        html += ('').join(tags)
        return html


class ListFormatter(BaseFormatter):

    def __init__(self, count, client=None, prefix='', suffix='', id=None, class_=None, class_for_empty=None, li_class=None, tag_for_empty='span', strip=False):
        """
        @param count: links count in the block (None - catch all)
        @keyword client: catch links only from client
        @keyword prefix: links prefix
        @keyword suffix: links suffix
        @keyword id: value for id attribute
        @keyword class_: CSS class for nonempty block
        @keyword class_for_empty: CSS class for empty block
        @keyword li_class: CSS class for LI elements
        @keyword tag_for_empty: HTML tag for empty block
        @keyword strip: skip UL tag or empty tag
        """
        super(ListFormatter, self).__init__(count, client=client)
        self.prefix = prefix
        self.suffix = suffix
        self.id = id
        self.class_ = class_
        self.class_for_empty = class_for_empty
        self.li_class = li_class
        self.tag_for_empty = tag_for_empty
        self.strip = strip

    def format(self, tags, links):

        def format_link(link):
            if self.prefix:
                link = self._add_prefix(link, self.prefix)
            if self.suffix:
                link = self._add_suffix(link, self.suffix)
            if self.li_class:
                attrs = ' class="%s"' % saxutils.escape(self.li_class)
            else:
                attrs = ''
            link = '<li%s>%s</li>' % (attrs, link)
            return link

        content = ('').join(map(format_link, links))
        if self.strip:
            html = content
        else:
            if links:
                css_class = self.class_
            else:
                css_class = self.class_for_empty
            html_tag = links and 'ul' or self.tag_for_empty
            html = self._format_container(html_tag, self.id, css_class, content)
        html += ('').join(tags)
        return html