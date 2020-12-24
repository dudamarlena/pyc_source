# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/xmlutilities.py
# Compiled at: 2010-12-12 22:28:56
import os, fileutils, pickle
from conf import settings
from sys import version
from clsexceptions import SoftwareCompatibilityError
thisVersion = version[0:3]
if float(settings.MINPYVERSION) < float(version[0:3]):
    try:
        import xml.etree.ElementTree as ET
        from xml.etree.ElementTree import Element, SubElement, dump
    except ImportError:
        import xml.etree.ElementTree as ET
        from xml.etree.ElementTree import Element, SubElement

elif thisVersion == '2.4':
    try:
        import cElementTree as ET
        from elementtree.ElementTree import Element, SubElement, dump
    except ImportError:
        import elementtree.ElementTree as ET
        from elementtree.ElementTree import Element, SubElement

else:
    print 'Sorry, please see the minimum requirements to run this Application'
    theError = (1100, 'This application requires Python 2.4 or higher.  You are current using version: %s' % thisVersion, 'import Error XMLDumper.py')
    raise SoftwareCompatibilityError, theError

class IDGeneration:

    def __init__(self):
        print 'xmlutilities initialized...'
        self.IDNumberSequences = {}
        self.cacheFile = 'sequences.dat'
        self.IDNumberSequences = self.getSequenceCache()
        self.IDNumberSequences = {}
        self.systemID = 0
        self.recordID = 0
        self.recIDLookup = {'client': 'c', 'need': 'n', 'service': 's', 'goal': 'g', 'action_step': 'as', 'entry_exit': 'ee', 'info_release': 'ir', 'household': 'h', 'member': 'm'}

    def setrecordID(self, precordID):
        self.recordID = precordID

    def getrecordID(self):
        return self.recordID

    def setsystemID(self, psystemID):
        self.systemID = psystemID

    def getsystemID(self):
        return self.systemID

    def setIDNumberSequence(self, psequenceID, pIDNumber):
        self.IDNumberSequences[psequenceID] = pIDNumber

    def getSequenceCache(self):
        if os.path.isfile(os.path.join(os.getcwd(), self.cacheFile)):
            cacheFile = open(self.cacheFile, 'rb')
            cacheData = pickle.load(self.cacheFile)
            cacheFile.close()
        else:
            cacheData = {}
        return cacheData

    def generateRecID(self, sequenceID):
        if self.IDNumberSequences.has_key(sequenceID):
            number = self.IDNumberSequences[sequenceID] + 1
        else:
            number = 1
        if sequenceID == 'system':
            self.setsystemID(number)
        else:
            self.setrecordID(number)
        self.setIDNumberSequence(sequenceID, number)
        IDNumber = '%s%010d' % (sequenceID, number)
        return IDNumber

    def generateSysID(self, sequenceName):
        IDNumber = '%s%08da' % (self.recIDLookup[sequenceName], self.getsystemID())
        return IDNumber

    def generateSysID2(self, sequenceName, keyValue):
        IDNumber = '%s%010da' % (self.recIDLookup[sequenceName], keyValue)
        return IDNumber

    def generateSystemID(self, systemID):
        systemID = self.generateRecID(systemID)
        return systemID

    def initializeSystemID(self, puserID):
        self.setsystemID(puserID)

    def cacheSequences(self):
        selfref_list = [
         1, 2, 3]
        selfref_list.append(selfref_list)
        output = open(self.cacheFile, 'wb')
        pickle.dump(self.IDNumberSequences, output)
        output.close()


def indent(elem, level=0):
    i = '\n' + level * '  '
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + '  '
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)

        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    elif level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i


def writeOutXML(writer_instance):
    print 'root_element is ', writer_instance.root_element
    tree = ET.ElementTree(writer_instance.root_element)
    if settings.DEBUG:
        print 'trying to write XML to: %s ' % os.path.join(writer_instance.outDirectory, 'page.xml')
    fileutils.checkPath(writer_instance.outDirectory)
    attempted_filename = 'page.xml'
    unique_filename = fileutils.getUniqueFileNameForMove(attempted_filename, writer_instance.outDirectory)
    tree.write(os.path.join(writer_instance.outDirectory, unique_filename))