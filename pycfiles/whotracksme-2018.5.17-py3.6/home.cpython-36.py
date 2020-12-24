# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/whotracksme/website/build/home.py
# Compiled at: 2018-05-17 05:30:15
# Size of source mod 2**32: 1194 bytes
from jinja2 import Markup
from whotracksme.website.plotting.companies import overview_bars
from whotracksme.website.build.companies import company_reach
from whotracksme.website.utils import print_progress
from whotracksme.website.templates import get_template, render_template
from whotracksme.website.build.blog import load_blog_posts

def build_home(data):
    top10 = company_reach(data.companies)
    header_graph = Markup(overview_bars(top10))
    posts = load_blog_posts()[:3]
    with open('_site/index.html', 'w') as (output):
        output.write(render_template(template=(get_template(data, 'index.html')),
          ts=header_graph,
          tracker_list=(data.trackers.sort_by(metric='reach')[:20]),
          trackers_list_company=(data.trackers.sort_by(metric='company_id')[:20]),
          most_tracked_sites=(data.sites.sort_by(metric='trackers')[:20]),
          least_tracked_sites=(data.sites.sort_by(metric='trackers', descending=False)[:20]),
          websites=(data.sites.summary_stats()),
          tracker_stats=(data.trackers.summary_stats()),
          top10=top10,
          posts=posts))
    print_progress(text='Generate home page')