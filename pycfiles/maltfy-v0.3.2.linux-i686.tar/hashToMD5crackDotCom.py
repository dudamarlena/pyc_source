# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/maltfy/hashToMD5crackDotCom.py
# Compiled at: 2014-12-24 13:01:28
from MaltegoTransform import *
import sys, json, urllib2, i3visiotools.apify.md5crack as md5crack

def hashToMD5crackDotCom(hash=None):
    """ 
                Method that checks if the given email is stored in the md5crack.com.

                :param email:   email to verify.

        """
    me = MaltegoTransform()
    jsonData = md5crack.checkIfCrackedInMD5crack(hash=hash)
    if not jsonData['parsed'] == '':
        newEnt = me.addEntity('i3visio.text', jsonData['parsed'])
        newEnt.setDisplayInformation('<h3>' + jsonData['parsed'] + '</h3><p>' + json.dumps(jsonData, sort_keys=True, indent=2) + '</p>')
        for field in jsonData.keys():
            if field != 'parsed':
                continue

    me.returnOutput()


if __name__ == '__main__':
    hashToMD5crackDotCom(hash=sys.argv[1])