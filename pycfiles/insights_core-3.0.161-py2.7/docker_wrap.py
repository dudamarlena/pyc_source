# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/client/docker_wrap.py
# Compiled at: 2019-05-16 13:41:33
from __future__ import absolute_import
from . import util
import json

class docker_wrapper:

    def __init__(self):
        cmd = [
         'docker', '-v']
        r = util.subp(cmd)
        if r.return_code != 0:
            raise Exception('Unable to communicate with the docker server')

    def inspect(self, obj_id):
        cmd = [
         'docker', 'inspect', obj_id]
        r = util.subp(cmd)
        if r.return_code != 0:
            raise Exception('Unable to inspect object: %s' % obj_id)
        return json.loads(r.stdout)

    def driver(self):
        cmd = [
         'docker', 'info']
        r = util.subp(cmd)
        if r.return_code != 0:
            raise Exception('Unable to get docker info')
        for line in r.stdout.strip().split('\n'):
            if line.startswith('Storage Driver'):
                pre, _, post = line.partition(':')
                return post.strip()

        raise Exception('Unable to get docker storage driver')

    def dm_pool(self):
        cmd = [
         'docker', 'info']
        r = util.subp(cmd)
        if r.return_code != 0:
            raise Exception('Unable to get docker info')
        for line in r.stdout.strip().split('\n'):
            if line.strip().startswith('Pool Name'):
                pre, _, post = line.partition(':')
                return post.strip()

        raise Exception('Unable to get docker pool name')

    def images(self, allI=False, quiet=False):
        cmd = [
         'docker', 'images', '-q', '--no-trunc']
        if allI:
            cmd.append('-a')
        r = util.subp(cmd)
        if r.return_code != 0:
            raise Exception('Unable to get docker images')
        images = r.stdout.strip().split('\n')
        if quiet:
            return images
        else:
            ims = []
            for i in images:
                inspec = self.inspect(i)
                inspec = inspec[0]
                dic = {}
                dic['Created'] = inspec['Created']
                if inspec['Config']:
                    dic['Labels'] = inspec['Config']['Labels']
                else:
                    dic['Labels'] = {}
                dic['VirtualSize'] = inspec['VirtualSize']
                dic['ParentId'] = inspec['Parent']
                dic['RepoTags'] = inspec['RepoTags']
                dic['RepoDigests'] = inspec['RepoDigests']
                dic['Id'] = inspec['Id']
                dic['Size'] = inspec['Size']
                ims.append(dic)

            return ims

    def containers(self, allc=False, quiet=False):
        cmd = [
         'docker', 'ps', '-q']
        if allc:
            cmd.append('-a')
        r = util.subp(cmd)
        if r.return_code != 0:
            raise Exception('Unable to get docker containers')
        containers = r.stdout.strip().split('\n')
        if quiet:
            return containers
        else:
            conts = []
            for i in containers:
                inspec = self.inspect(i)
                inspec = inspec[0]
                dic = {}
                dic['Status'] = inspec['State']['Status']
                dic['Created'] = inspec['Created']
                dic['Image'] = inspec['Config']['Image']
                dic['Labels'] = inspec['Config']['Labels']
                dic['NetworkSettings'] = inspec['NetworkSettings']
                dic['HostConfig'] = inspec['HostConfig']
                dic['ImageID'] = inspec['Image']
                dic['Command'] = inspec['Config']['Cmd']
                dic['Names'] = inspec['Name']
                dic['Id'] = inspec['Id']
                dic['Ports'] = inspec['NetworkSettings']['Ports']
                conts.append(dic)

            return conts