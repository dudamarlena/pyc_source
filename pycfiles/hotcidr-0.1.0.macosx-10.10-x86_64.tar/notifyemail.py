# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/skemper/workspace/hotcidr/venv/lib/python2.7/site-packages/hotcidr/notifyemail.py
# Compiled at: 2014-08-29 18:40:50
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.Utils import formatdate
import smtplib
date_fmt = '%m/%d/%y %H:%M'

def notifyGitBypass(ruleDict):
    me = '__FILL_IN_HERE__'
    to = ['__FILL_IN_HERE__']
    msg = MIMEMultipart()
    msg['Subject'] = 'Firewall rule bypassed Git Repository'
    msg['From'] = me
    msg['Reply-To'] = '__FILL_IN_HERE__'
    msg['To'] = '__FILL_IN_HERE__'
    msg['Date'] = formatdate(usegmt=True)
    message = MIMEText('From: HotCIDR\n    To: Network Administrator\n    Subject:\n\n    The following rule was entered directly into AWS without first being entered into the Git Repository. (May be malicious)\n\n    Removed from AWS Security Group: %s\n    With GroupID: %s\n\n    Direction: %s\n    IP Protocol: %s\n    Port Range: from port %s to port %s\n    Source: %s\n    Description: %s\n\n    It was subsequenty removed and added to the DELETED_RULES database for use in the Firewall Audit.\n    ' % (ruleDict['modifiedGroup'], ruleDict['groupID'], ruleDict['direction'], ruleDict['protocol'], ruleDict['fromport'], ruleDict['toport'], ruleDict['location'], ruleDict['description']))
    msg.attach(message)
    s = smtplib.SMTP('__SMTP_SERVER_HERE__')
    s.sendmail(me, to, msg.as_string())
    s.quit()