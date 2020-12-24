# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/cache/salt-napalm/lib/salt_napalm/_runners/napalm.py
# Compiled at: 2019-01-18 06:45:28
"""
NAPALM: NETWORK AUTOMATION AND PROGRAMMABILITY ABSTRACTION LAYER WITH MULTIVENDOR SUPPORT
=========================================================================================

Salt Runner to invoke arbitrary commands on network devices that are not
managed via a Proxy or regular Minion. Therefore, this Runner doesn't
necessarily require the targets to be up and running, as it will connect to
gather the facts, then execute the commands - with various limitations.
"""
from __future__ import absolute_import, print_function, unicode_literals
import copy, logging, threading, multiprocessing, salt.loader, salt.output, salt.utils.jid
from salt.ext import six
from salt.minion import SMinion
from salt.ext.six.moves import range
import salt.defaults.exitcodes
from salt.exceptions import SaltSystemExit
try:
    from salt.utils import clean_kwargs
except ImportError:
    from salt.utils.args import clean_kwargs

try:
    import napalm
    HAS_NAPALM = True
except ImportError:
    HAS_NAPALM = False

__virtualname__ = b'napalm'
log = logging.getLogger(__name__)

def __virtual__():
    return HAS_NAPALM


def _salt_call_and_return(minion_id, function, queue, arg=None, jid=None, events=True, **opts):
    """
    """
    opts[b'minion_id'] = minion_id
    ret = salt_call(function, **opts)
    if events:
        __salt__[b'event.send']((b'napalm/runner/{jid}/ret/{minion_id}').format(minion_id=minion_id, jid=jid), {b'fun': function, 
           b'fun_args': arg, 
           b'id': minion_id, 
           b'jid': jid, 
           b'return': ret, 
           b'success': True})
    queue.put({minion_id: ret})


def _receive_replies_async(queue):
    """
    """
    while True:
        ret = queue.get()
        if ret == b'FIN.':
            break
        out_fmt = salt.output.out_format(ret, __opts__.get(b'output', b'nested'), opts=__opts__)
        print(out_fmt)


class SProxyMinion(SMinion):
    """
    Create an object that has loaded all of the minion module functions,
    grains, modules, returners etc.  The SProxyMinion allows developers to
    generate all of the salt minion functions and present them with these
    functions for general use.
    """

    def gen_modules(self, initial_load=False):
        """
        Tell the minion to reload the execution modules
        CLI Example:
        .. code-block:: bash
            salt '*' sys.reload_modules
        """
        grains = copy.deepcopy(self.opts[b'grains'])
        cached_pillar = None
        if self.opts.get(b'proxy_use_cached_grains', True):
            cached_grains = self.opts.pop(b'proxy_cached_grains', None)
        if not cached_grains and self.opts.get(b'proxy_preload_grains', True):
            self.opts[b'grains'] = salt.loader.grains(self.opts)
            self.opts[b'grains'].update(grains)
        elif cached_grains:
            self.opts[b'grains'].update(cached_grains)
        cached_pillar = None
        if self.opts.get(b'proxy_use_cached_pillar', True):
            cached_pillar = self.opts.pop(b'proxy_cached_pillar', None)
        if not cached_pillar and self.opts.get(b'proxy_load_pillar', True):
            self.opts[b'pillar'] = salt.pillar.get_pillar(self.opts, self.opts[b'grains'], self.opts[b'id'], saltenv=self.opts[b'saltenv'], pillarenv=self.opts.get(b'pillarenv')).compile_pillar()
        if b'proxy' not in self.opts[b'pillar'] and b'proxy' not in self.opts:
            errmsg = (b'No "proxy" configuration key found in pillar or opts dictionaries for id {id}. Check your pillar/options configuration and contents. Salt-proxy aborted.').format(id=self.opts[b'id'])
            log.error(errmsg)
            self._running = False
            raise SaltSystemExit(code=salt.defaults.exitcodes.EX_GENERIC, msg=errmsg)
        if b'proxy' not in self.opts:
            self.opts[b'proxy'] = self.opts[b'pillar'][b'proxy']
        self.proxy = salt.loader.proxy(self.opts)
        self.utils = salt.loader.utils(self.opts, proxy=self.proxy)
        self.functions = salt.loader.minion_mods(self.opts, utils=self.utils, notify=False, proxy=self.proxy)
        self.returners = salt.loader.returners(self.opts, self.functions, proxy=self.proxy)
        self.functions[b'sys.reload_modules'] = self.gen_modules
        fq_proxyname = self.opts[b'proxy'][b'proxytype']
        self.functions.pack[b'__proxy__'] = self.proxy
        self.proxy.pack[b'__salt__'] = self.functions
        self.proxy.pack[b'__ret__'] = self.returners
        self.proxy.pack[b'__pillar__'] = self.opts[b'pillar']
        self.utils = salt.loader.utils(self.opts, proxy=self.proxy)
        self.proxy.pack[b'__utils__'] = self.utils
        self.proxy.reload_modules()
        if (b'{0}.init').format(fq_proxyname) not in self.proxy or (b'{0}.shutdown').format(fq_proxyname) not in self.proxy:
            errmsg = (b'Proxymodule {0} is missing an init() or a shutdown() or both. ').format(fq_proxyname) + b'Check your proxymodule.  Salt-proxy aborted.'
            log.error(errmsg)
            self._running = False
            raise SaltSystemExit(code=salt.defaults.exitcodes.EX_GENERIC, msg=errmsg)
        proxy_init_fn = self.proxy[(fq_proxyname + b'.init')]
        proxy_init_fn(self.opts)
        if not cached_grains and self.opts.get(b'proxy_load_grains', True):
            self.opts[b'grains'] = salt.loader.grains(self.opts, proxy=self.proxy)
            self.opts[b'grains'].update(grains)
        self.grains_cache = self.opts[b'grains']
        self.ready = True
        return


