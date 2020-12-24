# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/maltfy/expandPropertiesFromI3visioEntity.py
# Compiled at: 2014-12-24 13:01:28
from MaltegoTransform import *
import sys, json, constants

def expandPropertiesFromI3visioEntity(argv):
    """ 
                Method that expands the properties from a given i3visio entity. It is useful to create new Entities based on the contents of the properties.
                :param argv:    the serialized entity.

                :return:        Nothing is returned but the code of the entities is created.
        """
    me = MaltegoTransform()
    me.parseArguments(argv)
    found_fields = {}
    for entity in constants.I3VISIO_ENTITIES:
        found_fields[entity] = me.getVar(entity)

    for field in found_fields.keys():
        if found_fields[field] != None:
            newEnt = me.addEntity(field, str(found_fields[field]))

    try:
        attributes = me.getVar('attributes')
        attJson = json.loads(attributes)
        for att in attJson:
            newEnt = me.addEntity(str(att['type']), str(att['value']))
            newEnt.addAdditionalFields('attributes', 'attributes', True, str(att['attributes']))

    except:
        pass

    me.returnOutput()
    return


if __name__ == '__main__':
    expandPropertiesFromI3visioEntity(sys.argv)