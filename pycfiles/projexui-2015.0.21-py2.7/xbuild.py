# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/projex/scripts/xbuild.py
# Compiled at: 2016-07-03 23:28:12
__doc__ = ' \nDefines the builder class for building versions.\n'
__authors__ = [
 'Eric Hulser']
__author__ = (',').join(__authors__)
__credits__ = []
__copyright__ = 'Copyright (c) 2011-2016'
__license__ = 'MIT'
__maintainer__ = 'Eric Hulser'
__email__ = 'eric.hulser@gmail.com'
if __name__ == '__main__':
    import logging
    logging.basicConfig()
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    from projex.xbuild.builder import build_cmd
    build_cmd()