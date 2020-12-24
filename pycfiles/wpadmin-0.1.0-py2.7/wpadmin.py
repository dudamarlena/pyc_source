# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\wpadmin.py
# Compiled at: 2014-06-15 18:25:01
"""
For usage and a list of options, try this:
$ python wpadmin.py -h
"""
__version__ = '0.1.0'
import os
from functools import wraps

class NotInWordPressRootError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def wp_root(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if os.path.isdir(os.path.join(os.getcwd(), 'wp-content', 'themes')) and os.path.isdir(os.path.join(os.getcwd(), 'wp-content', 'plugins')):
            return f(*args, **kwargs)
        raise NotInWordPressRootError('You must run this script from                                       the WordPress root folder.')

    return decorated_function


@wp_root
def starttheme(args):
    """Creates theme folder with the following empty files/folders:
    index.php, style.css, images/, css/ and js/. If with_timber is
    True then it additionally creates views/base.twig
    """
    theme_root = os.path.join(os.getcwd(), 'wp-content', 'themes', args.name)
    os.makedirs(theme_root)
    for f in ['index.php', 'README.md', 'style.css', 'functions.php',
     '404.php']:
        fh = open(os.path.join(theme_root, f), 'w')
        if '.php' in f:
            fh.write('<?php\n\n')
        fh.close()

    if args.classic:
        static_dir = theme_root
    else:
        static_dir = os.path.join(theme_root, 'static')
        os.makedirs(static_dir)
        functionsphp = open(os.path.join(theme_root, 'functions.php'), 'a')
        functionsphp.write("Timber::$dirname = 'templates';\n")
        functionsphp.close()
        twig_templates = os.path.join(theme_root, 'templates')
        os.makedirs(os.path.join(twig_templates))
        open(os.path.join(twig_templates, 'base.twig'), 'a').close()
    for d in ['images', 'css', 'js']:
        os.makedirs(os.path.join(static_dir, d))


@wp_root
def startplugin(args):
    """Creates plugin folder with a php file of the same name."""
    plugin_root = os.path.join(os.getcwd(), 'wp-content', 'plugins', args.name)
    os.makedirs(plugin_root)
    open(os.path.join(plugin_root, 'README.md'), 'a').close()
    f = open(os.path.join(plugin_root, args.name + '.php'), 'w')
    f.write('<?php\n\n')
    f.close()


def _main():
    """Parse options and execute wpadmin commands"""
    import argparse
    parser = argparse.ArgumentParser(description='Create WordPress                                      theme/plugin skeleton')
    subparsers = parser.add_subparsers()
    parser_starttheme = subparsers.add_parser('starttheme')
    parser_starttheme.add_argument('name')
    parser_starttheme.add_argument('-c', '--classic', help='create classic theme                                     skeleton', action='store_true')
    parser_starttheme.set_defaults(func=starttheme)
    parser_startplugin = subparsers.add_parser('startplugin')
    parser_startplugin.add_argument('name')
    parser_startplugin.set_defaults(func=startplugin)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    _main()