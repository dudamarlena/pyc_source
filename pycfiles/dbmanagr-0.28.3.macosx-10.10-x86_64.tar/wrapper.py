# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dbmanagr/wrapper.py
# Compiled at: 2015-10-11 07:17:06
import sys, os, logging, pdb, urllib2, json, ijson
from dbmanagr.writer import Writer
from dbmanagr import logger as log
from dbmanagr.jsonable import from_json
COMMANDS = {'dbdiff': 'differ', 
   'dbexec': 'executer', 
   'dbexport': 'exporter', 
   'dbgraph': 'grapher', 
   'dbnav': 'navigator'}

class Wrapper(object):

    def __init__(self, options=None):
        self.options = options

    def write(self):
        try:
            sys.stdout.write(Writer.write(self.run()))
        except BaseException as e:
            log.logger.exception(e)
            return -1

        return 0

    def execute(self):
        """To be overridden by sub classes"""
        pass

    def run(self):
        try:
            if self.options is not None and self.options.daemon:
                log.logger.debug('Executing remotely')
                return self.executer(*sys.argv)
            else:
                log.logger.debug('Executing locally')
                return self.execute()

        except BaseException as e:
            log.logger.exception(e)
            if log.logger.getEffectiveLevel() <= logging.DEBUG:
                if os.getenv('UNITTEST', 'False') == 'True':
                    raise
                if self.options.trace:
                    pdb.post_mortem(sys.exc_info()[2])
            else:
                log.log_error(e)

        return

    def executer(self, *args):
        """Execute remotely"""
        options = self.options
        try:
            url = ('http://{host}:{port}/{path}').format(host=options.host, port=options.port, path=COMMANDS[options.prog])
            request = json.dumps(args[1:])
            log.logger.debug('Request to %s:\n%s', url, request)
            response = urllib2.urlopen(url, request)
            for i in ijson.items(response, 'item'):
                yield from_json(i)

        except urllib2.HTTPError as e:
            raise from_json(json.load(e))
        except urllib2.URLError as e:
            log.logger.error('Daemon not available: %s', e)
        except BaseException as e:
            log.logger.exception(e)