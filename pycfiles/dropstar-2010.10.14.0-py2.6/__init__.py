# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dropstar/__init__.py
# Compiled at: 2010-10-14 14:04:21
"""
dropSTAR: Drop Scripts, Templates and RPC

Wraps HTTP handler to pass in state.  Simple and light.
"""
import logging
from unidist.log import log
from procblock import procyaml
import httpd
DEFAULT_LISTEN_PORT = 8080

class DropStar:

    def __init__(self, sites):
        """Returns a dropSTAR server object, which wraps everything you need.
    
    HTTP and XMLRPC servers run in their own threads on starting.  Many sites
    may be run off one set of thread listeners on a single port, or many thread
    listeners can be specified on their respective ports.
    
    This allows many dropSTAR installations on a single machine, and the ability
    to add totally new sites to an existing dropSTAR installation without
    running a second dropSTAR process or interfering with any of the existing
    dropSTAR sites.
    
    
    Args:
      sites: dict, keyed on site main host-header for listening.  Contains
          a dictionary with site information such as the key "port", which
          specifies the port to listen on, and key "packages", which contains
          a list of packages and their mount points.
    """
        self.sites = sites
        log('DropStar: __init__: %s' % sites)
        self.conf = {}
        self.ports = {}
        self.listeners = {}
        self.Load()
        self._Start()

    def Load(self):
        """Load the YAML configuration file.  Sets self.conf"""
        for site_conf_filename in self.sites:
            conf = procyaml.ImportYaml(site_conf_filename)
            self.conf[site_conf_filename] = conf
            for (site_name, site_conf) in conf.items():
                if 'port' in site_conf:
                    port = site_conf['port']
                else:
                    port = DEFAULT_LISTEN_PORT
                    log('Site configuration does not specify port: %s.%s:  Using default: %s' % (site_conf_filename, site_name, port), logging.INFO)
                if port not in self.ports:
                    self.ports[port] = []
                port_sites = (site_name, site_conf)
                self.ports[port].append(port_sites)
                log('Loaded port: %s: %s' % (site_name, site_conf_filename))

    def _Start(self):
        """Start all the listening pools."""
        for (port, port_sites) in self.ports.items():
            log('Creating Listener: %s (%s site(s))' % (port, len(port_sites)), logging.INFO)
            self.listeners[port] = httpd.HttpdThread(port, port_sites, self.conf)
            self.listeners[port].start()