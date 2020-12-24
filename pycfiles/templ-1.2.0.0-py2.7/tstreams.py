# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\templ\tstreams.py
# Compiled at: 2013-07-26 11:14:51
"""
Copyright 2013 Brian Mearns

This file is part of templ.

templ is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

templ is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with templ.  If not, see <http://www.gnu.org/licenses/>.
"""
import os, filepos as tFilepos, texceptions, abc

class TemplateOutputStream(object):
    """
    A really simple not-quite stream-like object that just supports a write and close
    method.

    I can't really remember why I needed a new class...I think I needed a standard interface
    that I could back with an FD integer, instead of a stream like object. Or something.
    Mostly, I wanted to make sure I wasn't relying on anything other than write and
    maybe close.
    """

    @abc.abstractmethod
    def write(self, data):
        pass

    @abc.abstractmethod
    def close(self):
        pass


class TemplateStreamOutputStream(TemplateOutputStream):

    def __init__(self, stream):
        self.__stream = stream

    def write(self, data):
        try:
            self.__stream.write(data)
        except IOError as e:
            raise texceptions.TemplateIOException(e, None)

        return

    def close(self):
        try:
            self.__stream.close()
        except IOError as e:
            raise texceptions.TemplateIOException(e, None)

        return


class TemplateFDOutputStream(TemplateOutputStream):

    def __init__(self, fd):
        self.__fd = fd

    def write(self, data):
        try:
            os.write(self.__fd, data)
        except OSError as e:
            raise texceptions.TemplateIOException(e, None)

        return

    def close(self):
        try:
            os.close(self.__fd)
        except OSError as e:
            raise texceptions.TemplateIOException(e, None)

        return


class BufferedTemplateOutputStream(TemplateOutputStream):
    """
    Implements the same interface as `TemplateOutputStream`, but isn't backed by a file,
    it just buffers everything that's written.
    """

    def __init__(self):
        self.__buffered = ''

    def write(self, data):
        self.__buffered += data

    def close(self):
        pass

    def str(self):
        return self.__buffered


