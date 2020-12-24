# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/icy/code/vite/.env/lib/python3.7/site-packages/vite/vite.py
# Compiled at: 2019-10-02 11:57:00
# Size of source mod 2**32: 7451 bytes
"""
Vite - A simple and minimal static site generator that JustWorks™
Author: Anirudh <icyph0x@pm.me>
License: MIT
"""
import sys, pathlib, os, jinja2, time, http.server, socketserver, shutil, datetime
from markdown2 import markdown_path
from huepy import *
from livereload import Server
from subprocess import call
PAGES_PATH = 'pages/'
BUILD_PATH = 'build/'
TEMPL_PATH = 'templates/'
TEMPL_FILE = ''
PORT = 1911

def import_config():
    global TEMPL_FILE
    try:
        sys.path.append(os.getcwd())
        globals()['config'] = __import__('config')
        TEMPL_FILE = os.path.join(TEMPL_PATH, config.template)
    except ImportError:
        print(bad('Error: config.py not found.'))
        print(que("Are you sure you're in a project directory?"))
        sys.exit(1)


def create_project(path):
    try:
        abs_path = pathlib.Path(path).resolve()
        cur_path = pathlib.Path('.').resolve()
        os.makedirs(os.path.join(path, 'build'))
        os.mkdir(os.path.join(path, 'pages'))
        os.mkdir(os.path.join(path, 'templates'))
        os.mkdir(os.path.join(path, 'static'))
        create_config(path)
        create_template(path)
        print(good('Created project directory at %s.' % abs_path))
    except FileExistsError:
        print(bad('Error: specified path exists.'))


def create_path(path):
    head, tail = os.path.split(path)
    now = datetime.datetime.now()
    today = now.strftime('%Y-%m-%d')
    try:
        os.makedirs(os.path.join(PAGES_PATH, head))
    except FileExistsError:
        pass

    if os.path.exists(os.path.join(PAGES_PATH, head, tail)):
        print(bad('Error: specified path exists.'))
    else:
        with open(os.path.join(PAGES_PATH, head, tail), 'w') as (f):
            to_write = '---\ntemplate:\ntitle:\nsubtitle:\ndate: {t}\n---\n'.format(t=today)
            f.write(to_write)
        print(good('Created %s.') % os.path.join(PAGES_PATH, head, tail))


def create_config(path):
    with open(os.path.join(path, 'config.py'), 'w') as (f):
        f.write("# config.py - Vite's configuration script\n\ntitle = ''\nauthor = ''\nheader = ''\nfooter = '' \npost_build = []\ntemplate = 'index.html'  # default is index.html\n")


def create_template(path):
    with open(os.path.join(path, 'templates', 'index.html'), 'w') as (f):
        f.write('<!DOCTYPE html>\n<html>\n<header>\n\t{{ header }}\n\t<title>\n\t\t{{ title }}\t\n\t</title>\n</header>\n\n<body>\n\t{{ body }}\n</body>\n\n<footer>\n\t{{ footer }}\n\t<p> {{ author }} </p>\n<footer>\n\n                ')


def jinja_render(html, tmpl):
    template_loader = jinja2.FileSystemLoader('./')
    env = jinja2.Environment(loader=template_loader)
    try:
        template = env.get_template(tmpl)
        meta = html.metadata
        output = template.render(title=(meta['title'] if 'title' in meta else config.title), author=(meta['author'] if 'author' in meta else config.author),
          header=(meta['header'] if 'header' in meta else config.header),
          footer=(meta['footer'] if 'footer' in meta else config.footer),
          date=(meta['date'] if 'date' in meta else ''),
          subtitle=(meta['subtitle'] if 'subtitle' in meta else ''),
          body=html)
        return output
    except jinja2.exceptions.TemplateNotFound:
        print(bad('Error: specified template not found: %s' % tmpl))
        sys.exit(1)


def fm_template(metadata):
    try:
        page_template = os.path.join(os.path.join(TEMPL_PATH, metadata['template']))
    except KeyError:
        page_template = TEMPL_FILE

    return page_template


def markdown_render(filename):
    html = markdown_path((os.path.join(PAGES_PATH, filename)), extras=['metadata', 'fenced-code-blocks', 'header-ids', 'footnotes', 'smarty-pants'])
    return html


def html_gen():

    def index_render(f, d=''):
        index_html = markdown_render(os.path.join(d, f))
        output = jinja_render(index_html, fm_template(index_html.metadata))
        with open(os.path.join(BUILD_PATH, d, 'index.html'), 'w') as (ff):
            ff.write(output)
            if d:
                print(run('Rendered ' + white('%s/%s') % (d, f)))
            else:
                print(run('Rendered ' + white('%s') % f))

    def normal_render(f, d=''):
        html_text = markdown_render(os.path.join(d, f))
        html_file = os.path.splitext(os.path.join(BUILD_PATH, d, f))[0]
        os.mkdir(html_file)
        output = jinja_render(html_text, fm_template(html_text.metadata))
        with open(os.path.join(html_file, 'index.html'), 'w') as (ff):
            ff.write(output)
            if d:
                print(run('Rendered ' + white('%s/%s') % (d, f)))
            else:
                print(run('Rendered ' + white('%s') % f))

    for root, dirs, files in os.walk(PAGES_PATH):
        for d in dirs:
            os.mkdir(os.path.join(BUILD_PATH, d))
            for f in os.listdir(os.path.join(PAGES_PATH, d)):
                if os.path.splitext(f)[1] != '.md':
                    shutil.copyfile(os.path.join(PAGES_PATH, d, f), os.path.join(BUILD_PATH, d, f))
                    print(run('Copied ' + white('%s/%s') % (d, f)))
                elif f == '_index.md':
                    index_render(f, d)
                else:
                    normal_render(f, d)

    for f in os.listdir(PAGES_PATH):
        if os.path.isfile(os.path.join(PAGES_PATH, f)):
            if os.path.splitext(f)[1] != '.md':
                shutil.copyfile(os.path.join(PAGES_PATH, f), os.path.join(BUILD_PATH, f))
                print(run('Copied ' + white('%s') % f))
            elif f == '_index.md':
                index_render(f)
            else:
                normal_render(f)


def server():
    server = Server()
    try:
        print(run(f"Serving the {italic(yellow('build'))} directory at {white(http://localhost:{PORT})}"))
        print(white('Ctrl+C') + ' to stop.')
        server.serve(port=PORT, root='build/')
    except KeyboardInterrupt:
        print(info('Stopping server.'))
        sys.exit(1)


def clean():
    for f in os.listdir(BUILD_PATH):
        fpath = os.path.join(BUILD_PATH, f)
        try:
            if os.path.isfile(fpath):
                os.unlink(fpath)
            else:
                if os.path.isdir(fpath):
                    shutil.rmtree(fpath)
        except Exception as e:
            try:
                print(e)
            finally:
                e = None
                del e


def builder():
    path = os.getcwd()
    start = time.process_time()
    if not os.listdir(os.path.join(path, PAGES_PATH)):
        print(info(italic('pages') + ' directory is empty. Nothing to build.'))
        sys.exit(1)
    else:
        clean()
        html_gen()
        if os.path.exists(os.path.join(os.getcwd(), 'static')):
            shutil.copytree(os.path.join(os.getcwd(), 'static'), os.path.join(BUILD_PATH, 'static'))
        print(good('Done in %0.5fs.' % (time.process_time() - start)))
    try:
        if config.post_build != '':
            print(run('Running post-build actions...'))
            for s in config.post_build:
                print(info((f"{s}")))
                call([s])

    except AttributeError:
        pass