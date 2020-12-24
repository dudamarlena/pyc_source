# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/windflow/services/cli.py
# Compiled at: 2018-04-18 11:33:58
# Size of source mod 2**32: 1778 bytes
import argparse, logging
from tornado.log import enable_pretty_logging
from windflow.services import Service

class CommandLine(Service):
    __doc__ = '\n    Command line interface service.\n\n    '

    def __init__(self, default_handler=None):
        self.default_handler = default_handler
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--debug', '-d', action='store_true', help='enable debugging features')
        self.parser.add_argument('--verbose', '-v', action='count', help='increase output verbosity')
        self.subparsers = self.parser.add_subparsers(dest='handler')
        self.subparsers.required = not callable(default_handler)

    def register(self, service, method='register_commands'):
        return getattr(service, method)(self.subparsers)

    def parse(self, args=None, namespace=None):
        return self.parser.parse_args(args, namespace)

    def run(self, args=None, namespace=None):
        options = self.parser.parse_args(args=args, namespace=namespace)
        enable_pretty_logging()
        logger = logging.getLogger(__name__)
        if options.debug:
            logging.getLogger('root').setLevel(logging.INFO)
        if options.verbose:
            if options.verbose >= 1:
                logging.getLogger('root').setLevel(logging.DEBUG)
            if options.verbose >= 2:
                logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO if options.verbose < 2 else logging.DEBUG)
        try:
            handler = options.handler
        except AttributeError as e:
            if not callable(self.default_handler):
                raise
            handler = None

        return handler or self.default_handler(logger, options)