# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\files\research\databrowse\databrowse\support\specimen_support.py
# Compiled at: 2018-06-29 17:51:46
""" support/specimen_support.py - Functions to Support Specimen Database """
import os
from lxml import etree
import crc_algorithms
_specimendb = '/databrowse/specimens'
NS = {'specimen': 'http://thermal.cnde.iastate.edu/specimen'}
NSSTR = '{http://thermal.cnde.iastate.edu/specimen}'
OUTPUT_STRING = 0
OUTPUT_ELEMENT = 1
OUTPUT_ETREE = 2
norecursion = []
attributekeys = {NSSTR + 'dimension': 'direction', 
   NSSTR + 'direction': 'name', 
   NSSTR + 'reference': 'face', 
   NSSTR + 'plane': 'face', 
   NSSTR + 'geometry': 'component', 
   NSSTR + 'physicalproperties': 'component', 
   NSSTR + 'flawparameters': 'index', 
   NSSTR + 'fiducialmark': 'name'}
mergechildren = [
 NSSTR + 'actionlog', NSSTR + 'identifiers', NSSTR + 'measurements', NSSTR + 'reldests']

class SpecimenException(Exception):
    """ Error Handling Class for Specimen Database """
    pass


def GetSpecimen(specimen, output=OUTPUT_STRING, specimendb=_specimendb):
    """ Fetch the XML Representation of a Specimen with Specimen Group Data Integrated """
    filename = os.path.join(specimendb, specimen + '.sdb')
    if not os.path.exists(filename):
        raise SpecimenException('Unable to Locate Specimen Data File')
    else:
        if not os.access(filename, os.R_OK):
            raise SpecimenException('Unable to Access Specimen Database')
        try:
            f = open(filename, 'r')
            specimenxml = etree.XML(f.read())
            f.close()
        except:
            raise SpecimenException('Unable to Read Specimen Data File "%s"' % filename)

    groupidelem = specimenxml.xpath('specimen:groups/specimen:groupid', namespaces=NS)
    if len(groupidelem) > 1:
        groups = {}
        for group in [ x.text for x in groupidelem ]:
            filename = os.path.join(specimendb, group + '.sdg')
            if not os.path.exists(filename):
                pass
            elif not os.access(filename, os.R_OK):
                raise SpecimenException('Unable to Access Group File ' + filename)
            else:
                try:
                    f = open(filename, 'r')
                    groups[group] = etree.XML(f.read())
                    f.close()
                except:
                    raise SpecimenException('Unable to Read Specimen Group Data File' + filename)

        if len(groups) > 0:
            groupnames = groups.keys()
            groupxml = groups[groupnames[0]]
            for groupname in groupnames[1:]:
                _combine_element(groupxml, groups[groupname], groupname)

            if len(groupxml.xpath('//@override', namespaces=NS)) > 0:
                print etree.tostring(groupxml, pretty_print=True)
                raise SpecimenException('Group File Conflict - Will Not Continue Until Conflict Is Resolved - Specimen ' + specimen)
            _combine_element(specimenxml, groupxml, groupnames[0])
        if output == OUTPUT_STRING:
            print etree.tostring(specimenxml, pretty_print=True)
        else:
            if output == OUTPUT_ELEMENT:
                return specimenxml
            if output == OUTPUT_ETREE:
                return specimenxml.getroottree()
            raise SpecimenException('Invalid Return Type')
    elif len(groupidelem) == 1:
        groupid = groupidelem[0].text
        filename = os.path.join(specimendb, groupid + '.sdg')
        if not os.path.exists(filename):
            if output == OUTPUT_STRING:
                print etree.tostring(specimenxml, pretty_print=True)
            else:
                if output == OUTPUT_ELEMENT:
                    return specimenxml
                if output == OUTPUT_ETREE:
                    return specimenxml.getroottree()
                raise SpecimenException('Invalid Return Type')
        else:
            if not os.access(filename, os.R_OK):
                raise SpecimenException('Unable to Access Specimen Database')
            try:
                f = open(filename, 'r')
                groupxml = etree.XML(f.read())
                f.close()
            except:
                raise SpecimenException('Unable to Read Specimen Group Data File')

        _combine_element(specimenxml, groupxml, groupid)
        if output == OUTPUT_STRING:
            print etree.tostring(specimenxml, pretty_print=True)
        else:
            if output == OUTPUT_ELEMENT:
                return specimenxml
            if output == OUTPUT_ETREE:
                return specimenxml.getroottree()
            raise SpecimenException('Invalid Return Type')
    elif len(groupidelem) == 0:
        if output == OUTPUT_STRING:
            print etree.tostring(specimenxml, pretty_print=True)
        else:
            if output == OUTPUT_ELEMENT:
                return specimenxml
            if output == OUTPUT_ETREE:
                return specimenxml.getroottree()
            raise SpecimenException('Invalid Return Type')
    else:
        raise SpecimenException('Error Selecting Group ID Tag from Specimen Data File')


def tagname(el):
    if el.tag in attributekeys:
        try:
            return el.tag + el.get(attributekeys[el.tag])
        except:
            raise SpecimenException('Required attribute "' + attributekeys[el.tag] + '" missing from element "' + el.tag + '"')

    else:
        return el.tag


def _combine_element(one, other, group):
    """ Private Function to Recursively Combine etree Elements, Preferencing the First Element """
    mapping = {}
    for el in one:
        mapping[tagname(el)] = el

    for el in [ el for el in other if tagname(el) not in [NSSTR + 'notes', NSSTR + 'specimenslist', NSSTR + 'identifiertags', NSSTR + 'groups', NSSTR + 'groupid'] ]:
        if len(el) == 0 and tagname(el) not in norecursion and tagname(el) not in mergechildren:
            if tagname(el) not in mapping:
                mapping[tagname(el)] = el
                if not el.get('fromgroup'):
                    el.set('fromgroup', group)
                one.append(el)
            else:
                mapping[tagname(el)].set('override', group)
        elif tagname(el) in norecursion:
            if tagname(el) not in mapping:
                mapping[tagname(el)] = el
                if not el.get('fromgroup'):
                    el.set('fromgroup', group)
                one.append(el)
            else:
                mapping[tagname(el)].set('override', group)
        elif tagname(el) in mergechildren:
            if tagname(el) not in mapping:
                mapping[tagname(el)] = el
                for child in el:
                    if not el.get('fromgroup'):
                        el.set('fromgroup', group)

                one.append(el)
            else:
                for child in el:
                    if not el.get('fromgroup'):
                        child.set('fromgroup', group)
                    mapping[tagname(el)].append(child)

        else:
            try:
                _combine_element(mapping[tagname(el)], el, group)
            except KeyError:
                mapping[tagname(el)] = el
                if not el.get('fromgroup'):
                    el.set('fromgroup', group)
                one.append(el)


def GenerateCheckdigit(basename):
    alg = crc_algorithms.Crc(width=4, poly=67, reflect_in=False, xor_in=0, reflect_out=False, xor_out=0)
    crc = alg.bit_by_bit(basename) & 15
    letters = 'ACEFGHJKLMPRTWXN'
    crcletter = letters[crc]
    return crcletter