class NAPALMProxy(SProxyMinion):

    def __init__(self, opts):
        self.opts = opts
        self.gen_modules()


def get_connection(driver, hostname, username, password, timeout=60, optional_args=None, provider=None, minion_id=None, with_pillar=False, with_grains=False, default_pillar=None, default_grains=None):
    """
    Return the NAPALM connection object together with the associated Salt
    dunders packed, i.e., ``__salt__``, ``__utils__``, ``__opts__``, etc.

    This function establishes the connection to the remote device through
    NAPALM and returns the connection object.

    .. note::
        This function is not designed for CLI usage, but rather invoked from
        other Salt Runners.
        Similarly, it is up to the developer to ensure that the connection is
        closed properly.

    driver
        Specifies the network device operating system.
        For a complete list of the supported operating systems please refer to the
        `NAPALM Read the Docs page`_.

    hostname
        The IP Address or name server to use when connecting to the device.

    username
        The username to be used when connecting to the device.

    password
        The password needed to establish the connection.

        .. note::
            This field may not be mandatory when working with SSH-based drivers, and
            the username has a SSH key properly configured on the device targeted to
            be managed.

    optional_args
        Dictionary with the optional arguments.
        Check the complete list of supported `optional arguments`_.

    provider: ``napalm_base``
        The library that provides the ``get_network_device`` function.
        This option is useful when the user has more specific needs and requires
        to extend the NAPALM capabilities using a private library implementation.
        The only constraint is that the alternative library needs to have the
        ``get_network_device`` function available.

    default_grains:
        Dictionary of the default Grains to make available within the functions
        loaded.

    with_grains: ``False``
        Whether to load the Grains modules and collect Grains data and make it
        available inside the Execution Functions.

    default_pillar:
        Dictionary of the default Pillar data to make it available within the
        functions loaded.

    with_pillar: ``False``
        Whether to load the Pillar modules and compile Pillar data and make it
        available inside the Execution Functions.

    minion_id:
        The ID of the Minion to compile Pillar data for.

    .. _`NAPALM Read the Docs page`: https://napalm.readthedocs.io/en/latest/#supported-network-operating-systems
    .. _`optional arguments`: http://napalm.readthedocs.io/en/latest/support/index.html#list-of-supported-optional-arguments

    Usage Example:

    .. code-block:: python

        napalm_device = __salt__['napalm.get_connection']('eos', '1.2.3.4', 'test', 'test')
    """
    if not optional_args:
        optional_args = {}
    opts = copy.deepcopy(__opts__)
    if b'proxy' not in opts:
        opts[b'proxy'] = {}
    opts[b'proxy'].update({b'proxytype': b'napalm', 
       b'driver': driver, 
       b'hostname': hostname, 
       b'username': username, 
       b'passwd': password, 
       b'timeout': timeout, 
       b'optional_args': optional_args, 
       b'provider': provider})
    if b'saltenv' not in opts:
        opts[b'saltenv'] = b'base'
    if minion_id:
        opts[b'id'] = minion_id
    opts[b'grains'] = {}
    if default_grains:
        opts[b'grains'] = default_grains
    if with_grains:
        opts[b'grains'].update(salt.loader.grains(opts))
    opts[b'pillar'] = {}
    if default_pillar:
        opts[b'pillar'] = default_pillar
    if with_pillar:
        opts[b'pillar'].update(salt.pillar.get_pillar(opts, opts[b'grains'], opts[b'id'], saltenv=opts[b'saltenv'], pillarenv=opts.get(b'pillarenv')).compile_pillar())
    __utils__ = salt.loader.utils(opts)
    functions = salt.loader.minion_mods(opts, utils=__utils__, context=__context__)
    napalm_device = __utils__[b'napalm.get_device'](opts, salt_obj=functions)
    napalm_device.update({b'__utils__': __utils__, b'__opts__': opts, b'__salt__': functions})
    return napalm_device


