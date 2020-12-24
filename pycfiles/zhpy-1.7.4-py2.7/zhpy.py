# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\zhpy\zhpy.py
# Compiled at: 2015-10-22 21:48:08
"""Transform zhpy source to python source

zhpy is the python language with chinese native keywords, variables, and
parameters support, independent on python's version.

zhpy's core function is a convertor/pre-processor to translate chinese
python code to nature python code (english) and vice versa.

zhpy is motivated by HYRY's origin code.

gasolin+zhpy@gmail.com

This is the MIT license:
http://www.opensource.org/licenses/mit-license.php

Copyright (c) 2007~ Fred Lin and contributors. zhpy is a trademark of Fred Lin.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
from zhdc import worddict, twdict, cndict
supported_dicts = [
 (
  'plugtw', twdict),
 (
  'plugcn', cndict)]

def merger(anno_dict, use_dict=worddict, verbose=True, reverse=False):
    u"""
    merge extra bindings into worddict

Accept args:
    anno_dict:
        source dict
    use_dict:
        target dict to be merged, default: 'worddict'
    verbose:
        show detail message, default: True

    merger could accept list input:

    >>> keys = [('遊戲', 'pygame'), ('螢幕', 'screen')]
    >>> merger(keys)
    add 遊戲=pygame
    add 螢幕=screen
    >>> '遊戲' in worddict
    True

    merger could accept dict input:

    >>> keydic = {'作業系統':'os', '分支':'fork'}
    >>> merger(keydic)
    add 分支=fork
    add 作業系統=os
    >>> '作業系統' in worddict
    True
    """
    if isinstance(anno_dict, dict):
        data_iter = anno_dict.iteritems()
    else:
        data_iter = anno_dict
    if reverse:
        rev_iter = []
        for k, v in data_iter:
            rev_iter.append((v, k))

        data_iter = rev_iter
    for k, v in data_iter:
        if k not in use_dict:
            use_dict[k] = v
            if verbose:
                print 'add %s=%s' % (k, v)
        elif verbose:
            print 'already has key: %s, %s' % (k, v)


import os, ConfigParser

def _ini_annotator(verbose=True, force=False):
    """
    find ini files and use keywords defined in ini during
    convertion progress.

Accept args:
    verbose:
        show detail message, default: True

    """
    if not force and getattr(_ini_annotator, 'already', False):
        return
    _ini_annotator.already = True
    inifiles = []
    for x in os.listdir('.'):
        if x.endswith('.ini'):
            inifiles.append(x)

    for f in inifiles:
        if verbose:
            print 'file', f
        conf = ConfigParser.ConfigParser()
        try:
            conf.read(f)
            for sect in conf.sections():
                if verbose:
                    print 'sect:', sect
                merger(conf.items(sect))

        except:
            print '!%s is not a valid keyword file' % f


def _py_annotator(verbose=False, force=False):
    """
    find python keyword plugins and update to dicts

Accept args:
    verbose:
        show detail message, default: False

    'verbose' argument is only for debug(will generate too mush messages).
    """
    if not force and getattr(_py_annotator, 'already', False):
        return
    _py_annotator.already = True
    has_annotator = False
    for plugin, use_dict in supported_dicts:
        try:
            load_dict = __import__(plugin, globals(), locals(), ['tools'])
            for tool in load_dict.tools:
                if verbose:
                    print tool.title
                merger(tool.keyword, use_dict=use_dict, verbose=verbose)

            merger(use_dict, verbose=verbose)
            has_annotator = True
        except ImportError as e:
            if verbose:
                print 'import plug%s error' % plugin, e

    if not has_annotator:
        raise ReferenceError('no plugin was referenced in annotator')


_py_annotator.__loaded = False

def annotator(verbose=True, force=False):
    """
    provide two ways to expand the worddict:

      1. ini files

      2. python plugin system.

