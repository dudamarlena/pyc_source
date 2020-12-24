# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dvdje/htmlparser.py
# Compiled at: 2013-10-29 23:55:47
# Size of source mod 2**32: 7141 bytes
"""HTML parser classes."""
import datetime, getpass, html.entities, html.parser, http.cookiejar, logging
logger = logging.getLogger(__name__)

class EditEntryLinks(html.parser.HTMLParser):
    __doc__ = 'Makes a list of all of the entry editor URLs on a VBulletin Blogs page.\n\n    Instance attributes:\n    urls -- the list of entry editor URLs found on the page\n    next_page_url -- the URL of the next page of blog entries or None\n    '

    def __init__(self):
        super().__init__(strict=False)
        self.urls = []
        self.next_page_url = None
        return

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a':
            if 'rel' in attrs:
                rel = attrs['rel']
                if rel == 'nofollow' and attrs.get('class') == 'edit_blog':
                    logger.debug('Found entry editor URL: %s', attrs['href'])
                    self.urls.append(attrs['href'])
                elif rel == 'next':
                    self.next_page_url = attrs['href']
                    logger.debug('Found next page URL: %s', self.next_page_url)


class DJParser(html.parser.HTMLParser):
    __doc__ = 'Parses DV dream journal entries.\n\n    Class attributes:\n    category_map -- mapping of checkbox id names to the tag they represent\n\n    Instance attributes:\n    date -- date of the dream journal entry\n    title -- title of the entry\n    tags -- category tags describing the type of journal entry\n    '
    category_map = {'cb_2': 'lucid', 
     'cb_3': 'non-lucid', 
     'cb_4': 'nightmare', 
     'cb_5': 'false awakening', 
     'cb_6': 'memorable', 
     'cb_7': 'task of the month', 
     'cb_8': 'task of the year', 
     'cb_9': 'dream fragment', 
     'cb_10': 'side notes'}

    def __init__(self):
        super().__init__(strict=False)
        self.reset()

    def reset(self):
        logger.debug('Reset parser')
        super().reset()
        self._date = {'year': None, 
         'month': None, 
         'day': None, 
         'hour': None, 
         'minute': None}
        self.date = None
        self.title = None
        self.tags = []
        self.entry = []
        self.keep_reading_entry = False
        return

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'input':
            eid = attrs.get('id')
            if eid == 'titlefield':
                self.title = attrs['value']
                logger.debug('Found entry title: %s', self.title)
            else:
                if attrs.get('name') == 'categories[]' and 'checked' in attrs:
                    category = DJParser.category_map.get(attrs['id'])
                    logger.debug('Found entry category tag: %s', category)
                    self.tags.append(category)
                else:
                    if eid == 'publish_date':
                        n = int(attrs['value'])
                        logger.debug('Found entry publish day: %s', n)
                        self._date['day'] = n
                    else:
                        if eid == 'publish_year':
                            n = int(attrs['value'])
                            logger.debug('Found entry publish year: %s', n)
                            self._date['year'] = n
                        else:
                            if eid == 'publish_hour':
                                n = int(attrs['value'])
                                logger.debug('Found entry publish hour: %s', n)
                                self._date['hour'] = n
                            elif attrs.get('name') == 'publish[minute]':
                                n = int(attrs['value'])
                                logger.debug('Found entry publish minute: %s', n)
                                self._date['minute'] = n
        else:
            if tag == 'select' and attrs.get('name') == 'publish[month]':
                logger.debug('Found entry publish month selection area')
                self._date['month'] = 0
            else:
                if self._date['month'] == 0 and tag == 'option' and 'selected' in attrs:
                    n = int(attrs['value'])
                    logger.debug('Found entry publish month: %s', n)
                    self._date['month'] = n
                elif tag == 'textarea':
                    if attrs.get('id') == 'vB_Editor_001_editor':
                        self.keep_reading_entry = True
                        logger.debug('Found entry text area')

    def handle_data(self, data):
        if self.keep_reading_entry:
            logger.debug('Append chunk: %s char(s)', len(data))
            self.entry.append(data)

    def handle_entityref(self, name):
        if self.keep_reading_entry:
            c = chr(html.entities.name2codepoint.get(name, 32))
            logger.debug('Append entity: %s -> %s', name, c)
            self.entry.append(c)

    def handle_charref(self, name):
        if self.keep_reading_entry:
            c = chr(int(name[1:], 16)) if name.startswith('x') else chr(int(name))
            logger.debug('Append char ref: %s -> %s', name, c)
            self.entry.append(c)

    def handle_endtag(self, tag):
        if tag == 'textarea' and self.keep_reading_entry:
            logger.debug('Concatenating')
            self.entry = ''.join(self.entry).replace('\r', '')
            logger.debug('Done parsing entry text area')
            self.keep_reading_entry = False
        elif tag == 'body':
            self.date = datetime.datetime(**self._date)