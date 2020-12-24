# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/services/config.py
# Compiled at: 2011-04-22 06:35:42
""" configuration service """
import sys, os, logging, glob
from twisted.application import internet, service
from twisted.internet.defer import Deferred
import yaml
from copy import deepcopy

class configService(service.Service):
    name = 'config'

    def __init__(self, filename=None, is_subconfig=False):
        """Initialize the config class and load a config"""
        self.logger = logging.getLogger('config')
        self.generic_options = {}
        self.network_options = {}
        self.filename = filename
        self.name = 'config'
        self.generic_options_default = {}
        if not filename:
            return
        try:
            configs = yaml.load_all(open(filename, 'r'))
            self.generic_options = configs.next()
            if not is_subconfig:
                self.network_options = configs.next()
                if not self.network_options:
                    self.network_options = {}
            for option in self.generic_options.keys():
                self.generic_options_default[option] = False

        except IOError:
            pass

    def _create_preceding(self, network, channel=None):
        """
        create preceding dictionary entries for network/channel options

        >>> c=configService()
        >>> c.network_options
        {}
        >>> c._create_preceding("samplenetwork", "#samplechannel")
        >>> c.network_options
        {'samplenetwork': {'#samplechannel': {}}}
        >>> c._create_preceding("othernetwork")
        >>> c.network_options
        {'othernetwork': {}, 'samplenetwork': {'#samplechannel': {}}}
        """
        if network:
            if network not in self.network_options:
                self.network_options[network] = {}
            if channel:
                if channel not in self.network_options[network]:
                    self.network_options[network][channel] = {}

    def get(self, option, default, module=None, network=None, channel=None, set_default=True):
        """
        get an option and set the default value, if the option is unset.

        >>> c=configService()
        >>> c.get("option", "default")
        'default'
        >>> c.get("option", "unset?")
        'default'

        @param set_default: if True, the default will be set in the
                            config, if its used. If False, the default
                            will be returned, but the config will not
                            be changed.
        """
        if module:
            option = module + '.' + option
        if channel and channel[0] not in '#+!&':
            channel = None
        if network in self.network_options:
            if channel in self.network_options[network]:
                if option in self.network_options[network][channel]:
                    return deepcopy(self.network_options[network][channel][option])
            if option in self.network_options[network]:
                return deepcopy(self.network_options[network][option])
        if option in self.generic_options:
            return deepcopy(self.generic_options[option])
        else:
            if network:
                if channel:
                    self._create_preceding(network, channel)
                    self.network_options[network][channel][option] = default
                else:
                    self._create_preceding(network)
                    self.network_options[network][option] = default
            elif option == 'config.writeDefaultValues' or self.has('config.writeDefaultValues') and self.getBool('config.writeDefaultValues', False) and set_default:
                self.set(option, default, still_default=False)
            else:
                self.set(option, default, still_default=True)
            return default

    def has(self, option, module=None):
        """
        Test, in which networks/channels a option is set.
        Returns a tuple: (general_bool, network_list, (network, channel) list)

        >>> c=configService()
        >>> c.has("testkey")
        (False, [], [])
        >>> c.set("testkey", "testvalue")
        >>> c.has("testkey")
        (True, [], [])
        >>> c.set("testkey", "othervalue", network="samplenetwork")
        >>> c.has("testkey")
        (True, ['samplenetwork'], [])
        """
        general = False
        networks = []
        channels = []
        if module:
            option = module + '.' + option
        for item in self.generic_options.keys():
            if item == option:
                general = True

        for network in self.network_options.keys():
            if option in self.network_options[network].keys():
                networks.append(network)

        for network in self.network_options.keys():
            for channel in self.network_options[network].keys():
                if type(self.network_options[network][channel]) == dict:
                    if option in self.network_options[network][channel].keys():
                        channels.append((network, channel))

        return (
         general, networks, channels)

    def set(self, option, value, module=None, network=None, channel=None, still_default=False):
        if module:
            option = module + '.' + option
        if channel and channel[0] not in '#+!&':
            channel = None
        if network:
            if channel:
                self._create_preceding(network, channel)
                self.network_options[network][channel][option] = value
            else:
                self._create_preceding(network)
                self.network_options[network][option] = value
        else:
            self.generic_options[option] = value
            self.generic_options_default[option] = still_default
        self.writeConfig()
        return

    def delete(self, option, module=None, network=None, channel=None):
        """
        >>> c=configService()
        >>> c.set("key", "value")
        >>> c.get("key", "unset")
        'value'
        >>> c.delete("key")
        >>> c.get("key", "unset")
        'unset'
        """
        if module:
            option = module + '.' + option
        if network:
            if channel:
                try:
                    del self.network_options[network][channel][option]
                except IndexError:
                    pass

            else:
                try:
                    del self.network_options[network][option]
                except IndexError:
                    pass

        else:
            try:
                del self.generic_options[option]
            except IndexError:
                pass

    def getNetworks(self):
        ret = []
        for network in self.network_options.keys():
            ret.append(network)

        return ret

    def getChannels(self, network):
        if network in self.network_options.keys():
            try:
                options = self.network_options[network].keys()
                ret = []
                for option in options:
                    if type(self.network_options[network][option]) == dict:
                        ret.append(option)

                return ret
            except AttributeError:
                return []

    def setConfig(self, opt, value, module=None, network=None, channel=None):
        self.logger.debug('deprecated call to setConfig for opt %s' % opt)
        self.set(opt, value, module, network, channel)

    def delConfig(self, opt, module=None, network=None, channel=None):
        self.logger.debug('deprecated call to delConfig for opt %s' % opt)
        delete(opt, module, network, channel)

    def hasConfig(self, option, module=None):
        self.logger.debug('deprecated call to hasConfig for opt %s' % option)
        return self.has(option, module)

    def getConfig(self, option, defaultvalue='', module=None, network=None, channel=None, set_default=True):
        self.logger.debug('deprecated call to getConfig for opt %s' % option)
        return self.get(option, defaultvalue, module, network, channel, set_default)

    def getPath(self, option, datadir, defaultvalue='', module=None, network=None, channel=None):
        value = self.get(option, defaultvalue, module, network, channel)
        if value[0] == '/':
            return value
        else:
            return datadir + '/' + value

    def getBool(self, option, defaultvalue='', module=None, network=None, channel=None):
        """
        >>> c=configService()
        >>> c.set("key", "1")
        >>> c.set("key2", "on")
        >>> c.set("key3", "True")
        >>> c.getBool("key") and c.getBool("key2") and c.getBool("key3")
        True
        >>> c.set("key", "False")
        >>> c.set("key2", "any string which is not in [True, true, on, On, 1]")
        >>> c.getBool("key") or c.getBool("key2")
        False
        """
        return self.get(option, defaultvalue, module, network, channel) in ['True', 'true', 'On', 'on', '1', True, 1]

    def writeConfig(self):
        if not self.filename:
            return False
        file = open(self.filename, 'w')
        generic_options = deepcopy(self.generic_options)
        if not self.getBool('writeDefaultValues', False, 'config'):
            for option in self.generic_options_default.keys():
                if option in generic_options and self.generic_options_default[option]:
                    del generic_options[option]

        file.write(yaml.dump_all([generic_options, self.network_options], default_flow_style=False))
        file.close()
        return True

    def startService(self):
        service.Service.startService(self)

    def stopService(self):
        self.writeConfig()
        service.Service.stopService(self)


