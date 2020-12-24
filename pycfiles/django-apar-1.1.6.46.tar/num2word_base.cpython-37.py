# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/utils/formattings/num2words/num2word_base.py
# Compiled at: 2020-01-05 09:49:45
# Size of source mod 2**32: 11018 bytes
"""
Module: num2word_base.py
Version: 1.0

Author:
   Taro Ogawa (tso@users.sourceforge.org)
   
Copyright:
    Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.

Licence:
    This module is distributed under the Lesser General Public Licence.
    http://www.opensource.org/licenses/lgpl-license.php

History:
    1.1: add to_splitnum() and inflect()
         add to_year() and to_currency() stubs
"""
from .orderedmapping import OrderedMapping

class Num2Word_Base(object):

    def __init__(self):
        self.cards = OrderedMapping()
        self.cards_str = OrderedMapping()
        self.is_title = False
        self.precision = 2
        self.exclude_title = []
        self.negword = '(-) '
        self.pointword = '(.)'
        self.errmsg_nonnum = 'type(%s) not in [long, int, float]'
        self.errmsg_floatord = 'Cannot treat float %s as ordinal.'
        self.errmsg_negord = 'Cannot treat negative num %s as ordinal.'
        self.errmsg_toobig = 'abs(%s) must be less than %s.'
        self.base_setup()
        self.setup()
        self.set_numwords()
        self.set_numwords_str()
        self.MAXVAL = 1000 * self.cards.order[0]

    def set_numwords(self):
        self.set_high_numwords(self.high_numwords)
        self.set_mid_numwords(self.mid_numwords)
        self.set_low_numwords(self.low_numwords)

    def set_numwords_str(self):
        self.set_high_numwords_str(self.high_numwords_str)
        self.set_mid_numwords_str(self.mid_numwords_str)
        self.set_low_numwords_str(self.low_numwords_str)

    def gen_high_numwords(self, units, tens, lows):
        out = [u + t for t in tens for u in units]
        out.reverse()
        return out + lows

    def gen_high_numwords_str(self, units, tens, lows):
        out = [u + t for t in tens for u in units]
        out.reverse()
        return out + lows

    def set_mid_numwords(self, mid):
        for key, val in mid:
            self.cards[key] = val

    def set_mid_numwords_str(self, mid):
        for key, val in mid:
            self.cards_str[key] = val

    def set_low_numwords(self, numwords):
        for word, n in zip(numwords, list(range(len(numwords) - 1, -1, -1))):
            self.cards[n] = word

    def set_low_numwords_str(self, numwords):
        for word, n in zip(numwords, list(range(len(numwords) - 1, -1, -1))):
            self.cards_str[n] = word

    def splitnum(self, value):
        for elem in self.cards:
            if elem > value:
                continue
            else:
                out = []
                if value == 0:
                    div, mod = (1, 0)
                else:
                    div, mod = divmod(value, elem)
            if div == 1 and value >= 1000:
                out.append((str(1), 1))
            else:
                if div == value:
                    return [
                     (
                      div * self.cards[elem], div * elem)]
                if not div > 1000 or div % 10 != 0 or div > 1000:
                    out.append(self.splitnum(div))
                else:
                    pass
            if div != 0:
                if div != 1:
                    out.append((str(div), div))
                elif round(elem / 1000) != 0:
                    out.append((self.cards[elem], elem))
                else:
                    out.append((str(elem), elem))
                if mod >= 1000:
                    if mod % 10 != 0 or mod >= 1000:
                        out.append(self.splitnum(mod))
            elif mod != 0 and mod % 10 == 0:
                out.append((str(mod), mod))
            else:
                if mod != 0:
                    out.append((str(mod), mod))
            return out

    def splitnum_str--- This code section failed: ---

 L. 120       0_2  SETUP_LOOP          362  'to 362'
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                cards_str
                8  GET_ITER         
            10_12  FOR_ITER            360  'to 360'
               14  STORE_FAST               'elem'

 L. 121        16  LOAD_FAST                'elem'
               18  LOAD_FAST                'value'
               20  COMPARE_OP               >
               22  POP_JUMP_IF_FALSE    26  'to 26'

 L. 122        24  CONTINUE             10  'to 10'
             26_0  COME_FROM            22  '22'

 L. 124        26  BUILD_LIST_0          0 
               28  STORE_FAST               'out'

 L. 125        30  LOAD_FAST                'value'
               32  LOAD_CONST               0
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE    48  'to 48'

 L. 126        38  LOAD_CONST               (1, 0)
               40  UNPACK_SEQUENCE_2     2 
               42  STORE_FAST               'div'
               44  STORE_FAST               'mod'
               46  JUMP_FORWARD         62  'to 62'
             48_0  COME_FROM            36  '36'

 L. 128        48  LOAD_GLOBAL              divmod
               50  LOAD_FAST                'value'
               52  LOAD_FAST                'elem'
               54  CALL_FUNCTION_2       2  '2 positional arguments'
               56  UNPACK_SEQUENCE_2     2 
               58  STORE_FAST               'div'
               60  STORE_FAST               'mod'
             62_0  COME_FROM            46  '46'

 L. 130        62  LOAD_FAST                'div'
               64  LOAD_CONST               1
               66  COMPARE_OP               ==
               68  POP_JUMP_IF_FALSE   148  'to 148'

 L. 131        70  LOAD_FAST                'mod'
               72  LOAD_CONST               0
               74  COMPARE_OP               !=
               76  POP_JUMP_IF_FALSE    86  'to 86'
               78  LOAD_FAST                'value'
               80  LOAD_FAST                'elem'
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_TRUE    126  'to 126'
             86_0  COME_FROM            76  '76'
               86  LOAD_FAST                'mod'
               88  LOAD_CONST               1000
               90  COMPARE_OP               >=
               92  POP_JUMP_IF_FALSE   102  'to 102'
               94  LOAD_FAST                'value'
               96  LOAD_FAST                'elem'
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_TRUE    126  'to 126'
            102_0  COME_FROM            92  '92'

 L. 132       102  LOAD_FAST                'value'
              104  LOAD_FAST                'elem'
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_FALSE   254  'to 254'
              110  LOAD_FAST                'value'
              112  LOAD_CONST               1000
              114  COMPARE_OP               >=
              116  POP_JUMP_IF_FALSE   254  'to 254'
              118  LOAD_FAST                'div'
              120  LOAD_CONST               0
              122  COMPARE_OP               >
              124  POP_JUMP_IF_FALSE   254  'to 254'
            126_0  COME_FROM           100  '100'
            126_1  COME_FROM            84  '84'

 L. 133       126  LOAD_FAST                'out'
              128  LOAD_METHOD              append
              130  LOAD_FAST                'self'
              132  LOAD_ATTR                cards_str
              134  LOAD_CONST               1
              136  BINARY_SUBSCR    
              138  LOAD_CONST               1
              140  BUILD_TUPLE_2         2 
              142  CALL_METHOD_1         1  '1 positional argument'
              144  POP_TOP          
              146  JUMP_FORWARD        254  'to 254'
            148_0  COME_FROM            68  '68'

 L. 136       148  LOAD_FAST                'div'
              150  LOAD_FAST                'value'
              152  COMPARE_OP               ==
              154  POP_JUMP_IF_FALSE   180  'to 180'

 L. 137       156  LOAD_FAST                'div'
              158  LOAD_FAST                'self'
              160  LOAD_ATTR                cards_str
              162  LOAD_FAST                'elem'
              164  BINARY_SUBSCR    
              166  BINARY_MULTIPLY  
              168  LOAD_FAST                'div'
              170  LOAD_FAST                'elem'
              172  BINARY_MULTIPLY  
              174  BUILD_TUPLE_2         2 
              176  BUILD_LIST_1          1 
              178  RETURN_VALUE     
            180_0  COME_FROM           154  '154'

 L. 138       180  LOAD_FAST                'div'
              182  LOAD_CONST               20
              184  COMPARE_OP               >
              186  POP_JUMP_IF_FALSE   200  'to 200'
              188  LOAD_FAST                'div'
              190  LOAD_CONST               10
              192  BINARY_MODULO    
              194  LOAD_CONST               0
              196  COMPARE_OP               !=
              198  POP_JUMP_IF_TRUE    208  'to 208'
            200_0  COME_FROM           186  '186'
              200  LOAD_FAST                'div'
              202  LOAD_CONST               20
              204  COMPARE_OP               >
              206  POP_JUMP_IF_FALSE   226  'to 226'
            208_0  COME_FROM           198  '198'

 L. 139       208  LOAD_FAST                'out'
              210  LOAD_METHOD              append
              212  LOAD_FAST                'self'
              214  LOAD_METHOD              splitnum_str
              216  LOAD_FAST                'div'
              218  CALL_METHOD_1         1  '1 positional argument'
              220  CALL_METHOD_1         1  '1 positional argument'
              222  POP_TOP          
              224  JUMP_FORWARD        254  'to 254'
            226_0  COME_FROM           206  '206'

 L. 140       226  LOAD_FAST                'div'
              228  LOAD_CONST               0
              230  COMPARE_OP               !=
              232  POP_JUMP_IF_FALSE   254  'to 254'

 L. 141       234  LOAD_FAST                'out'
              236  LOAD_METHOD              append
              238  LOAD_FAST                'self'
              240  LOAD_ATTR                cards_str
              242  LOAD_FAST                'div'
              244  BINARY_SUBSCR    
              246  LOAD_FAST                'div'
              248  BUILD_TUPLE_2         2 
              250  CALL_METHOD_1         1  '1 positional argument'
              252  POP_TOP          
            254_0  COME_FROM           232  '232'
            254_1  COME_FROM           224  '224'
            254_2  COME_FROM           146  '146'
            254_3  COME_FROM           124  '124'
            254_4  COME_FROM           116  '116'
            254_5  COME_FROM           108  '108'

 L. 143       254  LOAD_FAST                'out'
              256  LOAD_METHOD              append
              258  LOAD_FAST                'self'
              260  LOAD_ATTR                cards_str
              262  LOAD_FAST                'elem'
              264  BINARY_SUBSCR    
              266  LOAD_FAST                'elem'
              268  BUILD_TUPLE_2         2 
              270  CALL_METHOD_1         1  '1 positional argument'
              272  POP_TOP          

 L. 145       274  LOAD_FAST                'mod'
              276  LOAD_CONST               20
              278  COMPARE_OP               >
          280_282  POP_JUMP_IF_FALSE   298  'to 298'
              284  LOAD_FAST                'mod'
              286  LOAD_CONST               10
              288  BINARY_MODULO    
              290  LOAD_CONST               0
              292  COMPARE_OP               !=
          294_296  POP_JUMP_IF_TRUE    308  'to 308'
            298_0  COME_FROM           280  '280'
              298  LOAD_FAST                'mod'
              300  LOAD_CONST               20
              302  COMPARE_OP               >
          304_306  POP_JUMP_IF_FALSE   326  'to 326'
            308_0  COME_FROM           294  '294'

 L. 146       308  LOAD_FAST                'out'
              310  LOAD_METHOD              append
              312  LOAD_FAST                'self'
              314  LOAD_METHOD              splitnum_str
              316  LOAD_FAST                'mod'
              318  CALL_METHOD_1         1  '1 positional argument'
              320  CALL_METHOD_1         1  '1 positional argument'
              322  POP_TOP          
              324  JUMP_FORWARD        356  'to 356'
            326_0  COME_FROM           304  '304'

 L. 147       326  LOAD_FAST                'mod'
              328  LOAD_CONST               0
              330  COMPARE_OP               !=
          332_334  POP_JUMP_IF_FALSE   356  'to 356'

 L. 148       336  LOAD_FAST                'out'
              338  LOAD_METHOD              append
              340  LOAD_FAST                'self'
              342  LOAD_ATTR                cards_str
              344  LOAD_FAST                'mod'
              346  BINARY_SUBSCR    
              348  LOAD_FAST                'mod'
              350  BUILD_TUPLE_2         2 
              352  CALL_METHOD_1         1  '1 positional argument'
              354  POP_TOP          
            356_0  COME_FROM           332  '332'
            356_1  COME_FROM           324  '324'

 L. 150       356  LOAD_FAST                'out'
              358  RETURN_VALUE     
              360  POP_BLOCK        
            362_0  COME_FROM_LOOP        0  '0'

