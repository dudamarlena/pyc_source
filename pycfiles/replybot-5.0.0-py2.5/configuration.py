# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/botlib/configuration.py
# Compiled at: 2008-08-09 12:39:34
"""Configuration file parsing."""
__metaclass__ = type
__all__ = [
 'Configuration',
 'config']
import os, errno, logging, datetime, ConfigParser
_multiplier = {'m': 'minutes', 
   'h': 'hours', 
   'd': 'days', 
   'w': 'weeks'}
COMMA = ','

class Configuration:
    """Global configuration class."""

    def load(self, filename, selector='DEFAULT'):
        """Load the configuration file, using the specified selector.

        :param filename: The configuration file name
        :type filename: string
        :param selector: The section selector name
        :type selector: string
        """
        self._cfg = ConfigParser.SafeConfigParser()
        self._cfg.read(filename)
        self.database_url = self._cfg.get('SYSTEM', 'database_url')
        self.log_file = self._cfg.get('SYSTEM', 'log_file')
        log_level = self._cfg.get('SYSTEM', 'log_level')
        self.mail_server = self._cfg.get('SYSTEM', 'mail_server')
        mail_port = self._cfg.get('SYSTEM', 'mail_port')
        self.mail_user = self._cfg.get('SYSTEM', 'mail_user')
        self.mail_password = self._cfg.get('SYSTEM', 'mail_password')
        self.replybot_from = self._cfg.get(selector, 'replybot_from')
        self.replybot_mailfrom = self._cfg.get(selector, 'replybot_mailfrom')
        self.replybot_who = self._cfg.get(selector, 'replybot_who')
        grace_period = self._cfg.get(selector, 'grace_period')
        cache_period = self._cfg.get(selector, 'cache_period')
        self.cache_directory = self._cfg.get(selector, 'cache_directory')
        self.reply_url = self._cfg.get(selector, 'reply_url')
        self.content_type = self._cfg.get(selector, 'content_type')
        self.reply_context = self._cfg.get(selector, 'reply_context')
        self.mail_port = int(mail_port)
        self.log_level = getattr(logging, log_level.upper())
        if self.mail_user.capitalize() == 'None':
            self.mail_user = None
        if self.mail_password.capitalize() == 'None':
            self.mail_password = None
        if grace_period[(-1)] in 'mhdw':
            key = _multiplier[grace_period[(-1)]]
            val = int(grace_period[:-1])
        else:
            key = 'days'
            val = int(grace_period)
        self.grace_period = datetime.timedelta(**{key: val})
        if cache_period[(-1)] in 'mhdw':
            key = _multiplier[cache_period[(-1)]]
            val = int(cache_period[:-1])
        else:
            key = 'days'
            val = int(cache_period)
        self.cache_period = datetime.timedelta(**{key: val})
        try:
            os.makedirs(self.cache_directory)
        except OSError, error:
            if error.errno != errno.EEXIST:
                raise

        return


config = Configuration()