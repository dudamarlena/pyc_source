# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tfnz/docker.py
# Compiled at: 2018-05-18 20:34:30
# Size of source mod 2**32: 4703 bytes
import sys, requests.exceptions, json, logging
from typing import Optional

class Docker:
    docker_socket = '/var/run/docker.sock'
    docker_url_base = 'http+unix://%2Fvar%2Frun%2Fdocker.sock'
    session = None

    @staticmethod
    def description(docker_image_id: str, *, conn: Optional['Connection']=None) -> dict:
        """Describe a docker image.

        :param docker_image_id: Docker image id.
        :param conn: An optional connection to the location.
        :return: A dict representation of image metadata."""
        can_connect_local = True
        try:
            r = Docker._session().get('%s/images/%s/json' % (Docker.docker_url_base, docker_image_id))
            if r.status_code == 404:
                logging.info("Local docker doesn't have image, trying for remote")
            else:
                descr = json.loads(r.text)
                removes = ('Container', 'Comment', 'ContainerConfig', 'GraphDriver')
                for remove in removes:
                    if remove in descr:
                        del descr[remove]

                return descr
        except requests.exceptions.ConnectionError:
            can_connect_local = False

        if conn is not None:
            logging.info('Retrieving description: ' + docker_image_id)
            msg = conn.send_blocking_cmd(b'retrieve_description', {'image_id': docker_image_id})
            if 'description' in msg.params:
                return msg.params['description']
        elif can_connect_local:
            if conn is not None:
                raise RuntimeError('Cannot find image in either local docker or remote image cache: ' + docker_image_id)
            else:
                raise RuntimeError('Cannot find image in local docker: ' + docker_image_id)
        else:
            Docker._docker_warning()

    @staticmethod
    def tarball(docker_image_id: str) -> bytes:
        """Retrieve the tarball of a docker image.

        :param docker_image_id: Docker image id.
        :return: A stream of bytes that would be the contents of the tar archive."""
        try:
            r = Docker._session().get('%s/images/%s/get' % (Docker.docker_url_base, docker_image_id))
            return r.content
        except requests.exceptions.ConnectionError:
            Docker._docker_warning()

    @staticmethod
    def last_image() -> str:
        """Finding the most recent docker image on this machine.

        :return: Docker image id of the most recently built docker image"""
        r = None
        try:
            r = Docker._session().get('%s/images/json' % Docker.docker_url_base)
        except requests.exceptions.ConnectionError:
            Docker._docker_warning()

        if len(r.text) == 0:
            raise ValueError('Docker has no local images.')
        obj = json.loads(r.text)
        return obj[0]['Id'][7:19]

    @staticmethod
    def _docker_warning():
        print("\n    Cannot (and need to) connect to the docker socket\n    -------------------------------------------------\n    \n    The remote cache does not have a description for the combination of this image and this user.\n    If you think it should, have changed you which user account you're using?\n    Is docker running on this machine? \n    You may need to run sudo chmod 666 /var/run/docker.sock\n    ",
          file=(sys.stderr))
        raise RuntimeError('Need a functioning local Docker')

    @staticmethod
    def _session():
        if Docker.session is None:
            import requests_unixsocket
            Docker.session = requests_unixsocket.Session()
        return Docker.session