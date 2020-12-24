# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rulebox\bbcode.py
# Compiled at: 2010-12-21 14:32:54
"""A set of rules used to transform BBCode into HTML.

-----------------------------
Example Usage
-----------------------------

::

    from cgi import escape
    import suit # easy_install suit
    from rulebox import bbcode
    rules = bbcode.rules
    # Load the BBCode templates
    for key, value in rules.items():
        if 'var' in value and 'label' in value['var']:
            rules[key]['var']['template'] = open(
                os.path.join(
                    'bbcode',
                    value['var']['label'] + '.tpl'
                )
            ).read()
    code = escape(
        '[b]Test[/b],
        True
    ).replace('
','<br />
')
    config = {
        'escape': ''
    }
    print suit.execute(rules, code, config)
    # Result: assuming it loaded the default templates, "<strong>Test</strong>"

Basic usage; see http://www.suitframework.com/docs/ for how to use other rules.

-----------------------------
Rules
-----------------------------

``rules``
    dict - Contains the rules for the BBCode Ruleset.
"""
import suit
from rulebox import templating
__all__ = [
 'attribute', 'linebreaks', 'listitems', 'rules', 'size', 'style',
 'template']

def attribute(params):
    """Create rule out of attribute."""
    params['var'] = params['var'].copy()
    if 'create' in params['tree']:
        params['var']['equal'] = params['tree']['create']
    return params


def linebreaks(params):
    """Remove the HTML line breaks."""
    params['string'] = params['string'].replace('<br />', '')
    return params


def listitems(params):
    """Create the list items."""
    if not params['var']['equal'] or params['var']['equal'] in ('1', 'a', 'A', 'i',
                                                                'I'):
        params['string'] = params['string'].replace('<br />', '')
        params['string'] = params['string'].split(params['var']['delimiter'])
        split = []
        for (key, value) in enumerate(params['string']):
            if key != 0:
                value = ('').join((
                 params['var']['open'],
                 value,
                 params['var']['close']))
            split.append(value)

        params['string'] = ('').join(split)
    else:
        params['var']['template'] = ('').join((
         params['open']['open'],
         params['string'],
         params['open']['rule']['close']))
    return params


def size(params):
    """Define the correct size."""
    params['var']['equal'] = int(params['var']['equal']) + 7
    if params['var']['equal'] > 30:
        params['var']['equal'] = 30
    return params


def style(params):
    """Prevent style hacking"""
    explode = params['var']['equal'].split(';', 2)
    params['var']['equal'] = explode[0]
    params['var']['equal'] = params['var']['equal'].replace('"', '').replace("'", '')
    return params


def template(params):
    """Substitute variables into the template."""
    templating.var.equal = params['var']['equal']
    templating.var.string = params['string']
    params['string'] = suit.execute(templating.rules, params['var']['template'])
    return params


rules = {'[': templating.rules['['], 
   '[align]': {'close': '[/align]', 
               'functions': [
                           templating.walk, templating.copyvar, attribute, style, template], 
               'var': {'equal': '', 
                       'label': 'align', 
                       'template': ''}}, 
   '[align=': {'close': ']', 
               'create': '[align]'}, 
   '[b]': {'close': '[/b]', 
           'functions': [
                       templating.walk, templating.copyvar, template], 
           'var': {'equal': '', 
                   'label': 'b', 
                   'template': ''}}, 
   '[code]': {'close': '[/code]', 
              'functions': [
                          templating.walk, templating.copyvar, linebreaks, template], 
              'skip': True, 
              'var': {'equal': '', 
                      'label': 'code', 
                      'template': ''}}, 
   '[color]': {'close': '[/color]', 
               'functions': [
                           templating.walk, templating.copyvar, attribute, style, template], 
               'var': {'equal': '', 
                       'label': 'color', 
                       'template': ''}}, 
   '[color=': {'close': ']', 
               'create': '[color]'}, 
   '[email]': {'close': '[/email]', 
               'functions': [
                           templating.walk, templating.copyvar, attribute, template], 
               'var': {'equal': '', 
                       'label': 'email', 
                       'template': ''}}, 
   '[email=': {'close': ']', 
               'create': '[email]'}, 
   '[font]': {'close': '[/font]', 
              'functions': [
                          templating.walk, templating.copyvar, attribute, style, template], 
              'var': {'equal': 'serif', 
                      'label': 'font', 
                      'template': ''}}, 
   '[font=': {'close': ']', 
              'create': '[font]'}, 
   '[i]': {'close': '[/i]', 
           'functions': [
                       templating.walk, templating.copyvar, template], 
           'var': {'equal': '', 
                   'label': 'i', 
                   'template': ''}}, 
   '[img]': {'close': '[/img]', 
             'functions': [
                         templating.walk, templating.copyvar, template], 
             'var': {'equal': '', 
                     'label': 'img', 
                     'template': ''}}, 
   '[list]': {'close': '[/list]', 
              'functions': [
                          templating.walk, templating.copyvar, attribute, listitems, template], 
              'var': {'close': '</li>', 
                      'delimiter': '[*]', 
                      'equal': '', 
                      'label': 'list', 
                      'open': '<li>', 
                      'template': ''}}, 
   '[list=': {'close': ']', 
              'create': '[list]'}, 
   '[s]': {'close': '[/s]', 
           'functions': [
                       templating.walk, templating.copyvar, template], 
           'var': {'equal': '', 
                   'label': 's', 
                   'template': ''}}, 
   '[size]': {'close': '[/size]', 
              'functions': [
                          templating.walk, templating.copyvar, attribute, style, size,
                          template], 
              'var': {'equal': '3', 
                      'label': 'size', 
                      'template': ''}}, 
   '[size=': {'close': ']', 
              'create': '[size]'}, 
   '[quote]': {'close': '[/quote]', 
               'functions': [
                           templating.walk, templating.copyvar, attribute, template], 
               'var': {'equal': '', 
                       'label': 'quote', 
                       'template': ''}}, 
   '[quote=': {'close': ']', 
               'create': '[quote]'}, 
   '[u]': {'close': '[/u]', 
           'functions': [
                       templating.walk, templating.copyvar, attribute, template], 
           'var': {'equal': '', 
                   'label': 'u', 
                   'template': ''}}, 
   '[url]': {'close': '[/url]', 
             'functions': [
                         templating.walk, templating.copyvar, attribute, template], 
             'var': {'equal': '', 
                     'label': 'url', 
                     'template': ''}}, 
   '[url=': {'close': ']', 
             'create': '[url]'}}