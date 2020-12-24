# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tgsociable/widgets.py
# Compiled at: 2007-03-25 06:19:39
import pkg_resources
from turbogears import widgets
import turbogears
resource_dir = pkg_resources.resource_filename('tgsociable', 'static')
widgets.register_static_directory('tgsociable', resource_dir)
from tgsociable.sites import all_sites

class SociableWidget(widgets.Widget):
    __module__ = __name__
    template = '\n<div class="sociable" xmlns:py="http://purl.org/kid/ns#">\n  <span class="sociable_tagline">\n    <strong py:content="sociable_tagline">get_option("sociable_tagline");</strong>\n    <span py:content="sociable_tagline_description">_("These icons link to social bookmarking sites where readers can share and discover new web pages.", \'sociable\')</span>\n  </span>\n\n  <ul>  \n    <li py:for="site in sites">\n      <a py:attrs="site[\'anchor_attrs\']">\n        <img py:attrs="site[\'img_attrs\']" />\n      </a>\n    </li>\n  </ul>\n</div>\n    '
    css = [
     widgets.CSSLink('tgsociable', 'css/sociable.css')]
    javascript = [
     widgets.JSLink('tgsociable', 'javascript/description_selection.js')]
    params_doc = {'active_sites': 'Sites to display sociable icons for', 'sociable_tagline': 'Tag line heading', 'sociable_tagline_description': 'Tag line explanation', 'extra_sites': 'Sites not in the existing sites list that you want to use'}
    params = params_doc.keys()
    active_sites = [
     'Digg', 'Reddit', 'del.icio.us']
    sociable_tagline = 'Share and Enjoy:'
    sociable_tagline_description = 'These icons link to social bookmarking sites where readers can share and discover new web pages.'
    extra_sites = {}

    def update_params(self, d):
        super(SociableWidget, self).update_params(d)
        active_sites = d['active_sites']
        d['sites'] = []
        my_all_sites = all_sites.copy()
        my_all_sites.update(d['extra_sites'])
        for sitename in active_sites:
            if sitename not in my_all_sites:
                continue
            site = my_all_sites[sitename]
            url = site['url']
            url = url.replace('PERMALINK', d['post_url'])
            url = url.replace('TITLE', d['post_title'])
            url = url.replace('RSS', d['blog_rss'])
            url = url.replace('BLOGNAME', d['blog_name'])
            sociable_version = '2.0'
            url = url.replace('VERSION', sociable_version)
            anchor_attrs = {}
            anchor_attrs['href'] = url
            if 'description' in site:
                anchor_attrs['onfocus'] = "sociable_description_link(this, '%s')" % (site['description'],)
            img_attrs = {}
            img_attrs['src'] = site['favicon']
            img_attrs['title'] = sitename
            img_attrs['alt'] = sitename
            img_attrs['class'] = 'sociable_hovers'
            if 'class' in site:
                img_attrs['class'] += ' ' + site['class']
            d['sites'].append(dict(anchor_attrs=anchor_attrs, img_attrs=img_attrs))