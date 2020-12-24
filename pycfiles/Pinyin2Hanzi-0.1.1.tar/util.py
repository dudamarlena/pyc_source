# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../../Pinyin2Hanzi/util.py
# Compiled at: 2016-02-07 22:15:55
from __future__ import print_function, unicode_literals, absolute_import
import os, sys
try:
    reload(sys)
    sys.setdefaultencoding(b'utf-8')
except:
    pass

PY2 = sys.version_info[0] == 2
if not PY2:
    xrange = range

    def as_text(v):
        if v is None:
            return
        else:
            if isinstance(v, bytes):
                return v.decode(b'utf-8', errors=b'ignore')
            if isinstance(v, str):
                return v
            raise ValueError(b'Unknown type %r' % type(v))
            return


    def is_text(v):
        return isinstance(v, str)


else:
    xrange = xrange

    def as_text(v):
        if v is None:
            return
        else:
            if isinstance(v, unicode):
                return v
            if isinstance(v, str):
                return v.decode(b'utf-8', errors=b'ignore')
            raise ValueError(b'Invalid type %r' % type(v))
            return


    def is_text(v):
        return isinstance(v, unicode)


def is_chinese(v):
    if is_text(v):
        if len(v) == 0:
            return False
        return all(b'一' <= c <= b'\u9fff' or c == b'〇' for c in v)
    raise ValueError(b'Invalid type %r' % type(v))


def current_dir():
    return os.path.dirname(os.path.realpath(__file__))


__removetone_dict = {b'ā': b'a', 
   b'á': b'a', 
   b'ǎ': b'a', 
   b'à': b'a', 
   b'ē': b'e', 
   b'é': b'e', 
   b'ě': b'e', 
   b'è': b'e', 
   b'ī': b'i', 
   b'í': b'i', 
   b'ǐ': b'i', 
   b'ì': b'i', 
   b'ō': b'o', 
   b'ó': b'o', 
   b'ǒ': b'o', 
   b'ò': b'o', 
   b'ū': b'u', 
   b'ú': b'u', 
   b'ǔ': b'u', 
   b'ù': b'u', 
   b'ü': b'v', 
   b'ǖ': b'v', 
   b'ǘ': b'v', 
   b'ǚ': b'v', 
   b'ǜ': b'v', 
   b'ń': b'n', 
   b'ň': b'n', 
   b'\ue7c7': b'm'}

def remove_tone(one_py):
    u""" 删除拼音中的音调
    lǔ -> lu
    """
    one_py = as_text(one_py)
    r = as_text(b'')
    for c in one_py:
        if c in __removetone_dict:
            r += __removetone_dict[c]
        else:
            r += c

    return r


def normlize_pinyin(one_py):
    u""" 规范化
    ue -> ve
    """
    if b'ue' in one_py:
        return one_py.replace(b'ue', b've')
    if b'ng' == one_py:
        return b'en'
    return one_py


def simplify_pinyin(one_py):
    return normlize_pinyin(remove_tone(one_py.lower()))


