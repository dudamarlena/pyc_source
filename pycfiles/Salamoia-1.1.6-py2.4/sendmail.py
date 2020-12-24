# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/nacl/info/sendmail.py
# Compiled at: 2007-12-02 16:26:59
from smtplib import *
from salamoia.h2o.logioni import *

def sendmail(mail):
    server = SMTP('localhost')
    server.set_debuglevel(1)
    try:
        dest = mail['To']
        cc = mail['Cc']
        if type(dest) == type(''):
            dest = [
             dest]
        if type(cc) == type(''):
            cc = [
             cc]
        if cc:
            dest = dest + cc
        Ione.log('SENDING TO %s' % dest)
        server.sendmail(mail['From'], dest, mail.as_string())
    except:
        Ione.log('Mail form:%s to:%s' % (mail['From'], mail['To']))
        server.quit()
        return 0

    server.quit()
    return 1


from salamoia.tests import *
runDocTests()