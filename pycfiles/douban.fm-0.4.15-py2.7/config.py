# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/doubanfm/config.py
# Compiled at: 2016-06-22 17:23:26
from threading import Thread
import cPickle as pickle, ConfigParser, logging, time, os
from doubanfm.API.login import request_token
from doubanfm.check import is_latest, update_package, is_mplayer
from doubanfm.exceptions import ConfigError
is_mplayer()
logger = logging.getLogger('doubanfm')
THEME = [
 'default', 'larapaste', 'monokai', 'tomorrow']
PATH_CONFIG = os.path.expanduser('~/.doubanfm_config')
PATH_HISTORY = os.path.expanduser('~/.doubanfm_history')
PATH_TOKEN = os.path.expanduser('~/.doubanfm_token')
CONFIG = '\n[key]\nUP = k\nDOWN = j\nTOP = g\nBOTTOM = G\nOPENURL = w\nRATE = r\nNEXT = n\nBYE = b\nQUIT = q\nPAUSE = p\nLOOP = l\nMUTE = m\nLRC = o\nHELP = h\nHIGH = i\n'
KEYS = {'UP': 'k', 
   'DOWN': 'j', 
   'TOP': 'g', 
   'BOTTOM': 'G', 
   'OPENURL': 'w', 
   'RATE': 'r', 
   'NEXT': 'n', 
   'BYE': 'b', 
   'QUIT': 'q', 
   'PAUSE': 'p', 
   'LOOP': 'l', 
   'MUTE': 'm', 
   'LRC': 'o', 
   'HELP': 'h', 
   'HIGH': 'i'}

class Config(object):
    """
    提供默认值
    """

    def __init__(self):
        self.volume = 50
        self.channel = 0
        self.theme_id = 0
        self.user_name = ''
        self.netease = False
        self.run_times = 0
        self.last_time = time.time()
        self.total_time = 0
        self.liked = 0
        self.banned = 0
        self.played = 0
        self.is_latest = True
        self.login_data = self.get_login_data()

    def output(args):

        def _deco(func):

            def _func(self):
                print '\x1b[31m♥\x1b[0m ' + args,
                tmp = func(self)
                print ' [\x1b[32m OK \x1b[0m]'
                return tmp

            return _func

        return _deco

    def get_login_data(self):
        u"""
        提供登陆的认证

        这里顺带增加了 volume, channel, theme_id , netease, run_times的默认值
        """
        if os.path.exists(PATH_TOKEN):
            with open(PATH_TOKEN, 'r') as (f):
                login_data = pickle.load(f)
            if 'cookies' not in login_data:
                login_data = request_token()
        else:
            login_data = request_token()
        self.get_default_set(login_data)
        self.get_user_states(login_data)
        self.get_is_latest_version(login_data)
        Thread(target=self.check_version).start()
        return login_data

    def check_version(self):
        self.is_latest = is_latest('douban.fm')

    def get_is_latest_version(self, login_data):
        self.is_latest = login_data.get('is_latest', True)
        if not self.is_latest:
            if_update = raw_input('检测到douban.fm有更新, 是否升级?(Y) ')
            if if_update.lower() == 'y':
                update_package('douban.fm')
                with open(PATH_TOKEN, 'w') as (f):
                    login_data['is_latest'] = True
                    pickle.dump(login_data, f)
                print '请重新打开douban.fm(升级失败可能需要sudo权限, 试试sudo pip install --upgrade douban.fm)'
                os._exit(0)

    def get_default_set(self, login_data):
        u"""
        记录退出时的播放状态
        """
        self.cookies = login_data.get('cookies', '')
        self.user_name = login_data.get('user_name', '')
        print '\x1b[31m♥\x1b[0m Get local token - Username: \x1b[33m%s\x1b[0m' % login_data['user_name']
        self.channel = login_data.get('channel', 0)
        print '\x1b[31m♥\x1b[0m Get channel [\x1b[32m OK \x1b[0m]'
        self.volume = login_data.get('volume', 50)
        print '\x1b[31m♥\x1b[0m Get volume [\x1b[32m OK \x1b[0m]'
        self.theme_id = login_data.get('theme_id', 0)
        print '\x1b[31m♥\x1b[0m Get theme [\x1b[32m OK \x1b[0m]'
        self.netease = login_data.get('netease', False)
        self.keys = self.get_keys()

    def get_user_states(self, login_data):
        u"""
        统计用户信息
        """
        self.run_times = login_data.get('run_times', 0)
        self.total_time = login_data.get('total_time', 0)

    @output('Get keys')
    def get_keys(self):
        u"""
        获取配置并检查是否更改
        """
        if not os.path.exists(PATH_CONFIG):
            with open(PATH_CONFIG, 'w') as (F):
                F.write(CONFIG)
        else:
            config = ConfigParser.ConfigParser()
            with open(PATH_CONFIG, 'r') as (cfgfile):
                config.readfp(cfgfile)
                options = config.options('key')
                for option in options:
                    option = option.upper()
                    if option in KEYS:
                        KEYS[option] = config.get('key', option)

        return KEYS

    @property
    def history(self):
        try:
            with open(PATH_HISTORY, 'r') as (f):
                history = pickle.load(f)
        except IOError:
            history = []

        return history

    def save_config(self, volume, channel, theme, netease):
        u"""
        存储历史记录和登陆信息
        """
        self.login_data['cookies'] = self.cookies
        self.login_data['volume'] = volume
        self.login_data['channel'] = channel
        self.login_data['theme_id'] = theme
        self.login_data['netease'] = netease
        self.login_data['run_times'] = self.run_times + 1
        self.login_data['last_time'] = self.last_time
        self.login_data['total_time'] = self.total_time + time.time() - self.last_time
        self.login_data['is_latest'] = self.is_latest
        with open(PATH_TOKEN, 'w') as (f):
            pickle.dump(self.login_data, f)


db_config = Config()