# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ua_mapper/wsgi.py
# Compiled at: 2011-08-30 06:51:11
import hashlib, memcache
from pywurfl.algorithms import TwoStepAnalysis
from ua_mapper import wurfl

class UAMapper(object):
    default = 'medium'
    default_user_agent = ''

    def map(self, device):
        """
        Override this method to perform your own custom mapping.
        """
        if device.resolution_width < 240:
            return 'medium'
        else:
            return 'high'

    def __call__(self, environ, start_response):
        mc = memcache.Client([environ['MEMCACHED_SOCKET']], debug=0)
        if 'HTTP_USER_AGENT' in environ:
            user_agent = unicode(environ['HTTP_USER_AGENT'])
        else:
            user_agent = unicode(self.default_user_agent)
        key = self.get_cache_key(user_agent)
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        output = mc.get(key)
        if not output:
            output = self.gen_output(user_agent, start_response)
            mc.set(key, output)
        return [output]

    def gen_output(self, user_agent, start_response):
        output = self.default
        devices = wurfl.devices
        search_algorithm = TwoStepAnalysis(devices)
        device = devices.select_ua(user_agent, search=search_algorithm)
        return self.map(device)

    def get_cache_key(self, user_agent):
        return hashlib.md5(user_agent).hexdigest()


application = UAMapper()