# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jenkviz/command.py
# Compiled at: 2012-01-25 11:56:32
__author__ = 'Benoit Delbosc'
__copyright__ = 'Copyright (C) 2012 Nuxeo SA <http://nuxeo.com>'
import os, logging
from model import open_db, close_db, list_builds
from crawl import Crawl
from graphviz import graphviz

def cmd_list(args, options):
    db = open_db(options)
    list_builds(db)
    close_db(db)
    return 0


def cmd_crawl(args, options):
    if len(args) != 1:
        logging.error('Missing build URL')
        return 1
    if options.to_file and not os.path.exists(options.to_file):
        os.mkdir(options.to_file)
    if options.from_file and not os.path.exists(options.from_file):
        os.mkdir(options.from_file)
    db = open_db(options)
    crawl = Crawl(db, options)
    if options.reverse:
        roots = crawl.reverse_crawl(args[0])
    else:
        roots = crawl.crawl(args[0])
    close_db(db)
    stat = roots[0].extra
    logging.info('Started: %s\n\tend: %s\n\telapsed: %s\n\tduration: %ss\n\tNb builds: %s\n\ttrhoughput: %s\n' % (
     stat['start'], stat['stop'], stat['elapsed'], stat['duration'], stat['count'], stat['throughput']))
    if not options.output:
        svg_file = roots[0].getId() + '.svg'
    else:
        svg_file = options.output
    graphviz(roots, svg_file)
    logging.info('%s generated.' % svg_file)
    return 0


def cmd_info(args, options):
    if len(args) != 1:
        logging.error('Missing bid')
        return 1
    db = open_db(options)
    close_db(db)
    return 0


def cmd_report(args, options):
    if len(args) != 1:
        logging.error('Missing bid')
        return 1
    if not options.output:
        logging.error('Missing --output option')
        return 1
    db = open_db(options)
    close_db(db)
    return 0