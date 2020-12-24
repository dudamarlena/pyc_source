# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/bxt_description_generator/bxt_description_generator.py
# Compiled at: 2009-11-07 23:29:25
"""
This software is licensed under version 2.0 of the WTFPL (see COPYING for details)
"""
import sys, os, re
from models import *
from jinja2 import Environment, PackageLoader
reload(sys)
sys.setdefaultencoding('utf-8')

def absolute_path(path):
    """ Get the absolute path of a file, from this script """
    ROOT = os.path.dirname(os.path.realpath(__file__))
    os.path.join(ROOT, path)
    return os.path.join(ROOT, path)


def cleanify(name):
    """ Strip out some things that don't play well in element ids """
    return re.sub("[\\. ']", '_', name)


def main():
    try:
        directory = sys.argv[1]
        template = sys.argv[2]
    except IndexError:
        try:
            import easygui
            directory = None
            while not directory:
                directory = easygui.diropenbox('Where are the files?')

            template = None
            while not template:
                template = easygui.choicebox('What template do you want?', choices=os.listdir(absolute_path('templates')))

        except ImportError:
            sys.stderr.write('Usage: ' + sys.argv[0] + ' <directory> <template>\n')
            exit()

    root = Folder(directory)
    root.scan()
    env = Environment(loader=PackageLoader('bxt_description_generator', 'templates'))
    env.filters['cleanify'] = cleanify
    template = env.get_template(template)
    output = template.render(root=root).encode('utf-8')
    try:
        easygui.codebox(text=output)
    except NameError:
        print output

    return


if __name__ == '__main__':
    sys.exit(main())