# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/multiblend/__init__.py
# Compiled at: 2009-04-08 10:18:50
r"""Multiblend - simple distributed Blender rendering.

Usage:
    multiblend.py \
            -b <blenderfile> \
            -s <startframe> \
            -e <endframe> \
            [-T] \
            [-S Scene name] \
            [-E]

    The -T option will cause Multiblend to skip testing the nodes.
    The -S option can denote the scene to render.
    The -E option will cause Multiblend to skip frames that already exist.

Configuration
=============

Configuration is read from /etc/multiblend and ~/.multiblendrc. Below
you find an example config file::

    [main]
    chunks=100
    nodes=2
    outputpath=/home/sybren/documents/blender/output
    ssh=/usr/bin/ssh -Tq
    scp=/usr/bin/scp -q
    echoing_shell=False
    nice=3

    [node0]
    hostname=localhost
    blender=/home/sybren/blender-2.41-linux-glibc232-py24-i386/blender
    workdir=/home/sybren/tmp

    [node1]
    hostname=zebra
    blender=/home/sybren/blender-2.41-linux-glibc232-py24-i386/blender
    workdir=/tmp

The list of nodes should contain the hostnames or IP addresses of the
nodes, the path to the Blender executable, and the working directory.
The number of nodes should be set in the [main] section.

The 'echoing_shell' option is optional and defaults to False. It can
be set in the [main] section for all the nodes, and can be specified
for specific nodes. First try without this option. If you get the
message that Blender is not executable on nodes where it actually is
executable, try echoing_shell=True.

WARNING: The working directory should be different from the directory
the blender file is in. Otherwise, you might lose your work.

Setting up a node
=================

The node where this script is run, is called the "master node". All
other nodes are just called "node".

The node should be reachable from the master node using SSH, without
having to type a password. Use 'ssh-keygen' to generate a suitable SSH
key, and use 'ssh-copy-id' to copy the key from the master node to the
other nodes. That generally does the trick. If you want to run a
Blender instance on the master node as well, include a node with
hostname=localhost.

License
=======

This software is covered by the Gnu Public License, or GPL. For more
information, see http://www.stuvel.eu/license.
"""
__author__ = 'Sybren A. Stüvel'
__email__ = 'sybren@stuvel.eu'
__revision__ = '1.4'
__url__ = 'http://stuvel.eu/multiblend'
import ConfigParser, datetime, getopt, os, os.path, sys, time
from multiblend.logging import Logger
log = Logger('MAIN')
if 'DEBUG' in os.environ:
    logging.set_level(logging.DEBUG)
else:
    logging.set_level(logging.INFO)
from multiblend.node import Node
from multiblend.popen import DebuggingPopen
from multiblend.dispatcher import FrameDispatcher

def node_names(config):
    """Generator, iterates over the node names"""
    for nodenr in xrange(config['nodes']):
        yield 'node%i' % nodenr


def load_config():
    """Loads the configuration file.
    
    Loads the config from /etc/multiblend and ~/.multiblendrc.
    """
    conf = ConfigParser.ConfigParser()
    home = os.environ['HOME']
    read = conf.read(['/etc/multiblend', '%s/.multiblendrc' % home])
    if not read:
        print __doc__
        raise SystemExit('No configuration file found. An example file can be seen above, in the documentation. Place it in ~/.multiblendrc and alter it to match your situation.')
    try:
        config = dict(outputpath=conf.get('main', 'outputpath'), chunks=conf.getint('main', 'chunks'), nodes=conf.getint('main', 'nodes'), ssh=conf.get('main', 'ssh'), scp=conf.get('main', 'scp'), nice=conf.getint('main', 'nice'))
    except ConfigParser.NoOptionError, e:
        print __doc__
        print 70 * '='
        log.critical('A key is missing in the configuration file: %s' % e)
        raise SystemExit()

    try:
        config['echoing_shell'] = conf.getboolean('main', 'echoing_shell')
    except ConfigParser.NoOptionError, e:
        config['echoing_shell'] = False

    for node in node_names(config):
        try:
            config[node] = dict(hostname=conf.get(node, 'hostname'), blender=conf.get(node, 'blender'), workdir=conf.get(node, 'workdir'))
        except ConfigParser.NoOptionError, e:
            print __doc__
            print 70 * '='
            log.critical('A key is missing in the configuration file: %s' % e)
            raise SystemExit()

        try:
            config[node]['echoing_shell'] = conf.getboolean(node, 'echoing_shell')
        except ConfigParser.NoOptionError, e:
            config[node]['echoing_shell'] = config['echoing_shell']

    config['scene'] = None
    return config


def parse_options(required=('-b', '-s', '-e')):
    """Parses the commandline options.

    Returns the options in a dict.
    """
    try:
        (opts, args) = getopt.gnu_getopt(sys.argv[1:], 'b:s:e:TS:E')
    except getopt.GetoptError, e:
        print __doc__
        raise SystemExit(str(e))

    opts = dict(opts)
    for option in required:
        if option not in opts:
            print __doc__
            raise SystemExit('Option %s is required.' % option)

    if args:
        print __doc__
        raise SystemExit('Unknown argument %s' % args)
    return opts