class TemplateInputStream(object):

    def __init__(self, istream, name=None):
        self.__istream = istream
        self.__name = name
        if name is None:
            self.__name = '<input-stream>'
        self.__linelengths = []
        self.__pos = 0
        self.__buffer = ''
        self.__eoi = False
        return

    def read--- This code section failed: ---

 L. 111         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  '__buffer'
                6  LOAD_FAST             1  'limit'
                9  SLICE+2          
               10  STORE_FAST            2  'data'

 L. 112        13  LOAD_FAST             0  'self'
               16  LOAD_ATTR             0  '__buffer'
               19  LOAD_FAST             1  'limit'
               22  SLICE+1          
               23  LOAD_FAST             0  'self'
               26  STORE_ATTR            0  '__buffer'

 L. 113        29  LOAD_FAST             1  'limit'
               32  LOAD_GLOBAL           1  'len'
               35  LOAD_FAST             2  'data'
               38  CALL_FUNCTION_1       1  None
               41  BINARY_SUBTRACT  
               42  STORE_FAST            3  'remaining'

 L. 114        45  LOAD_FAST             3  'remaining'
               48  LOAD_CONST               0
               51  COMPARE_OP            4  >
               54  POP_JUMP_IF_FALSE   262  'to 262'
               57  LOAD_FAST             0  'self'
               60  LOAD_ATTR             2  '__eoi'
               63  UNARY_NOT        
             64_0  COME_FROM            54  '54'
               64  POP_JUMP_IF_FALSE   262  'to 262'

 L. 115        67  LOAD_GLOBAL           1  'len'
               70  LOAD_FAST             0  'self'
               73  LOAD_ATTR             0  '__buffer'
               76  CALL_FUNCTION_1       1  None
               79  LOAD_CONST               0
               82  COMPARE_OP            2  ==
               85  POP_JUMP_IF_TRUE    106  'to 106'
               88  LOAD_ASSERT              AssertionError
               91  LOAD_GLOBAL           1  'len'
               94  LOAD_FAST             0  'self'
               97  LOAD_ATTR             0  '__buffer'
              100  CALL_FUNCTION_1       1  None
              103  RAISE_VARARGS_2       2  None

 L. 116       106  LOAD_FAST             0  'self'
              109  LOAD_ATTR             4  '__istream'
              112  LOAD_ATTR             5  'readline'
              115  CALL_FUNCTION_0       0  None
              118  LOAD_FAST             0  'self'
              121  STORE_ATTR            0  '__buffer'

 L. 117       124  LOAD_GLOBAL           1  'len'
              127  LOAD_FAST             0  'self'
              130  LOAD_ATTR             0  '__buffer'
              133  CALL_FUNCTION_1       1  None
              136  STORE_FAST            4  'linelength'

 L. 118       139  LOAD_FAST             4  'linelength'
              142  LOAD_CONST               0
              145  COMPARE_OP            2  ==
              148  POP_JUMP_IF_FALSE   163  'to 163'

 L. 119       151  LOAD_GLOBAL           6  'True'
              154  LOAD_FAST             0  'self'
              157  STORE_ATTR            2  '__eoi'
              160  JUMP_ABSOLUTE       262  'to 262'

 L. 121       163  LOAD_GLOBAL           1  'len'
              166  LOAD_FAST             0  'self'
              169  LOAD_ATTR             7  '__linelengths'
              172  CALL_FUNCTION_1       1  None
              175  LOAD_CONST               0
              178  COMPARE_OP            2  ==
              181  POP_JUMP_IF_FALSE   199  'to 199'

 L. 122       184  LOAD_FAST             4  'linelength'
              187  BUILD_LIST_1          1 
              190  LOAD_FAST             0  'self'
              193  STORE_ATTR            7  '__linelengths'
              196  JUMP_FORWARD         27  'to 226'

 L. 124       199  LOAD_FAST             0  'self'
              202  LOAD_ATTR             7  '__linelengths'
              205  LOAD_ATTR             8  'append'
              208  LOAD_FAST             0  'self'
              211  LOAD_ATTR             7  '__linelengths'
              214  LOAD_CONST               -1
              217  BINARY_SUBSCR    
              218  LOAD_FAST             4  'linelength'
              221  BINARY_ADD       
              222  CALL_FUNCTION_1       1  None
              225  POP_TOP          
            226_0  COME_FROM           196  '196'

 L. 126       226  LOAD_FAST             2  'data'
              229  LOAD_FAST             0  'self'
              232  LOAD_ATTR             0  '__buffer'
              235  LOAD_FAST             3  'remaining'
              238  SLICE+2          
              239  INPLACE_ADD      
              240  STORE_FAST            2  'data'

 L. 127       243  LOAD_FAST             0  'self'
              246  LOAD_ATTR             0  '__buffer'
              249  LOAD_FAST             3  'remaining'
              252  SLICE+1          
              253  LOAD_FAST             0  'self'
              256  STORE_ATTR            0  '__buffer'
              259  JUMP_FORWARD          0  'to 262'
            262_0  COME_FROM           259  '259'

 L. 129       262  LOAD_GLOBAL           1  'len'
              265  LOAD_FAST             2  'data'
              268  CALL_FUNCTION_1       1  None
              271  LOAD_FAST             1  'limit'
              274  COMPARE_OP            1  <=
              277  POP_JUMP_IF_TRUE    301  'to 301'
              280  LOAD_ASSERT              AssertionError
              283  LOAD_GLOBAL           1  'len'
              286  LOAD_FAST             2  'data'
              289  CALL_FUNCTION_1       1  None
              292  LOAD_FAST             1  'limit'
              295  BUILD_TUPLE_2         2 
              298  RAISE_VARARGS_2       2  None

 L. 130       301  LOAD_FAST             0  'self'
              304  DUP_TOP          
              305  LOAD_ATTR             9  '__pos'
              308  LOAD_GLOBAL           1  'len'
              311  LOAD_FAST             2  'data'
              314  CALL_FUNCTION_1       1  None
              317  INPLACE_ADD      
              318  ROT_TWO          
              319  STORE_ATTR            9  '__pos'

 L. 131       322  LOAD_FAST             2  'data'
              325  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 325

    def unget(self, string):
        self.__pos -= len(string)
        self.__buffer = string + self.__buffer

    def tell(self):
        return self.__pos

    def getPosition(self, pos=None):
        if pos is None:
            pos = self.__pos
        lines = len(self.__linelengths)
        i = 0
        for i in xrange(lines):
            if pos < self.__linelengths[i]:
                break

        sol = 0
        if i > 0:
            sol = self.__linelengths[(i - 1)]
        offset = pos - sol
        return tFilepos.Filepos(self.__name, i + 1, offset + 1)