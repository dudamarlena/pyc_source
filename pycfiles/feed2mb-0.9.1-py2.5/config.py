# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/feed2mb/config.py
# Compiled at: 2010-10-19 17:02:44
from ConfigParser import ConfigParser, NoOptionError
from parsetime import parsetime
import sys

class MicroblogConfig(ConfigParser):

    def __init__(self, filename):
        self._configs = []
        ConfigParser.__init__(self)
        x = self.read(filename)
        if len(x) == 0:
            raise Exception('erro')

    def configs(self):
        sections = self.sections()
        sections.remove('global')
        for section in sections:
            config = {}
            config['url'] = self.get(section, 'url').strip()
            config['section'] = section
            config['service'] = self.get(section, 'service').strip()
            config['oauth_token'] = self.get(section, 'oauth_token').strip()
            config['oauth_secret'] = self.get(section, 'oauth_secret').strip()
            if config['service'] != 'twitter':
                config['username'] = self.get(section, 'username').strip()
                config['password'] = self.get(section, 'password').strip()
            config['mode'] = self.get(section, 'mode').strip()
            try:
                config['items'] = self.getint(section, 'items')
            except NoOptionError:
                config['items'] = 5

            try:
                config['pidfile'] = self.get('global', 'pidfile').strip()
            except NoOptionError:
                config['pidfile'] = None

            try:
                config['interval'] = parsetime(self.get('global', 'interval').strip())
            except:
                print 'Error in the interval setting'
                sys.exit(1)

            try:
                config['consumer_key'] = self.get(section, 'consumer_key').strip()
            except:
                print 'Error in the consumer_key setting'
                sys.exit(1)

            try:
                config['consumer_secret'] = self.get(section, 'consumer_secret').strip()
            except:
                print 'Error in the consumer_secret setting'
                sys.exit(1)

            try:
                config['shortener'] = self.get(section, 'shortener').strip()
            except NoOptionError:
                config['shortener'] = 'tinyurl'

            if config['service'] == 'wordpress':
                config['xmlrpc_url'] = self.get(section, 'xmlrpc_url').strip()
            self._configs.append(config)

        return self._configs