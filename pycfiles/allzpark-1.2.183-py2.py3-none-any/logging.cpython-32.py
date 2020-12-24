# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__setup__/ally_plugin/logging.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Nov 7, 2012\n\n@package: ally plugin\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nUpdate the default logging.\n'
from ..ally.logging import info_for
from .distribution import application_mode, APP_DEVEL
from ally.container import ioc
from ally.design import processor
import logging

@ioc.before(info_for)
def updateInfos():
    info_for().append('__plugin__')


@ioc.start(priority=ioc.PRIORITY_TOP)
def updateDevelopment():
    if application_mode() == APP_DEVEL:
        logging.getLogger(processor.__name__).setLevel(logging.INFO)