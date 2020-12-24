# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/commandline/color_mode_option.py
# Compiled at: 2009-10-07 18:08:46
import parsing, sys, os
from testoob.reporting.color_support import auto_color_support
color_choices = [
 'never', 'always', 'auto']
parsing.parser.add_option('--color-mode', metavar='WHEN', type='choice', choices=color_choices, default='auto', help='When should output be in color? Choices are ' + str(color_choices) + ", default is '%default'")

def process_options(options):

    def color_output():
        if options.color_mode == 'always':
            return True
        if options.color_mode == 'auto' and auto_color_support(sys.stderr):
            return True
        return False

    if color_output():
        from testoob.reporting import ColoredTextReporter
        parsing.kwargs['reporter_class'] = ColoredTextReporter


parsing.option_processors.append(process_options)