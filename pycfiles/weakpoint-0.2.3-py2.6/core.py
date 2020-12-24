# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/weakpoint/core.py
# Compiled at: 2012-11-21 04:54:41
from argparse import ArgumentParser
from pkg_resources import resource_filename, load_entry_point
from weakpoint import __version__
from weakpoint.fs import Directory, File
from weakpoint.utils import normpath
from weakpoint.config import Config
from weakpoint.parsers import markdown
from weakpoint.renderers import Renderer
from weakpoint.exceptions import OptionException, RendererException
from weakpoint.slides import Slides
from copy import deepcopy
import sys

class WeakPoint(object):
    default_config = {'markup': 'markdown,'}

    def __init__(self, args=None):
        self.opts = self._get_opts(args)
        self.opts['func']()

    def generate(self):
        self.src = Directory('.')
        self._load_config()
        html = self._parse()
        htmldump = Slides(html)
        slides = htmldump.slides
        navi = htmldump.navi
        variables = {}
        variables.update(self.config)
        variables['slides'] = slides
        variables['navi'] = navi
        rendered = self._render(variables)
        out = File('index.html')
        if out.exists:
            out.rm()
        File('index.html', rendered).mk()

    def init(self):
        self.dest = Directory(self.opts['dest'])
        self.src = Directory(self._get_theme(self.opts['theme']))
        if not self.src.exists:
            raise OptionException('Theme not found.')
        self.src.cp(self.dest.path)

    def _render(self, variables):
        try:
            return Renderer(self.src.path).render('layout.html', variables)
        except RendererException, e:
            print e
            sys.exit(1)

    def _parse(self):
        path = File(normpath(self.src.path, 'slides.md'))
        if not path.exists:
            print 'slides.md is required, abort'
            sys.exit(1)
        if self.config['markup'] == 'markdown':
            return markdown.Parser().parse(path.content)
        print ('no such markup: {0}').format(config['markup'])
        sys.exit(1)

    def _load_config(self):
        self.config = deepcopy(self.default_config)
        f = File(normpath(self.src.path, 'config.yaml'))
        if f.exists:
            self.config.update(Config(f.content))
        else:
            print 'missing config.yaml, abort'
            sys.exit(1)

    def _get_theme(self, theme):
        return resource_filename(__name__, ('themes/{0}').format(theme))

    def _get_opts(self, args):
        opts = {}
        parser = ArgumentParser()
        subparser = parser.add_subparsers()
        parser.add_argument('-V', '--version', action='version', version=('{0}').format(__version__), help="Show %(prog)s's version.")
        gen = subparser.add_parser('gen')
        gen.set_defaults(func=self.generate)
        init = subparser.add_parser('init')
        init.set_defaults(func=self.init)
        init.add_argument('dest', metavar='destination', help='The location %(prog)s initializes.')
        init.add_argument('-t', '--theme', default='light', help='Sets the theme of slideshow.')
        for (option, value) in vars(parser.parse_args(args)).iteritems():
            if value is not None:
                if isinstance(option, str):
                    option = option.decode('utf-8')
                if isinstance(value, str):
                    value = value.decode('utf-8')
                opts[option] = value

        return opts