def banner():
    """Prints the startup banner"""
    print 60 * '='
    print 'Starting Multiblend %s' % __revision__
    print ('Created by %s <%s>' % (__author__.decode('utf-8'), __email__)).encode('utf-8')
    print __url__
    print 60 * '='
    print


def nodelist(test_nodes=True):
    """Returns a list of approved nodes."""
    nodelist = []
    for nodename in node_names(config):
        node = Node(config, nodename)
        if test_nodes:
            if node.test():
                nodelist.append(node)
                log.info('Approved %s' % node)
            else:
                log.info('Disapproved %s' % node)
        else:
            nodelist.append(node)
            log.info('Added %s without testing.' % node)

    return nodelist


def check_options_and_config(options, config, nodes):
    """Checks the options and config file, to see if there are any
    conflicts.
    """
    outpath = config['outputpath']
    if not os.path.exists(outpath):
        log.critical("Output path %s doesn't exist" % outpath)
        raise SystemExit()
    if not os.path.isdir(outpath):
        log.critical('Output path %s exists but is not a directory' % outpath)
        raise SystemExit()
    blenderfile = os.path.abspath(os.path.realpath(options['-b']))
    blenderdir = os.path.dirname(blenderfile)
    for node in nodes:
        if not node.hostname == 'localhost':
            continue
        workdir = os.path.abspath(os.path.realpath(node.workdir))
        if workdir == blenderdir:
            log.critical('Directory of %s is the same as the work directory for the master node. This is not allowed.' % options['-b'])
            raise SystemExit()


def set_scene(config, options):
    """Sets the 'scene' config key from the -S option"""
    if '-S' in options:
        config['scene'] = options['-S']
        log.info('Rendering scene %s' % config['scene'])


def create_frame_dispatcher(options, config, node_count):
    """Creates a frame dispatcher for the given configuration and commandline
    options.
    """
    start = int(options['-s'])
    end = int(options['-e'])
    chunksize = config['chunks']
    fd_output_path = '-E' in options and config['outputpath'] or ''
    return FrameDispatcher(start, end, chunksize, node_count, fd_output_path)


def distrib_cache():
    """Distributes the cache directory belonging to the blend file to
    the working directory of the nodes.
    """
    global config
    banner()
    config = load_config()
    options = parse_options(required=('-b', ))
    log.info('Distributing cache files for file: %s' % options['-b'])
    cache_dir = 'blendcache_%s' % os.path.splitext(options['-b'])[0]
    log.debug('Cache dir: %s' % cache_dir)
    nodes = nodelist('-T' not in options)
    if not nodes:
        log.error('No nodes available')
        raise SystemExit()
    for node in nodes:
        log.info('Syncing to %s' % node)
        target = '%s:%s%s' % (node.hostname, node.workdir, os.path.sep)
        rsync = DebuggingPopen(node.log, ('rsync', cache_dir, target,
         '-va', '--delete'))
        rsync.tochild.close()
        for line in rsync.fromchild:
            log.debug(line.strip())

        rsync.fromchild.close()
        rsync.wait()


def doctest():
    """Runs doctests on multiblend"""
    print 'Running doctest'
    import doctest, multiblend, multiblend.logging, multiblend.node, multiblend.popen, multiblend.dispatcher
    doctest.testmod(multiblend)
    doctest.testmod(multiblend.logging)
    doctest.testmod(multiblend.node)
    doctest.testmod(multiblend.popen)
    doctest.testmod(multiblend.dispatcher)
    raise SystemExit()


def main():
    """Runs multiblend"""
    global config
    if len(sys.argv) >= 2 and sys.argv[1] == 'DOCTEST':
        doctest()
    start_time = datetime.datetime.now()
    banner()
    config = load_config()
    options = parse_options()
    nodes = nodelist('-T' not in options)
    if not nodes:
        log.error('No nodes available')
        raise SystemExit()
    check_options_and_config(options, config, nodes)
    dispatcher = create_frame_dispatcher(options, config, len(nodes))
    for node in nodes:
        node.renderchunks(options['-b'], dispatcher)

    try:
        time.sleep(2)
        done = False
        while not done:
            done = True
            for node in nodes:
                if node.rendering:
                    done = False
                    break

            time.sleep(1)

    except KeyboardInterrupt:
        log.info('Ctrl+C pressed, trying to stop them all. Please be patient.')
        for node in nodes:
            node.abort()

    end_time = datetime.datetime.now()
    time.sleep(2)
    log.info('Done multiblendering.')
    log.info('Start time: %s' % start_time)
    log.info('End time  : %s' % end_time)
    log.info('Spent     : %s' % (end_time - start_time))


if __name__ == '__main__':
    main()