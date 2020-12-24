# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/apify/haveibeenpwned.py
# Compiled at: 2014-12-25 06:48:18
import sys, json, urllib2

def checkIfHackedInHIBP(email=None):
    """ 
                Method that checks if the given email is stored in the HIBP website. An example of the json received:
[{"Title":"Adobe","Name":"Adobe","Domain":"adobe.com","BreachDate":"2013-10-4","AddedDate":"2013-12-04T00:12Z","PwnCount":152445165,"Description":"The big one. In October 2013, 153 million Adobe accounts were breached with each containing an internal ID, username, email, <em>encrypted</em> password and a password hint in plain text. The password cryptography was poorly done and <a href="http://stricture-group.com/files/adobe-top100.txt" target="_blank">many were quickly resolved back to plain text</a>. The unencrypted hints also <a href="http://www.troyhunt.com/2013/11/adobe-credentials-and-serious.html" target="_blank">disclosed much about the passwords</a> adding further to the risk that hundreds of millions of Adobe customers already faced.","DataClasses":["Email addresses","Password hints","Passwords","Usernames"]}]

                :param email:   email to verify.

                :return:        Python structure for the Json received.
        """
    apiURL = 'https://haveibeenpwned.com/api/v2/breachedaccount/' + email
    data = urllib2.urlopen(apiURL).read()
    jsonData = json.loads(data)
    return jsonData


if __name__ == '__main__':
    checkIfHackedInHIBP(email=sys.argv[1])