def call(method, driver, hostname, username, password, timeout=60, optional_args=None, provider=None, **kwargs):
    """
    Execute an arbitrary NAPALM method and return the result.

    method
        The name of the NAPALM method to invoke. Example: ``get_bgp_neighbors``.

    driver
        Specifies the network device operating system.
        For a complete list of the supported operating systems please refer to the
        `NAPALM Read the Docs page`_.

    hostname
        The IP Address or name server to use when connecting to the device.

    username
        The username to be used when connecting to the device.

    password
        The password needed to establish the connection.

        .. note::
            This field may not be mandatory when working with SSH-based drivers, and
            the username has a SSH key properly configured on the device targeted to
            be managed.

    optional_args
        Dictionary with the optional arguments.
        Check the complete list of supported `optional arguments`_.

    provider: ``napalm_base``
        The library that provides the ``get_network_device`` function.
        This option is useful when the user has more specific needs and requires
        to extend the NAPALM capabilities using a private library implementation.
        The only constraint is that the alternative library needs to have the
        ``get_network_device`` function available.

    .. _`NAPALM Read the Docs page`: https://napalm.readthedocs.io/en/latest/#supported-network-operating-systems
    .. _`optional arguments`: http://napalm.readthedocs.io/en/latest/support/index.html#list-of-supported-optional-arguments

    CLI Example:

    .. code-block:: bash

        salt-run napalm.call get_bgp_neighbors eos 1.2.3.4 test test123
    """
    napalm_device = get_connection(driver, hostname, username, password, timeout=timeout, optional_args=optional_args, provider=provider)
    __utils__ = napalm_device[b'__utils__']
    ret = __utils__[b'napalm.call'](napalm_device, method, **kwargs)
    try:
        __utils__[b'napalm.call'](napalm_device, b'close')
    except Exception as err:
        log.error(err)

    return ret


