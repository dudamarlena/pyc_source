# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/aam/generator/render.py
# Compiled at: 2014-06-25 05:34:25
import os, shutil
from aam.options import *
from aam.utils import mkdir
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

def render():
    env = Environment(loader=FileSystemLoader(hub.root.template_path, encoding='utf-8'), autoescape=False)
    env.globals.update(title=hub.site.name, site_url=hub.site.url.strip().lstrip().rstrip('/'), site_name=hub.site.name.strip().lstrip(), site_owner=hub.site.owner, pages=hub.site.pages, repo_switch=hub.site.repo_switch, book_switch=hub.site.book_switch, analytics=hub.site.analytics)
    if not os.path.exists(hub.site.deploy_path):
        print "Can't find deploy folder. Please creat a new one or use 'aam init'."
        exit(1)
    shutil.rmtree(hub.site.deploy_path)
    os.chdir(hub.site.path)
    mkdir('deploy')
    for page in hub.site.pages:
        if page['type'] == 'page':
            output_path = os.path.join(hub.site.path, 'deploy/%s' % page['link'])
            html = env.get_template('page.html').render(title=hub.site.name + ' | ' + page['title'], page=page)
            with open(output_path, 'w') as (f):
                f.write(html)
        elif page['type'] == 'home':
            home = env.get_template('home.html').render(home=page)
            output_path = os.path.join(hub.site.deploy_path, 'Home.html')
            with open(output_path, 'w') as (f):
                f.write(home)

    if hub.site.repo_switch:
        html = env.get_template('repo.html').render(title=hub.site.name + ' | ' + 'Github Repo', repos=hub.site.github_repo)
        with open(os.path.join(hub.site.deploy_path, 'github_repo.html'), 'w') as (f):
            f.write(html)
    if hub.site.book_switch:
        html = env.get_template('douban.html').render(title=hub.site.name + ' | ' + 'Douban Book', douban_name=hub.site.douban_name)
        with open(os.path.join(hub.site.deploy_path, 'douban_book.html'), 'w') as (f):
            f.write(html)
    shutil.copytree(hub.root.static_path, hub.site.static_path)