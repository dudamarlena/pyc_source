# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thot/plugins/Tagging.py
# Compiled at: 2013-03-05 21:43:25
import types, logging
from operator import itemgetter
__all__ = [
 'PageTags', 'PageCategory']

def add_to_keyed_list(key, collection, page, none_is_key=None):
    if key in page:
        if type(page[key]) is types.ListType:
            drawer = page[key]
        else:
            drawer = [
             page[key]]
    else:
        if none_is_key:
            drawer = [
             none_is_key]
        else:
            return
        for d in drawer:
            if d in collection:
                collection[d].append(page)
            else:
                collection[d] = [
                 page]


class PageTags(object):
    """
    Mapper of pages to tags.

    This plugin does two things:
     1. reads the tags from the pages
     2. injects new parametrized output pages
    The beforementioned collection mediates between the steps.
    """
    run_at = [
     'after_page_parsed', 'after_parsing']
    field = 'tags'
    none_is_key = False

    def __init__(self, site, settings):
        self.site = site
        self.site_settings = settings
        self.collection = {}
        logging.debug('Plugin "%s" has been initalized.', self)

    def after_page_parsed(self, page):
        """ Step 1: tags from page """
        if page.is_public:
            add_to_keyed_list(self.field, self.collection, page, self.none_is_key)

    def _pop_index_page(self, pages):
        """
        Gets the page that servers as template for the field's index,
        removes it from the stack of pages if necessary.
        """
        for page in pages:
            if 'index' in page:
                if type(page['index']) is types.ListType and self.field in page['index']:
                    if len(page['index']) <= 1:
                        pages.remove(page)
                    else:
                        page['index'].remove(self.field)
                    return page
                if page['index'] == self.field:
                    pages.remove(page)
                    return page

        return

    def _get_url(self, page):
        """
        Suggests a functional url.
        """
        url = self.field + '/'
        url += page['params']['field_value'].lower().replace(' ', '-')
        url += '/index.html'
        return url

    def after_parsing(self, pages):
        """
        Step 2: inject new parametrized pages
        which will serve as archive, category or tag indices.
        """
        index_page = self._pop_index_page(pages)
        if not index_page:
            logging.warn('Index page for "%s" could not be found.' + ' Please create one with "{status: hidden, index: \'%s\'}".', self.field, self.field)
            return
        for field_value in self.collection:
            self.collection[field_value].sort(key=itemgetter('date', 'url'), reverse=True)
            p = index_page.copy()
            params = dict(field=self.field, field_value=field_value, collection=self.collection[field_value])
            p['params'] = params
            p['url'] = self._get_url(p)
            p['title'] = p['title'] % params
            pages.append(p)


class PageCategory(PageTags):
    """
    Mapper of pages to categories.
    """
    field = 'category'
    none_is_key = 'Uncategorized'