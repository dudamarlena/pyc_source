# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/rpc/unit/frontend/test_controller.py
# Compiled at: 2018-01-08 12:01:55
# Size of source mod 2**32: 1444 bytes
import mock, pytest
from mercury.rpc.controller import RPCController

@pytest.fixture()
def frontend_controller(async_mongodb):
    jobs_collection = async_mongodb.rpc_jobs
    tasks_collection = async_mongodb.rpc_tasks
    inventory_client = mock.Mock()
    controller = RPCController(inventory_client, jobs_collection, tasks_collection)
    return controller


class TestFrontendController(object):

    @pytest.mark.asyncio
    async def test_get_job(self, frontend_controller):
        job = await frontend_controller.get_job('job-1')
        assert job.get('job_id') == 'job-1'

    @pytest.mark.asyncio
    async def test_get_job_none(self, frontend_controller):
        job = await frontend_controller.get_job('job-x')
        assert job == None