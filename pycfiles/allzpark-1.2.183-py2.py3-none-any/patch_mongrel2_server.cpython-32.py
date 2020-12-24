# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/cdm/patch_mongrel2_server.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Nov 23, 2011\n\n@package: support cdm\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the Mongrel2 web server plugins patch for the cdm.\n'
from ..cdm import use_linked_cdm
from __setup__.ally_http import server_type
from ally.container import ioc, support
ioc.doc(use_linked_cdm, '\n!!!Attention, if the mongrel2 server is selected this option will always be "false"\n')

@ioc.before(use_linked_cdm, auto=False)
def use_linked_cdm_force():
    if server_type() == 'mongrel2':
        support.force(use_linked_cdm, False)