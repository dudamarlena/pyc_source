# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/maltfy/bitcoinAddressToBlockchainDetails.py
# Compiled at: 2014-12-24 13:01:28
from MaltegoTransform import *
import sys, json, urllib2, i3visiotools.apify.blockchain as blockchain

def bitcoinAddressToBlockchainDetails(bitcoinAddress=None):
    """ 
                Method that checks if the given bitcoinAddress is stored in the HIBP website.

                :param bitcoinAddress:  bitcoinAddress to verify.

        """
    jsonData = blockchain.getBitcoinAddressDetails(address=bitcoinAddress)
    me = MaltegoTransform()
    newEnt = me.addEntity('i3visio.bitcoin.address', bitcoinAddress)
    newEnt.setDisplayInformation(json.dumps(jsonData, sort_keys=True, indent=2))
    newEnt.addAdditionalFields('Final balance (nanobitcoins)', 'Final balance (nanobitcoins)', True, str(jsonData['final_balance']))
    newEnt.addAdditionalFields('Total sent (nanobitcoins)', 'Total sent (nanobitcoins)', True, str(jsonData['total_sent']))
    newEnt.addAdditionalFields('Total received (nanobitcoins)', 'Total received (nanobitcoins)', True, str(jsonData['total_received']))
    newEnt.addAdditionalFields('Number of transactions', 'Number of transactions', True, str(jsonData['n_tx']))
    me.returnOutput()


if __name__ == '__main__':
    bitcoinAddressToBlockchainDetails(bitcoinAddress=sys.argv[1])