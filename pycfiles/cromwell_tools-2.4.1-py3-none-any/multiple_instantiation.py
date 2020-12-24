# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/cromulent/multiple_instantiation.py
# Compiled at: 2019-11-22 16:06:13
import inspect
from cromulent.model import Destruction, EndOfExistence, Activity, Appellation, LinguisticObject

class DestructionActivity(Destruction, Activity):
    _uri_segment = 'Activity'
    _type = ['crm:E6_Destruction', 'crm:E7_Activity']

    @property
    def type(self):
        return [
         'Destruction', 'Activity']


DestructionActivity._classhier = inspect.getmro(DestructionActivity)[:-1]

class EoEActivity(EndOfExistence, Activity):
    _uri_segment = 'Activity'
    _type = ['crm:64_End_of_Existence', 'crm:E7_Activity']
    _niceType = ['EndOfExistence', 'Activity']

    @property
    def type(self):
        return [
         'EndOfExistence', 'Activity']


EoEActivity._classhier = inspect.getmro(EoEActivity)[:-1]