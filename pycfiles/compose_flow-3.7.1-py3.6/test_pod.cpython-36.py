# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_pod.py
# Compiled at: 2020-01-28 12:24:29
# Size of source mod 2**32: 3814 bytes
import shlex
from unittest import mock
from compose_flow.commands import Workflow
from tests import BaseTestCase

class PodTestCase(BaseTestCase):

    def _get_mock_pod_list_raw(self):
        """
        Return a string mocking raw pod list data
        """
        raw_data = 'NAME                                          READY     STATUS    RESTARTS   AGE\ncelerybeat-568bdbc99d-m8x4n                   1/1       Running   0          96m\ngeneric-workers-6c744b8fb8-7sjb8              1/1       Running   0          96m\ngeneric-workers-6c744b8fb8-9rrjx              1/1       Running   0          96m\ngeneric-workers-6c744b8fb8-c66gl              1/1       Running   0          96m\ngeneric-workers-6c744b8fb8-rjrns              1/1       Running   0          96m\npublished-frontend-reports-5dd4b54fd5-r42gg   1/1       Running   0          96m\nredis-master-0                                1/1       Running   0          2d3h\nweb-b5496d46f-hjt4q                           1/1       Running   0          96m\nweb-b5496d46f-k9lwq                           1/1       Running   0          96m\nweb-b5496d46f-spdqd                           1/1       Running   0          96m\n'
        return raw_data

    @mock.patch('compose_flow.shell.execute')
    @mock.patch('compose_flow.commands.subcommands.pod.Pod.switch_rancher_context')
    def test_exec_pod_with_specified_container_and_index(self, *mocks):
        """
        Basic test to ensure the command runs as expected
        """
        argv = shlex.split('-e test pod exec generic-workers --container generic-workers -i 2 /bin/bash')
        workflow = Workflow(argv=argv)
        pod = workflow.subcommand
        pod.list_pods = mock.MagicMock()
        pod.list_pods.return_value = self._get_mock_pod_list_raw()
        workflow.run()
        target_command = f"rancher kubectl -n {workflow.project_name} exec -it generic-workers-6c744b8fb8-c66gl --container generic-workers -- /bin/bash"
        self.assertEqual(target_command, mocks[1].call_args[0][0])

    @mock.patch('compose_flow.shell.execute')
    @mock.patch('compose_flow.commands.subcommands.pod.Pod.switch_rancher_context')
    def test_exec_pod_without_specified_container(self, *mocks):
        """
        Test that the command works when no container is specified
        """
        argv = shlex.split('-e test pod exec generic-workers /bin/bash')
        workflow = Workflow(argv=argv)
        pod = workflow.subcommand
        pod.list_pods = mock.MagicMock()
        pod.list_pods.return_value = self._get_mock_pod_list_raw()
        workflow.run()
        target_command = f"rancher kubectl -n {workflow.project_name} exec -it generic-workers-6c744b8fb8-7sjb8  -- /bin/bash"
        self.assertEqual(target_command, mocks[1].call_args[0][0])

    @mock.patch('compose_flow.shell.execute')
    @mock.patch('compose_flow.commands.subcommands.pod.Pod.switch_rancher_context')
    def test_exec_pod_with_specified_namespace(self, *mocks):
        """
        Test that we can override the namespace with --namespace.
        """
        argv = shlex.split('-e test pod exec --namespace foobar generic-workers /bin/bash')
        workflow = Workflow(argv=argv)
        pod = workflow.subcommand
        pod.list_pods = mock.MagicMock()
        pod.list_pods.return_value = self._get_mock_pod_list_raw()
        workflow.run()
        target_command = 'rancher kubectl -n foobar exec -it generic-workers-6c744b8fb8-7sjb8  -- /bin/bash'
        self.assertEqual(target_command, mocks[1].call_args[0][0])