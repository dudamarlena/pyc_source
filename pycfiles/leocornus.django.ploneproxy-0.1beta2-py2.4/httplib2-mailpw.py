# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/leocornus/django/ploneproxy/samples/httplib2-mailpw.py
# Compiled at: 2010-05-20 09:02:10
"""

"""
import urllib, httplib2
http = httplib2.Http('.cache')
mailpw_url = 'http://10.20.9.65:8080/gsdc/gsdc/default/mail_password'
headers = {}
headers['Content-type'] = 'application/x-www-form-urlencoded'
headers['User-Agent'] = 'Leocornus Django PloneProxy'
mail_form = {}
mail_form['userid'] = 'tsmith'
(response, content) = http.request(mailpw_url, 'POST', headers=headers, body=urllib.urlencode(mail_form))
print content
print '=============================================='
print response
print '=============================================='