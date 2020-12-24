# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/PyNOAAGeoMagIndiceHandler/NOAADataCenterCollection.py
# Compiled at: 2012-09-18 11:22:18
from __future__ import with_statement
import os, sys, re, pynav, time, datetime, pytz, pyaeso, spharm, matplotlib, xml_marshaller, xmlbuilder, numpy as np
from pynav import Pynav
from xml_marshaller import xml_marshaller
from xml_marshaller.xml_marshaller import *
from xmlbuilder import XMLBuilder
from PyNOAAGeoMagIndiceHandler import decorator
from decorator import DictAssign

class NOAADataReference(object):

    class NOAADataReferenceImpl(object):
        DictReference = {'field': {'name': 'dict', 
                     'value': [
                             'NOAADictCollector'], 
                     'dict': {'name': 'position', 
                              'value': [
                                      'system'], 
                              'position': {'name': 'localtion', 
                                           'value': [
                                                   'earth', 'sonde', 'satellite']}, 
                              'localtion': {'name': 'site', 
                                            'value': [
                                                    'spo', 'sum', 'thd', 'smo', 'rpb', 'nwr', 'mlo', 'ice', 'brw', 'bmw', 'arh']}, 
                              'site': {'name': 'detector', 
                                       'value': [
                                               'ozone'], 
                                       'detector': {'name': [
                                                           'stringfield', 'listfield', 'collectionfield'], 
                                                    'value': [
                                                            'title', 'field', 'laps', 'url', '1m', '5m', '1h', '12h', '24h', '1w', '1m', '1y', '2y'], 
                                                    'stringfield': {'name': 'str', 
                                                                    'value': [
                                                                            'title', 'url']}, 
                                                    'listfield': {'name': 'list', 
                                                                  'value': [
                                                                          'field']}, 
                                                    'collectionfield': {'name': 'dict', 
                                                                        'value': [
                                                                                'laps', '1m', '5m', '1h', '12h', '24h', '1w', '1m', '1y', '2y']}}}}}}
        NOAADictCollector = {'system': {'earth': {'spo': {'ozone': {'laps': {'1h': {'url': 'ftp://ftp.cmdl.noaa.gov/ozwv/surfo3/south_pole/spclsoz'}}}}, 
                                'sum': {'ozone': {'laps': {'1h': {'url': 'ftp://ftp.cmdl.noaa.gov/ozwv/surfo3/summit_greenland/sutclsoz'}}}}, 
                                'thd': {'ozone': {'laps': {'1h': {'url': 'ftp://ftp.cmdl.noaa.gov/ozwv/surfo3/trinidad_head/thtclsoz'}}}}, 
                                'smo': {'ozone': {'laps': {'1h': {'url': 'ftp://ftp.cmdl.noaa.gov/ozwv/surfo3/samoa/smclsoz'}}}}, 
                                'rpb': {'ozone': {'laps': {'1h': {'url': 'ftp://ftp.cmdl.noaa.gov/ozwv/surfo3/barbados/baclsoz'}}}}, 
                                'nwr': {'ozone': {'laps': {'1h': {'url': 'ftp://ftp.cmdl.noaa.gov/ozwv/surfo3/niwot_ridge/nwclsoz'}}}}, 
                                'mlo': {'ozone': {'laps': {'1h': {'url': 'ftp://ftp.cmdl.noaa.gov/ozwv/surfo3/mauna_loa/mlclsoz'}}}}, 
                                'ice': {'ozone': {'laps': {'1h': {'url': 'ftp://ftp.cmdl.noaa.gov/ozwv/surfo3/westman_iceland/vmclsoz'}}}}, 
                                'brw': {'ozone': {'laps': {'1h': {'url': 'ftp://ftp.cmdl.noaa.gov/ozwv/surfo3/barrow/brclsoz'}}}}, 
                                'bmw': {'ozone': {'laps': {'1h': {'url': 'ftp://ftp.cmdl.noaa.gov/ozwv/surfo3/bermuda/bmclsoz'}}}}, 
                                'arh': {'ozone': {'laps': {'1h': {'url': 'ftp://ftp.cmdl.noaa.gov/ozwv/surfo3/arrival_heights/ahclsoz'}}}}}}}

    NodeImpl = NOAADataReferenceImpl()

    class NOAADataReferenceFactory(object):
        DictReference = {'name': None, 'value': []}
        DictFactory = {}
        CurrentID = 0
        NewAllocName = None
        NewAllocValue = None
        NewAllocContent = None

        def GetNewAlloc(self):
            return self.NewAllocContent

        def SetNewAlloc(self, value):
            self.NewAllocName, self.NewAllocContent = value
            self.CurrentID += 1
            self.NewDict = {self.CurrentID: dict(self.DictReference)}
            self.NewDict[self.CurrentID]['name'] = self.NewAllocName
            self.NewDict[self.CurrentID]['value'] = self.NewAllocContent
            self.DictFactory.update(self.NewDict)

        PropertyNewAlloc = property(GetNewAlloc, SetNewAlloc)
        ID = None

        def GetID(self):
            return self.Name

        def SetID(self, value):
            self.ID = value

        PropertyID = property(GetID, SetID)
        Name = None

        def GetName(self):
            return self.Name

        def SetName(self, value):
            self.Name = value

        PropertyName = property(GetName, SetName)
        Value = None

        def GetValue(self):
            return self.Value

        def SetValue(self, value):
            self.Value = value

        PropertyValue = property(GetValue, SetValue)

    def __init__(self, **Kargs):
        for ItemKey in Kargs.keys():
            setattr(self.Data, ItemKey, Kargs[ItemKey])


if __name__.__eq__('__main__'):
    ObjNOAATest = NOAADataReference()