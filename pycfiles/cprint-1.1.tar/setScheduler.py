# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/pasindu/Documents/Framework/Utils/CPragmaModifier/ComponentAPIs/setScheduler.py
# Compiled at: 2018-05-18 04:59:47
import logging, sys
from ..Parameter import Parameter
from ..Directive import Directive

def setSchedule(sourceObj, mechanism, lineNumber=None):
    nextObj = sourceObj.root
    while nextObj:
        if isinstance(nextObj, Directive):
            if lineNumber:
                if nextObj.lineNumber == lineNumber:
                    for clause in nextObj.elements:
                        if clause.name == 'schedule':
                            for parameter in clause.elements:
                                if isinstance(parameter, Parameter):
                                    if len(parameter.enums) > 0 and mechanism in parameter.enums:
                                        parameter.body = mechanism

            else:
                for clause in nextObj.elements:
                    if clause.name == 'schedule':
                        for parameter in clause.elements:
                            if isinstance(parameter, Parameter):
                                if len(parameter.enums) > 0 and mechanism in parameter.enums:
                                    parameter.body = mechanism

        nextObj = nextObj.getNext()