# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/maltfy/uriToEntities.py
# Compiled at: 2014-12-24 13:01:29
from MaltegoTransform import *
import sys, entify.lib.processing as processing, json, constants

def uriToI3visioEntities(argv):
    """ 
                Method that obtains all the entities in a given profile.

                :param argv:    the serialized entity.

                :return:        Nothing is returned but the code of the entities is created.
        """
    me = MaltegoTransform()
    uri = sys.argv[1]
    found_fields = {}
    import urllib2
    data = urllib2.urlopen(uri).read()
    entities = processing.getEntitiesByRegexp(data=data)
    for elem in entities:
        newEnt = me.addEntity(elem['type'], elem['value'])
        newEnt.addAdditionalFields('i3visio.attributes', 'i3visio.attributes', True, str(elem['attributes']))

    me.returnOutput()


if __name__ == '__main__':
    uriToI3visioEntities(sys.argv)