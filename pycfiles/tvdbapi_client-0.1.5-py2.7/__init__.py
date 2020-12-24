# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.6.0-i686/egg/tvdbapi_client/__init__.py
# Compiled at: 2015-11-08 19:16:28
"""Provide a simple entry point to configure an API client."""
import logging, pbr.version
logging.getLogger(__package__).addHandler(logging.NullHandler())
__version__ = pbr.version.VersionInfo(__package__).version_string()

def get_client(config_file=None, apikey=None, username=None, userpass=None, service_url=None, verify_ssl_certs=None, select_first=None):
    """Configure the API service and creates a new instance of client.

    :param str config_file: absolute path to configuration file
    :param str apikey: apikey from thetvdb
    :param str username: username used on thetvdb
    :param str userpass: password used on thetvdb
    :param str service_url: the url for thetvdb api service
    :param str verify_ssl_certs: flag for validating ssl certs for
                                 service url (https)
    :param str select_first: flag for selecting first series from
                             search results
    :returns: tvdbapi client
    :rtype: tvdbapi_client.api.TVDBClient
    """
    from oslo_config import cfg
    from tvdbapi_client import api
    if config_file is not None:
        cfg.CONF([], default_config_files=[config_file])
    else:
        if apikey is not None:
            cfg.CONF.set_override('apikey', apikey, 'tvdb')
        if username is not None:
            cfg.CONF.set_override('username', username, 'tvdb')
        if userpass is not None:
            cfg.CONF.set_override('userpass', userpass, 'tvdb')
        if service_url is not None:
            cfg.CONF.set_override('service_url', service_url, 'tvdb')
        if verify_ssl_certs is not None:
            cfg.CONF.set_override('verify_ssl_certs', verify_ssl_certs, 'tvdb')
        if select_first is not None:
            cfg.CONF.set_override('select_first', select_first, 'tvdb')
    return api.TVDBClient()


__all__ = [
 '__version__', 'get_client']