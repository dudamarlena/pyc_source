# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/cpen/codepen_downloader.py
# Compiled at: 2018-11-20 01:05:21
# Size of source mod 2**32: 1742 bytes
import requests
from bs4 import BeautifulSoup
from jinja2 import Template
import re, json, os, sys, shutil
extract_regex = '[a-zA-z]+/pen/[a-zA-z]{6}'
with open(os.path.join(os.path.dirname(__file__), 'templates', 'index.html')) as (template):
    index_html_template = Template(template.read())

def download_codepen(codepen_url, target_directory=None):
    parsed_url = re.search(extract_regex, codepen_url).group()
    codepen = BeautifulSoup(requests.get('https://codepen.io/{}'.format(parsed_url)).text, 'html.parser')
    if target_directory is None:
        target_directory = codepen.find('title').text
    data = json.loads(codepen.find(id='init-data')['value'])
    resources = json.loads(data['__item'])['resources']
    html = codepen.find('pre', id='html').find('code').text.strip()
    js = codepen.find('pre', id='js').find('code').text.strip()
    css = codepen.find('pre', id='css').find('code').text.strip()
    if os.path.exists(target_directory):
        shutil.rmtree(target_directory)
    os.makedirs(target_directory)
    with open(os.path.join(target_directory, 'index.html'), 'w') as (index_html):
        index_html.write((index_html_template.render)(**locals()))
    if css:
        with open(os.path.join(target_directory, 'main.css'), 'w') as (main_css):
            main_css.write(css)
    if js:
        with open(os.path.join(target_directory, 'main.js'), 'w') as (main_js):
            main_js.write(js)


def main(args=sys.argv[1:]):
    if not args:
        print('Usage:\ncpen <url> <target folder>')
    else:
        download_codepen(args[0], args[1] if len(args) > 1 else None)


if __name__ == '__main__':
    main()