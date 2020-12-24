# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tfnz/endpoint.py
# Compiled at: 2018-05-18 20:34:30
# Size of source mod 2**32: 6322 bytes
import weakref, logging, requests, time
from requests.exceptions import ConnectionError, ReadTimeout
from typing import List, Optional, Tuple
from tfnz.container import Container

class Cluster:
    __doc__ = 'An object representing a collection of containers, load balanced and published to an endpoint.\n\n        :param containers: An optional list of containers to initialise the cluster with.\n        :param rewrite: An optional string to be rewritten into the http host header.'

    def __init__(self, *, containers: Optional[List[Container]]=None, rewrite: Optional[str]=None):
        self.uuid = None
        self.conn = None
        self.containers = {}
        self.rewrite = rewrite
        for container in containers:
            self.add_container(container)

    def add_container(self, container):
        """Add a container to the cluster.

        :param container: the container to add."""
        if container.uuid in self.containers:
            pass
        container.wait_until_ready()
        self.containers[container.uuid] = container
        if self.conn is not None:
            self.conn().send_blocking_cmd(b'add_to_cluster', {'cluster':self.uuid,  'container':container.uuid})

    def remove_container(self, container):
        """Remove a container from the cluster.

        :param container: the container to remove."""
        try:
            del self.containers[container.uuid]
            if self.conn is not None:
                self.conn().send_cmd(b'remove_from_cluster', {'cluster':self.uuid,  'container':container.uuid})
        except KeyError:
            pass

    def uuids(self):
        return self.containers.keys()

    def __repr__(self):
        return "<Cluster '%s' containers=%d>" % (self.uuid, len(self.containers))


class WebEndpoint:
    __doc__ = 'An HTTP proxy that can expose a number of clusters onto a domain.'

    def __init__(self, location, domain: str):
        self.conn = weakref.ref(location.conn)
        self.domain = domain
        self.clusters = {}

    def publish(self, cluster: Cluster, fqdn: str, *, ssl: Optional[Tuple]=None):
        """Publish a cluster onto an http/https endpoint.
        To update a cluster, merely re-publish onto the same endpoint.

        :param cluster: The cluster to publish.
        :param fqdn: The fqdn to publish.
        :param ssl: A tuple of (cert.pem, key.pem) or (cert.pem, key.pem, cert.intermediate)."""
        if not fqdn.endswith(self.domain):
            raise ValueError('Web endpoint for (%s) cannot publish: %s' % (self.domain, fqdn))
        else:
            if cluster.uuid in self.clusters:
                return
            combined = None
            if ssl is not None:
                if len(ssl) not in (2, 3):
                    raise ValueError('SSL needs to be a tuple of (cert.pem, key.pem) or (cert.pem, key.pem, cert.intermediate')
                combined = ''
                with open(ssl[0]) as (f):
                    combined += f.read()
                with open(ssl[1]) as (f):
                    combined += f.read()
                if len(ssl) is 3:
                    with open(ssl[2]) as (f):
                        combined += f.read()
        subdomain = fqdn[:-len(self.domain)]
        msg = self.conn().send_blocking_cmd(b'publish_web', {'domain':self.domain,  'subdomain':subdomain, 
         'rewrite':cluster.rewrite, 
         'ssl':combined, 
         'containers':list(cluster.uuids())})
        logging.info('Published (%s) at: %s' % (msg.uuid.decode(), subdomain + self.domain))
        cluster.uuid = msg.uuid
        cluster.conn = weakref.ref(self.conn())
        self.clusters[msg.uuid] = cluster
        return msg.uuid

    @staticmethod
    def wait_http_200(fqdn: str, *, ssl: Optional[bool]=False):
        """Poll the gateway for an http 200 from this cluster.

        :param fqdn: the fqdn to poll.
        :param ssl: optionally connect via ssl."""
        url = '%s://%s' % ('https' if ssl else 'http', fqdn)
        attempts_remaining = 30
        while True:
            try:
                r = requests.get(url, timeout=5)
                if r.status_code == 200:
                    break
            except (ConnectionError, ConnectionRefusedError, ReadTimeout):
                pass

            attempts_remaining -= 1
            if attempts_remaining == 0:
                raise ValueError('Could not connect to: ' + url)
            time.sleep(1)

    def unpublish(self, cluster: Cluster):
        """Remove a cluster from a web endpoint.

        :param cluster: the cluster to remove."""
        if cluster.uuid is None or cluster.uuid not in self.clusters:
            return
        self.conn().send_cmd(b'unpublish_web', {'cluster': cluster.uuid})
        logging.info('Unpublished: ' + cluster.uuid.decode())
        cluster.conn = None
        del self.clusters[cluster.uuid]

    def __repr__(self):
        return "<WebEndpoint '%s' clusters=%d>" % (self.domain, len(self.clusters))