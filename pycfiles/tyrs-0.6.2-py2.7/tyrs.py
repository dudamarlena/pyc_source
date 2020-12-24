# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tyrs/tyrs.py
# Compiled at: 2011-12-23 08:19:16
"""
   Tyrs

   @author:     Nicolas Paris <nicolas.caen@gmail.com>
   @date:       23/12/2011
   @licence:    GPLv3

"""
__revision__ = '0.6.2'
import sys, utils, config, locale, tweets, argparse, gettext
from urllib2 import URLError
from timeline import Timeline
from container import Container
from interface import Interface
from completion import Completion
locale.setlocale(locale.LC_ALL, '')
container = Container()

def arguments():
    """
    Parse all arguments from the CLI
    """
    parser = argparse.ArgumentParser('Tyrs: a twitter client writen in python with curses.')
    parser.add_argument('-a', '--account', help='Use another account, store in a different file.')
    parser.add_argument('-c', '--config', help='Use another configuration file.')
    parser.add_argument('-g', '--generate-config', help='Generate a default configuration file.')
    parser.add_argument('-v', '--version', action='version', version='Tyrs %s' % __revision__, help='Show the current version of Tyrs')
    args = parser.parse_args()
    return args


def main():
    utils.set_console_title()
    init_conf()
    init_tyrs()


def init_tyrs():
    init_timelines()
    init_api()
    init_interface()


def init_conf():
    conf = config.Config(arguments())
    container.add('conf', conf)


def init_api():
    api = tweets.Tweets()
    container.add('api', api)
    try:
        api.authentication()
    except URLError as e:
        print 'error:%s' % e
        sys.exit(1)


def init_interface():
    user_interface = Interface()
    container.add('interface', user_interface)


def init_timelines():
    buffers = ('home', 'mentions', 'direct', 'search', 'user', 'favorite', 'thread',
               'user_retweet')
    timelines = {}
    for buff in buffers:
        timelines[buff] = Timeline(buff)

    container.add('timelines', timelines)
    container.add('buffers', buffers)
    completion = Completion()
    container.add('completion', completion)


if __name__ == '__main__':
    gettext.install('tyrs', unicode=1)
    main()