def salt_call(function, driver, hostname, username, password, timeout=60, optional_args=None, provider=None, minion_id=None, with_grains=True, preload_grains=True, with_pillar=True, preload_pillar=False, default_grains=None, default_pillar=None, cache_grains=False, cache_pillar=False, use_cached_grains=True, use_cached_pillar=True, args=(), **kwargs):
    """
    Invoke a Salt Execution Function that requires or invokes an NAPALM
    functionality (directly or indirectly).

    driver
        Specifies the network device operating system.
        For a complete list of the supported operating systems please refer to
        the `NAPALM Read the Docs page`_.

    hostname
        The IP Address or name server to use when connecting to the device.

    username
        The username to be used when connecting to the device.

    password
        The password needed to establish the connection.

        .. note::
            This field may not be mandatory when working with SSH-based drivers,
            and the username has a SSH key properly configured on the device
            targeted to be managed.

    optional_args
        Dictionary with the optional arguments.
        Check the complete list of supported `optional arguments`_.

    provider: ``napalm_base``
        The library that provides the ``get_network_device`` function.
        This option is useful when the user has more specific needs and requires
        to extend the NAPALM capabilities using a private library implementation.
        The only constraint is that the alternative library needs to have the
        ``get_network_device`` function available.

    preload_grains: ``True``
        Whether to preload the Grains before establishing the connection with
        the remote network device.

    default_grains:
        Dictionary of the default Grains to make available within the functions
        loaded.

    with_grains: ``True``
        Whether to load the Grains modules and collect Grains data and make it
        available inside the Execution Functions.
        The Grains will be loaded after opening the connection with the remote
        network device.

    preload_pillar: ``False``
        Whether to preload Pillar data before opening the connection with the
        remote network device.

    default_pillar:
        Dictionary of the default Pillar data to make it available within the
        functions loaded.

    with_pillar: ``True``
        Whether to load the Pillar modules and compile Pillar data and make it
        available inside the Execution Functions.

    arg
        The list of arguments to send to the Salt function.

    kwargs
        Key-value arguments to send to the Salt function.

    minion_id:
        The ID of the Minion to compile Pillar data for.

    use_cached_pillar: ``True``
        Use cached Pillars whenever possible. If unable to gather cached data,
        it falls back to compiling the Pillar.

    use_cached_grains: ``True``
        Use cached Grains whenever possible. If unable to gather cached data,
        it falls back to collecting Grains.

    cache_pillar: ``False``
        Cache the compiled Pillar data before returning.

        .. warning::
            This option may be dangerous when targeting a device that already
            has a Proxy Minion associated, however recommended otherwise.

    cache_grains: ``False``
        Cache the collected Grains before returning.

        .. warning::
            This option may be dangerous when targeting a device that already
            has a Proxy Minion associated, however recommended otherwise.

    .. _`NAPALM Read the Docs page`: https://napalm.readthedocs.io/en/latest/#supported-network-operating-systems
    .. _`optional arguments`: http://napalm.readthedocs.io/en/latest/support/index.html#list-of-supported-optional-arguments

    CLI Example:

    .. code-block:: bash

        salt-run napalm.salt_call bgp.neighbors junos 1.2.3.4 test test123
        salt-run napalm.salt_call net.load_config junos 1.2.3.4 test test123 text='set system ntp peer 1.2.3.4'
    """
    if not minion_id:
        minion_id = hostname
    if not optional_args:
        optional_args = {}
    opts = copy.deepcopy(__opts__)
    opts[b'id'] = minion_id
    opts[b'pillarenv'] = __opts__.get(b'pillarenv', b'base')
    opts[b'__cli'] = __opts__.get(b'__cli', b'salt-call')
    if b'proxy' not in opts:
        opts[b'proxy'] = {}
    opts[b'proxy'].update({b'proxytype': b'napalm', 
       b'driver': driver, 
       b'hostname': hostname, 
       b'username': username, 
       b'passwd': password, 
       b'timeout': timeout, 
       b'optional_args': optional_args, 
       b'provider': provider})
    opts[b'napalm'] = opts[b'proxy']
    if b'saltenv' not in opts:
        opts[b'saltenv'] = b'base'
    if not default_grains:
        default_grains = {}
    if b'os' not in default_grains:
        default_grains[b'os'] = driver
    if use_cached_grains or use_cached_pillar:
        minion_cache = __salt__[b'cache.fetch']((b'minions/{}').format(minion_id), b'data')
    opts[b'grains'] = default_grains
    if not default_pillar:
        default_pillar = {}
    opts[b'pillar'] = default_pillar
    opts[b'proxy_load_pillar'] = with_pillar
    opts[b'proxy_load_grains'] = with_grains
    opts[b'proxy_preload_pillar'] = preload_pillar
    opts[b'proxy_preload_grains'] = preload_grains
    opts[b'proxy_cache_grains'] = cache_grains
    opts[b'proxy_cache_pillar'] = cache_pillar
    opts[b'proxy_use_cached_grains'] = use_cached_grains
    if use_cached_grains:
        opts[b'proxy_cached_grains'] = minion_cache.get(b'grains')
    opts[b'proxy_use_cached_pillar'] = use_cached_pillar
    if use_cached_pillar:
        opts[b'proxy_cached_pillar'] = minion_cache.get(b'pillar')
    napalm_px = NAPALMProxy(opts)
    kwargs = clean_kwargs(**kwargs)
    ret = None
    try:
        try:
            ret = napalm_px.functions[function](*args, **kwargs)
        except Exception as err:
            log.error(err, exc_info=True)

    finally:
        napalm_px.proxy[b'napalm.shutdown'](opts)

    if cache_grains:
        __salt__[b'cache.store']((b'minions/{}/data').format(minion_id), b'grains', napalm_px.opts[b'grains'])
    if cache_pillar:
        __salt__[b'cache.store']((b'minions/{}/data').format(minion_id), b'pillar', napalm_px.opts[b'pillar'])
    return ret


