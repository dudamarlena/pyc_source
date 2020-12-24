# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/recompute/instance.py
# Compiled at: 2019-03-25 07:11:52
# Size of source mod 2**32: 7144 bytes
"""instance.py

We model (`username`, `host`, `password`) as an "instance".
`Instance` class holds username, host and password information.
It can be saved to and read from the global configuration file.
`InstanceManager` class reads instances from the configuration file by interacting with `ConfigManager`.

"""
from recompute import process
from recompute import cmd
from recompute import utils
import logging, pickle, os
logger = utils.get_logger(__name__)
PROBE_CACHE = '.recompute/table'

class Instance(object):
    __doc__ = 'Instance is a container for (`username`, `password`, `host`).'

    def __init__(self, username=None, password=None, host=None):
        """
    Parameters
    ----------
    username : str, optional
      User Name to log in to remote machine (default None)
    password : str, optional
      Password to log in to remote machine (default None)
    host : str, optional
      IP address or host name of remote machine (default None)
    """
        self.username = username
        self.password = password
        self.host = host

    def resolve_str(self, loginstr):
        """Create Instance object from string of type "username@host"

    Parameters
    ----------
    loginstr : str
      String of type "username@host"

    Returns
    -------
      instance.Instance
      An Instance object build based on `loginstr`
    """
        try:
            self.username, self.host = loginstr.strip().split('@')
            return self
        except ValueError:
            logging.error('Check Login [{}]'.format(loginstr))
            exit()

    def resolve_conf(self, conf):
        """Create Instance object from string of type "username@host"

    Parameters
    ----------
    conf : configparser.SectionProxy
      An instance section from config file

    Returns
    -------
      instance.Instance
      An Instance object build based on `conf`
    """
        self.username = conf['username']
        self.password = conf['password']
        self.host = conf['host']
        return self

    def __repr__(self):
        """Representation of form "username@host"

    Returns
    -------
    str
      "username@host" representation
    """
        return '{username}@{host}'.format(username=(self.username),
          host=(self.host))

    def __eq__(self, other):
        """Equivalence check of Instance objects

    Returns
    -------
    bool
      `True` if two instances are equivalent, `False` otherwise
    """
        return self.username == other.username and self.password == other.password and self.host == other.host


class InstanceManager(object):
    __doc__ = 'InstanceManager manages instances by interacting with ConfigManager.'

    def __init__(self, confman):
        """
    Parameters
    ----------
    confman : config.ConfigManager
      Configuration Manager object
    """
        self.confman = confman

    def add_instance(self, instance):
        """Add an instance to global config

    Parameters
    ----------
    instance : instance.Instance
      An Instance object
    """
        if not self.is_active(instance):
            raise AssertionError('Instance Inactive')
        elif not len([i for i in self.get_all() if i == instance]) == 0:
            raise AssertionError('Duplicate Instance')
        self.confman.add_instance(instance)

    def is_active(self, instance):
        """Is an instance active?

    Parameters
    ----------
    instance : instance.Instance
      An Instance object

    Returns
    -------
    bool
      `True` if instance is active, `False` otherwise
    """
        return not process.fetch_stderr(' '.join([
         cmd.SSH_HEADER.format(password=(instance.password)),
         cmd.SSH_TEST.format(username=(instance.username), host=(instance.host))]))

    def get(self, idx=None):
        """Find instance section from config file.

    Create an Instance object from the read instance section.

    Parameters
    ----------
    idx : int, optional
      Index of instance section in config file (default None)

    Returns
    -------
    instance.Instance
      An Instance object build on instance section read from config
    """
        instance = self.confman.get_instance(idx)
        assert instance, 'Instance inactive or absent in config'
        return Instance(instance['username'], instance['password'], instance['host'])

    def get_all(self):
        """Return a list of instances from config file.

    Read all the instance sections in config file.
    Create a list of Instance objects from the read sections.

    Returns
    -------
    list
      A list of Instance objects read from config
    """
        return [Instance().resolve_conf(instance) for instance in self.confman.get_instances()]

    def get_active(self):
        """Return a list of active instances.

    Create a list of Instance objects from the read sections.
    Filter out the inactive instances.

    Returns
    -------
    list
      A list of active Instance objects read from config
    """
        return [instance for instance in self.get_all() if self.is_active(instance)]

    def fetch(self):
        """Fetch an active instance by reading config file

    Returns
    -------
    instance.Instance
      An active Instance object
    """
        for instance in self.get_all():
            if self.is_active(instance):
                return instance

    def probe(self, force=False):
        """Probe all the active instances for the following information.

    * Free GPU Memory
    * Free Disk Space

    Parameters
    ----------
    force : bool, optional
      When set to `True`, probes remote devices for information
      When `False`, read from local cache (default False)

    Returns
    -------
    prettytable.PrettyTable
      A pretty-looking table of required information
    """
        if not force:
            if os.path.exists(PROBE_CACHE):
                return utils.tabulate_instances(pickle.load(open(PROBE_CACHE, 'rb')))
        instances = {}
        for instance in self.get_active():
            instances[str(instance)] = [
             str(instance), 'active', '-', '-']
            logger.info(instance)
            try:
                free_gpu_memory = int(process.remote_execute(cmd.GPU_FREE_MEMORY, instance)[(-1)])
                logger.info('FREE GPU')
                logger.info(free_gpu_memory)
                free_disk_space = utils.parse_free_results(process.remote_execute(cmd.DISK_FREE_MEMORY, instance)[(-1)])
                logger.info('FREE DISK')
                logger.info(free_disk_space)
                instances[str(instance)][2] = free_gpu_memory
                instances[str(instance)][3] = free_disk_space
            except ValueError:
                instances[str(instance)][1] = 'active'
                continue

        pickle.dump(instances, open(PROBE_CACHE, 'wb'))
        return utils.tabulate_instances(instances)