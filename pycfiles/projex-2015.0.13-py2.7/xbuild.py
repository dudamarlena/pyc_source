# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/projex/scripts/xbuild.py
# Compiled at: 2016-07-03 23:28:12
""" 
Defines the builder class for building versions.
"""
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