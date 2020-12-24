# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\jld\cmd\pypre.py
# Compiled at: 2009-03-24 20:56:20
""" A simple preprocessor based on the Mako template engine
    @author: Jean-Lou Dupont
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: pypre.py 894 2009-03-25 00:56:18Z JeanLou.Dupont $'
import os, sys
from optparse import OptionParser
import jld.template as tpl
_options = []
_usage = '%prog [options] input_file   \n\nPreprocessor based on the Mako template engine\nversion $LastChangeRevision$ by Jean-Lou Dupont\n'

def main():
    parser = OptionParser(usage=_usage)
    for o in _options:
        parser.add_option(o['o1'], dest=o['var'], action=o['action'], default=o['default'])

    (options, args) = parser.parse_args()
    if len(args) < 1:
        print 'Error: not enough arguments'
        return 0
    input = args[0]
    if not os.path.isfile(input):
        print 'Error: invalid input_file parameter'
        return 0
    try:
        template = tpl.Tpl(input)
        result = template.render()
    except Exception, e:
        print 'Error: template processing failed [%s]' % e
        return 0

    print result


if __name__ == '__main__':
    sys.exit(main())