# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__setup__/ally_core/assembler.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Nov 24, 2011

@package: ally core
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the configurations for the assemblers.
"""
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
    return [assembleGet(), assembleInsert(), assembleUpdateModel(), assembleUpdate(), assembleDelete()]