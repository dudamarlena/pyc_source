# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/babigo/main.py
# Compiled at: 2012-06-15 23:37:06
import os, os.path, urllib, httplib2, ConfigParser as configparser
from BeautifulSoup import BeautifulStoneSoup

class BabigoException(Exception):
    """ Babigo Exception Class
    """
    pass


class Babigo(object):
    """ Babigo: Babigo Translate Class
    """

    def __init__(self, appid=None, cache=None):
        super(Babigo, self).__init__()
        self.cache = None
        self._read_rcfile()
        if appid is not None:
            self.appid = appid
        if cache is not None:
            self.cache = cache
        return

    def _read_rcfile(self):
        """ read $HOME/.babigorc
        """
        homedir = os.getenv('HOME')
        rcfile = homedir + os.path.sep + '.babigorc'
        con = configparser.SafeConfigParser(allow_no_value=True)
        if os.path.exists(rcfile):
            con.read(rcfile)
            self.appid = con.get('SETTINGS', 'appid')
            self.cache = con.get('SETTINGS', 'cache')

    def translate(self, sentence):
        """ translate your sentence to babigo sentence

        Arguments:
        - `self`:
        - `sentence`:
        """
        h = httplib2.Http(self.cache)
        params = {'results': 'ma,uniq', 
           'uniq_filter': '9|10', 
           'sentence': sentence.encode('utf-8')}
        query = urllib.urlencode(params)
        headers = {'Host': 'jlp.yahooapis.jp', 
           'User-Agent': 'Yahoo AppID: %s' % self.appid, 
           'Content-Type': 'application/x-www-form-urlencoded', 
           'Content-Length': '%d' % len(query)}
        entry_point = 'http://jlp.yahooapis.jp/MAService/V1/parse'
        res, content = h.request(entry_point, 'POST', query, headers=headers)
        if res['status'] == '200':
            psss

    def translate_sentence2babigo(self, sentence):
        try:
            assert isinstance(sentence, unicode)
            kana_sentence = self.get_kana_sentence(sentence)
            if kana_sentence:
                babi_sentence = self._insert_babi(kana_sentence)
                return babi_sentence
            return False
        except Exception as e:
            raise BabigoException(e)

    def get_kana_sentence(self, sentence):
        """ translate your sentence to babigo sentence
            optional feature
        Arguments:
        - `self`:
        - `sentence`: traslate target sentence
        """
        h = httplib2.Http(self.cache)
        sentence = dict(sentence=sentence.encode('utf-8'))
        query = urllib.urlencode(sentence)
        headers = {'Host': 'jlp.yahooapis.jp', 
           'User-Agent': 'Yahoo AppID: %s' % self.appid, 
           'Content-Type': 'application/x-www-form-urlencoded', 
           'Content-Length': '%d' % len(query)}
        entry_point = 'http://jlp.yahooapis.jp/FuriganaService/V1/furigana'
        res, content = h.request(entry_point, 'POST', query, headers=headers)
        if res['status'] == '200':
            return self._concat_sentence(content)
        else:
            return False

    def _concat_sentence(self, content):
        """ concat sentence from web api

        Arguments:
        - `content`: Web API Response , format:XML
        """
        soup = BeautifulStoneSoup(content)
        wlist = soup.find('wordlist')
        sentence = ''
        for word in wlist.findAll('word'):
            if word.find('furigana'):
                sentence += word.find('furigana').getText()
            elif word.find('surface'):
                sentence += word.find('surface').getText()

        return sentence

    def _insert_babi(self, sentence):
        """ insert into  babigo into sentence

        Arguments:
        - `self`:
        - `sentence`:
        """
        assert isinstance(sentence, unicode)
        kana = [
         'あかさたなはまやらわがざだばぱ',
         'いきしちにひみりぎじぢびぴ',
         'うくすつぬふむゆるぐずづぶぷ',
         'えけせてねへめれげげぜでべぺ',
         'おこそとのほもよろをごぞどぼぽ']
        mother_a = [ x for x in kana[0] ]
        mother_i = [ x for x in kana[1] ]
        mother_u = [ x for x in kana[2] ]
        mother_e = [ x for x in kana[3] ]
        mother_o = [ x for x in kana[4] ]
        result = ''
        for c in sentence:
            if c in mother_a:
                result += c + 'ば'
            elif c in mother_i:
                result += c + 'び'
            elif c in mother_u:
                result += c + 'ぶ'
            elif c in mother_e:
                result += c + 'べ'
            elif c in mother_o:
                result += c + 'ぼ'
            else:
                result += c

        return result