# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/mozart/music/netease.py
# Compiled at: 2019-05-07 04:25:47
# Size of source mod 2**32: 2907 bytes
import re, requests, json, binascii
from Crypto.Cipher import AES
from .base import Music
from mozart import config
from .exception import MusicDoesnotExists
__all__ = [
 'Netease']

def encode_netease_data(data) -> str:
    data = json.dumps(data)
    key = binascii.unhexlify('7246674226682325323F5E6544673A51')
    encryptor = AES.new(key, AES.MODE_ECB)
    pad = 16 - len(data) % 16
    fix = chr(pad) * pad
    byte_data = (data + fix).encode('utf-8')
    return binascii.hexlify(encryptor.encrypt(byte_data)).upper().decode()


class Netease(Music):

    def __init__(self, *args, **kwargs):
        (super(Netease, self).__init__)(*args, **kwargs)
        if not self.use_id:
            self.music_id = self.get_music_id_from_url(self.real_url)
        self.get_music_from_id()
        print(self.__repr__())

    def get_music_from_id(self):
        if self.music_id:
            self._get_music_info()
            self._get_download_url()

    def _get_music_info(self):
        s = requests.Session()
        s.headers.update(config.fake_headers)
        s.headers.update({'referer': 'http://music.163.com/'})
        eparams = {'method':'POST', 
         'params':{'c': '[{id:%s}]' % self.music_id}, 
         'url':'http://music.163.com/api/v3/song/detail'}
        data = {'eparams': encode_netease_data(eparams)}
        r = s.post('http://music.163.com/api/linux/forward', data=data)
        if r.status_code != requests.codes.ok:
            raise Exception(r.text)
        else:
            j = r.json()
            if len(j['songs']) > 0:
                self._cover = j['songs'][0]['al']['picUrl']
                self._song = j['songs'][0]['al']['name']
                self._singer = j['songs'][0]['ar'][0]['name']
            else:
                raise MusicDoesnotExists('音乐不存在，请检查')

    def _get_download_url(self):
        """ 从网易云音乐下载 """
        eparams = {'method':'POST', 
         'url':'http://music.163.com/api/song/enhance/player/url', 
         'params':{'ids':[
           self.music_id], 
          'br':320000}}
        data = {'eparams': encode_netease_data(eparams)}
        s = requests.Session()
        s.headers.update(config.fake_headers)
        s.headers.update({'referer': 'http://music.163.com/'})
        r = s.post('http://music.163.com/api/linux/forward', data=data)
        if r.status_code != requests.codes.ok:
            raise Exception(r.text)
        j = r.json()
        self._download_url = j['data'][0]['url']
        self._rate = int(j['data'][0]['br'] / 1000)

    @classmethod
    def get_music_id_from_url(cls, url) -> str:
        music_ids = re.findall('music.163.com/song/(\\d+)/', url)
        if music_ids:
            mid = music_ids[0]
            return mid
        else:
            return ''