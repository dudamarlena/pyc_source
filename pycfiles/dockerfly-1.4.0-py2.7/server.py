# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dockerfly/http/server.py
# Compiled at: 2016-07-11 02:09:06
import time, traceback, uuid
from os.path import join
from flask import Flask, request
from flask import json
from flask.ext.restful import abort, Api, Resource
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import include
from dockerfly.settings import dockerfly_version, RUN_ROOT
from dockerfly.runtime import container as ContainerStatus
from dockerfly.dockerlib.container import Container as ContainerCtl
from dockerfly.contrib.filelock import FileLock
from dockerfly.errors import DockerflyException, VEthStatusException
from dockerfly.logger import getLogger
dockerfly_app = Flask(__name__)
dockerfly_api = Api(dockerfly_app)
logger = getLogger()

def abort_if_container_doesnt_exist(container_id):
    for item in ContainerStatus.get_all_status():
        if item.get('id', None) and container_id and len(container_id) >= 12 and item['id'].startswith(container_id):
            return item['id']

    abort(404, message=json.dumps({'errno': 1000, 'errMsg': ("Container {} doesn't exist").format(container_id)}))
    return


class Version(Resource):

    def get(self):
        return {'version': dockerfly_version}


class ContainerList(Resource):

    def get(self):
        return ContainerStatus.get_all_status()

    def post(self):
        """json template

            {
                "eths": [
                    [
                        "testDockerflyv0",
                        "eth0",
                        "172.16.11.239/24"
                    ]
                ],
                "gateway": "172.16.11.1",
                "id": null,
                "pid": null,
                "image_name": "centos:centos6_sshd",
                "container_name": "testDockerflyxxx",
                "last_modify_time": 0,
                "run_cmd": "/usr/sbin/sshd -D",
                "status": "running",
                "desc": "create a container by template"
            }
        """
        try:
            container = None
            create_containers_json = request.get_json()
            for container in create_containers_json:
                with FileLock(join(RUN_ROOT, 'verify_ips.lock')):
                    for eth in container['eths']:
                        ContainerStatus.verify_ips(eth[2])

                    eth_names = [ eth[0] for eth in container['eths'] ]
                    if len(eth_names) > len(set(eth_names)):
                        raise VEthStatusException('You set duplicate eth!')
                    container['uuid'] = str(uuid.uuid1())
                    container['id'] = None
                    container['pid'] = None
                    ContainerStatus.add_status([container])
                container['id'] = ContainerCtl.create(container['image_name'], container['run_cmd'], container['container_name'])
                ContainerCtl.start(container['id'], container['eths'], container['gateway'])
                if container.get('resize', None):
                    ContainerCtl.resize(container['id'], container['resize'])
                container['pid'] = ContainerCtl.get_pid(container['id'])
                container['last_modify_time'] = time.time()
                ContainerStatus.update_status([container], key='uuid')

            return (create_containers_json, 201)
        except Exception as e:
            logger.error(traceback.format_exc())
            if container and container.get('id', None):
                ContainerCtl.remove(container['id'])
            ContainerStatus.remove_status([container.get('uuid', None)], key='uuid')
            if not container:
                return ({'errno': 1000, 'errMsg': 'invalid json request'}, 400)
            return ({'errno': 1000, 'errMsg': e.message}, 400)

        return


class Container(Resource):

    def get(self, container_id):
        container_id = abort_if_container_doesnt_exist(container_id)
        return (ContainerStatus.get_status(container_id), 200)

    def delete(self, container_id):
        container_id = abort_if_container_doesnt_exist(container_id)
        try:
            ContainerCtl.remove(container_id)
            ContainerStatus.remove_status([container_id])
        except DockerflyException as e:
            return ({'errno': e.errno, 'errMsg': e.message}, 400)
        except Exception as e:
            logger.error(traceback.format_exc())
            return ({'errno': 1000, 'errMsg': e.message}, 400)

        return ({'msg': 'OK'}, 200)


class ContainerActive(Resource):

    def put(self, container_id):
        container_id = abort_if_container_doesnt_exist(container_id)
        try:
            container_status = ContainerStatus.get_status(container_id)
            if container_status['status'] == 'stopped':
                ContainerCtl.start(container_id, container_status['eths'], container_status['gateway'])
                container_status['last_modify_time'] = time.time()
                container_status['status'] = 'running'
                ContainerStatus.update_status([container_status])
            return (
             container_status, 202)
        except DockerflyException as e:
            return ({'errno': e.errno, 'errMsg': e.message}, 400)
        except Exception as e:
            logger.error(traceback.format_exc())
            return ({'errno': 1000, 'errMsg': e.message}, 400)


class ContainerInactive(Resource):

    def put(self, container_id):
        container_id = abort_if_container_doesnt_exist(container_id)
        try:
            container_status = ContainerStatus.get_status(container_id)
            if container_status['status'] == 'running':
                ContainerCtl.stop(container_id)
                container_status['last_modify_time'] = time.time()
                container_status['status'] = 'stopped'
                ContainerStatus.update_status([container_status])
            return (
             container_status, 202)
        except DockerflyException as e:
            return ({'errno': e.errno, 'errMsg': e.message}, 400)
        except Exception as e:
            logger.error(traceback.format_exc())
            return ({'errno': 1000, 'errMsg': e.message}, 400)


class ContainerTaskList(Resource):

    def post(self, container_id):
        container_id = abort_if_container_doesnt_exist(container_id)
        return ({'errMsg': 'Not Implement'}, 400)


class ContainerTask(Resource):

    def get(self, task_id):
        return ({'errMsg': 'Not Implement'}, 400)

    def delete(self, task_id):
        return ({'errMsg': 'Not Implement'}, 400)


dockerfly_api.add_resource(Version, '/v1/version')
dockerfly_api.add_resource(ContainerList, '/v1/containers')
dockerfly_api.add_resource(Container, '/v1/container/<string:container_id>')
dockerfly_api.add_resource(ContainerActive, '/v1/container/<string:container_id>/active')
dockerfly_api.add_resource(ContainerInactive, '/v1/container/<string:container_id>/inactive')
dockerfly_api.add_resource(ContainerTaskList, '/v1/container/<string:container_id>/tasks')
dockerfly_api.add_resource(ContainerTask, '/v1/container/<string:container_id>/task/<string:task_id>')

def run_server(host, port, debug=False, process=20):
    http_server = HTTPServer(WSGIContainer(dockerfly_app))
    http_server.bind(port, address=host)
    http_server.start(process)
    IOLoop.current().start()


if __name__ == '__main__':
    run_server(host='0.0.0.0', port=5123, debug=True)