def loadConfig(myconfigfile, modulesconfigdirglob):
    if os.path.exists(myconfigfile):
        myconfig = configService(myconfigfile)
        for file in glob.glob(modulesconfigdirglob):
            tmp = configService(file, is_subconfig=True)
            for option in tmp.generic_options.keys():
                if not myconfig.has(option)[0]:
                    myconfig.set(option, tmp.get(option, ''), still_default=True)

            del tmp

        return myconfig
    else:
        return
        return


if __name__ == '__main__':
    import doctest, unittest
    doctest.testmod()

    class configTest(unittest.TestCase):

        def setUp(self):
            os.mkdir('test_configsnippets')
            os.mkdir('test_configsnippets2')
            file = open('test_configsnippets/foomod.yaml', 'w')
            file.write("fooMod.setting1: 'blub'\nfooMod.setting2: true\nfooMod.setting3: false")
            file.close()
            c = configService('testconfig.yaml')
            c.writeConfig()
            self.config = loadConfig('testconfig.yaml', 'test_configsnippets/*.yaml')

        def tearDown(self):
            os.remove('test_configsnippets/foomod.yaml')
            os.rmdir('test_configsnippets')
            os.rmdir('test_configsnippets2')
            os.remove('testconfig.yaml')

        def testDefaults(self):
            blub = self.config.get('setting1', 'unset', 'fooMod')
            self.assertTrue(blub == 'blub', "fooMod.setting1 is '%s' instead of 'blub'" % blub)
            blub2 = self.config.get('setting4', 'new_setting', 'fooMod')
            self.assertTrue(blub2 == 'new_setting', "blub2 is '%s' instead of 'new_setting'" % blub2)
            self.config.writeConfig()
            config2 = loadConfig('testconfig.yaml', 'test_configsnippets2/*.yaml')
            self.assertTrue(config2.hasConfig('setting1', 'fooMod')[0] == False)
            self.assertTrue(config2.hasConfig('setting4', 'fooMod')[0] == False)

        def testWriteDefaults(self):
            self.config.set('writeDefaultValues', True, 'config')
            blub = self.config.get('setting1', 'unset', 'fooMod')
            self.assertTrue(blub == 'blub', "fooMod.setting1 is '%s' instead of 'blub'" % blub)
            blub2 = self.config.get('setting4', 'new_setting', 'fooMod')
            self.assertTrue(blub2 == 'new_setting', "blub2 is '%s' instead of 'new_setting'" % blub2)
            self.config.writeConfig()
            config2 = loadConfig('testconfig.yaml', 'test_configsnippets2/*.yaml')
            self.assertTrue(config2.hasConfig('setting1', 'fooMod')[0] == True)
            self.assertTrue(config2.hasConfig('setting4', 'fooMod')[0] == True)


    unittest.main()