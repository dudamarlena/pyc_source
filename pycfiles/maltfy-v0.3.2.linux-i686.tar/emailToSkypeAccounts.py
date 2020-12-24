# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/maltfy/emailToSkypeAccounts.py
# Compiled at: 2014-12-24 13:31:47
from MaltegoTransform import *
import sys, json, i3visiotools.apify.skype as skype

def emailToSkypeAccount(query=None):
    """ 
                Method that checks if the given email is appears in Skype.

                :param query:   query to verify.

        """
    me = MaltegoTransform()
    jsonData = skype.checkInSkype(query=query)
    for user in jsonData:
        newEnt = me.addEntity('i3visio.profile', 'skype://' + str(user['i3visio.alias']))
        newEnt.setDisplayInformation('<h3>' + user['i3visio.alias'] + '</h3><p>')
        for field in user.keys():
            if user[field] != None:
                try:
                    newEnt.addAdditionalFields(field, field, True, str(user[field]).encode('utf-8'))
                except:
                    pass

    me.returnOutput()
    return


if __name__ == '__main__':
    emailToSkypeAccount(query=sys.argv[1])