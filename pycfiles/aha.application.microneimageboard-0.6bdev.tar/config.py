# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/application/config.py
# Compiled at: 2010-11-20 20:00:26
__author__ = 'Atsushi Shibata <shibata@webcore.co.jp>'
__docformat__ = 'plaintext'
__licence__ = 'BSD'
import logging

def appConfig():
    import aha
    config = aha.Config()
    from aha.dispatch.router import get_router, get_fallback_router
    fr = get_fallback_router()
    fr.connect('*url', controller='main', action='index')
    config.debug = True
    config.useappstatus = False
    if config.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    main()