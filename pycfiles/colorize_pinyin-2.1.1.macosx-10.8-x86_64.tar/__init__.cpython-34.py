# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/site-packages/colorize_pinyin/__init__.py
# Compiled at: 2016-01-24 00:37:43
# Size of source mod 2**32: 16943 bytes
"""
search for chinese pinyin and wrap it with HTML.

colorize pinyin
===============

search for chinese pinyin and wrap it with HTML.

module provides some useful functions for working with Chinese pinyin,
"phonetic system for transcribing the Mandarin pronunciations of
Chinese characters into the Latin alphabet" (c) `wikipedia <https://en.wikipedia.org/wiki/Pinyin>`_
.

usage sample
============

    >>> colorized_HTML_string_from_string('nǐ hǎo')
    '<span class="pinYinWrapper"><span class="t3">nǐ</span> <span class="t3">hǎo</span></span>'

    >>> ranges_of_pinyin_in_string('nǐ hǎo')
    [Range(location=0, length=2), Range(location=3, length=3)]  # == [(0, 2), (3, 3)]

requirements
============

``lxml`` is only required if you want to work with DOM.  but it does not listed in requirements because if you want to use them, surely you already have ``lxml`` on the board; for other cases we don't need additional third-party libs.

functions that designed to work with ``lxml`` marked with ``[*]``.

functions
=========

modify given DOM by replacing children text nodes containing pinyin with
wrapper element:

``colorize_DOM`` ``[*]``

undo colorize:

``uncolorize_DOM`` ``[*]``

detect and wrap pinyin with HTML in plain text string:

``colorized_HTML_string_from_string``

do the same, but returns a wrapper -- DOM element:

``colorized_HTML_element_from_string`` ``[*]``

searching for pinyin in string of text:

``ranges_of_pinyin_in_string``

finding out what tone has some pinyin word:

``determine_tone``

remove tones (diacritics) from pinyin string:

``lowercase_string_by_removing_pinyin_tones``

constants
=========

``PINYIN_LIST`` -- specially sorted list of all possible pinyin words.

``PINYIN_LIST_BY_LEN`` -- same as ``PINYIN_LIST`` but grouped by len descending.

``PINYIN_WRAPPER_CLASS`` -- default class used by ``[un]colorize_DOM``.

classes
=======

``Range`` -- 2-named-tuple with ``[0]`` location and ``[1]`` length.
"""
from collections import namedtuple
from .__main__ import main
__all__ = [
 'Range',
 'ignore_links_node_filter',
 'colorize_DOM',
 'uncolorize_DOM',
 'colorized_HTML_string_from_string',
 'colorized_HTML_element_from_string',
 'ranges_of_pinyin_in_string',
 'determine_tone',
 'lowercase_string_by_removing_pinyin_tones',
 'PINYIN_LIST',
 'PINYIN_WRAPPER_CLASS',
 'TONES_CLASSES',
 'main']
__version__ = '2.1.1'
try:
    unicode
except NameError:
    u = utf = lambda s: s
else:
    from itertools import imap as map
    u = --- This code section failed: ---

 L. 112         0  LOAD_GLOBAL              isinstance
                3  LOAD_FAST                's'
                6  LOAD_GLOBAL              unicode
                9  CALL_FUNCTION_2       2  '2 positional, 0 named'
               12  POP_JUMP_IF_FALSE    19  'to 19'
               15  LOAD_FAST                's'
               18  RETURN_END_IF_LAMBDA
             19_0  COME_FROM            12  '12'
               19  LOAD_GLOBAL              str
               22  LOAD_FAST                's'
               25  CALL_FUNCTION_1       1  '1 positional, 0 named'
               28  LOAD_ATTR                decode
               31  LOAD_STR                 'utf8'
               34  CALL_FUNCTION_1       1  '1 positional, 0 named'
               37  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
    utf = --- This code section failed: ---

 L. 113         0  LOAD_GLOBAL              isinstance
                3  LOAD_FAST                's'
                6  LOAD_GLOBAL              unicode
                9  CALL_FUNCTION_2       2  '2 positional, 0 named'
               12  POP_JUMP_IF_FALSE    28  'to 28'
               15  LOAD_FAST                's'
               18  LOAD_ATTR                encode
               21  LOAD_STR                 'utf8'
               24  CALL_FUNCTION_1       1  '1 positional, 0 named'
               27  RETURN_END_IF_LAMBDA
             28_0  COME_FROM            12  '12'
               28  LOAD_GLOBAL              str
               31  LOAD_FAST                's'
               34  CALL_FUNCTION_1       1  '1 positional, 0 named'
               37  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
