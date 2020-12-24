# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/bass/event.py
# Compiled at: 2015-09-12 09:48:13
# Size of source mod 2**32: 7954 bytes
"""
bass.event
-----
Objects and functions related to events and event handlers.
"""
import logging, re, sys
from datetime import datetime, date
from os.path import join, splitext, getctime, basename
from . import setting
from .markup import converter
event_handler = {}

def combine(h1, h2):

    def _h12(node):
        h1(node)
        h2(node)

    return _h12


def add_handler(event, handler):
    """add handler for event 'event'"""
    if callable(handler):
        if event in event_handler:
            logging.debug('Event handler for %s extended', event)
            event_handler[event] = combine(event_handler[event], handler)
        else:
            logging.debug('New event handler for %s', event)
            event_handler[event] = handler
    else:
        logging.debug('Event handler for %s is not a callable', event)


def copy_handler(from_event, to_event):
    """copy handler for event 'from_event' to event 'to_event'"""
    if from_event in event_handler:
        logging.debug('Event handler for %s copied from %s', to_event, from_event)
        event_handler[to_event] = event_handler[from_event]
    else:
        logging.debug('No event handler for %s - cannot copy', from_event)


def remove_handler(event):
    """remove handler for event 'event'"""
    if event in event_handler:
        logging.debug('Event handler for %s removed', event)
        del event_handler[event]
    else:
        logging.debug('No event handler for %s - cannot remove', event)


def event(event, node):
    """call handler for event 'event'"""
    if event in event_handler:
        event_handler[event](node)


class Processor:

    def __init__(self, converter=None):
        """construct page processor for given markup converter"""
        self.convert = converter

    def __call__(self, node):
        """convert node.content, node.preview and node.meta, which are set by node.__init__();
           use elements of node.meta as attributes of node; set node.url"""
        if self.convert:
            node.preview = self.convert(node.preview) if node.preview else ''
            node.content = self.convert(node.content)
        full_path = join(setting.input, node.path)
        node.meta = complete_meta(node.meta, full_path)
        for key, value in node.meta.items():
            setattr(node, key, value)

        page_name = splitext(node.path)[0]
        node.url = '/{0}.html'.format(page_name)


def complete_meta(meta, path):
    """complete metadata for node with given path"""
    if 'title' not in meta:
        title = splitext(basename(path))[0]
        meta['title'] = title.replace('-', ' ').replace('_', ' ').capitalize()
    if 'tags' in meta:
        if isinstance(meta['tags'], list):
            pass
        elif isinstance(meta['tags'], str):
            meta['tags'] = [tag.strip() for tag in meta['tags'].split()]
    else:
        meta['tags'] = []
    if 'skin' not in meta:
        meta['skin'] = 'default'
    if 'id' not in meta:
        meta['id'] = ''
    fix_date_time(meta, datetime.fromtimestamp(getctime(path)))
    return meta


def fix_date_time(meta, ctime):
    """fix metadata date, time, datetime based on existing metadata and ctime of node"""
    date_part = meta.get('date')
    time_part = meta.get('time')
    if 'datetime' in meta:
        if date_part is None:
            if isinstance(meta['datetime'], datetime):
                date_part = meta['datetime'].date()
    else:
        if isinstance(meta['datetime'], date):
            date_part = meta['datetime']
        if time_part is None:
            if isinstance(meta['datetime'], datetime):
                time_part = meta['datetime'].time()
        meta['date'] = date_part
        meta['time'] = time_part
    if date_part is not None and time_part is not None:
        meta['datetime'] = datetime(date_part.year, date_part.month, date_part.day, time_part.hour, time_part.minute, time_part.second, time_part.microsecond, time_part.tzinfo)
    else:
        if date_part is not None:
            meta['datetime'] = datetime(date_part.year, date_part.month, date_part.day)
        else:
            meta['datetime'] = ctime
            meta['date'] = ctime.date()
            meta['time'] = ctime.time()


if setting.markdown:
    markdown_processor = Processor(converter['mkd'])
    add_handler('generate:post:page:extension:mkd', markdown_processor)
    copy_handler('generate:post:page:extension:mkd', 'generate:post:page:extension:md')
if setting.rest:
    rest_processor = Processor(converter['rst'])
    add_handler('generate:post:page:extension:rst', rest_processor)
if setting.textile:
    textile_processor = Processor(converter['txi'])
    add_handler('generate:post:page:extension:txi', textile_processor)
html_processor = Processor(converter['html'])
add_handler('generate:post:page:extension:html', html_processor)
text_processor = Processor(converter['txt'])
add_handler('generate:post:page:extension:txt', text_processor)

def partition(lst, size):
    """divide list in list of sub-lists of length <= size"""
    return [lst[offset:offset + size] for offset in range(0, len(lst), size)]


def add_toc(page, nodelist, skin, sep='_', size=10):
    """add a table of contents to the specified node, apply pagination if necessary.

    Parameters:
        - page (Node): node to which table of contents is added
        - nodelist ([Node]): nodes to include in table of contents
        - skin (string|callable):
            - string: name of template to render one node in nodelist
            - callable: callable to render one node in nodelist
    Return value: None
    """
    if callable(skin):
        func = skin
    else:
        if isinstance(skin, str):
            func = setting.template[skin].render
        else:
            logging.critical("Bad parameter 'skin' in function 'add_toc'")
            sys.exit(1)
        parts = partition([func(this=node) for node in nodelist], size)
        page.prev, page.next = (None, None)
        previous = page
        logging.debug('TOC main page name=%s path=%s', page.name, page.path)
        logging.debug('TOC has %d parts', len(parts))
        if len(parts) > 0:
            page.toc = '\n'.join(parts[0])
        else:
            page.toc = ''
    if len(parts) > 1:
        for p, part in enumerate(parts[1:]):
            current = page.copy(sep + str(p + 1))
            logging.debug('subpage name=%s path=%s', current.name, current.path)
            current.toc = '\n'.join(part)
            page.add(current)
            previous.next = current
            current.prev = previous
            previous = current

        previous.next = None


def idref_replace(mo):
    catch = setting.root.pages(idref=mo.group(2), deep=True)
    return 'href={0}{1}{0}'.format(mo.group(1), catch[0].url if catch else '#')


idref_regex = re.compile('href=([\'\\"])idref:\\s*(\\w+?)\\1')

def resolve_idref(node):
    """replace href="idref:FOO" with href="BAR" where BAR is the URL of the page with id=FOO"""
    node.content = idref_regex.sub(idref_replace, node.content)