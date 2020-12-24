# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/spotsh/model.py
# Compiled at: 2011-02-24 22:37:21
from utils import to_str

class Instance(object):

    def __init__(self, instance):
        self.instance = instance

    def __repr__(self):
        return '\nID:     %s\nKey:    %s\nState:  %s\nIP:     %s\n' % (
         self.instance['id'],
         self.instance['key'],
         self.instance['state'],
         self.instance['ip'])

    def __str__(self):
        return self.__repr__()


class Appliance(object):

    def __init__(self, appliance):
        self.appliance = appliance

    def __repr__(self):
        return '\nName:   %s\nSize:   %s\nKey:    %s\n' % (
         self.appliance['name'],
         self.appliance['size'],
         self.appliance['key'])

    def __str__(self):
        return self.__repr__()


class Provider(object):

    def __init__(self, provider):
        self.provider = provider

    def __repr__(self):
        return to_str('\nID:          %s\nContinent:   %s\nCountry:     %s\nCity:        %s\nMin Cost:    %s\nMax Cost:    %s\n' % (
         self.provider['id'],
         self.provider['continent'],
         self.provider['country'],
         self.provider['city'],
         self.provider['min_cost'],
         self.provider['max_cost']))

    def __str__(self):
        return self.__repr__()


class Hardware(object):

    def __init__(self, hardware):
        self.hardware = hardware

    def __repr__(self):
        return '\nName:        %s\nCost:        %s\nCPU:         %s\nMemory:      %s\nMax Hours:   %s\nKey:         %s\n' % (
         self.hardware['name'],
         self.hardware['cost'],
         self.hardware['cpu'],
         self.hardware['memory'],
         self.hardware['max_hours'],
         self.hardware['key'])

    def __str__(self):
        return self.__repr__()