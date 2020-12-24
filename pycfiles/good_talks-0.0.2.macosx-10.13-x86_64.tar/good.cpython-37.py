# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jsmith/Projects/personal/presentations/2018/packaging_talk/venv/lib/python3.7/site-packages/talks/good.py
# Compiled at: 2018-09-25 19:18:49
# Size of source mod 2**32: 333 bytes


class Talk:

    def thank(self, speaker=None, crowd=None):
        payload = 'Thanks!'
        if crowd:
            payload = f"Thanks for coming to {crowd}"
        if speaker:
            payload = f"Thanks you {speaker} for giving this talk"
        print(payload)
        return payload