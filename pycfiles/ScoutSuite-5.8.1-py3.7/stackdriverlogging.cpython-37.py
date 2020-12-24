# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/gcp/facade/stackdriverlogging.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 539 bytes
import google.cloud as stackdriverlogging
from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently

class StackdriverLoggingFacade:

    async def get_sinks(self, project_id: str):
        try:
            client = stackdriverlogging.Client(project=project_id)
            return await run_concurrently(lambda : [sink for sink in client.list_sinks()])
        except Exception as e:
            try:
                print_exception('Failed to retrieve sinks: {}'.format(e))
                return []
            finally:
                e = None
                del e