PINYIN_LIST_BY_LEN = ((6, 'zhuang,shuang,chuang'.split(',')),
 (
  5, 'zhuan,zhuai,zhong,zheng,zhang,xiong,xiang,shuan,shuai,sheng,shang,qiong,qiang,niang,liang,kuang,jiong,jiang,huang,guang,chuan,chuai,chong,cheng,chang'.split(',')),
 (
  4, 'zuan,zong,zhuo,zhun,zhui,zhua,zhou,zhen,zhei,zhao,zhan,zhai,zeng,zang,yuan,yong,ying,yang,xuan,xing,xiao,xian,weng,wang,tuan,tong,ting,tiao,tian,teng,tang,suan,song,shuo,shun,shui,shua,shou,shen,shei,shao,shan,shai,seng,sang,ruan,rong,reng,rang,quan,qing,qiao,qian,ping,piao,pian,peng,pang,nüe,nuan,nong,ning,niao,nian,neng,nang,ming,miao,mian,meng,mang,lüe,luan,long,ling,liao,lian,leng,lang,kuan,kuai,kong,keng,kang,juan,jing,jiao,jian,huan,huai,hong,heng,hang,guan,guai,gong,geng,gang,feng,fang,duan,dong,ding,diao,dian,deng,dang,cuan,cong,chuo,chun,chui,chua,chou,chen,chao,chan,chai,ceng,cang,bing,biao,bian,beng,bang'.split(',')),
 (
  3, 'zuo,zun,zui,zou,zhu,zhi,zhe,zha,zen,zei,zao,zan,zai,yun,yue,you,yin,yao,yan,xun,xue,xiu,xin,xie,xia,wen,wei,wan,wai,tuo,tun,tui,tou,tie,tao,tan,tai,suo,sun,sui,sou,shu,shi,she,sha,sen,sei,sao,san,sai,ruo,run,rui,rua,rou,ren,rao,ran,qun,que,qiu,qin,qie,qia,pou,pin,pie,pen,pei,pao,pan,pai,nü,nuo,nou,niu,nin,nie,nen,nei,nao,nan,nai,mou,miu,min,mie,men,mei,mao,man,mai,lü,luo,lun,lou,liu,lin,lie,lia,lei,lao,lan,lai,kuo,kun,kui,kua,kou,ken,kei,kao,kan,kai,jun,jue,jiu,jin,jie,jia,huo,hun,hui,hua,hou,hen,hei,hao,han,hai,guo,gun,gui,gua,gou,gen,gei,gao,gan,gai,fou,fen,fei,fan,duo,dun,dui,dou,diu,die,dia,den,dei,dao,dan,dai,cuo,cun,cui,cou,chu,chi,che,cha,cen,cao,can,cai,bin,bie,ben,bei,bao,ban,bai,ang'.split(',')),
 (
  2, 'zu,zi,ze,za,yu,yo,yi,ye,ya,xu,xi,wu,wo,wa,tu,ti,te,ta,su,si,se,sa,ru,ri,re,qu,qi,pu,po,pi,pa,ou,nu,ni,ng,ne,na,mu,mo,mi,me,ma,lu,li,le,la,ku,ke,ka,ju,ji,hu,he,ha,gu,ge,ga,fu,fo,fa,er,en,ei,du,di,de,da,cu,ci,ce,ca,bu,bo,bi,ba,ao,an,ai'.split(',')),
 (
  1, 'o,n,m,e,a,r'.split(',')))
PINYIN_LIST = []
for _, l in PINYIN_LIST_BY_LEN:
    PINYIN_LIST.extend(l)

del _
del l
PINYIN_WRAPPER_CLASS = 'pinYinWrapper'
TONES_CLASSES = ('t0', 't1', 't2', 't3', 't4')

def ignore_links_node_filter(node):
    """ignore_links_node_filter(node) --> False if node's tag is 'a'."""
    return node.tag.lower() != 'a'