Accept args:
    verbose:
        show detail message, default: True

    """
    _ini_annotator(verbose, force)
    _py_annotator(False, force)


def zh_ord(tmp):
    ur"""
    convert chinese variable to pseudo hex identifer

    >>> '範例'.decode("utf8")
    u'\u7bc4\u4f8b'
    >>> s = '範例'.decode("utf8")
    >>> zh_ord(s)
    'p_7bc4_4f8b_v'
    """
    word_list = []
    for i in tmp:
        ori = str(hex(ord(i)))[2:]
        word_list.append(ori)

    return 'p_' + ('_').join(word_list) + '_v'


variable_to_number = zh_ord
from pyparsing import srange, Word, quotedString, pythonStyleComment, QuotedString

def convertToEnglish(s, l, t):
    """search worddict to match keywords

    if not in keyword, replace the chinese variable/argument/
    function name/class name/method name to a variable with prefix 'p'
    """
    tmp = t[0].encode('utf8')
    if tmp in worddict:
        word = worddict[tmp].decode('utf8')
    else:
        word = zh_ord(t[0])
    return word


chineseChars = srange('[\\0x0080-\\0xfe00]')
chineseWord = Word(chineseChars)
chineseWord.setParseAction(convertToEnglish)
tripleQuote = QuotedString('"""', multiline=True, unquoteResults=False) | QuotedString("'''", multiline=True, unquoteResults=False)
pythonWord = tripleQuote | quotedString | pythonStyleComment | chineseWord
try:
    import chardet
    has_chardet = True
except:
    has_chardet = False
    print 'chardet module is not installed'

def convertor(text, verbose=False, encoding='', outcoding=''):
    u"""
    convert zhpy source (Chinese) to Python Source.

    annotator will be called automatically.

Accept args:
    test:
        source to be converted
    verbose:
        show detail message, default: False
    encoding:
        codec for encoding
    outcoding:
        codec for output encoding

    #annotator()
    >>> convertor("印出 'hello'")
    "print 'hello'"

    >>> convertor("印出 'hello'", encoding="utf8")
    "print 'hello'"

    >>> convertor('測試_範例')
    'test_p_7bc4_4f8b_v'

    more keyword test cases are in /tests folder.
    """
    annotator(force=False)
    if encoding and encoding.lower() != 'utf-8':
        utext = text.decode(encoding)
    elif has_chardet:
        try:
            det = chardet.detect(text)
            if verbose:
                print 'chardet', det
            if det['confidence'] >= 0.8:
                encoding = chardet.detect(text)['encoding']
            else:
                if verbose:
                    print 'low confidence encoding detection,\n                                use utf8 encoding'
                encoding = 'utf8'
            if isinstance(text, unicode):
                utext = text
            else:
                utext = text.decode(encoding)
        except UnicodeDecodeError as e:
            print "can't recognize your language,                         set to sys.stdout.encoding"
            utext = text.decode('utf8')
        except ImportError as e:
            if verbose:
                print 'proceed no chardet mode'
            utext = text.decode('utf8')

    else:
        utext = text
    result = pythonWord.transformString(utext)
    if outcoding:
        return result.encode(outcoding)
    else:
        if isinstance(text, unicode):
            return result
        if encoding:
            return result.encode(encoding)
        return result


import sys
has_zhtraceback = None
try:
    import traceback
    from pyzh import python_convertor, rev_annotator
    has_zhtraceback = True
except:
    print 'not support chinese traceback'
    has_zhtraceback = None

def try_run(result, global_ns={}, local_ns={}, verbose=True, zhtrace=True):
    """
    execute result and catch exceptions in specified namespace

Accept args:
    result:
        the converted source to be executed
    global_ns:
        Global namespace, deafult is {}
    local_ns:
        Local namespace, default is: {}

    >>> global_ns = {'x':'g'}
    >>> local_ns = {'x':'l'}
    >>> global_ns.update( {"__name__": "__main__", "__doc__": None})
    >>> try_run("print 'hello'", {}, {})
    hello
    >>> try_run("print x", global_ns, local_ns)
    l
    >>> try_run("print x", global_ns)
    g
    """
    try:
        sys.path.insert(0, '')
        exec result in global_ns, local_ns
    except Exception as e:
        if has_zhtraceback and zhtrace:
            display = os.getenv('LANG')
            if display == None:
                lang = None
            elif 'zh_TW' in display:
                lang = 'tw'
            elif 'zh_CN' in display:
                lang = 'cn'
            else:
                lang = None
            stack = traceback.format_exc()
            if lang:
                rev_annotator(lang)
                print python_convertor(stack, lang, traceback=True).decode('utf-8')
            else:
                print stack
        else:
            if verbose:
                print result
            print e

    return


def zh_exec(content, global_ns={'__name__': '__main__', '__doc__': None}, local_ns={}, outcoding=''):
    u"""
    the zhpy exec

Accept args:
    content:
        the source to be converted and executed with zhpy in specified
        namespace
    global_ns:
        Global namespace, deafult is {"__name__": "__main__", "__doc__": None}
    local_ns:
        Local namespace, default is: {}

    >>> zh_exec("印出 'hello'")
    hello
    """
    result = convertor(content, outcoding=outcoding)
    if local_ns == {}:
        local_ns = global_ns
    try_run(result, global_ns, local_ns)