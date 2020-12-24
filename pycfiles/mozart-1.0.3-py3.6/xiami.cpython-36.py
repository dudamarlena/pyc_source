# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/mozart/music/xiami.py
# Compiled at: 2019-05-07 04:28:47
# Size of source mod 2**32: 1805 bytes
import re
from .base import Music
from .exception import MusicDoesnotExists
from mozart import config
import requests
__all__ = [
 'XiaMi']

class XiaMi(Music):

    def __init__(self, *args, **kwargs):
        (super(XiaMi, self).__init__)(*args, **kwargs)
        if not self.use_id:
            self.music_id = self.get_music_id_from_url(self.real_url)
        self.get_music_from_id()
        print(self.__repr__())

    def get_music_from_id(self):
        if self.music_id:
            params = {'v':'2.0',  'app_key':'1', 
             'r':'song/detail', 
             'id':self.music_id}
            s = requests.Session()
            s.headers.update(config.fake_headers)
            s.head('http://m.xiami.com')
            s.headers.update({'referer': 'http://m.xiami.com/'})
            r = s.get('http://api.xiami.com/web', params=params)
            if r.status_code != requests.codes.ok:
                raise Exception('获取音乐失败')
            try:
                j = r.json()
                self._song = j['data']['song']['song_name']
                self._singer = j['data']['song']['singers']
                self._cover = j['data']['song']['logo']
                self._download_url = j['data']['song']['listen_file']
            except Exception:
                raise MusicDoesnotExists('音乐不存在，请检查')

    def _get_music_info(self):
        pass

    def _get_download_url(self):
        pass

    @classmethod
    def get_music_id_from_url(cls, url):
        music_ids = re.findall('www.xiami.com/song/(\\d+)', url)
        if music_ids:
            return music_ids[0]
        else:
            return ''