def colorize_DOM(root_node, node_filter=ignore_links_node_filter, pinyin_wrapper_class=PINYIN_WRAPPER_CLASS, tones_classes=TONES_CLASSES):
    """colorize_DOM(root_node, node_filter, pinyin_wrapper_class, tones_classes) --> None

    modify given DOM in place.  using ``etree``.
    detect and colorize pinyin in text nodes of *root_node* and its
    child nodes ignoring nodes for which *node_filter* returns False.
    text nodes will be replaced with <span> wrapper whose class
    attribute is *pinyin_wrapper_class*.
    wrapper will contain only text nodes and <span>s with one of
    *tones_classes* accordingly to the tone of containing pinyin.

    parameters:
        root_node -- instance of ``etree``.
        node_filter -- callable.
            parameters:
                node -- instance of ``etree``.
            return value:
                True to allow function to look up for pinyin inside
                node itself or its child nodes, otherwise False.
                its useful to deny colorizing of <a> or other elements
                that should have their own colors by design.
        pinyin_wrapper_class -- class for wrapper <span>
        tones_classes -- 5-tuple of class names for <span> inside
            wrapper.  element with index [0] will be used for zero
            tone, [1] for first and so on.

    return value:
        None
    """
    if node_filter is None:
        node_filter = lambda : True
    count = 1
    for i, child in enumerate(list(root_node)):
        if node_filter(child):
            colorize_DOM(child, node_filter, pinyin_wrapper_class, tones_classes)
        if child.tail:
            elem = colorized_HTML_element_from_string(child.tail, pinyin_wrapper_class, tones_classes)
            if elem is not None:
                child.tail = None
                root_node.insert(i + count, elem)
                count += 1
            else:
                continue

    if root_node.text:
        elem = colorized_HTML_element_from_string(root_node.text, pinyin_wrapper_class, tones_classes)
        if elem is not None:
            root_node.text = None
            root_node.insert(0, elem)


def uncolorize_DOM(root_node, pinyin_wrapper_class=PINYIN_WRAPPER_CLASS):
    """uncolorize_DOM(root_node, pinyin_wrapper_class) --> None

    opposite to ``colorize_DOM``.  replace back wrappers (nodes with
    class equal to *pinyin_wrapper_class*) with contained text.
    """
    for child in root_node:
        if child.get('class') == pinyin_wrapper_class:
            inner_text = ''.join(child.itertext())
            previous = child.getprevious()
            before = previous.tail if previous is not None and previous.tail else ''
            after = child.tail if child.tail else ''
            new_txt = before + inner_text + after
            if previous is not None:
                previous.tail = new_txt
            else:
                root_node.text = new_txt
            root_node.remove(child)
        else:
            uncolorize_DOM(child, pinyin_wrapper_class)


def colorized_HTML_string_from_string(string, pinyin_wrapper_class=PINYIN_WRAPPER_CLASS, tones_classes=TONES_CLASSES):
    """colorized_HTML_string_from_string(string[, pinyin_wrapper_class][, tones_classes]) --> unicode

    detect and wrap pinyin with HTML in plain text *string*.  if no
    pinyin found, string won't be modified and no wrapper applied.

    return value:
        string represents one HTML element <span> whose class is
        *pinyin_wrapper_class*.  it contains child text nodes and
        inner <span>s with classes set according to contained pinyin
        tone.  these classes can be specified by *tone_classes*
        argument.
        returns None if no pinyin found or all tones are zero.
    """
    string = u(string)
    ranges = ranges_of_pinyin_in_string(string)
    if not ranges:
        return
    pinyin_wrapper_class = u(pinyin_wrapper_class)
    tones_classes = (u(tones_classes[0]), u(tones_classes[1]),
     u(tones_classes[2]), u(tones_classes[3]),
     u(tones_classes[4]))
    words = list(map(lambda r: r._slice(string), ranges))
    tones = list(map(determine_tone, words))
    if not any(tones):
        return
    prev_end = 0
    result = '<span class="%s">' % pinyin_wrapper_class
    for range, word, tone in zip(ranges, words, tones):
        result += string[prev_end:range.location]
        result += '<span class="{}">{}</span>'.format(tones_classes[tone], word)
        prev_end = range.location + range.length

    result += string[prev_end:] + '</span>'
    return result


