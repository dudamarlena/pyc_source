# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pavelstudenik/Develop/vhm-manager/venv/lib/python3.7/site-packages/vhmlib/main.py
# Compiled at: 2020-04-06 03:08:12
# Size of source mod 2**32: 2865 bytes
import configparser, getopt, json, logging, sys, time, requests
from . import core
logging.basicConfig(level=(logging.INFO))
logger = logging.getLogger(__name__)
TIMER_RULE = ((60, 10), (600, 60), (1800, 300))
plugins = {'core': core}

def timer(counter):
    sleep_time = 1
    for c, s in TIMER_RULE:
        if counter > c:
            sleep_time = s

    return sleep_time


class Agent:

    def __init__(self, configfile):
        self.token = None
        self.server = 'http://127.0.0.1:8000'
        config = configparser.ConfigParser()
        config.read(configfile)
        for section in config.sections():
            self.token = config[section]['token']
            self.server = config[section]['server']

    def __call__(self, loop=False, token=None):
        token = self.token or token
        counter = 0
        response = requests.get(('{}/api/ping'.format(self.server)), headers={'Token': token})
        response.raise_for_status()
        response.json()
        while True:
            try:
                response = requests.get(('{}/api/task'.format(self.server)), headers={'Token': token})
                for task in response.json():
                    time_start = time.time()
                    try:
                        app, module, fce = task['command'].split(':')
                        module = getattr(plugins[app], module.capitalize())
                        logger.info('Command: {}'.format(task))
                        return_code, stdout = getattr(module, fce)(json.loads(task['params']))
                    except Exception as exp:
                        try:
                            return_code = -1
                            stdout = str(exp)
                        finally:
                            exp = None
                            del exp

                    data = {'id':task['id'], 
                     'result':stdout, 
                     'exit_code':return_code, 
                     'time':time.time() - time_start}
                    requests.put(('{}/api/task'.format(self.server)),
                      headers={'Token': token}, json=data)
                    counter = 0

                if not loop:
                    break
                sleep_time = timer(counter)
                time.sleep(sleep_time)
                counter += 1
            except KeyboardInterrupt:
                return 0


def application(argv):
    settings = {}
    try:
        opts, args = getopt.getopt(argv, 'hd', ['daemon', 'help', 'token='])
    except getopt.GetoptError:
        print('vhm-agent')
        return 2
    else:
        for opt, arg in opts:
            if opt in ('-d', '--daemon'):
                settings['loop'] = True
            if opt == '--token':
                settings['token'] = arg

        return Agent(configfile='/etc/vmh/config.ini')(**settings)


if __name__ == '__main__':
    sys.exit(application(sys.argv[1:]))