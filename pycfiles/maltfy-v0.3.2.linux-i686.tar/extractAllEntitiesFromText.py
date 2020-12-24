# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/maltfy/extractAllEntitiesFromText.py
# Compiled at: 2014-12-24 13:01:28
from MaltegoTransform import *
import sys
from entify import entify
import json, constants, i3visiotools.apify.blockchain as blockchain

def extractAllEntitiesFromI3visioText(argv):
    """ 
                Method that obtains all the entities in a given i3visio.Object that contains an i3visio.text property.

                :param argv:    the serialized entity.

                :return:        Nothing is returned but the code of the entities is created.
        """
    me = MaltegoTransform()
    found_fields = {}
    data = sys.argv[1]
    entities = entify.getEntitiesByRegexp(data=data)
    for type_regexp in entities:
        for k in type_regexp.keys():
            for element in type_regexp[k]['found_exp']:
                if k == 'i3visio.bitcoin.address':
                    bitcoinAddress = str(element)
                    newEnt = me.addEntity(k, str(element))
                    jsonData = blockchain.getBitcoinAddressDetails(address=bitcoinAddress)
                    newEnt.setDisplayInformation(json.dumps(jsonData, sort_keys=True, indent=2))
                    newEnt.addAdditionalFields('Final balance (nanobitcoins)', 'Final balance (nanobitcoins)', True, str(jsonData['final_balance']))
                    newEnt.addAdditionalFields('Total sent (nanobitcoins)', 'Total sent (nanobitcoins)', True, str(jsonData['total_sent']))
                    newEnt.addAdditionalFields('Total received (nanobitcoins)', 'Total received (nanobitcoins)', True, str(jsonData['total_received']))
                    newEnt.addAdditionalFields('Number of transactions', 'Number of transactions', True, str(jsonData['n_tx']))
                else:
                    newEnt = me.addEntity(k, str(element))

    me.returnOutput()


if __name__ == '__main__':
    extractAllEntitiesFromI3visioText(sys.argv)