# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/reviewday/html_helper.py
# Compiled at: 2011-11-21 09:24:20


def job_data_for_type(jobs, job_type):
    """ Return a reference to the first job of the specified type. """
    for job in jobs:
        for jt, data in job.iteritems():
            if jt == job_type:
                return data


def fail_status(job_data):
    """ Return a reference to the first job of the specified type. """
    if job_data['status'] == 'Failed':
        return '<font style="color: #FF0000;">(Fail)</font>'
    else:
        if job_data['status'] == 'Success':
            return '<font style="color: #00AA00;">(Pass)</font>'
        return ''