# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__setup__/ally_core/assembler.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Nov 24, 2011\n\n@package: ally core\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the configurations for the assemblers.\n'
from ally.container import ioc
from ally.core.impl.assembler import AssembleGet, AssembleInsert, AssembleUpdate, AssembleDelete, AssembleUpdateModel
from ally.core.spec.resources import IAssembler

@ioc.entity
def assembleGet() -> IAssembler:
    return AssembleGet()


@ioc.entity
def assembleDelete() -> IAssembler:
    return AssembleDelete()


@ioc.entity
def assembleInsert() -> IAssembler:
    return AssembleInsert()


@ioc.entity
def assembleUpdate() -> IAssembler:
    return AssembleUpdate()


@ioc.entity
def assembleUpdateModel() -> IAssembler:
    return AssembleUpdateModel()


@ioc.entity
def assemblers():
    return [
     assembleGet(), assembleInsert(), assembleUpdateModel(), assembleUpdate(), assembleDelete()]