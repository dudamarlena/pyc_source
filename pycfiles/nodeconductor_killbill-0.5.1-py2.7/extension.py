# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_killbill/extension.py
# Compiled at: 2016-09-25 09:47:37
from __future__ import absolute_import
from nodeconductor.core import NodeConductorExtension

class KillBillExtension(NodeConductorExtension):

    class Settings:
        NODECONDUCTOR_KILLBILL = {'BACKEND': {'api_url': 'http://killbill.example.com/1.0/kb/', 
                       'username': 'admin', 
                       'password': 'password', 
                       'api_key': 'bob', 
                       'api_secret': 'lazar', 
                       'currency': 'USD'}, 
           'INVOICE': {'logo': 'gcloud-logo.png', 
                       'company': 'OpenNode', 
                       'address': 'Lille 4-205', 
                       'country': 'Estonia', 
                       'email': 'info@opennodecloud.com', 
                       'postal': '80041', 
                       'phone': '(+372) 555-55-55', 
                       'bank': 'American Bank', 
                       'account': '123456789'}}

    @staticmethod
    def django_app():
        return 'nodeconductor_killbill'

    @staticmethod
    def rest_urls():
        from .urls import register_in
        return register_in

    @staticmethod
    def celery_tasks():
        from celery.schedules import crontab
        return {'update-today-usage': {'task': 'nodeconductor.killbill.update_today_usage', 
                                  'schedule': crontab(minute=10), 
                                  'args': ()}}