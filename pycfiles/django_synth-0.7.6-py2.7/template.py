# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\django_synth\template.py
# Compiled at: 2014-09-09 12:03:27
from __future__ import print_function
import datetime, django, django.template.base as base, django.utils.timezone as tz, django.utils.translation as tr, functools, re, synth, sys
from inspect import getargspec, getsource
from django.conf import settings
from django.core import urlresolvers
from django.template import generic_tag_compiler, StringOrigin, TemplateSyntaxError
if not settings.configured:
    settings.configure()
if hasattr(django, 'setup'):
    django.setup()
default_formats = {'TEMPLATE_STRING_IF_INVALID': settings.TEMPLATE_STRING_IF_INVALID, 
   'DATE_FORMAT': settings.DATE_FORMAT, 
   'DATETIME_FORMAT': settings.DATETIME_FORMAT, 
   'MONTH_DAY_FORMAT': settings.MONTH_DAY_FORMAT, 
   'SHORT_DATE_FORMAT': settings.SHORT_DATE_FORMAT, 
   'SHORT_DATETIME_FORMAT': settings.SHORT_DATETIME_FORMAT, 
   'TIME_FORMAT': settings.TIME_FORMAT, 
   'YEAR_MONTH_FORMAT': settings.YEAR_MONTH_FORMAT}
engine = getattr(settings, 'SYNTH_ENGINE', 'django')
directories = getattr(settings, 'SYNTH_DIRECTORIES', list(settings.TEMPLATE_DIRS or []))
debug = getattr(settings, 'SYNTH_DEBUG', bool(settings.TEMPLATE_DEBUG))
cache = getattr(settings, 'SYNTH_CACHE', not debug)
formats = getattr(settings, 'SYNTH_FORMATS', default_formats)
print('Loaded synth; version: %s; default engine: %s; debug: %s.' % (
 synth.version(), engine, debug), file=sys.stderr)

def load_library(name):
    return SynthLibrary(base.get_library(name))


caching_off = synth.CACHE_NONE
caching_on = synth.CACHE_ALL | synth.CACHE_PER_PROCESS
caching = caching_off if debug else caching_on
synth.Template.set_default_options({'formats': formats, 
   'debug': debug, 
   'directories': directories, 
   'loaders': [
             load_library], 
   'resolvers': [
               urlresolvers], 
   'caching': caching})

class NullContextManager(object):

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        pass


noop = NullContextManager()

class Timer(object):

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.start = datetime.datetime.now()

    def __exit__(self, type, value, traceback):
        now = datetime.datetime.now()
        ms = (now - self.start).microseconds // 1000
        print('[synth] %s: %dms' % (self.name, ms), file=sys.stderr)


class SynthTemplate(object):

    def __init__(self, template_string, dirs=None, name=None, origin=None):
        if debug and origin is None:
            origin = StringOrigin(template_string)
        self.nodelist = SynthTemplateNodeList(template_string, dirs, name)
        self.name = name
        self.origin = origin
        return

    def __iter__(self):
        for node in self.nodelist:
            for subnode in node:
                yield subnode

    def _render(self, context):
        return self.nodelist.render(context)

    def render(self, context):
        """Display stage -- can be called many times"""
        context.render_context.push()
        try:
            return self._render(context)
        finally:
            context.render_context.pop()


class SynthLibrary(object):

    def __init__(self, library):
        self.tags = {name:wrap_tag(name, fn) for name, fn in getattr(library, 'tags', {}).items()}
        self.filters = {name:wrap_filter(name, fn) for name, fn in getattr(library, 'filters', {}).items()}


class SynthParser(base.Parser):

    def __init__(self, segments):
        super(SynthParser, self).__init__(list(map(SynthToken, segments)))
        self.index = 0

    def advance_until(self, tag_names):
        while self.index + 1 < len(self.tokens) and self.tokens[(self.index + 1)].contents not in tag_names:
            self.index += 1

    def parse(self, tag_names=None):
        if tag_names:
            self.advance_until(tag_names)
        return SynthTokenNodeList(self.tokens[(self.index - 1)])

    def skip_past(self, tag_name):
        self.advance_until((tag_name,))

    def next_token(self):
        i = self.index
        self.index += 1
        return self.tokens[i]

    def delete_first_token(self):
        self.index += 1


