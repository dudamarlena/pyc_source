# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/archipelagenthypervisorgeolocalization/__init__.py
# Compiled at: 2013-03-20 13:50:16
import geoloc

def make_archipel_plugin(configuration, entity, group):
    """
    This function is the plugin factory. It will be called by the object you want
    to be plugged in. It must return a list whit at least on dictionary containing
    a key for the the plugin informations, and a key for the plugin object.
    @type configuration: Config Object
    @param configuration: the general configuration object
    @type entity: L{TNArchipelEntity}
    @param entity: the entity that has load the plugin
    @type group: string
    @param group: the entry point group name in which the plugin has been loaded
    @rtype: array
    @return: array of dictionary containing the plugins informations and objects
    """
    return [
     {'info': geoloc.TNHypervisorGeolocalization.plugin_info(), 'plugin': geoloc.TNHypervisorGeolocalization(configuration, entity, group)}]


def version():
    """
    This function can be called runarchipel -v in order to get the version of the
    installed plugin. You only should have to change the egg name.
    @rtype: tupple
    @return: tupple containing the package name and the version
    """
    import pkg_resources
    return (
     __name__, pkg_resources.get_distribution('archipel-agent-hypervisor-geolocalization').version, [geoloc.TNHypervisorGeolocalization.plugin_info()])