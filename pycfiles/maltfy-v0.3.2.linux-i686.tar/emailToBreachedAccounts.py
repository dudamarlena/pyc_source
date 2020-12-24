# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/maltfy/emailToBreachedAccounts.py
# Compiled at: 2014-12-24 13:01:28
from MaltegoTransform import *
import sys, json, urllib2, i3visiotools.apify.haveibeenpwned as HIBP

def emailToBreachedAccounts(email=None):
    """ 
                Method that checks if the given email is stored in the HIBP website.

                :param email:   email to verify.

        """
    me = MaltegoTransform()
    jsonData = HIBP.checkIfHackedInHIBP(email=email)
    for breach in jsonData:
        newEnt = me.addEntity('i3visio.breach', breach['Title'])
        newEnt.setDisplayInformation('<h3>' + breach['Title'] + '</h3><p>' + json.dumps(breach, sort_keys=True, indent=2) + '!</p>')
        for field in breach.keys():
            if field != 'Title':
                continue

    me.returnOutput()


if __name__ == '__main__':
    emailToBreachedAccounts(email=sys.argv[1])