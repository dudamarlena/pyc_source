# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aasms.py
# Compiled at: 2011-09-09 08:08:46
import urllib, urllib2
SMS_URL = 'http://sms.aaisp.net.uk/sms.cgi'

class SmsSender(object):

    def __init__(self, username=None, iccid=None, password=None):
        """Create a new SmsSender.

                Creates a new SmsSender. Requires either username or iccid, and password as assigned by aaisp.net.
                """
        if username and iccid:
            raise SmsError('must not have both username and iccid')
        self.username = username
        self.iccid = iccid
        self.password = password

    def send(self, message, destination=None, limit=None, sendtime=None, replace=False, flash=False, report=False, costcentre=None, private=False, udh=None, originator=None):
        """Send a SMS message.

                Warning: This is the bit that's billable!
                """
        if not (destination or self.iccid):
            raise SmsError('Must have a destination or iccid')
        if destination and self.iccid:
            raise SmsError("Got destination and iccid, don't know where to send message")
        if self.iccid and not originator:
            raise SmsError('iccid requires originator')
        fields = {'password': self.password, 
           'message': message}
        if destination != None:
            fields['destination'] = destination
        if self.iccid != None:
            fields['iccid'] = self.iccid
        if self.username != None:
            fields['username'] = self.username
        if limit:
            fields['limit'] = limit
        if sendtime:
            fields['sendtime'] = sendtime
        if replace:
            fields['replace'] = 1
        if flash:
            fields['flash'] = 1
        if report:
            fields['report'] = 1
        if costcentre:
            fields['costcentre'] = 1
        if private:
            fields['private'] = 1
        if udh:
            fields['udh'] = udh
        if originator:
            fields['originator'] = originator
        data = urllib.urlencode(fields)
        response = urllib2.urlopen(SMS_URL, data)
        line1 = response.readline()
        status = response.readline()
        if status.startswith('ERR:'):
            raise SmsError(status[:-2])
        return


class SmsError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

    def error(self):
        """Get the error message as reported by aaisp.net or ourselves"""
        return self.value