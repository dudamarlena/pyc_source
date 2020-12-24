# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/opentargets_validator/cli.py
# Compiled at: 2020-01-16 04:41:30
from __future__ import print_function, absolute_import
from __future__ import unicode_literals
import argparse, logging, logging.config, sys
from .helpers import file_or_resource
from .validator import validate
from opentargets_urlzsource import URLZSource

def main():
    logging.config.fileConfig(file_or_resource(b'logging.ini'), disable_existing_loggers=False)
    logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser(description=b'OpenTargets evs validator')
    parser.add_argument(b'data_source_file', nargs=b'?', default=b'-', help=b'The prefix to prepend default: STDIN')
    parser.add_argument(b'--schema', dest=b'schema', help=b'set the schema file to use', action=b'store')
    parser.add_argument(b'--log-level', dest=b'loglevel', help=b'set the log level def: WARNING', action=b'store', default=b'WARNING')
    parser.add_argument(b'--log-lines', dest=b'loglines', help=b'number of log errors to print out [no longer supported]', action=b'store', type=int, default=None)
    parser.add_argument(b'--hash', dest=b'hash', help=b'calculate hash of each line for uniqueness', action=b'store_true')
    args = parser.parse_args()
    if args.loglevel:
        try:
            root_logger = logging.getLogger()
            root_logger.setLevel(logging.getLevelName(args.loglevel))
            logger.setLevel(logging.getLevelName(args.loglevel))
        except Exception as e:
            root_logger.exception(e)

    if not args.schema:
        logger.error(b'A --schema <schemafile> has to be specified.')
        return 1
    else:
        if args.loglines is not None:
            logger.error(b'--log-lines is no longer supported')
            return 3
        valid = True
        if args.data_source_file == b'-':
            valid = validate(sys.stdin, args.schema, args.hash)
        else:
            with URLZSource(args.data_source_file).open() as (fh):
                valid = validate(fh, args.schema, args.hash)
        if not valid:
            return 2
        return 0


if __name__ == b'__main__':
    sys.exit(main())