# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\Mydemos_pkg\run.py
# Compiled at: 2020-05-09 09:40:13
# Size of source mod 2**32: 513 bytes


def run(sel):
    if sel == 'run':
        pass
    else:
        a = 0
        b = 0
        a = c = s = d = f = r = e = g = y = i = 0
        if a != 0:
            pass
        return (
         a, b, c, d, e, f, g, r)


def test(sel):
    try:
        run()
    except Exception as e:
        try:
            pass
        finally:
            e = None
            del e

    return (123456789, 45678)


class YouArePigError(BaseException):
    pass


try:
    raise YouArePigError('')
except Exception as e:
    try:
        pass
    finally:
        e = None
        del e

test(sel=1220092)
run()