# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/apify/blockchain.py
# Compiled at: 2014-12-25 06:48:18
import sys, json, urllib2

def getBitcoinAddressDetails(address=None):
    """ 
                Method that checks the presence of a Bitcoin Address in blockchain.info:
{
  "total_sent": 41301084, 
  "total_received": 52195147, 
  "final_balance": 10894063, 
  "address": "1APKyS2TEdFMjXjJfMCgavFtoWuv2QNXTw", 
  "hash160": "66f21efc754af07e87913db46bf24df2eb0d5075", 
...
}

                :param address: Bitcoin address to verify.

                :return:        Python structure for the Json received.
        """
    apiURL = 'https://blockchain.info/rawaddr/' + str(address)
    data = urllib2.urlopen(apiURL).read()
    jsonData = json.loads(data)
    return jsonData


if __name__ == '__main__':
    getBitcoinAddressDetails(address=sys.argv[1])