# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/cblog/widgets/sitewide.py
# Compiled at: 2006-12-15 15:49:41
__all__ = [
 'archive_links', 'ArchiveLinks', 'category_links', 'CategoryLinks', 'events', 'fancyflash', 'FancyFlash', 'gravatar', 'Gravatar', 'mochikit', 'profile', 'Profile', 'search_form', 'SearchForm', 'sitewidgets']
import md5
from datetime import datetime
from turbogears import validators, url, config
from turbogears.widgets import *
from cblog import model
from cblog.widgets.gravatar import *
from cblog.widgets.fancyflash import *
from cblog.widgets.jslibs import *
sitewidgets = [
 'mochikit', 'events', 'archive_links', 'category_links', 'fancyflash', 'gravatar', 'profile', 'search_form']

class Profile(Widget):
    """A profile summary to be shown in the sidebar.

    TODO:
    """
    __module__ = __name__
    template = '    <p xmlns:py="http://purl.org/kid/ns#" id="profile"></p>\n    '


class ArchiveLinks(Widget):
    """A list of links to monthly archive pages."""
    __module__ = __name__
    params = [
     'archives']
    template = '    <ul xmlns:py="http://purl.org/kid/ns#" id="archive-links">\n      <li py:for="month, entry_count in archives"><a\n        href="${tg.url(month.strftime(\'/archive/%Y-%m\'))}"\n        >${month.strftime(\'%B %Y\')} (${entry_count})</a></li>\n    </ul>\n    '

    def get_archives(self):
        """Assemble a list of months and number of post in each."""
        archives = {}
        for entry in model.Entry.select():
            month = entry.month
            if archives.has_key(month):
                archives[month] += 1
            else:
                archives[month] = 1

        archives = [ x for x in archives.items() ]
        archives.sort()
        archives.reverse()
        return archives

    def update_params(self, params):
        super(ArchiveLinks, self).update_params(params)
        params['archives'] = self.get_archives()


class CategoryLinks(Widget):
    """A list of links to posts by category."""
    __module__ = __name__
    params = [
     'tags']
    template = '    <ul xmlns:py="http://purl.org/kid/ns#" id="category-links">\n      <li py:for="tagname, count in tags"><a\n        href="${tg.url(\'/tag/%s\' % tagname)}"\n        >${tagname} (${count})</a></li>\n    </ul>\n    '

    def update_params(self, params):
        super(CategoryLinks, self).update_params(params)
        tags = [ (tag.name, tag.entry_count) for tag in model.Tag.select() if tag.entry_count ]
        tags.sort(key=lambda x: x[1])
        tags.reverse()
        params['tags'] = tags


class SearchForm(Form):
    """A simple search form with two different submit buttons."""
    __module__ = __name__
    template = '    <form xmlns:py="http://purl.org/kid/ns#"\n        name="${name}"\n        action="${action}"\n        method="${method}"\n        class="searchform"\n        py:attrs="form_attrs"\n    >\n        <div py:for="field in hidden_fields"\n            py:replace="field.display(value_for(field), **params_for(field))" />\n        <div py:for="field in fields"\n            py:replace="field.display(value_for(field), **params_for(field))" />\n        <div py:for="btn in submit"\n            py:replace="btn.display(btn.label)" />\n    </form>\n    '
    javascript = [
     events, JSLink('cblog', 'javascript/searchform.js')]


class SearchFormFields(WidgetsList):
    __module__ = __name__
    q = TextField('q', label=_('Search post'), help_text=_('Enter search term (case-insensitive).'), attrs=dict(maxlength=50))


class SearchFormSchema(validators.Schema):
    __module__ = __name__
    q = validators.UnicodeString(not_empty=True, max=50, strip=True)


archive_links = ArchiveLinks()
category_links = CategoryLinks()
fancyflash = FancyFlash()
gravatar = Gravatar(url='/gravatar', size=config.get('gravatars.size', 80), rating=config.get('gravatars.rating', 'R'), default=config.get('gravatars.default_image_url', None))
profile = Profile()
search_form = SearchForm(name='searchform', fields=SearchFormFields(), submit=[SubmitButton('title', label=_('Title')), SubmitButton('fulltext', label=_('Text'))], validator=SearchFormSchema())