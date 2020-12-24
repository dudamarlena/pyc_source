# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/gateway_acl/patch_ally_core.py
# Compiled at: 2013-10-29 05:40:54
"""
Created on Aug 31, 2013

@package: gateway acl
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the ally core setup patch.
"""
import logging
from ally.container import support, app, ioc
from ..sql_alchemy.db_application import assemblySQLAssembler
from ..sql_alchemy.patch_ally_core import updateAssemblySQLAssembler
from ..sql_alchemy.processor import transaction
log = logging.getLogger(__name__)
try:
    from __setup__ import ally_core
except ImportError:
    log.info('No ally core component available, thus no need to register ACL assemblers to it')
else:
    from __setup__.ally_core.resources import assemblyAssembler, updateAssemblyAssembler, processMethod
    from acl.core.impl.processor import assembler
    processFilter = indexFilter = indexAccess = support.notCreated
    support.createEntitySetup(assembler)

    @ioc.after(updateAssemblyAssembler)
    def updateAssemblyAssemblerForFilter():
        assemblyAssembler().add(processFilter(), before=processMethod())


    @ioc.after(updateAssemblySQLAssembler)
    def updateAssemblySQLAssemblerForFilter():
        assemblySQLAssembler().add(processFilter(), before=processMethod())


    @app.setup(app.CHANGED)
    def updateAssemblyAssemblerForAccess():
        assemblyAssembler().add(transaction(), indexFilter(), indexAccess())