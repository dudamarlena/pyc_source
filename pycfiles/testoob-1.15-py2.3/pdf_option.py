# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/commandline/pdf_option.py
# Compiled at: 2009-10-07 18:08:46
import parsing
parsing.parser.add_option('--pdf', metavar='FILE', help='output results in PDF (requires ReportLab)')

def process_options(options):
    if options.pdf is not None:
        parsing.require_modules('--pdf', 'reportlab')
        from testoob.reporting import PdfReporter
        parsing.kwargs['reporters'].append(PdfReporter(filename=options.pdf))
    return


parsing.option_processors.append(process_options)