def colorized_HTML_element_from_string(string, pinyin_wrapper_class=PINYIN_WRAPPER_CLASS, tones_classes=TONES_CLASSES):
    """colorized_HTML_element_from_string(string[, pinyin_wrapper_class][, tones_classes]) --> etree.Element or *string*

    same as ``colorized_HTML_string_from_string``, but returns an
    ``etree.Element`` or None.
    """
    string = u(string)
    ranges = ranges_of_pinyin_in_string(string)
    if not ranges:
        return
    pinyin_wrapper_class = u(pinyin_wrapper_class)
    tones_classes = (u(tones_classes[0]), u(tones_classes[1]),
     u(tones_classes[2]), u(tones_classes[3]),
     u(tones_classes[4]))
    words = list(map(lambda r: r._slice(string), ranges))
    tones = list(map(determine_tone, words))
    if not any(tones):
        return
    import lxml.etree as ET
    wrapper = ET.Element('span')
    wrapper.set('class', pinyin_wrapper_class)
    wrapper.text = string[:ranges[0].location]
    for i, range in enumerate(ranges):
        word = range._slice(string)
        span = ET.SubElement(wrapper, 'span')
        span.set('class', tones_classes[determine_tone(word)])
        span.text = word
        if len(ranges) > i + 1:
            span.tail = string[range.location + range.length:ranges[(i + 1)].location]
            continue

    span.tail = string[range.location + range.length:]
    return wrapper


_diacritics = (('āáǎăà', 'a'), ('ēéěè', 'e'), ('ōóǒò', 'o'), ('ūúǔùǖǘǚǜ', 'u'), ('īíǐì', 'i'))

def lowercase_string_by_removing_pinyin_tones(s):
    """lowercase_string_by_removing_pinyin_tones(string) --> unicode

    simplify / plainize chinese pinyin by converting it to lower case and
    removing diacritics from letters 'a', 'e', 'o', 'u', i'.
    """
    s = u(s).lower()
    for diacrs, normal in _diacritics:
        for diacr in diacrs:
            s = s.replace(diacr, normal)

    return s


_t1 = 'āēūǖīō'
_t2 = 'áéúǘíó'
_t3 = 'ǎăěǔǚǐǒ'
_t4 = 'àèùǜìò'

def determine_tone(pinyin):
    """determine_tone(string) --> {0..4}

    detect tone of given pinyin word.
    return value:
        int from 0 up to 4, where 0 means that tone undetermined.
    """
    pinyin = u(pinyin).lower()
    for letter in pinyin:
        if letter in _t1:
            return 1
        if letter in _t2:
            return 2
        if letter in _t3:
            return 3
        if letter in _t4:
            return 4

    return 0


Range = namedtuple('Range', ('location', 'length'))

def _slice(self, obj):
    return obj[self.location:self.location + self.length]


Range._slice = _slice

def ranges_of_pinyin_in_string(s):
    """ranges_of_pinyin_in_string(string) --> list<Range>

    searches for pinyin in given string *s*.  *s* must be either
    unicode string or utf-8 encoded ``str``, or anything else that
    can be converted by ``u`` function.

    return value:
        list of ranges of pinyin,
        where ``Range`` is 2-namedtuple of (location, length).
        list can be empty.
    """
    result = []
    plain_s = lowercase_string_by_removing_pinyin_tones(s).replace('v', ' ')
    plain_s_len = len(plain_s)
    char_p = 0
    while char_p < plain_s_len:
        if not plain_s[char_p].islower():
            char_p += 1
            continue
        for word_len, words in PINYIN_LIST_BY_LEN:
            word = plain_s[char_p:char_p + word_len]
            if word in words:
                after_word = char_p + word_len
                if word_len > 1:
                    if after_word + 1 < plain_s_len:
                        if plain_s[after_word] in 'aoeiu':
                            shorten_word = word[:-1]
                            if shorten_word in PINYIN_LIST_BY_LEN[(7 - word_len)][1]:
                                if plain_s[after_word] in 'iu':
                                    word = shorten_word
                                    word_len = len(word)
                                else:
                                    for wl, ws in PINYIN_LIST_BY_LEN:
                                        next_w = plain_s[after_word - 1:after_word - 1 + wl]
                                        if next_w in ws:
                                            word = shorten_word
                                            word_len = len(word)
                                            break

                        break
        else:
            while char_p < plain_s_len and not plain_s[char_p].isspace():
                char_p += 1

            while char_p < plain_s_len and plain_s[char_p].isspace():
                char_p += 1

            word = None

        if word:
            result.append(Range(char_p, word_len))
            char_p += word_len
            continue

    return result