def load_template(driver, hostname, username, password, timeout=60, optional_args=None, provider=None, minion_id=None, with_grains=True, preload_grains=False, with_pillar=True, preload_pillar=False, default_grains=None, default_pillar=None, **kwargs):
    """
    Execute ``net.load_template`` with the optimal settings: as this function
    implies template rendering it is often best to load Grains and compile
    Pillar data.

    driver
        Specifies the network device operating system.
        For a complete list of the supported operating systems please refer to
        the `NAPALM Read the Docs page`_.

    hostname
        The IP Address or name server to use when connecting to the device.

    username
        The username to be used when connecting to the device.

    password
        The password needed to establish the connection.

        .. note::
            This field may not be mandatory when working with SSH-based drivers,
            and the username has a SSH key properly configured on the device
            targeted to be managed.

    optional_args
        Dictionary with the optional arguments.
        Check the complete list of supported `optional arguments`_.

    provider: ``napalm_base``
        The library that provides the ``get_network_device`` function.
        This option is useful when the user has more specific needs and requires
        to extend the NAPALM capabilities using a private library implementation.
        The only constraint is that the alternative library needs to have the
        ``get_network_device`` function available.

    preload_grains: ``False``
        Whether to preload the Grains before establishing the connection with
        the remote network device.

    default_grains:
        Dictionary of the default Grains to make available within the functions
        loaded.

    with_grains: ``True``
        Whether to load the Grains modules and collect Grains data and make it
        available inside the Execution Functions.
        The Grains will be loaded after opening the connection with the remote
        network device.

    preload_pillar: ``False``
        Whether to preload Pillar data before opening the connection with the
        remote network device.

    default_pillar:
        Dictionary of the default Pillar data to make it available within the
        functions loaded.

    with_pillar: ``True``
        Whether to load the Pillar modules and compile Pillar data and make it
        available inside the Execution Functions.

    minion_id:
        The ID of the Minion to compile Pillar data for.

    .. _`NAPALM Read the Docs page`: https://napalm.readthedocs.io/en/latest/#supported-network-operating-systems
    .. _`optional arguments`: http://napalm.readthedocs.io/en/latest/support/index.html#list-of-supported-optional-arguments

    CLI Example:

    .. code-block:: bash

        salt-run napalm.load_template junos 1.2.3.4 test test123 template_name=salt://path/to/template.jinja
    """
    return salt_call(b'net.load_template', driver, hostname, username, password, timeout=timeout, optional_args=optional_args, provider=provider, minion_id=minion_id, preload_pillar=preload_pillar, preload_grains=preload_grains, with_pillar=with_pillar, with_grains=with_grains, default_grains=default_grains, default_pillar=default_pillar, **kwargs)


def load_config(driver, hostname, username, password, timeout=60, optional_args=None, provider=None, **kwargs):
    """
    Execute ``net.load_config`` to load a static configuration on the network
    device.

    driver
        Specifies the network device operating system.
        For a complete list of the supported operating systems please refer to the
        `NAPALM Read the Docs page`_.

    hostname
        The IP Address or name server to use when connecting to the device.

    username
        The username to be used when connecting to the device.

    password
        The password needed to establish the connection.

        .. note::
            This field may not be mandatory when working with SSH-based drivers, and
            the username has a SSH key properly configured on the device targeted to
            be managed.

    optional_args
        Dictionary with the optional arguments.
        Check the complete list of supported `optional arguments`_.

    provider: ``napalm_base``
        The library that provides the ``get_network_device`` function.
        This option is useful when the user has more specific needs and requires
        to extend the NAPALM capabilities using a private library implementation.
        The only constraint is that the alternative library needs to have the
        ``get_network_device`` function available.

    .. _`NAPALM Read the Docs page`: https://napalm.readthedocs.io/en/latest/#supported-network-operating-systems
    .. _`optional arguments`: http://napalm.readthedocs.io/en/latest/support/index.html#list-of-supported-optional-arguments

    CLI Example:

    .. code-block:: bash

        salt-run napalm.load_config eos 1.2.3.4 test test123 text='ntp server 10.10.10.1'
    """
    return salt_call(b'net.load_config', driver, hostname, username, password, timeout=timeout, optional_args=optional_args, provider=provider, **kwargs)


