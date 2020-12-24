# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/whotracksme/website/builder.py
# Compiled at: 2018-05-17 05:30:15
# Size of source mod 2**32: 5850 bytes
import concurrent.futures
from whotracksme.data.loader import DataSource
from whotracksme.website.build.home import build_home
from whotracksme.website.build.blog import build_blogpost_list, build_blogpost_pages, load_blog_posts
from whotracksme.website.build.websites import build_website_list, build_website_pages
from whotracksme.website.build.trackers import build_trackers_list, build_tracker_pages
from whotracksme.website.templates import create_site_structure, copy_custom_error_pages, generate_sitemap
from whotracksme.website.build.companies import build_company_reach_chart_page
from whotracksme.website.utils import print_progress
DATA_DIRECTORY = 'data'
STATIC_PATH = 'static'
DATA_FOLDER = 1
STATIC_FOLDER = 2
TEMPLATES_FOLDER = 4
BLOG_FOLDER = 8
ALL = DATA_FOLDER | STATIC_FOLDER | TEMPLATES_FOLDER | BLOG_FOLDER

class Builder:

    def __init__(self):
        self.data_source = None
        self.blog_posts = None

    def build(self):
        self.feed_event(ALL)

    def on_data_folder_change(self):
        self.feed_event(DATA_FOLDER)

    def on_templates_folder_change(self):
        self.feed_event(TEMPLATES_FOLDER)

    def on_static_folder_change(self):
        self.feed_event(STATIC_FOLDER)

    def on_blog_folder_change(self):
        self.feed_event(BLOG_FOLDER)

    def feed_event(self, event):
        futures = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=9) as (executor):
            if event & STATIC_FOLDER:
                create_site_structure(static_path=STATIC_PATH)
                print_progress(text='Create _site')
            else:
                if self.data_source is None or event & DATA_FOLDER:
                    data_source = DataSource()
                    print_progress(text='Load data sources')
                else:
                    if self.blog_posts is None or event & BLOG_FOLDER:
                        self.blog_posts = load_blog_posts()
                        print_progress(text='Load blog posts')
                    else:
                        if event & DATA_FOLDER or event & TEMPLATES_FOLDER:
                            print_progress(text='Generate error pages')
                            copy_custom_error_pages(data=data_source)
                        if event & DATA_FOLDER or event & TEMPLATES_FOLDER:
                            futures.append(executor.submit(build_home, data=data_source))
                            futures.append(executor.submit(build_trackers_list, data=data_source))
                            futures.append(executor.submit(build_tracker_pages, data=data_source))
                            futures.append(executor.submit(build_website_list, data=data_source))
                            futures.append(executor.submit(build_website_pages, data=data_source))
                            futures.append(executor.submit(build_company_reach_chart_page, data=data_source))
                    if event & DATA_FOLDER or event & BLOG_FOLDER or event & TEMPLATES_FOLDER:
                        futures.append(executor.submit(build_blogpost_list,
                          data=data_source,
                          blog_posts=(self.blog_posts)))
                        futures.append(executor.submit(build_blogpost_pages,
                          data=data_source,
                          blog_posts=(self.blog_posts)))
                if event & DATA_FOLDER or event & BLOG_FOLDER or event & TEMPLATES_FOLDER:
                    futures.append(executor.submit(generate_sitemap,
                      data=data_source,
                      blog_posts=(self.blog_posts)))
            concurrent.futures.wait(futures)
            for future in futures:
                future.result()

            print('Done')