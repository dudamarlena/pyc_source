# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/mpgutils/OptParseExtensions.py
# Compiled at: 2009-08-18 16:54:35
"""
Created on Jul 7, 2009

@author: nemesh
"""
from optparse import IndentedHelpFormatter
import textwrap, string

class IndentedHelpFormatterWithNL(IndentedHelpFormatter):
    """This class is blatantly stolen from some usenet help found at
  http://groups.google.com/group/comp.lang.python/browse_thread/thread/6df6e6b541a15bc2/09f28e26af0699b1?pli=1
  The desire here is to allow newlines into your help string in optparse, so you can do some programatic formatting"""

    def format_description(self, description):
        if not description:
            return ''
        desc_width = self.width - self.current_indent
        indent = ' ' * self.current_indent
        bits = description.split('\n')
        formatted_bits = [ textwrap.fill(bit, desc_width, initial_indent=indent, subsequent_indent=indent) for bit in bits
                         ]
        result = ('\n').join(formatted_bits) + '\n'
        return result

    def format_option(self, option):
        result = []
        opts = self.option_strings[option]
        opt_width = self.help_position - self.current_indent - 2
        if len(opts) > opt_width:
            opts = '%*s%s\n' % (self.current_indent, '', opts)
            indent_first = self.help_position
        else:
            opts = '%*s%-*s  ' % (self.current_indent, '', opt_width, opts)
            indent_first = 0
        result.append(opts)
        if option.help:
            help_text = self.expand_default(option)
            help_lines = []
            for para in help_text.split('\n'):
                table = ('').join(((' ' if n != 10 else chr(n)) for n in xrange(256) if n < 32 or n > 126))
                para = string.translate(para, table)
                t = textwrap.wrap(para, self.help_width)
                help_lines.extend(t)

            result.append('%*s%s\n' % (
             indent_first, '', help_lines[0]))
            result.extend([ '%*s%s\n' % (self.help_position, '', line) for line in help_lines[1:]
                          ])
        elif opts[(-1)] != '\n':
            result.append('\n')
        return ('').join(result)