__pinyin = set([b'gu', b'qiao', b'qian', b'qve', b'ge', b'gang', b'ga', b'lian', b'liao', b'rou', b'zong',
 b'tu', b'seng', b'yve', b'ti', b'te', b'jve', b'ta', b'nong', b'zhang', b'fan', b'ma', b'gua', b'die', b'gui',
 b'guo', b'gun', b'sang', b'diu', b'zi', b'ze', b'za', b'chen', b'zu', b'ba', b'dian', b'diao', b'nei', b'suo',
 b'sun', b'zhao', b'sui', b'kuo', b'kun', b'kui', b'cao', b'zuan', b'kua', b'den', b'lei', b'neng', b'men',
 b'mei', b'tiao', b'geng', b'chang', b'cha', b'che', b'fen', b'chi', b'fei', b'chu', b'shui', b'me', b'tuan',
 b'mo', b'mi', b'mu', b'dei', b'cai', b'zhan', b'zhai', b'can', b'ning', b'wang', b'pie', b'beng', b'zhuang',
 b'tan', b'tao', b'tai', b'song', b'ping', b'hou', b'cuan', b'lan', b'lao', b'fu', b'fa', b'jiong', b'mai',
 b'xiang', b'mao', b'man', b'a', b'jiang', b'zun', b'bing', b'su', b'si', b'sa', b'se', b'ding', b'xuan',
 b'zei', b'zen', b'kong', b'pang', b'jie', b'jia', b'jin', b'lo', b'lai', b'li', b'peng', b'jiu', b'yi', b'yo',
 b'ya', b'cen', b'dan', b'dao', b'ye', b'dai', b'zhen', b'bang', b'nou', b'yu', b'weng', b'en', b'ei', b'kang',
 b'dia', b'er', b'ru', b'keng', b're', b'ren', b'gou', b'ri', b'tian', b'qi', b'shua', b'shun', b'shuo', b'qun',
 b'yun', b'xun', b'fiao', b'zan', b'zao', b'rang', b'xi', b'yong', b'zai', b'guan', b'guai', b'dong', b'kuai',
 b'ying', b'kuan', b'xu', b'xia', b'xie', b'yin', b'rong', b'xin', b'tou', b'nian', b'niao', b'xiu', b'fo',
 b'kou', b'niang', b'hua', b'hun', b'huo', b'hui', b'shuan', b'quan', b'shuai', b'chong', b'bei', b'ben',
 b'kuang', b'dang', b'sai', b'ang', b'sao', b'san', b'reng', b'ran', b'rao', b'ming', b'null', b'lie', b'lia',
 b'min', b'pa', b'lin', b'mian', b'mie', b'liu', b'zou', b'miu', b'nen', b'kai', b'kao', b'kan', b'ka', b'ke',
 b'yang', b'ku', b'deng', b'dou', b'shou', b'chuang', b'nang', b'feng', b'meng', b'cheng', b'di', b'de', b'da',
 b'bao', b'gei', b'du', b'gen', b'qu', b'shu', b'sha', b'she', b'ban', b'shi', b'bai', b'nun', b'nuo', b'sen', b'lve',
 b'kei', b'fang', b'teng', b'xve', b'lun', b'luo', b'ken', b'wa', b'wo', b'ju', b'tui', b'wu', b'le', b'ji', b'huang',
 b'tuo', b'cou', b'la', b'mang', b'ci', b'tun', b'tong', b'ca', b'pou', b'ce', b'gong', b'cu', b'lv', b'dun', b'pu',
 b'ting', b'qie', b'yao', b'lu', b'pi', b'po', b'suan', b'chua', b'chun', b'chan', b'chui', b'gao', b'gan', b'zeng',
 b'gai', b'xiong', b'tang', b'pian', b'piao', b'cang', b'heng', b'xian', b'xiao', b'bian', b'biao', b'zhua', b'duan',
 b'cong', b'zhui', b'zhuo', b'zhun', b'hong', b'shuang', b'juan', b'zhei', b'pai', b'shai', b'shan', b'shao', b'pan',
 b'pao', b'nin', b'hang', b'nie', b'zhuai', b'zhuan', b'yuan', b'niu', b'na', b'miao', b'guang', b'ne', b'hai', b'han',
 b'hao', b'wei', b'wen', b'ruan', b'cuo', b'cun', b'cui', b'bin', b'bie', b'mou', b'nve', b'shen', b'shei', b'fou', b'xing',
 b'qiang', b'nuan', b'pen', b'pei', b'rui', b'run', b'ruo', b'sheng', b'dui', b'bo', b'bi', b'bu', b'chuan', b'qing',
 b'chuai', b'duo', b'o', b'chou', b'ou', b'zui', b'luan', b'zuo', b'jian', b'jiao', b'sou', b'wan', b'jing', b'qiong',
 b'wai', b'long', b'yan', b'liang', b'lou', b'huan', b'hen', b'hei', b'huai', b'shang', b'jun', b'hu', b'ling', b'ha', b'he',
 b'zhu', b'ceng', b'zha', b'zhe', b'zhi', b'qin', b'pin', b'ai', b'chai', b'qia', b'chao', b'ao', b'an', b'qiu', b'ni', b'zhong',
 b'zang', b'nai', b'nan', b'nao', b'chuo', b'tie', b'you', b'nu', b'nv', b'zheng', b'leng', b'zhou', b'lang', b'e'])
__shengmu = set([b'b', b'p', b'm', b'f', b'd', b't', b'n', b'l', b'g', b'k', b'h', b'j', b'q', b'x', b'zh', b'ch', b'sh', b'r', b'z', b'c', b's'])
__single_yunmu = set([b'a', b'o', b'e', b'i', b'u', b'v'])
__complex_yunmu = set([b'ai', b'ei', b'ui', b'ao', b'ou', b'iu', b'ie', b've', b'er', b'an', b'en', b'in', b'un', b'ang', b'eng', b'ing', b'ong'])

def is_pinyin(v):
    return v in __pinyin


def all_pinyin():
    for _ in __pinyin:
        yield _


def is_shengmu(v):
    return v in __shengmu


def is_single_yunmu(v):
    return v in __single_yunmu


def is_complex_yunmu(v):
    return v in __complex_yunmu


def is_yunmu(v):
    return is_single_yunmu(v) or is_complex_yunmu(v)


def get_shengmu(one_py):
    if len(one_py) == 0:
        return
    else:
        if len(one_py) == 1:
            if is_shengmu(one_py):
                return one_py
            else:
                return

        else:
            if is_shengmu(one_py[:2]):
                return one_py[:2]
            else:
                if is_shengmu(one_py[:1]):
                    return one_py[:1]
                return

        return