# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/awsglue/job.py
# Compiled at: 2019-08-21 04:11:21
# Size of source mod 2**32: 1498 bytes


class Job:

    @classmethod
    def continuation_options(cls):
        return ['--continuation-option', 'continuation-enabled', 'continuation-readonly', 'continuation-ignore']

    @classmethod
    def job_bookmark_options(cls):
        return ['--job-bookmark-option', 'job-bookmark-enable', 'job-bookmark-pause', 'job-bookmark-disable']

    @classmethod
    def id_params(cls):
        return ['--JOB_NAME', '--JOB_ID', '--JOB_RUN_ID', '--SECURITY_CONFIGURATION']

    @classmethod
    def encryption_type_options(cls):
        return ['--encryption-type', 'sse-s3']

    def __init__(self, glue_context):
        self._job = glue_context._jvm.Job
        self._glue_context = glue_context

    def init(self, job_name, args={}):
        self._job.init(job_name, self._glue_context._glue_scala_context, args)

    def isInitialized(self):
        return self._job.isInitialized()

    def commit(self):
        self._job.commit()