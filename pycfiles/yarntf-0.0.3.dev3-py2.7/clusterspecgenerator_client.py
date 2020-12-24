# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarntf/clusterspecgenerator_client.py
# Compiled at: 2017-04-27 10:33:55
import grpc, yarntf.clusterspecgenerator_pb2 as csg, yarntf.clusterspecgenerator_pb2_grpc as csg_grpc

class ClusterSpecGeneratorClient:

    def __init__(self, target):
        self.channel = grpc.insecure_channel(target)
        self.stub = csg_grpc.ClusterSpecGeneratorStub(self.channel)

    def register_container(self, application_id, ip, port, job_name, task_index, tb_port):
        container = csg.Container()
        container.applicationId = application_id
        container.ip = ip
        container.port = port
        container.jobName = job_name
        container.taskIndex = task_index
        container.tbPort = tb_port
        request = csg.RegisterContainerRequest(container=container)
        try:
            self.stub.RegisterContainer(request)
        except grpc.RpcError:
            return False

        return True

    def get_cluster_spec(self, application_id):
        request = csg.GetClusterSpecRequest()
        request.applicationId = application_id
        try:
            reply = self.stub.GetClusterSpec(request)
        except grpc.RpcError:
            return

        return reply.clusterSpec