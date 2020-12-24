# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/catalyze/helpers/pods.py
# Compiled at: 2015-06-19 15:08:12
from __future__ import absolute_import
from catalyze import config, output

def metadata(session, pod_id):
    route = '%s/v1/pods/metadata' % (config.paas_host,)
    for pod in session.get(route, verify=True):
        if pod['id'] == pod_id:
            return pod

    output.error('Could not find the pod associated with this environment. Please contact Catalyze support. Please include your environment ID - found via "catalyze support-ids"')