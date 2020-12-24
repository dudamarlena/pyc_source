# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sample_graphs/email_geolocated_ip.py
# Compiled at: 2016-07-13 17:51:17
from robograph.datamodel.base import graph
from robograph.datamodel.nodes.lib import value, http, email

def email_geolocated_ip(recipients_list, smtp_server_params, ip_addr):
    subject = value.Value(value='Test mail')
    smtp_server_params['sender'] = 'test@test.com'
    smtp_server_params['mime_type'] = 'text/html'
    smtp_server_params['recipients_list'] = recipients_list
    sendmail = email.SmtpEmail(**smtp_server_params)
    http_params = dict(url='https://api.ip2country.info/ip?' + ip_addr, mime_type='application/json')
    geolocate = http.Get(**http_params)
    g = graph.Graph('email_geolocated_ip', [subject, geolocate, sendmail])
    g.connect(sendmail, geolocate, 'body')
    g.connect(sendmail, subject, 'subject')
    return g