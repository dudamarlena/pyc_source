# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tfnz/location.py
# Compiled at: 2018-08-12 21:56:11
# Size of source mod 2**32: 17687 bytes
import logging, socket, time, os, requests, requests.exceptions, termios, sys
from typing import Union, List, Optional
from base64 import b64encode
from subprocess import run, CalledProcessError, DEVNULL
from messidge import default_location
from messidge.client.connection import Connection
from . import TaggedCollection, Taggable, Waitable
from .docker import Docker
from .endpoint import WebEndpoint
from .node import Node
from .send import Sender
from .tunnel import Tunnel
from .volume import Volume
from .container import ExternalContainer

class Location(Waitable):
    __doc__ = 'The root location object.\n\n        :param location: An optional fqdn of the location (i.e. tiny.20ft.nz).\n        :param location_ip: A optional explicit ip for the broker.\n        :param quiet: Set true to not configure logging.\n        :param debug_log: Set true to log at DEBUG logging level.\n        :param new_node_callback: An optional callback for when a node is created ... signature (object)\n        '

    def __init__(self, *, location=None, location_ip=None, quiet=False, debug_log=False, new_node_callback=None):
        super().__init__()
        self.location = location if location is not None else default_location(prefix='~/.20ft')
        self.nodes = {}
        self.volumes = TaggedCollection()
        self.externals = TaggedCollection()
        self.tunnels = {}
        self.endpoints = {}
        self.new_node_callback = new_node_callback
        self.last_heartbeat = time.time()
        ip = location_ip if location_ip is not None else self.location
        try:
            run(['ping', '-c', '1', ip], check=True, stdout=DEVNULL)
        except CalledProcessError:
            raise RuntimeError('Cannot ping the requested ip: ' + ip)

        if debug_log:
            if quiet:
                raise ValueError("Can't select both quiet and verbose logging")
        if debug_log or quiet is False:
            logging.basicConfig(level=(logging.DEBUG if debug_log else logging.INFO), format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
              datefmt='%m%d%H%M%S')
        self.conn = Connection((self.location), prefix='~/.20ft', location_ip=location_ip, exit_on_exception=True)
        self.user_pk = self.conn.keys.public_binary()
        self.conn.register_commands(self, Location._commands)
        self.conn.start()
        self.conn.wait_until_ready()
        self.wait_until_ready()
        self.conn.loop.register_on_idle(self._heartbeat)
        try:
            self.stdin_attr = termios.tcgetattr(sys.stdin.fileno())
        except (termios.error, AttributeError):
            self.stdin_attr = None

    def run(self):
        """Wait until the message loop completes, may raise an exception passed from the background thread."""
        try:
            try:
                self.conn.wait_until_complete()
            except KeyboardInterrupt:
                pass

        finally:
            self.complete()
            self.disconnect()

    def complete(self, container=None, returncode=0):
        """Stop the background loop, causes 'run' to return. Call to close from the background thread."""
        logging.debug('Complete called on location')
        self.conn.loop.stop()

    def disconnect(self, container=None, returncode=0):
        """Disconnect from the location - without calling this the object cannot be garbage collected"""
        if self.conn is None:
            return
        if self.stdin_attr is not None:
            try:
                termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW, self.stdin_attr)
                print('', end='\r', flush=True)
            except ValueError:
                pass

        for endpoint in list(self.endpoints.values()):
            [endpoint.unpublish(cluster) for cluster in list(endpoint.clusters.values())]

        for node in self.nodes.values():
            for container in [c for c in node.containers.values() if not c.dead]:
                node.destroy_container(container)

        logging.info('Disconnecting: ' + self.location)
        self.conn.disconnect()
        self.conn = None

    def node(self) -> Node:
        """Returns a node.

           :return: A node object"""
        return self.ranked_nodes()[0]

    def ranked_nodes(self) -> List[Node]:
        """Ranks the nodes in order of resource availability.

        :return: A list of node objects."""
        nodes = self.nodes.values()
        if len(nodes) == 0:
            raise ValueError('The location has no nodes')
        return sorted(nodes, key=(lambda node: node.stats['cpu'] + node.stats['memory'] - 10 * node.stats['paging']),
          reverse=True)

    def create_volume(self, *, tag: Optional[str]=None, asynchronous: Optional[bool]=True, termination_callback: Optional=None) -> Volume:
        """Creates a new volume

        :param tag: An optional globally visible tag.
        :param asynchronous: Enables asynchronous writes.
        :param termination_callback: a callback if this volume is destroyed - signature (container, returncode).
        :return: The new Volume object.

        Note that asynchronous writes cannot damage a ZFS filesystem although the physical state may lag behind the
        logical state by a number of seconds. Asynchronous ZFS is *very* much faster than synchronous."""
        tag = Taggable.valid_tag(tag)
        msg = self.conn.send_blocking_cmd(b'create_volume', {'user':self.user_pk,  'tag':tag, 
         'asynchronous':asynchronous})
        logging.info('Created volume: ' + msg.uuid.decode())
        vol = Volume(self, (msg.uuid), tag, termination_callback=termination_callback)
        self.volumes.add(vol)
        return vol

    def ensure_volume(self, key: Union[(bytes, str)]) -> Volume:
        """Return the volume with this uuid, tag or display_name - create the volume if it doesn't exist.

        :param key: The uuid or tag of the volume object to be returned.
        :return: A Volume object."""
        try:
            return self.volumes.get(self.user_pk, key)
        except KeyError:
            return self.create_volume(tag=key)

    def destroy_volume(self, volume: Volume):
        """Destroys an existing volume. This is not a 'move to trash', it will be destroyed.

        :param volume: The volume to be destroyed."""
        self.conn.send_blocking_cmd(b'destroy_volume', {'user':self.user_pk,  'volume':volume.uuid})
        logging.info('Destroyed volume: ' + volume.uuid.decode())
        volume.internal_destroy()
        self.volumes.remove(volume)

    def all_volumes(self) -> List[Volume]:
        """Returns a list of all volumes on this node.

        :return: A list of Volume objects."""
        return list(self.volumes.values())

    def volume(self, key: Union[(bytes, str)]) -> Volume:
        """Return the volume with this uuid, tag or display_name.

        :param key: The uuid or tag of the volume object to be returned.
        :return: A Volume object."""
        return self.volumes.get(self.user_pk, key)

    def endpoint_for(self, fqdn: str) -> WebEndpoint:
        """Return a WebEndpoint for the given fqdn.

        :param fqdn: The fully qualified name the endpoint will represent.
        :return: A WebEndpoint object."""
        for domain, ep in self.endpoints.items():
            if fqdn.endswith(domain):
                return ep

        raise ValueError('There is no endpoint capable of serving: ' + fqdn)

    def external_container(self, key: Union[(bytes, str)]) -> ExternalContainer:
        """Return the external container with this uuid, tag or display_name.

        :param key: The uuid or tag of the container to be returned.
        :return: An ExternalContainer object."""
        return self.externals.get(self.user_pk, key)

    def ensure_image_uploaded(self, docker_image_id: str, *, descr: Optional[dict]=None) -> List[str]:
        """Sends missing docker layers to the location.

        :param docker_image_id: use the short form id or tag
        :param descr: a previously found docker description
        :return: A list of layer sha256 identifiers

        This is not a necessary step and is implied when spawning a container."""
        if descr is None:
            descr = Docker.description(docker_image_id, conn=(self.conn))
        else:
            self.conn.send_cmd(b'cache_description', {'image_id':docker_image_id,  'description':descr})
        layers = Sender.layer_stack(descr)
        to_upload = Sender.upload_requirements(layers, self.conn)
        logging.info('Ensuring layers (%d) are uploaded for: %s' % (len(layers), docker_image_id))
        if len(to_upload) > 0:
            logging.info('Layers to upload: %d of %d' % (len(to_upload), len(layers)))
            Sender.send(docker_image_id, to_upload, self.conn)
        return layers

    @staticmethod
    def all_locations():
        """Returns a (text) list of 20ft locations that have an account on this machine."""
        dirname = os.path.expanduser('~/.20ft/')
        all_files = os.listdir(dirname)
        locations = []
        for file in all_files:
            if file[-4:] == '.pub':
                continue
            if file + '.pub' in all_files:
                locations.append(file)

        return locations

    def _heartbeat(self):
        if time.time() - self.last_heartbeat < 30:
            return
        self.last_heartbeat = time.time()
        self.conn.send_cmd(b'heartbeat')

    def tunnel_onto(self, container, port, localport, bind, *, timeout=30) -> Tunnel:
        if isinstance(port, str):
            port = int(port)
        if isinstance(localport, str):
            localport = int(localport)
        container.wait_until_ready()
        tunnel = Tunnel(self.conn, container.parent(), container, port, localport, bind, timeout)
        self.tunnels[tunnel.uuid] = tunnel
        tunnel.connect()
        return tunnel

    def wait_tcp(self, container, dest_port):
        logging.info('Waiting on tcp (%d): %s' % (dest_port, container.uuid.decode()))
        self.conn.send_blocking_cmd(b'wait_tcp', {'container':container.uuid,  'port':dest_port})

    def wait_http_200(self, container, dest_port, fqdn, path, localport=None) -> Tunnel:
        addr = socket.gethostbyname(fqdn)
        if addr != '127.0.0.1':
            raise ValueError("FQDN '%s' does not resolve to localhost" % fqdn)
        logging.info('Waiting on http 200: ' + container.uuid.decode())
        tnl = self.tunnel_onto(container, dest_port, localport, None)
        logging.debug('Tunnel connected onto: ' + container.uuid.decode())
        url = 'http://%s:%d/%s' % (fqdn, tnl.localport(), path if path is not None else '')
        r = requests.get(url, timeout=240)
        if r.status_code == 200:
            logging.info('Connected onto: ' + url)
            return tnl
        raise ValueError('Could not connect to: ' + url)

    def destroy_tunnel(self, tunnel: Tunnel, container=None, with_command=True):
        tunnel.destroy(with_command)
        del self.tunnels[tunnel.uuid]

    def _from_proxy(self, msg):
        try:
            tunnel = self.tunnels[msg.uuid]
        except KeyError:
            logging.debug('Data apparently from an already removed tunnel (dropped)')
            return
        else:
            try:
                tunnel.from_proxy(msg)
            except KeyError:
                logging.debug('Data arrived from a proxy we seemingly already closed')

    def _close_proxy(self, msg):
        try:
            tunnel = self.tunnels[msg.uuid]
        except KeyError:
            logging.debug('Asked to close a proxy on an already removed tunnel (dropped)')
            return
        else:
            try:
                tunnel.close_proxy(msg)
            except KeyError:
                logging.debug('Asked to close a proxy that we already closed')

    def _resource_offer(self, msg):
        self.endpoints = {dom['domain']:WebEndpoint(self, dom['domain']) for dom in msg.params['domains']}
        self.nodes = {node[0]:Node(self, node[0], self.conn, node[1]) for node in msg.params['nodes']}
        self.volumes = TaggedCollection([Volume(self, vol['uuid'], vol['tag']) for vol in msg.params['volumes']])
        self.externals = TaggedCollection([ExternalContainer(self, xtn['uuid'], xtn['node'], xtn['ip'], xtn['tag']) for xtn in msg.params['externals']])
        self.mark_as_ready()

    def _update_stats(self, msg):
        node = self._ensure_node(msg)
        node.update_stats(msg.params['stats'])

    def _node_created(self, msg):
        if msg.params['node'] in self.nodes:
            return
        logging.debug('Notify - node created: ' + b64encode(msg.params['node']).decode())
        n = Node(self, msg.params['node'], self.conn, {'memory':1000,  'cpu':1000,  'paging':0,  'ave_start_time':0})
        self.nodes[msg.params['node']] = n
        if self.new_node_callback is not None:
            self.new_node_callback(n)

    def _node_destroyed(self, msg):
        logging.debug('Notify - node destroyed: ' + b64encode(msg.params['node']).decode())
        node = self._ensure_node(msg)
        node.internal_destroy()
        del self.nodes[msg.params['node']]

    def _volume_created(self, msg):
        logging.debug('Notify - volume created: ' + msg.params['volume'].decode())
        self.volumes.add(Volume(self, msg.params['volume'], msg.params['tag']))

    def _volume_destroyed(self, msg):
        logging.debug('Notify - volume destroyed: ' + msg.params['volume'].decode())
        vol = self.ensure_volume(msg.params['volume'])
        vol.internal_destroy()
        self.volumes.remove(vol)

    def _log(self, msg):
        if msg.params['error']:
            logging.error(msg.params['log'])
        else:
            logging.info(msg.params['log'])

    def _ensure_node(self, msg):
        if msg.params['node'] not in self.nodes:
            raise ValueError("Didn't know about node: " + b64encode(msg.params['node']).decode())
        return self.nodes[msg.params['node']]

    def _ensure_volume(self, msg):
        if msg.params['volume'] not in self.volumes:
            raise ValueError("Didn't know about volume: " + b64encode(msg.params['node']).decode())
        return self.volumes[msg.params['volume']]

    _commands = {b'resource_offer':([], False),  b'node_created':(
      [
       'node'], False), 
     b'node_destroyed':(
      [
       'node'], False), 
     b'volume_created':(
      [
       'volume', 'tag'], False), 
     b'volume_destroyed':(
      [
       'volume'], False), 
     b'external_created':(
      [
       'container', 'tag'], False), 
     b'external_destroyed':(
      [
       'container'], False), 
     b'from_proxy':(
      [
       'proxy'], False), 
     b'close_proxy':(
      [
       'proxy'], False), 
     b'update_stats':(
      [
       'node', 'stats'], False), 
     b'log':(
      [
       'error', 'log'], False)}

    def __repr__(self):
        return "<Location '%s' nodes=%d>" % (self.location, len(self.nodes))