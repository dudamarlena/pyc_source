# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/th13f/dev/drf-batch-requests/drf_batch_requests/settings.py
# Compiled at: 2018-02-16 09:59:50
from django.conf import settings
REQUESTS_CONSUMER_BACKEND = getattr(settings, 'DRF_BATCH_REQUESTS_CONSUMER_BACKEND', 'drf_batch_requests.backends.sync.SyncRequestsConsumeBackend')