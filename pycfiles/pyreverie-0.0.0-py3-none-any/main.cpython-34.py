# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /opt/griflet/venv/lib/python3.4/site-packages/pyrev/main.py
# Compiled at: 2017-02-20 22:35:35
# Size of source mod 2**32: 5166 bytes
__doc__ = 'Py-Re:VIEW: A Re:VIEW tool written in Python.\n'
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from logging import getLogger, StreamHandler
from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG
from .parser import Parser, ParseProblem
from .project import ReVIEWProject
from .version import VERSION
import os, sys, traceback

def lint(args, logger):
    logger.debug('Start running "lint".')
    if args.unacceptable_level == 'CRITICAL':
        unacceptable_level = CRITICAL
    else:
        if args.unacceptable_level == 'ERROR':
            unacceptable_level = ERROR
        else:
            if args.unacceptable_level == 'WARNING':
                unacceptable_level = WARNING
            else:
                if args.unacceptable_level == 'INFO':
                    unacceptable_level = INFO
                else:
                    if args.unacceptable_level == 'DEBUG':
                        unacceptable_level = DEBUG
                    else:
                        raise RuntimeError('Unknown level "{}"'.format(args.unacceptable_level))
    file_path = os.path.abspath(args.filename)
    if not os.path.exists(file_path):
        logger.error('"{}" does not exist'.format(args.filename))
        return
    if os.path.isdir(file_path):
        logger.debug('"{}" is a directory.'.format(file_path))
        source_dir = ReVIEWProject.guess_source_dir(file_path)
        logger.debug('source_dir: {}'.format(source_dir))
        if not source_dir:
            logger.error('Failed to detect source_dir')
            return
        project = ReVIEWProject.instantiate(source_dir, logger=logger)
        if not project:
            logger.error('Failed to instanciate Re:VIEW Project ({}).'.format(source_dir))
            return
        project.parse_source_files()
        try:
            parser = Parser(project=project, ignore_threshold=INFO, abort_threshold=unacceptable_level, logger=logger)
            for filename in project.source_filenames:
                logger.debug('Parsing "{}"'.format(filename))
                path = os.path.normpath('{}/{}'.format(project.source_dir, filename))
                parser.parse_file(path, 0, filename)
                dump_func = lambda x: sys.stdout.write('{}\n'.format(x))

            parser._dump_problems(dump_func=dump_func)
        except ParseProblem:
            logger.error(traceback.format_exc())

    else:
        logger.debug('"{}" is a file. Interpret a single script.'.format(args.filename))
    try:
        source_dir = os.path.dirname(file_path)
        project = ReVIEWProject(source_dir, logger=logger)
        project.parse_source_files()
        parser = Parser(project=project, ignore_threshold=INFO, abort_threshold=unacceptable_level, logger=logger)
        source_name = os.path.basename(args.filename)
        parser.parse_file(args.filename, 0, source_name)
        dump_func = lambda x: sys.stdout.write('{}\n'.format(x))
        parser._dump_problems(dump_func=dump_func)
    except ParseProblem:
        logger.error(traceback.format_exc())


def main():
    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('filename')
    parser.add_argument('--log', default='INFO', help='Set log level. e.g. DEBUG, INFO, WARN')
    parser.add_argument('-d', '--debug', action='store_true', help='Aliased to --log=DEBUG')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(VERSION), help='Show version and exit.')
    parser.add_argument('-u', '--unacceptable_level', action='store', default='CRITICAL', help='Error level that aborts the check.')
    args = parser.parse_args()
    if args.debug:
        args.log = 'DEBUG'
    logger = getLogger(__name__)
    handler = StreamHandler()
    logger.setLevel(args.log.upper())
    handler.setLevel(args.log.upper())
    logger.addHandler(handler)
    lint(args, logger)


if __name__ == '__main__':
    main()