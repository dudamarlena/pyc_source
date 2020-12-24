# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\iBizCase.py
# Compiled at: 2016-04-11 13:57:31
# Size of source mod 2**32: 2386 bytes
from __future__ import unicode_literals
from builtins import *
from src.Contracts.CaseSpec import CaseSpec

class iBizCase(CaseSpec):

    def __init__(self):
        self._spec = dict(auto_close='YES', priority='HIGH', status='NEW')

    def getSpec(self) -> dict:
        return self._spec

    Spec = property(getSpec)

    def getAutoClose(self) -> str:
        return self._spec.get('auto_close')

    AutoClose = property(getAutoClose)

    def getDescription(self) -> str:
        return self._spec.get('description')

    def setDescription(self, description: str):
        self._spec['description'] = description

    Description = property(getDescription, setDescription)

    def getDetail(self) -> str:
        return self._spec.get('detail')

    def setDetail(self, detail: str):
        self._spec['detail'] = detail

    Detail = property(getDetail, setDetail)

    def getInternalNotes(self) -> str:
        self._spec.get('internal_notes')

    def setInternalNotes(self, internal_notes: str):
        self._spec['internal_notes'] = internal_notes

    InternalNotes = property(getInternalNotes, setInternalNotes)

    def getIsResolved(self) -> bool:
        self._spec.get('is_resolved')

    def setIsResolved(self, is_resolved: bool):
        self._spec['is_resolved'] = is_resolved

    IsResolved = property(getIsResolved, setIsResolved)

    def getPriority(self) -> str:
        self._spec.get('priority')

    def setPriority(self, priority: str):
        self._spec['priority'] = priority

    Priority = property(getPriority, setPriority)

    def getReturnHours(self) -> int:
        self._spec.get('return_hours')

    def setReturnHours(self, return_hours: int):
        self._spec['return_hours'] = return_hours

    ReturnHours = property(getReturnHours, setReturnHours)

    def getStatus(self) -> str:
        self._spec.get('status')

    def setStatus(self, status: str):
        self._spec['status'] = status

    Status = property(getStatus, setStatus)

    def getType(self) -> str:
        self._spec.get('type')

    def setType(self, type: str):
        self._spec['type'] = type

    Type = property(getType, setType)