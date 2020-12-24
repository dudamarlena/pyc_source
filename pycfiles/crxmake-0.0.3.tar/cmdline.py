# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/crwy/cmdline.py
# Compiled at: 2020-02-03 23:11:43
from __future__ import print_function
import os, shutil, scrapy
from optparse import OptionParser
from crwy import version
from crwy.settings.default_settings import TEMPLATE_DIR
CRWY_SPIDER_TEMPLATE_DIR = os.path.join(TEMPLATE_DIR, 'spiders')
SCRAPY_SPIDER_TEMPLATE_DIR = os.path.join(scrapy.__path__[0], 'templates/spiders')

def install():
    scrapy_tmpl = os.listdir(SCRAPY_SPIDER_TEMPLATE_DIR)
    for tmpl in os.listdir(CRWY_SPIDER_TEMPLATE_DIR):
        if tmpl in scrapy_tmpl:
            print(('{} exist.').format(tmpl))
            continue
        shutil.copy(os.path.join(CRWY_SPIDER_TEMPLATE_DIR, tmpl), os.path.join(SCRAPY_SPIDER_TEMPLATE_DIR, tmpl))
        print(('{} installed.').format(tmpl))


def uninstall():
    crwy_tmpl = os.listdir(CRWY_SPIDER_TEMPLATE_DIR)
    for tmpl in os.listdir(SCRAPY_SPIDER_TEMPLATE_DIR):
        if tmpl not in crwy_tmpl:
            print(('{} not match, skip.').format(tmpl))
            continue
        os.remove(os.path.join(SCRAPY_SPIDER_TEMPLATE_DIR, tmpl))
        print(('{} uninstalled.').format(tmpl))


def execute():
    parser = OptionParser(usage='Usage: crwy [options] arg1 arg2')
    parser.add_option('-i', '--install', action='store_true', help='install crwy tmpl for scrapy')
    parser.add_option('-u', '--uninstall', action='store_true', help='uninstall crwy tmpl for scrapy')
    parser.add_option('-v', '--version', action='store_true', help='print version')
    options, args = parser.parse_args()
    if options.version:
        print(version)
    elif options.install:
        install()
    elif options.uninstall:
        uninstall()
    else:
        parser.print_help()


if __name__ == '__main__':
    execute()