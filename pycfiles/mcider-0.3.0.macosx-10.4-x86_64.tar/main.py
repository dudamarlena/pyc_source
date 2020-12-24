# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ogom/.pyenv/versions/2.7.6/lib/python2.7/site-packages/mcider/main.py
# Compiled at: 2014-12-15 17:58:57
""" mcider - main
Copyright(c) 2012-2014 ogom

Mcider is to convert markdown into slideshow.
"""
from __future__ import print_function
import os, webbrowser
from . import cli_helper
from . import converter
from . import util

def main():
    """ entry points """
    args = cli_helper.parser.parse_args()
    output_path = os.path.abspath(os.path.dirname(args.file.name))
    output_file = os.path.join(output_path, os.path.splitext(os.path.basename(args.file.name))[0] + '.html')
    if args.output:
        output_path = os.path.abspath(os.path.dirname(args.output.name))
        output_file = os.path.abspath(args.output.name)
    _contents = args.file.read().decode('utf-8') if util.py2k else args.file.read()
    opts = {'themes': args.themes, 
       'theme': args.theme, 
       'contents': _contents, 
       'extensions': args.extensions, 
       'clean': args.clean}
    if opts['themes'] is None or not os.path.isdir(opts['themes']):
        opts['themes'] = os.path.abspath(os.path.join(os.path.dirname(__file__), 'themes'))
    try:
        try:
            slide = converter.Slide(opts)
            html = slide.maker(output_path)
            util.fs_writer(output_file, html)
            if args.browser:
                url = 'file://' + output_file
                if slide.options['theme'] == 'io2012':
                    url += '?presentme='
                    url += 'true' if args.presenter else 'false'
                webbrowser.open_new_tab(url)
        except KeyError as e:
            print('KeyError: %s' % e)
        else:
            print('Output file is %s' % output_file)

    finally:
        print('Mcider is finished!')

    return


if __name__ == '__main__':
    main()