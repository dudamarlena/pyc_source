# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/elasticluster/providers/openstack.py
# Compiled at: 2014-10-22 16:00:16
__docformat__ = 'reStructuredText'
__author__ = 'Antonio Messina <antonio.s.messina@gmail.com>'
import os, threading
from novaclient import client
from novaclient.exceptions import NotFound
from paramiko import DSSKey, RSAKey, PasswordRequiredException
from paramiko.ssh_exception import SSHException
from elasticluster import log
from elasticluster.memoize import memoize
from elasticluster.providers import AbstractCloudProvider
from elasticluster.exceptions import SecurityGroupError, KeypairError, ImageError, InstanceError, ClusterError
DEFAULT_OS_NOVA_API_VERSION = '1.1'

class OpenStackCloudProvider(AbstractCloudProvider):
    """
    This implementation of
    :py:class:`elasticluster.providers.AbstractCloudProvider` uses the
    OpenStack native python bindings to connect to OpenStack clouds
    and manage instances.

    :param str username: username of the keystone user
    :param str password: password of the keystone user
    :param str project_name: name of the project to use
    :param str auth_url: url of keystone endpoint
    :param str region: OpenStack region to use
    :param str storage_path: path to store temporary data
    :param bool request_floating_ip: Whether ip are assigned automatically
                                    `True` or floating ips have to be
                                    assigned manually `False`
    
    """
    __node_start_lock = threading.Lock()

    def __init__(self, username, password, project_name, auth_url, region_name=None, storage_path=None, request_floating_ip=False, nova_api_version=DEFAULT_OS_NOVA_API_VERSION):
        self._os_auth_url = auth_url
        self._os_username = username
        self._os_password = password
        self._os_tenant_name = project_name
        self._os_region_name = region_name
        self.request_floating_ip = request_floating_ip
        self.nova_api_version = nova_api_version
        self._instances = {}
        self._cached_instances = []
        self.client = client.Client(self.nova_api_version, self._os_username, self._os_password, self._os_tenant_name, self._os_auth_url, region_name=self._os_region_name)

    def start_instance(self, key_name, public_key_path, private_key_path, security_group, flavor, image_id, image_userdata, username=None, node_name=None, **kwargs):
        """Starts a new instance on the cloud using the given properties.
        The following tasks are done to start an instance:

        * establish a connection to the cloud web service
        * check ssh keypair and upload it if it does not yet exist. This is
          a locked process, since this function might be called in multiple
          threads and we only want the key to be stored once.
        * check if the security group exists
        * run the instance with the given properties

        :param str key_name: name of the ssh key to connect
        :param str public_key_path: path to ssh public key
        :param str private_key_path: path to ssh private key
        :param str security_group: firewall rule definition to apply on the
                                   instance
        :param str flavor: machine type to use for the instance
        :param str image_id: image type (os) to use for the instance
        :param str image_userdata: command to execute after startup
        :param str username: username for the given ssh key, default None

        :return: str - instance id of the started instance
        """
        log.debug('Checking keypair `%s`.', key_name)
        with OpenStackCloudProvider.__node_start_lock:
            self._check_keypair(key_name, public_key_path, private_key_path)
        log.debug('Checking security group `%s`.', security_group)
        self._check_security_group(security_group)
        images = self._get_images()
        if image_id not in [ img.id for img in images ]:
            raise ImageError("No image found with id '%s' on cloud %s" % (
             image_id, self._os_auth_url))
        flavors = [ fl for fl in self._get_flavors() if fl.name == flavor ]
        if not flavors:
            raise FlavorError('No flavor found with name %s on cloud %s' % (
             flavor, self._os_auth_url))
        flavor = flavors[0]
        nics = None
        if 'network_ids' in kwargs:
            nics = [ {'net-id': netid.strip(), 'v4-fixed-ip': ''} for netid in kwargs['network_ids'].split(',') ]
            log.debug('Specifying networks for vm %s: %s', node_name, str.join(', ', [ nic['net-id'] for nic in nics ]))
        vm = self.client.servers.create(node_name, image_id, flavor, key_name=key_name, security_groups=[
         security_group], userdata=image_userdata, nics=nics)
        self._instances[vm.id] = vm
        return vm.id

    def stop_instance(self, instance_id):
        """Stops the instance gracefully.

        :param str instance_id: instance identifier
        """
        instance = self._load_instance(instance_id)
        instance.delete()
        del self._instances[instance_id]

    def get_ips(self, instance_id):
        """Retrieves the private and public ip addresses for a given instance.

        :return: tuple (IPs)
        """
        self._load_instance(instance_id)
        instance = self._load_instance(instance_id)
        IPs = sum(instance.networks.values(), [])
        if self.request_floating_ip:
            floating_ips = [ ip for ip in self.client.floating_ips.list() if ip.instance_id == instance.id ]
            if not floating_ips:
                log.debug('Public ip address has to be assigned through elasticluster.')
                ip = self._allocate_address(instance)
                IPs.insert(0, ip)
        return IPs

    def is_instance_running(self, instance_id):
        """Checks if the instance is up and running.

        :param str instance_id: instance identifier

        :return: bool - True if running, False otherwise
        """
        instance = self._load_instance(instance_id, force_reload=True)
        return instance.status == 'ACTIVE'

    def _check_keypair(self, name, public_key_path, private_key_path):
        """First checks if the keypair is valid, then checks if the keypair
        is registered with on the cloud. If not the keypair is added to the
        users ssh keys.

        :param str name: name of the ssh key
        :param str public_key_path: path to the ssh public key file
        :param str private_key_path: path to the ssh private key file

        :raises: `KeypairError` if key is not a valid RSA or DSA key,
                 the key could not be uploaded or the fingerprint does not
                 match to the one uploaded to the cloud.
        """
        pkey = None
        try:
            pkey = DSSKey.from_private_key_file(private_key_path)
        except PasswordRequiredException:
            log.warning('Unable to check key file `%s` because it is encrypted with a password. Please, ensure that you added it to the SSH agent with `ssh-add %s`', private_key_path, private_key_path)
        except SSHException:
            try:
                pkey = RSAKey.from_private_key_file(private_key_path)
            except PasswordRequiredException:
                log.warning('Unable to check key file `%s` because it is encrypted with a password. Please, ensure that you added it to the SSH agent with `ssh-add %s`', private_key_path, private_key_path)
            except SSHException:
                raise KeypairError('File `%s` is neither a valid DSA key or RSA key.' % private_key_path)

        try:
            keypair = self.client.keypairs.get(name)
            fingerprint = str.join(':', (i.encode('hex') for i in pkey.get_fingerprint()))
            if fingerprint != keypair.fingerprint:
                raise KeypairError('Keypair `%s` is present but has different fingerprint. Aborting!' % name)
        except NotFound:
            log.warning('Keypair `%s` not found on resource `%s`, Creating a new one', name, self._os_auth_url)
            with open(os.path.expanduser(public_key_path)) as (f):
                key_material = f.read()
                try:
                    self.client.keypairs.create(name, key_material)
                except Exception as ex:
                    log.error('Could not import key `%s` with name `%s` to `%s`', name, public_key_path, self._os_auth_url)
                    raise KeypairError('could not create keypair `%s`: %s' % (name, ex))

        return

    def _check_security_group(self, name):
        """Checks if the security group exists.

        :param str name: name of the security group
        :raises: `SecurityGroupError` if group does not exist
        """
        security_groups = self.client.security_groups.list()
        if name not in [ sg.name for sg in security_groups ]:
            raise SecurityGroupError('the specified security group %s does not exist' % name)

    @memoize(120)
    def _get_images(self):
        """Get available images. We cache the results in order to reduce
        network usage.

        """
        return self.client.images.list()

    @memoize(120)
    def _get_flavors(self):
        """Get available flavors. We cache the results in order to reduce
        network usage.

        """
        return self.client.flavors.list()

    def _load_instance(self, instance_id, force_reload=True):
        """Checks if an instance with the given id is cached. If not it
        will connect to the cloud and put it into the local cache
        _instances.

        :param str instance_id: instance identifier
        :param bool force_reload: reload instance from server
        :return: py:class:`novaclient.v1_1.servers.Server` - instance
        :raises: `InstanceError` is returned if the instance can't
                 be found in the local cache or in the cloud.
        """
        if force_reload:
            try:
                vm = self.client.servers.get(instance_id)
                self._instances[instance_id] = vm
                for i in self._cached_instances:
                    if i.id == instance_id:
                        self._cached_instances.remove(i)
                        self._cached_instances.append(vm)
                        break

            except NotFound:
                raise InstanceError('the given instance `%s` was not found on the coud' % instance_id)

        if instance_id in self._instances:
            return self._instances[instance_id]
        if instance_id not in [ i.id for i in self._cached_instances ]:
            self._cached_instances = self.client.servers.list()
        for inst in self._cached_instances:
            if inst.id == instance_id:
                self._instances[instance_id] = inst
                return inst

        raise InstanceError('the given instance `%s` was not found on the coud' % instance_id)

    def _allocate_address(self, instance):
        """Allocates a free public ip address to the given instance

        :param instance: instance to assign address to
        :type instance: py:class:`novaclient.v1_1.servers.Server`

        :return: public ip address
        """
        with OpenStackCloudProvider.__node_start_lock:
            free_ips = [ i for i in self.client.floating_ips.list() if not i.fixed_ip ]
            if not free_ips:
                free_ips.append(self.client.floating_ips.create())
            ip = free_ips.pop()
            instance.add_floating_ip(ip)
        return ip.ip

    def __getstate__(self):
        return {'auth_url': self._os_auth_url, 'username': self._os_username, 
           'password': self._os_password, 
           'project_name': self._os_tenant_name, 
           'region_name': self._os_region_name, 
           'request_floating_ip': self.request_floating_ip, 
           'instance_ids': self._instances.keys(), 
           'nova_api_version': self.nova_api_version}

    def __setstate__(self, state):
        self._os_auth_url = state['auth_url']
        self._os_username = state['username']
        self._os_password = state['password']
        self._os_tenant_name = state['project_name']
        self._os_region_name = state['region_name']
        self.request_floating_ip = state['request_floating_ip']
        self.nova_api_version = state.get('nova_api_version', DEFAULT_OS_NOVA_API_VERSION)
        self.client = client.Client(self.nova_api_version, self._os_username, self._os_password, self._os_tenant_name, self._os_auth_url, region_name=self._os_region_name)
        self._instances = {}
        self._cached_instances = []