Parse error at or near `COME_FROM' instruction at offset 148_0

    def to_cardinal(self, value):
        try:
            assert int(value) == value
        except (ValueError, TypeError, AssertionError):
            return self.to_cardinal_float(value)
        else:
            self.verify_num(value)
            out = ''
            if value < 0:
                value = abs(value)
                out = self.negword
            if value >= self.MAXVAL:
                raise OverflowError(self.errmsg_toobig % (value, self.MAXVAL))
            val = self.splitnum(value)
            words, num = self.clean(val)
            return self.title(out + words)

    def to_cardinal_str(self, value):
        try:
            assert int(value) == value
        except (ValueError, TypeError, AssertionError):
            return self.to_cardinal_float(value)
        else:
            self.verify_num(value)
            out = ''
            if value < 0:
                value = abs(value)
                out = self.negword
            if value >= self.MAXVAL:
                raise OverflowError(self.errmsg_toobig % (value, self.MAXVAL))
            val = self.splitnum_str(value)
            words, num = self.clean_str(val)
            return self.title_str(out + words)

    def to_cardinal_float(self, value):
        try:
            float(value) == value
        except (ValueError, TypeError, AssertionError):
            raise TypeError(self.errmsg_nonnum % value)

        pre = int(value)
        post = abs(value - pre)
        out = [
         self.to_cardinal(pre)]
        if self.precision:
            out.append(self.title(self.pointword))
        for i in range(self.precision):
            post *= 10
            curr = int(post)
            out.append(str(self.to_cardinal(curr)))
            post -= curr

        return ' '.join(out)

    def merge(self, curr, next):
        raise NotImplementedError

    def merge_str(self, curr, next):
        raise NotImplementedError

    def clean(self, val):
        out = val
        while len(val) != 1:
            out = []
            curr, next = val[:2]
            if isinstance(curr, tuple) and isinstance(next, tuple):
                out.append(self.merge(curr, next))
                if val[2:]:
                    out.append(val[2:])
            else:
                for elem in val:
                    if isinstance(elem, list):
                        if len(elem) == 1:
                            out.append(elem[0])
                        else:
                            out.append(self.clean(elem))
                    else:
                        out.append(elem)

            val = out

        return out[0]

    def clean_str(self, val):
        out = val
        while len(val) != 1:
            out = []
            curr, next = val[:2]
            if isinstance(curr, tuple) and isinstance(next, tuple):
                out.append(self.merge_str(curr, next))
                if val[2:]:
                    out.append(val[2:])
            else:
                for elem in val:
                    if isinstance(elem, list):
                        if len(elem) == 1:
                            out.append(elem[0])
                        else:
                            out.append(self.clean_str(elem))
                    else:
                        out.append(elem)

            val = out

        return out[0]

    def title(self, value):
        if self.is_title:
            out = []
            value = value.split()
            for word in value:
                if word in self.exclude_title:
                    out.append(word)
                else:
                    out.append(word[0].upper() + word[1:])

            value = ' '.join(out)
        return value

    def title_str(self, value):
        if self.is_title:
            out = []
            value = value.split()
            for word in value:
                if word in self.exclude_title:
                    out.append(word)
                else:
                    out.append(word[0].upper() + word[1:])

            value = ' '.join(out)
        return value

    def verify_ordinal(self, value):
        if not value == int(value):
            raise TypeError(self.errmsg_floatord % value)
        if not abs(value) == value:
            raise TypeError(self.errmsg_negord % value)

    def verify_num(self, value):
        return 1

    def set_wordnums(self):
        pass

    def to_ordinal(self, value):
        return self.to_cardinal(value)

    def to_ordinal_num(self, value):
        return value

    def inflect(self, value, text):
        text = text.split('/')
        if value == 1:
            return text[0]
        return ''.join(text)

    def to_splitnum(self, val, hightxt='', lowtxt='', jointxt='', divisor=100, longval=True):
        out = []
        try:
            high, low = val
        except TypeError:
            high, low = divmod(val, divisor)

        if high:
            hightxt = self.title(self.inflect(high, hightxt))
            out.append(self.to_cardinal(high))
            if low:
                if longval:
                    if hightxt:
                        out.append(hightxt)
                    if jointxt:
                        out.append(self.title(jointxt))
            elif hightxt:
                out.append(hightxt)
        if low:
            out.append(self.to_cardinal(low))
            if lowtxt:
                if longval:
                    out.append(self.title(self.inflect(low, lowtxt)))
        return ' '.join(out)

    def to_year(self, value, **kwargs):
        return self.to_cardinal(value)

    def to_currency(self, value, **kwargs):
        return self.to_cardinal(value)

    def base_setup(self):
        pass

    def setup(self):
        pass

    def test(self, value):
        try:
            _card = self.to_cardinal_str(value)
        except:
            _card = 'invalid'

        try:
            _ord = self.to_ordinal(value)
        except:
            _ord = 'invalid'

        try:
            _ordnum = self.to_ordinal_num(value)
        except:
            _ordnum = 'invalid'

        print('For %s, card is %s;\n\tord is %s; and\n\tordnum is %s.' % (
         value, _card, _ord, _ordnum))