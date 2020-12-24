# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\apsitemap\main.py
# Compiled at: 2017-10-12 22:46:19
# Size of source mod 2**32: 1597 bytes
from docopt import docopt
from .spider import Spider
from .urlset import UrlSet
from .utility import sitemap_log
_app_doc = "\n     _ _                               \n ___(_) |_ ___ _ __ ___   __ _ _ __    author:   gamelife1314\n/ __| | __/ _ \\ '_ ` _ \\ / _` | '_ \\   homepage: https://github.com/gamelife1314/sitemap\n\\__ \\ | ||  __/ | | | | | (_| | |_) |  email:    fudenglong1417@gmail.com\n|___/_|\\__\\___|_| |_| |_|\\__,_| .__/   version:  0.1\n                              |_|    \n\nUsage: \n    apsitemap  <domain> [options]  \n\nOptions:\n    -h, --help     view help.\n    -v, --version  view version.\n\nUslSet Options:\n    --changefreq <changefreq>   set the update frequency of site. eg: always, hourly, daily, weekly, monthly.\n    --lastmod <lastmod>         set the last modified time. eg: 2016-06-30.\n    --xml-file <xmlfile>        set the name of xmlfile.[default: sitemap.xml]\n    --txt-file <xmlfile>        set the name of xmlfile.[default: sitemap.txt]\n\nLog options:\n    --log-level <level>         set log level, eg: DEBUG, INFO, ERROR, WARNING, CRITICAL.[default: DEBUG]\n"

def main():
    args = docopt(_app_doc, version='0.2.3')
    sitemap_log.setLevel(args['--log-level'].upper())
    urlset = UrlSet(entry=(args['<domain>']), changefreq=(args['--changefreq']), lastmod=(args['--lastmod']))
    spider = Spider(entry=(args['<domain>']), urlset=urlset)
    spider.start()
    urlset.save_xml(args['--xml-file'])
    urlset.save_txt(args['--txt-file'])
    sitemap_log.info('Get %s urls', len(urlset))