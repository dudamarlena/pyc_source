# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/whotracksme/website/build/websites.py
# Compiled at: 2018-05-17 05:30:15
# Size of source mod 2**32: 2574 bytes
from operator import itemgetter
from jinja2 import Markup
from whotracksme.website.utils import print_progress
from whotracksme.website.build.companies import tracker_map_data, website_doughnout
from whotracksme.website.templates import get_template, render_template
from whotracksme.website.plotting.plots import profile_doughnut
from whotracksme.website.plotting.sankey import sankey_plot

def build_website_list(data):
    header_numbers = data.sites.summary_stats()
    sorted_websites = data.sites.sort_by(metric='popularity', descending=True)
    sorted_websites_cat = data.sites.sort_by(metric='category', descending=True)
    with open('_site/websites.html', 'w') as (output):
        output.write(render_template(template=(get_template(data, 'websites.html')),
          website_list=sorted_websites,
          website_list_cat=sorted_websites_cat,
          header_numbers=header_numbers))
    print_progress(text='Generate website list')


def website_page(template, site, rank, data):
    site_id = site.site
    website_url = f"www.{site_id}"
    profile = {'rank':rank, 
     'website_url':website_url, 
     'name':site.site}
    methods = {'cookies':site.cookies > 0.2, 
     'fingerprinting':site.bad_qs > 0.1}
    sankey_data = tracker_map_data(site_id, data)
    d_values, d_labels, d_total = website_doughnout(site_id, data)
    profile_dough = Markup(profile_doughnut(d_values, d_labels, d_total))
    rendered_sankey = Markup(sankey_plot(sankey_data))
    tracker_table = data.sites.trackers.get_site(site_id)
    with open('_site/websites/{}.html'.format(site.site), 'w') as (output):
        output.write(render_template(path_to_root='..',
          template=template,
          site={'overview': site._asdict()},
          profile=profile,
          methods=methods,
          sankey=rendered_sankey,
          doughnut=profile_dough,
          tracker_categories=d_labels,
          tracker_list=tracker_table))


def build_website_pages(data):
    template = get_template(data, 'website-page.html', path_to_root='..')
    for rank, site in enumerate(data.sites.sort_by(metric='popularity', descending=True).itertuples()):
        website_page(template, site, rank + 1, data)

    print_progress(text='Generate website pages')