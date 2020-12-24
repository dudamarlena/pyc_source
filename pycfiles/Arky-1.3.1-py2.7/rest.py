# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arky\rest.py
# Compiled at: 2018-01-13 17:26:35
from . import __PY3__
from . import __FROZEN__
from . import ROOT
from . import HOME
if not __PY3__:
    import cfg, slots
else:
    from . import cfg
    from . import slots
import io, os, sys, json, pytz, random, logging, requests, traceback, importlib
__PEER__ = False

def useCustomPeer(peer):
    __PEER__ = peer


def unuseCustomPeer():
    __PEER__ = False


def get(entrypoint, dic={}, **kw):
    """
        Generic GET call using requests lib. It returns server response as dict object.
        It randomly select one of peersregistered in cfg.peers list. A custom peer can 
        be used.

        Argument:
        entrypoint (str) -- entrypoint url path

        Keyword argument:
        dic (dict) -- api parameters as dict type
        **kw -- api parameters as keyword argument (overwriting dic ones)

        Return dict
        """
    args = dict(dic, **kw)
    returnKey = args.pop('returnKey', False)
    peer = kw.pop('peer', __PEER__)
    args = dict([k.replace('and_', 'AND:') if k.startswith('and_') else k, v] for k, v in args.items())
    try:
        text = requests.get((peer if peer else random.choice(cfg.peers)) + entrypoint, params=args, headers=cfg.headers, verify=cfg.verify, timeout=cfg.timeout).text
        data = json.loads(text)
    except Exception as error:
        data = {'success': False, 'error': error, 'peer': peer}
        if hasattr(error, '__traceback__'):
            data['details'] = '\n' + ('').join(traceback.format_tb(error.__traceback__)).rstrip()

    if data.get('success', False):
        if returnKey:
            data = data[returnKey]
            for key in [ k for k in ['balance', 'unconfirmedBalance', 'vote'] if k in data ]:
                data[key] = float(data[key]) / 100000000

    return data


def post(entrypoint, dic={}, **kw):
    peer = kw.pop('peer', __PEER__)
    payload = dict(dic, **kw)
    try:
        text = requests.post((peer if peer else random.choice(cfg.peers)) + entrypoint, data=json.dumps(payload), headers=cfg.headers, verify=cfg.verify, timeout=cfg.timeout).text
        data = json.loads(text)
    except Exception as error:
        data = {'success': False, 'error': error}
        if hasattr(error, '__traceback__'):
            data['details'] = '\n' + ('').join(traceback.format_tb(error.__traceback__)).rstrip()

    return data


def put(entrypoint, dic={}, **kw):
    peer = kw.pop('peer', __PEER__)
    payload = dict(dic, **kw)
    try:
        text = requests.put((peer if peer else random.choice(cfg.peers)) + entrypoint, data=json.dumps(payload), headers=cfg.headers, verify=cfg.verify, timeout=cfg.timeout).text
        data = json.loads(text)
    except Exception as error:
        data = {'success': False, 'error': error}
        if hasattr(error, '__traceback__'):
            data['details'] = '\n' + ('').join(traceback.format_tb(error.__traceback__)).rstrip()

    return data


def checkPeerLatency(peer):
    """
        Return peer latency in seconds.
        """
    try:
        r = requests.get(peer, timeout=cfg.timeout, verify=cfg.verify)
    except:
        return False

    return r.elapsed.total_seconds()


class Endpoint:

    def __init__(self, method, endpoint):
        self.method = method
        self.endpoint = endpoint

    def __call__(self, dic={}, **kw):
        return self.method(self.endpoint, dic, **kw)

    @staticmethod
    def createEndpoint(ndpt, method, path):
        newpath = ''
        for name in [ e for e in path.split('/') if e != '' ]:
            newpath += '/' + name
            if not hasattr(ndpt, name):
                setattr(ndpt, name, Endpoint(method, newpath))
            ndpt = getattr(ndpt, name)


def load_endpoints(network):
    global GET
    global POST
    global PUT
    try:
        with io.open(os.path.join(ROOT, 'ndpt', network + '.ndpt')) as (f):
            endpoints = json.load(f)
    except FileNotFoundError:
        sys.stdout.write('No endpoints file found\n')
        return False

    POST = Endpoint(post, '')
    for endpoint in endpoints['POST']:
        POST.createEndpoint(POST, post, endpoint)

    PUT = Endpoint(put, '')
    for endpoint in endpoints['PUT']:
        PUT.createEndpoint(PUT, put, endpoint)

    GET = Endpoint(get, '')
    for endpoint in endpoints['GET']:
        GET.createEndpoint(GET, get, endpoint)

    return True


def load(name):
    try:
        sys.modules[__package__].core.DAEMON_PEERS.set()
    except:
        pass

    sys.modules[__package__].core = importlib.import_module(('arky.{}').format(name))
    try:
        sys.modules[__package__].core.init()
    except AttributeError:
        raise Exception('%s package is not a valid blockchain familly' % name)

    try:
        sys.modules[__package__].__delattr__(name)
    except AttributeError:
        pass


def use(network, **kw):
    cfg.__dict__.clear()
    cfg.network = None
    cfg.hotmode = False
    try:
        sys.modules[__package__].__delattr__(network)
    except AttributeError:
        pass

    with io.open(os.path.join(ROOT, 'net', network + '.net')) as (f):
        data = json.load(f)
    data.update(**kw)
    cfg.__dict__.update(data)
    cfg.verify = os.path.join(os.path.dirname(sys.executable), 'cacert.pem') if __FROZEN__ else True
    cfg.begintime = slots.datetime.datetime(tzinfo=slots.pytz.UTC, *cfg.begintime)
    if data.get('seeds', []):
        cfg.peers = []
        for seed in data['seeds']:
            if checkPeerLatency(seed):
                cfg.peers.append(seed)
                break

    else:
        for peer in data.get('peers', []):
            peer = 'http://%s:%s' % (peer, data.get('port', 22))
            if checkPeerLatency(peer):
                cfg.peers = [
                 peer]
                break

    if len(cfg.peers) and load_endpoints(cfg.endpoints):
        load(cfg.familly)
        cfg.network = network
        cfg.hotmode = True
    else:
        raise Exception('Error occured during network seting...')
    logger = logging.getLogger()
    logger.handlers[0].setFormatter(logging.Formatter('[%s]' % network + '[%(asctime)s] %(message)s'))
    return