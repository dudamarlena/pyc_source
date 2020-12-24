# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/phishdetect/phishdetect-python/phishdetect/endpoints.py
# Compiled at: 2020-01-02 09:28:11
# Size of source mod 2**32: 1185 bytes
API_PATH = {'config':'/api/config/', 
 'analyze_domain':'/api/analyze/domain/', 
 'analyze_link':'/api/analyze/link/', 
 'analyze_html':'/api/analyze/html/', 
 'indicators_add':'/api/indicators/add/', 
 'indicators_fetch':'/api/indicators/fetch/', 
 'indicators_fetch_recent':'/api/indicators/fetch/recent/', 
 'indicators_fetch_all':'/api/indicators/fetch/all/', 
 'indicators_details':'/api/indicators/details/{sha256}/', 
 'events_add':'/api/events/add/', 
 'events_fetch':'/api/events/fetch/', 
 'reports_add':'/api/reports/add/', 
 'reports_fetch':'/api/reports/fetch/', 
 'reports_details':'/api/reports/details/{uuid}/', 
 'users_pending':'/api/users/pending/', 
 'users_active':'/api/users/active/', 
 'users_activate':'/api/users/activate/{api_key}/', 
 'users_deactivate':'/api/users/deactivate/{api_key}/'}