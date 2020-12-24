# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/eggbasket/rest.py
# Compiled at: 2008-07-13 16:55:56
""" rest-to-html conversion taken from the Zope core 
This implementation requires docutils 0.4.0+ from http://docutils.sf.net/
"""
try:
    import docutils
except ImportError:
    raise ImportError, 'Please install docutils 0.4.0+ from http://docutils.sourceforge.net/#download.'

version = docutils.__version__.split('.')
if not (version >= ['0', '4', '0'] or version >= ['0', '4']):
    raise ImportError, 'Old version of docutils found:\nGot: %(version)s, required: 0.4.0+\nPlease remove docutils from %(path)s and replace it with a new version. You\ncan download docutils at http://docutils.sourceforge.net/#download.\n' % {'version': docutils.__version__, 'path': docutils.__path__[0]}
import docutils.parsers.rst
for (title, options, conf) in docutils.parsers.rst.Parser.settings_spec[2]:
    if options == ['--file-insertion-enabled']:
        conf['default'] = 0
        break

import sys, os, locale
from docutils.core import publish_parts
default_enc = sys.getdefaultencoding()
default_output_encoding = 'unicode'
default_input_encoding = 'unicode'
default_level = 3
initial_header_level = default_level
default_language_code = 'en'

class Warnings:

    def __init__(self):
        self.messages = []

    def write(self, message):
        self.messages.append(message)


def render(src, writer='html4css1', report_level=1, stylesheet=None, input_encoding=default_input_encoding, output_encoding=default_output_encoding, language_code=default_language_code, initial_header_level=initial_header_level, settings={}):
    """get the rendered parts of the document the and warning object
    """
    settings = settings.copy()
    settings['input_encoding'] = input_encoding
    settings['output_encoding'] = output_encoding
    settings['stylesheet'] = stylesheet
    settings['stylesheet_path'] = None
    settings['file_insertion_enabled'] = 0
    settings['raw_enabled'] = 0
    if language_code:
        settings['language_code'] = language_code
    settings['language_code'] = language_code
    settings['initial_header_level'] = initial_header_level + 1
    settings['report_level'] = report_level
    settings['halt_level'] = 6
    settings['warning_stream'] = warning_stream = Warnings()
    parts = publish_parts(source=src, writer_name=writer, settings_overrides=settings, config_section='zope application')
    return (
     parts, warning_stream)


def HTML(src, writer='html4css1', report_level=1, stylesheet=None, input_encoding=default_input_encoding, output_encoding=default_output_encoding, language_code=default_language_code, initial_header_level=initial_header_level, warnings=None, settings={}):
    """ render HTML from a reStructuredText string 

        - 'src'  -- string containing a valid reST document

        - 'writer' -- docutils writer 

        - 'report_level' - verbosity of reST parser

        - 'stylesheet' - Stylesheet to be used

        - 'input_encoding' - encoding of the reST input string

        - 'output_encoding' - encoding of the rendered HTML output
        
        - 'report_level' - verbosity of reST parser

        - 'language_code' - docutils language
        
        - 'initial_header_level' - level of the first header tag
        
        - 'warnings' - will be overwritten with a string containing the warnings
        
        - 'settings' - dict of settings to pass in to Docutils, with priority

    """
    (parts, warning_stream) = render(src, writer=writer, report_level=report_level, stylesheet=stylesheet, input_encoding=input_encoding, output_encoding=output_encoding, language_code=language_code, initial_header_level=initial_header_level, settings=settings)
    header = '<h%(level)s class="title">%(title)s</h%(level)s>\n' % {'level': initial_header_level, 
       'title': parts['title']}
    subheader = '<h%(level)s class="subtitle">%(subtitle)s</h%(level)s>\n' % {'level': initial_header_level + 1, 
       'subtitle': parts['subtitle']}
    body = '%(docinfo)s%(body)s' % {'docinfo': parts['docinfo'], 
       'body': parts['body']}
    output = ''
    if parts['title']:
        output = output + header
    if parts['subtitle']:
        output = output + subheader
    output = output + body
    warnings = ('').join(warning_stream.messages)
    if output_encoding != 'unicode':
        return output.encode(output_encoding)
    else:
        return output


__all__ = ('HTML', 'render')
if __name__ == '__main__':
    import sys
    print HTML(open(sys.argv[1]).read())