def execute_devices(devices, fun, driver=None, username=None, password=None, timeout=60, optional_args=None, provider=None, with_grains=False, preload_grains=False, with_pillar=False, preload_pillar=False, default_grains=None, default_pillar=None, args=(), batch_size=10, sync=False, tgt=None, tgt_type=None, jid=None, events=True, cache_grains=False, cache_pillar=False, use_cached_grains=True, use_cached_pillar=True, **kwargs):
    """
    Execute a Salt function on a group of network devices listed in the
    ``devices`` argument.

    devices
        A list or a dictionary of devices to run against. This argument can be
        one of the following:

        - A list of hostnames.
        - A list of dictionaries with the connection details for each device.
          At minimum, each dictionary should have at least the ``hostname`` key.
          The rest of the authentication credentials, when not present, are
          inherited from ``driver``, ``username``, ``password``, etc.
        - A dictionary of dictionaries where each key is the minion ID / or
          hostname of each device, and the value is a dictionary with the
          authentication credentials. Similarly, when not present, the rest of
          the credentials are inherited from ``driver``, ``username``,
          ``password`` etc.

    fun
        The name of the Salt function to invoke.

    driver
        Specifies the network device operating system.
        For a complete list of the supported operating systems please refer to
        the `NAPALM Read the Docs page`_.

        This argument is optional and considered only for devices that don't
        have this field set.

    hostname
        The IP Address or name server to use when connecting to the device.

        This argument is optional and considered only for devices that don't
        have this field set.

    username
        The username to be used when connecting to the device.

        This argument is optional and considered only for devices that don't
        have this field set.

    password
        The password needed to establish the connection.

        This argument is optional and considered only for devices that don't
        have this field set.

        .. note::
            This field may not be mandatory when working with SSH-based drivers,
            and the username has a SSH key properly configured on the device
            targeted to be managed.

    optional_args
        Dictionary with the optional arguments.
        Check the complete list of supported `optional arguments`_.

        This argument is optional and considered only for devices that don't
        have this field set.

    provider: ``napalm_base``
        The library that provides the ``get_network_device`` function.
        This option is useful when the user has more specific needs and requires
        to extend the NAPALM capabilities using a private library implementation.
        The only constraint is that the alternative library needs to have the
        ``get_network_device`` function available.

        This argument is optional and considered only for devices that don't
        have this field set.

    preload_grains: ``False``
        Whether to preload the Grains before establishing the connection with
        the remote network device.

    default_grains:
        Dictionary of the default Grains to make available within the functions
        loaded.

    with_grains: ``False``
        Whether to load the Grains modules and collect Grains data and make it
        available inside the Execution Functions.
        The Grains will be loaded after opening the connection with the remote
        network device.

    preload_pillar: ``False``
        Whether to preload Pillar data before opening the connection with the
        remote network device.

    default_pillar:
        Dictionary of the default Pillar data to make it available within the
        functions loaded.

    with_pillar: ``False``
        Whether to load the Pillar modules and compile Pillar data and make it
        available inside the Execution Functions.

    args
        The list of arguments to send to the Salt function.

    kwargs
        Key-value arguments to send to the Salt function.

    batch_size: ``10``
        The size of each batch to execute.

    sync: ``False``
        Whether to return the results synchronously (or return them as soon
        as the device replies).

    events: ``True``
        Whether should push events on the Salt bus, similar to when executing
        equivalent through the ``salt`` command.

    use_cached_pillar: ``True``
        Use cached Pillars whenever possible. If unable to gather cached data,
        it falls back to compiling the Pillar.

    use_cached_grains: ``True``
        Use cached Grains whenever possible. If unable to gather cached data,
        it falls back to collecting Grains.

    cache_pillar: ``False``
        Cache the compiled Pillar data before returning.

        .. warning::
            This option may be dangerous when targeting a device that already
            has a Proxy Minion associated, however recommended otherwise.

    cache_grains: ``False``
        Cache the collected Grains before returning.

        .. warning::
            This option may be dangerous when targeting a device that already
            has a Proxy Minion associated, however recommended otherwise.

    CLI Example:

    .. code-block:: bash

        salt-run napalm.execute "['172.17.17.1', '172.17.17.2']" test.ping driver=eos username=test password=test123
    """
    __pub_user = kwargs.get(b'__pub_user')
    kwargs = clean_kwargs(**kwargs)
    if not jid:
        jid = salt.utils.jid.gen_jid()
    event_args = list(args[:])
    if kwargs:
        event_kwargs = {b'__kwarg__': True}
        event_kwargs.update(kwargs)
        event_args.append(event_kwargs)
    opts = {b'driver': driver, b'username': username, 
       b'password': password, 
       b'timeout': timeout, 
       b'optional_args': optional_args, 
       b'provider': provider, 
       b'with_grains': with_grains, 
       b'with_pillar': with_pillar, 
       b'preload_grains': preload_grains, 
       b'preload_pillar': preload_pillar, 
       b'default_grains': default_grains, 
       b'default_pillar': default_pillar, 
       b'args': args, 
       b'cache_grains': cache_grains, 
       b'cache_pillar': cache_pillar, 
       b'use_cached_grains': use_cached_grains, 
       b'use_cached_pillar': use_cached_pillar}
    opts.update(kwargs)
    devices_list = []
    minions_list = []
    if isinstance(devices, list):
        for device in devices:
            if isinstance(device, dict):
                devices_list.append(device)
                minions_list.append(device[b'minion_id'])
            elif isinstance(device, six.string_types):
                devices_list.append({b'hostname': device})
                minions_list.append(device)

    else:
        if isinstance(devices, dict):
            for minion_id, device_opts in six.iteritems(devices):
                device_opts[b'minion_id'] = minion_id
                devices_list.append(device_opts)
                minions_list.append(minion_id)

        elif isinstance(devices, six.string_types):
            devices_list.append({b'hostname': devices})
            minions_list.append(devices)
        if events:
            __salt__[b'event.send']((b'napalm/runner/{jid}/new').format(jid=jid), {b'fun': fun, 
               b'minions': minions_list, 
               b'arg': event_args, 
               b'jid': jid, 
               b'tgt': tgt, 
               b'tgt_type': tgt_type, 
               b'user': __pub_user})
        queue = multiprocessing.Queue()
        if not sync:
            thread = threading.Thread(target=_receive_replies_async, args=(queue,))
            thread.start()
        ret = {}
        batch_count = len(devices_list) / batch_size + 1
        for batch_index in range(batch_count):
            processes = []
            devices_batch = devices_list[batch_index * batch_size:(batch_index + 1) * batch_size]
            for device in devices_batch:
                minion_id = device.pop(b'minion_id', device[b'hostname'])
                for opt, val in six.iteritems(opts):
                    if opt not in device:
                        device[opt] = val

                device_proc = multiprocessing.Process(target=_salt_call_and_return, name=minion_id, args=(
                 minion_id, fun, queue, event_args, jid, events), kwargs=device)
                device_proc.start()
                processes.append(device_proc)

            for proc in processes:
                proc.join()

    queue.put(b'FIN.')
    if sync:
        resp = {}
        while True:
            ret = queue.get()
            if ret == b'FIN.':
                break
            resp.update(ret)

        return resp
    return {}


