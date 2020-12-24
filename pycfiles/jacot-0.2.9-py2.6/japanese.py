# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/jacot/japanese/japanese.py
# Compiled at: 2012-11-04 13:40:21
import tff
HINT_UTF8 = 0
HINT_CP932 = 1
HINT_EUCJP = 2

class JapaneseScanner(tff.Scanner):
    __data = None
    __utf8_state = 0
    __cp932_state = 0
    __eucjp_state = 0
    __count = 0
    __hint = HINT_UTF8

    def assign(self, value, termenc):
        self.__data = list(value)
        self.__utf8_state = 0
        self.__cp932_state = 0
        self.__eucjp_state = 0
        self.__count = 0

    def __iter__(self):
        for x in self.__data:
            c = ord(x)
            if self.__count != 0 and self.__cp932_state != 0:
                if 64 <= c and c <= 252:
                    try:
                        self.__cp932_state = ord((chr(self.__cp932_state) + x).decode('cp932'))
                        if self.__count == 1:
                            yield self.__cp932_state
                            self.__cp932_state = 0
                            self.__eucjp_state = 0
                            self.__utf8_state = 0
                            self.__count = 0
                            continue
                    except:
                        pass

                self.__hint = HINT_UTF8
                self.__cp932_state = 0
            if self.__count != 0 and self.__eucjp_state != 0:
                if 161 <= c:
                    if c <= 254:
                        try:
                            yield ord((chr(self.__eucjp_state) + x).decode('eucjp'))
                            self.__cp932_state = 0
                            self.__eucjp_state = 0
                            self.__count = 0
                            self.__hint = HINT_EUCJP
                            continue
                        except:
                            pass

                    self.__eucjp_state = 0
            elif c < 128:
                self.__utf8_state = 0
                self.__count = 0
                yield c
            elif c >> 6 == 2:
                if self.__count == 0:
                    if 129 <= c and c <= 159:
                        self.__cp932_state = c
                    elif 161 <= c and c <= 168:
                        self.__eucjp_state = c
                    elif c == 173:
                        self.__eucjp_state = c
                    elif 176 <= c:
                        self.__eucjp_state = c
                    else:
                        yield 63
                    self.__count = 1
                    self.__utf8_state = 0
                else:
                    self.__utf8_state = self.__utf8_state << 6 | c & 63
                    self.__count -= 1
                    if self.__count == 0:
                        if self.__utf8_state < 128:
                            yield 63
                        else:
                            self.__hint = HINT_UTF8
                            yield self.__utf8_state
                        self.__count = 0
                        self.__utf8_state = 0
            elif c >> 5 == 6:
                if self.__count != 0:
                    self.__count = 0
                    yield 63
                else:
                    self.__utf8_state = c & 31
                    self.__count = 1
                    self.__eucjp_state = c
            elif c >> 4 == 14:
                if self.__count != 0:
                    self.__count = 0
                    yield 63
                else:
                    self.__utf8_state = c & 15
                    self.__count = 2
                    if self.__hint == HINT_CP932:
                        self.__cp932_state = c
                    if self.__hint == HINT_EUCJP:
                        self.__eucjp_state = c
            elif c >> 3 == 30:
                if self.__count != 0:
                    self.__count = 0
                    yield 63
                else:
                    self.__utf8_state = c & 7
                    self.__count = 3
                    if c & 7 <= 4:
                        self.__eucjp_state = c
            elif c >> 2 == 62:
                if self.__count != 0:
                    self.__count = 0
                    yield 63
                else:
                    self.__utf8_state = c & 3
                    self.__count = 4
                    self.__eucjp_state = c
            elif c >> 1 == 126:
                if self.__count != 0:
                    self.__count = 0
                    yield 63
                else:
                    self.__utf8_state = c & 1
                    self.__count = 5
                    if c & 1 == 0:
                        self.__eucjp_state = c