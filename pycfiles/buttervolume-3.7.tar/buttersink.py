# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/buttersink/buttersink.py
# Compiled at: 2018-06-26 18:40:50
__doc__ = ' Main program to synchronize btrfs snapshots.  See README.md.\n\nCopyright (c) 2014 Ames Cornish.  All rights reserved.  Licensed under GPLv3.\n\n'
if True:
    if True:
        import argparse, errno, logging, logging.handlers, os.path, re, sys
        from util import humanize
        import BestDiffs, ButterStore, S3Store, SSHStore
theDebug = False
logger = logging.getLogger(__name__)
try:
    import version
    theVersion = version.version
except IOError:
    print "Can't import version.py"
    theVersion = '<unknown>'

theChunkSize = 20
command = argparse.ArgumentParser(description='Synchronize two sets of btrfs snapshots.', epilog='\n<src>, <dst>:   [btrfs://]/path/to/directory/[snapshot]\n                s3://bucket/prefix/[snapshot]\n                ssh://[user@]host/path/to/directory/[snapshot]\n\nIf only <dst> is supplied, just list available snapshots.  NOTE: The trailing\n"/" *is* significant.\n\nCopyright (c) 2014-2016 Ames Cornish.  All rights reserved.  Licensed under GPLv3.\nSee README.md and LICENSE.txt for more info.\n    ', formatter_class=argparse.RawDescriptionHelpFormatter)
command.add_argument('source', metavar='<src>', nargs='?', help='a source of btrfs snapshots')
command.add_argument('dest', metavar='<dst>', help='the btrfs snapshots to be updated')
command.add_argument('-n', '--dry-run', action='store_true', help="display what would be transferred, but don't do it")
command.add_argument('-d', '--delete', action='store_true', help='delete any snapshots in <dst> that are not in <src>')
command.add_argument('-e', '--estimate', action='store_true', help='use estimated size instead of measuring diffs with a local test send')
command.add_argument('-q', '--quiet', action='store_true', help='only display error messages')
command.add_argument('-l', '--logfile', type=argparse.FileType('a'), help='log debugging information to file')
command.add_argument('-V', '--version', action='version', version='%(prog)s ' + theVersion, help='display version')
command.add_argument('--part-size', action='store', type=int, default=theChunkSize, help='Size of chunks in a multipart upload')
command.add_argument('--exclude', action='append', type=str, help='regular expresion to exclude subvols')
command.add_argument('--server', action='store_true', help=argparse.SUPPRESS)
command.add_argument('--mode', help=argparse.SUPPRESS)

def _setupLogging(quiet, logFile, isServer):
    theDisplayFormat = '%(message)s'
    theDebugDisplayFormat = '%(levelname)7s:%(filename)s[%(lineno)d]: %(message)s'
    theLogFormat = '%(asctime)-15s: %(levelname)7s:%(filename)s[%(lineno)d]: %(message)s'
    theProgram = 'buttersink[%d]' % os.getpid()
    theSysLogFormat = theProgram + ': %(filename)s[%(lineno)d]: %(message)s'
    root = logging.getLogger()
    root.setLevel('INFO' if theDebug else 'DEBUG')

    def add(handler, level, format):
        handler = logging.StreamHandler(handler)
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter(format))
        root.addHandler(handler)

    level = 'DEBUG' if theDebug else 'INFO' if not quiet else 'WARN'
    formatString = theDebugDisplayFormat if theDebug else theDisplayFormat
    formatString = ('S|' if isServer else '  ') + formatString
    add(sys.stderr, level, formatString)
    if logFile is not None:
        add(logFile, 'DEBUG', theLogFormat)
    if isServer:
        handler = logging.handlers.SysLogHandler(address='/dev/log')
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter(theSysLogFormat))
        root.addHandler(handler)
    logging.getLogger('boto').setLevel('WARN')
    return


def parseSink(uri, isDest, willDelete, dryrun):
    """ Parse command-line description of sink into a sink object. """
    if uri is None:
        return
    else:
        pattern = re.compile('^((?P<method>[^:/]*)://)?(?P<fullpath>(?P<host>[^/]*)(/(?P<path>.*))?)$')
        match = pattern.match(uri)
        if match is None:
            raise Exception("Can't parse snapshot store '%s'" % uri)
        parts = match.groupdict()
        if parts['method'] is None:
            parts['method'] = 'btrfs'
        logger.debug(parts)
        if parts['method'] in ('btrfs', 'file'):
            path = parts['fullpath']
            host = None
        else:
            path = parts['path']
            host = parts['host']
        if isDest and not path.endswith('/'):
            path += '/'
        if not isDest:
            mode = 'r'
        elif willDelete:
            mode = 'w'
        else:
            mode = 'a'
        Sinks = {'btrfs': ButterStore.ButterStore, 
           's3': S3Store.S3Store, 
           'ssh': SSHStore.SSHStore}
        return Sinks[parts['method']](host, path, mode, dryrun)


def main():
    """ Main program. """
    try:
        args = command.parse_args()
        _setupLogging(args.quiet, args.logfile, args.server)
        logger.debug('Version: %s, Arguments: %s', theVersion, vars(args))
        if args.server:
            server = SSHStore.StoreProxyServer(args.dest, args.mode)
            return server.run()
        source = parseSink(args.source, False, args.delete, args.dry_run)
        dest = parseSink(args.dest, source is not None, args.delete, args.dry_run)
        if source is None:
            source = dest
            dest = None
        if not sys.stderr.isatty():
            source.showProgress = dest.showProgress = False
        elif dest is None or source.isRemote and not dest.isRemote:
            source.showProgress = True
        else:
            dest.showProgress = True
        with source:
            try:
                next(source.listVolumes())
            except StopIteration:
                logger.warn('No snapshots in source.')
                path = args.source or args.dest
                if path.endswith('/'):
                    logger.error("'%s' does not contain any snapshots.  Did you mean to type '%s'?", path, path[0:-1])
                else:
                    logger.error("'%s' is not a snapshot.  Did you mean to type '%s/'?", path, path)
                return 1

            if dest is None:
                for item in source.listContents():
                    print item

                if args.delete:
                    source.deletePartials()
                return 0
            with dest:
                volumes = source.listVolumes()
                if args.exclude:

                    def is_excluded(vol):
                        for path in source.getPaths(vol):
                            for pattern in args.exclude:
                                if re.match(pattern, path):
                                    return True

                        return False

                    volumes = (vol for vol in volumes if not is_excluded(vol))
                best = BestDiffs.BestDiffs(volumes, args.delete, not args.estimate)
                best.analyze(args.part_size << 20, source, dest)
                summary = best.summary()
                logger.info('Optimal synchronization:')
                for sink, values in summary.items():
                    logger.info('%s from %d diffs in %s', humanize(values.size), values.count, sink or 'TOTAL')

                for diff in best.iterDiffs():
                    if diff is None:
                        raise Exception("Missing diff.  Can't fully replicate.")
                    else:
                        diff.sendTo(dest, chunkSize=args.part_size << 20)

                if args.delete:
                    dest.deleteUnused()
        logger.debug('Successful exit')
        return 0
    except Exception as error:
        if isinstance(error, IOError) and error.errno == errno.EPERM and os.getuid() != 0:
            logger.error("You must be root to access a btrfs filesystem.  Use  'sudo'")
        else:
            if not theDebug:
                logger.debug('Trace information for debugging', exc_info=True)
            logger.error('ERROR: %s.', error, exc_info=theDebug)
        return 1

    return


if __name__ == '__main__':
    sys.exit(main())