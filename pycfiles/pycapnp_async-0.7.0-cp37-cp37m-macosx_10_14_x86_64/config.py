# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/cfl/ternaris/marv/pycapnp/buildutils/config.py
__doc__ = 'Config functions'
import sys, os, json
try:
    from configparser import ConfigParser
except:
    from ConfigParser import ConfigParser

pjoin = os.path.join
from .msg import debug, fatal, warn

def load_config(name, base='conf'):
    """Load config dict from JSON"""
    fname = pjoin(base, name + '.json')
    if not os.path.exists(fname):
        return {}
    try:
        with open(fname) as (f):
            cfg = json.load(f)
    except Exception as e:
        warn("Couldn't load %s: %s" % (fname, e))
        cfg = {}

    return cfg


def save_config(name, data, base='conf'):
    """Save config dict to JSON"""
    if not os.path.exists(base):
        os.mkdir(base)
    fname = pjoin(base, name + '.json')
    with open(fname, 'w') as (f):
        json.dump(data, f, indent=2)


def v_str(v_tuple):
    """turn (2,0,1) into '2.0.1'."""
    return ('.').join(str(x) for x in v_tuple)


def get_eargs():
    """ Look for options in environment vars """
    settings = {}
    zmq = os.environ.get('ZMQ_PREFIX', None)
    if zmq is not None:
        debug('Found environ var ZMQ_PREFIX=%s' % zmq)
        settings['zmq_prefix'] = zmq
    return settings


def cfg2dict(cfg):
    """turn a ConfigParser into a nested dict
    
    because ConfigParser objects are dumb.
    """
    d = {}
    for section in cfg.sections():
        d[section] = dict(cfg.items(section))

    return d


def get_cfg_args():
    """ Look for options in setup.cfg """
    if not os.path.exists('setup.cfg'):
        return {}
    cfg = ConfigParser()
    cfg.read('setup.cfg')
    cfg = cfg2dict(cfg)
    g = cfg.setdefault('global', {})
    for key in ['libzmq_extension',
     'bundle_libzmq_dylib',
     'no_libzmq_extension',
     'have_sys_un_h',
     'skip_check_zmq']:
        if key in g:
            g[key] = eval(g[key])

    cfg.update(cfg.pop('global'))
    return cfg


def config_from_prefix(prefix):
    """Get config from zmq prefix"""
    settings = {}
    if prefix.lower() in ('default', 'auto', ''):
        settings['zmq_prefix'] = ''
        settings['libzmq_extension'] = False
        settings['no_libzmq_extension'] = False
    elif prefix.lower() in ('bundled', 'extension'):
        settings['zmq_prefix'] = ''
        settings['libzmq_extension'] = True
        settings['no_libzmq_extension'] = False
    else:
        settings['zmq_prefix'] = prefix
        settings['libzmq_extension'] = False
        settings['no_libzmq_extension'] = True
    return settings


def merge(into, d):
    """merge two containers
    
    into is updated, d has priority
    """
    if isinstance(into, dict):
        for key in d.keys():
            if key not in into:
                into[key] = d[key]
            else:
                into[key] = merge(into[key], d[key])

        return into
    if isinstance(into, list):
        return into + d
    else:
        return d


def discover_settings(conf_base=None):
    """ Discover custom settings for ZMQ path"""
    settings = {'zmq_prefix': '', 
       'libzmq_extension': False, 
       'no_libzmq_extension': False, 
       'skip_check_zmq': False, 
       'build_ext': {}, 'bdist_egg': {}}
    if sys.platform.startswith('win'):
        settings['have_sys_un_h'] = False
    if conf_base:
        merge(settings, load_config('config', conf_base))
    merge(settings, get_cfg_args())
    merge(settings, get_eargs())
    return settings