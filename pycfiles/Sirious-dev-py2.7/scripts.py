# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/sirious/scripts.py
# Compiled at: 2011-11-28 10:49:50
import ConfigParser, logging, os
from pkg_resources import resource_filename
from twisted.internet import reactor, ssl
from sirious import SiriProxyFactory

def get_paths():
    cfg_dirs = [
     os.path.expanduser('~/.sirious/'), '/etc/sirious']
    if os.getenv('VIRTUAL_ENV'):
        cfg_dirs.insert(0, os.path.expandvars('${VIRTUAL_ENV}/.sirious/'))
    return cfg_dirs


def gen_certs():
    path = get_paths()[0]
    os.system('mkdir -p %s/ssl' % path)
    os.chdir(path)
    filename = resource_filename(__name__, 'scripts/gen_certs.zsh')
    print 'You will shortly be asked four questions. The correct answers are 1234, 1234, y, y.'
    os.system(filename)


def start_proxy():
    config = ConfigParser.RawConfigParser()
    cfg_dirs = get_paths()
    for dir in cfg_dirs[::-1]:
        config.read('sirious.cfg')

    try:
        core_settings = config.items('core')
    except ConfigParser.NoSectionError:
        core_settings = {}

    settings = {}
    settings['root'] = root = cfg_dirs[0]
    try:
        try:
            loglevel_name = core_settings['loglevel']
            loglevel = getattr(logging, loglevel_name.upper())
        except (KeyError, AttributeError):
            loglevel = logging.INFO

    finally:
        logging.basicConfig(format='%(asctime)s %(levelname)s [%(name)s] %(message)s', level=loglevel)

    plugins = []
    for plugin, cls in config.items('plugins'):
        logging.getLogger('sirious').info('Registering plugin %s.%s...' % (plugin, cls))
        try:
            kwargs = dict(config.items(cls))
        except ConfigParser.NoSectionError:
            kwargs = {}

        plugins.append((plugin, cls, kwargs))

    settings['plugins'] = plugins
    logging.getLogger('sirious').info('Starting up...')
    reactor.listenSSL(443, SiriProxyFactory(**settings), ssl.DefaultOpenSSLContextFactory(os.path.join(root, 'ssl', 'server.key'), os.path.join(root, 'ssl', 'server.crt')))
    reactor.run()