# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/commandline/bgcolor_option.py
# Compiled at: 2009-10-07 18:08:46
import parsing
bgcolor_choices = [
 'auto', 'light', 'dark']
parsing.parser.add_option('--bgcolor', metavar='WHEN', type='choice', choices=bgcolor_choices, default='auto', help="\n    What's the background color of the terminal. This is used to \n    determine a readable warning color. Choices are %s, default\n    is '%default'")

def process_options(options):
    import testoob.reporting
    testoob.reporting.options.bgcolor = options.bgcolor


parsing.option_processors.append(process_options)