# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/graphit/client.py
# Compiled at: 2010-03-28 16:45:12
"""
        Client library for GraphIT.
        Contains also mini-framework for helpers.
"""
import sys
from optparse import OptionParser
from urlparse import urlparse
from socket import gethostname
from restkit import RestClient, httpc

class GraphItAgent:
    """ 
                This class allow to connect on GraphIT server and submit
                some monitoring data.
                
                Exemple:
                
                >>> agent = GraphItAgent('http://graphit.lan/')
                >>> agent.add_value('load', '1m', 0.42)
                >>> agent.add_value('load', '5m', 0.2)
         """

    def __init__(self, base_url, login=None, passwd=None):
        self.base_url = base_url
        transport = httpc.HttpClient()
        if login and passwd:
            transport.add_authorization(httpc.BasicAuth((login, passwd)))
        self._client = RestClient(transport=transport)

    def add_value(self, set, feed, value, unit=''):
        """ Add a value in set for feed. """
        self._client.post(self.base_url, path='%s/%s' % (set.replace('/', '%2F'), feed.replace('/', '%2F')), body={'value': value, 'unit': unit}, headers={'Content-type': 'application/x-www-form-urlencoded; charset=utf-8'})


class GraphITWatcher(GraphItAgent):
    """ GraphIT Watcher is program used to watch a specific ressource
        and submit it values to the GraphIT daemon. """
    __name__ = None
    __version__ = None
    __wid__ = None
    __author__ = None

    def __init__(self):
        op = OptionParser(usage='usage: %prog [options] url')
        self.init_options(op)
        op.add_option('-s', '--set', help='Set "set" value of request (by default, hostname_wid)')
        op.add_option('-d', '--dry-run', action='store_true', default=False, help='run watcher but do not submit data to daemon.')
        op.add_option('-v', '--verbose', action='store_true', default=False, help='print submited values on STDOUT')
        op.add_option('--version', action='store_true', default=False, help='print version and exit')
        (self._options, args) = op.parse_args()
        if self._options.version:
            print '%s (%s) v%s by %s' % (
             self.__name__,
             self.__wid__,
             self.__version__,
             self.__author__)
            sys.exit(0)
        if len(args) < 1:
            op.error('Watcher needs URL of GraphIT daemon to which to send the data')
        self._url = urlparse(args[0])
        if self._url.scheme != 'http':
            op.error('GraphIT only support http protocol')
        if self._url.port is not None:
            port = ':%s' % self._url.port
        else:
            port = ''
        url = 'http://%s%s/%s' % (self._url.hostname, port, self._url.query)
        self.check_options(op, args)
        GraphItAgent.__init__(self, url, login=self._url.username, passwd=self._url.password)
        self.run()
        return

    def init_options(self, op):
        """ Method to overload for adding cli options to Watcher. """
        pass

    def check_options(self, op, args):
        """ Method to overload for checking new added cli options
                to watcher. """
        pass

    def get_set(self):
        """ Get "set" value for request. By default, I take hostname
                        and wid (Watcher ID), but value can be redefined by user
                        with "--set" cli option. """
        if self._options.set:
            return self._options.set
        else:
            return '%s_%s' % (gethostname(), self.__wid__)

    def submit(self, feed, value, unit=''):
        """ Submit value to GraphITd if dry run mode is not enabled. """
        if self._options.verbose:
            print 'Submitting value %s%s to %s/%s/%s...' % (
             value,
             unit,
             self._url.hostname,
             self.get_set(),
             feed)
        if not self._options.dry_run:
            self.add_value(self.get_set(), feed, value, unit)