def execute(tgt, fun, tgt_type=b'glob', roster=None, preview_target=False, target_details=False, driver=None, hostname=None, username=None, password=None, timeout=60, optional_args=None, provider=None, with_grains=False, preload_grains=False, with_pillar=False, preload_pillar=False, default_grains=None, default_pillar=None, args=(), batch_size=10, sync=False, events=True, cache_grains=False, cache_pillar=False, use_cached_grains=True, use_cached_pillar=True, **kwargs):
    """
    Invoke a Salt function on the list of devices matched by the Roster
    subsystem.

    tgt
        The target expression, e.g., ``*`` for all devices, or ``host1,host2``
        for a list, etc. The ``tgt_list`` argument must be used accordingly,
        depending on the type of this expression.

    fun
        The name of the Salt function to invoke.

    tgt_type: ``glob``
        The type of the ``tgt`` expression. Choose between: ``glob`` (default),
        ``list``, ``pcre``, ``rage``, or ``nodegroup``.

    roster
        The name of the Roster to generate the targets. Alternatively, you can
        specify the name of the Roster by configuring the ``napalm_roster``
        option into the Master config.

    preview_target: ``False``
        Return the list of Roster targets matched by the ``tgt`` and
        ``tgt_type`` arguments.

    target_details: ``False``
        When returning the list of targets provide also their details. This
        option is ignored when ``preview_target=False``.

    driver
        Specifies the network device operating system.
        For a complete list of the supported operating systems please refer to
        the `NAPALM Read the Docs page`_.

        This argument is optional and considered only for devices that don't
        have this field set.

    hostname
        The IP Address or name server to use when connecting to the device.

        This argument is optional and considered only for devices that don't
        have this field set.

    username
        The username to be used when connecting to the device.

        This argument is optional and considered only for devices that don't
        have this field set.

    password
        The password needed to establish the connection.

        This argument is optional and considered only for devices that don't
        have this field set.

        .. note::
            This field may not be mandatory when working with SSH-based drivers,
            and the username has a SSH key properly configured on the device
            targeted to be managed.

    optional_args
        Dictionary with the optional arguments.
        Check the complete list of supported `optional arguments`_.

        This argument is optional and considered only for devices that don't
        have this field set.

    provider: ``napalm_base``
        The library that provides the ``get_network_device`` function.
        This option is useful when the user has more specific needs and requires
        to extend the NAPALM capabilities using a private library implementation.
        The only constraint is that the alternative library needs to have the
        ``get_network_device`` function available.

        This argument is optional and considered only for devices that don't
        have this field set.

    preload_grains: ``False``
        Whether to preload the Grains before establishing the connection with
        the remote network device.

    default_grains:
        Dictionary of the default Grains to make available within the functions
        loaded.

    with_grains: ``False``
        Whether to load the Grains modules and collect Grains data and make it
        available inside the Execution Functions.
        The Grains will be loaded after opening the connection with the remote
        network device.

    preload_pillar: ``False``
        Whether to preload Pillar data before opening the connection with the
        remote network device.

    default_pillar:
        Dictionary of the default Pillar data to make it available within the
        functions loaded.

    with_pillar: ``False``
        Whether to load the Pillar modules and compile Pillar data and make it
        available inside the Execution Functions.

    arg
        The list of arguments to send to the Salt function.

    kwargs
        Key-value arguments to send to the Salt function.

    batch_size: ``10``
        The size of each batch to execute.

    sync: ``False``
        Whether to return the results synchronously (or return them as soon
        as the device replies).

    events: ``True``
        Whether should push events on the Salt bus, similar to when executing
        equivalent through the ``salt`` command.

    use_cached_pillar: ``True``
        Use cached Pillars whenever possible. If unable to gather cached data,
        it falls back to compiling the Pillar.

    use_cached_grains: ``True``
        Use cached Grains whenever possible. If unable to gather cached data,
        it falls back to collecting Grains.

    cache_pillar: ``False``
        Cache the compiled Pillar data before returning.

        .. warning::
            This option may be dangerous when targeting a device that already
            has a Proxy Minion associated, however recommended otherwise.

    cache_grains: ``False``
        Cache the collected Grains before returning.

        .. warning::
            This option may be dangerous when targeting a device that already
            has a Proxy Minion associated, however recommended otherwise.

    CLI Example:

    .. code-block:: bash

        salt-run napalm.execute_roster edge* test.ping
        salt-run napalm.execute_roster junos-edges test.ping tgt_type=nodegroup
    """
    exec_targets = []
    roster = roster or __opts__.get(b'napalm_roster', __opts__.get(b'roster'))
    if not roster:
        log.info(b'No Roster specified. Please use the ``roster`` argument, or set the ``napalm_roster`` option in the Master configuration.')
        targets = []
        if tgt_type == b'list':
            targets = tgt[:]
        else:
            if tgt_type == b'glob' and tgt != b'*':
                targets = [
                 tgt]
            for target in targets:
                exec_targets.append({b'minion_id': target, 
                   b'driver': driver, 
                   b'hostname': hostname, 
                   b'username': username, 
                   b'password': password, 
                   b'timeout': timeout, 
                   b'optional_args': optional_args, 
                   b'provider': provider})

    else:
        roster_modules = salt.loader.roster(__opts__, runner=__salt__)
        if b'.targets' not in roster:
            roster = (b'{mod}.targets').format(mod=roster)
        targets = roster_modules[roster](tgt, tgt_type=tgt_type)
        for minion_id, minion_details in six.iteritems(targets):
            target_opts = minion_details[b'minion_opts']
            target_opts[b'minion_id'] = minion_id
            exec_targets.append(target_opts)

        targets = list(targets.keys())
    if not exec_targets:
        return b'No devices matched your target. Please review your tgt / tgt_type arguments, or the Roster data source'
    if preview_target:
        if target_details:
            return exec_targets
        else:
            return targets

    jid = kwargs.get(b'__pub_jid')
    if not jid:
        jid = salt.utils.jid.gen_jid()
    if events:
        __salt__[b'event.send'](jid, {b'minions': list(targets.keys())})
    return execute_devices(exec_targets, fun, driver=driver, username=username, password=password, timeout=timeout, optional_args=optional_args, provider=provider, with_grains=with_grains, preload_grains=preload_grains, with_pillar=with_pillar, preload_pillar=preload_pillar, default_grains=default_grains, default_pillar=default_pillar, args=args, batch_size=batch_size, sync=sync, events=events, cache_grains=cache_grains, cache_pillar=cache_pillar, use_cached_grains=use_cached_grains, use_cached_pillar=use_cached_pillar, **kwargs)