class SynthToken(base.Token):

    def __init__(self, segment):
        self.pieces, self.renderer = segment
        contents = self.pieces[0]
        super(SynthToken, self).__init__(base.TOKEN_BLOCK, contents)

    def split_contents(self):
        return self.pieces[1:]


class SynthTokenNodeList(base.NodeList):

    def __init__(self, token):
        super(SynthTokenNodeList, self).__init__()
        self.synth_renderer = token.renderer

    def render(self, context):
        return self.synth_renderer(context, get_options_from(context))


class SynthTemplateNodeList(base.NodeList):

    def __init__(self, source, dirs, name):
        super(SynthTemplateNodeList, self).__init__()
        try:
            options = None if not dirs else {'directories': dirs}
            with Timer('parsing') if debug else noop:
                self.synth_template = synth.Template(source, engine, options)
        except RuntimeError as e:
            message = str(e)
            if 'parsing error' in message or 'missing tag' in message:
                location = ' (%s)' % name if name else ''
                raise TemplateSyntaxError(message + location)
            else:
                raise

        return

    def render(self, context):
        with Timer('rendering') if debug else noop:
            return self.synth_template.render_to_string(context)


def get_options_from(context):
    if context.use_tz or tz.get_current_timezone_name() != tz.get_default_timezone_name():
        timezone = tz.get_current_timezone()
    else:
        timezone = None
    options = {'caseless': False, 
       'safe': not context.autoescape, 
       'application': context.current_app, 
       'timezone': timezone, 
       'language': None if not context.use_i18n else (get_language(), get_language_bidi()), 
       'formats': None if not context.use_l10n else {}}
    return options


def render_node(node, context, options, args, kwargs):
    if not options:
        return node.render(context)
    safe = options['safe']
    application = options['application']
    timezone = options['timezone']
    language = options['language']
    localized = options['localized']
    context.autoescape = not safe
    context.current_app = application
    context.use_tz = bool(timezone)
    context.use_i18n = bool(language)
    context.use_l10n = bool(localized)
    if language:
        tr.activate(language[0])
    if localized:
        pass
    with tz.override(timezone) if timezone else noop:
        return node.render(context)


def get_arg_names(name, tag):
    try:
        return tag.func_code.co_varnames
    except:
        try:
            return tuple(getargspec(tag)[0])
        except:
            raise Exception('Unable to get arguments names for tag: ' + name)


CUSTOM_ARGUMENT_NAMES = ('parser', 'token')
string_literal = '\\s*(?:\'(\\w+)\'|"(\\w+)")\\s*'
string_literals = string_literal + '(?:,' + string_literal + ')*(,\\s*)?'
tag_name_pattern = re.compile('parser\\.parse\\(\\s*\\(' + string_literals + '\\)\\s*\\)')

def wrap_filter(name, fn):
    return lambda value, *args, **kwargs: fn(value, *args)


def wrap_tag(name, fn):
    middle_names, last_names, is_pure = None, None, False
    if isinstance(fn, functools.partial) and fn.func == generic_tag_compiler:
        pass
    else:
        arg_names = get_arg_names(name, fn)
        if arg_names[:2] != CUSTOM_ARGUMENT_NAMES:
            raise Exception('Invalid tag argument names: %s' % arg_names)
        if name == 'blocktrans':
            middle_names = frozenset(('plural', ))
            last_names = frozenset(('endblocktrans', ))
        else:
            source = getsource(fn)
            names = [ item for sublist in tag_name_pattern.findall(source) for item in sublist if item ]
            if names:
                middle_names = frozenset([ name for name in names if not name.startswith('end') ])
                last_names = frozenset([ name for name in names if name.startswith('end') ] or ['end' + name])

    def tag_wrapper(segments):
        parser = SynthParser(segments)
        node = fn(parser, parser.next_token())
        return lambda context, options, *args, **kwargs: render_node(node, context, options, args, kwargs)

    return (
     tag_wrapper, middle_names, last_names, is_pure)


class SynthContext(base.Context):
    pass