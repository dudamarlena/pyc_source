# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/doubanfm/lrc2dic.py
# Compiled at: 2016-06-22 17:23:26
"""
歌词解析, 把歌词解析成字典形式
reference: (http://reverland.org/python/2014/10/09/lrc/)
"""
import re

def lrc2dict(lrc):

    def remove(x):
        return x.strip('[|]')

    lrc_dict = {}
    for line in lrc.split('\n'):
        if line.strip('\n'):
            time_stamps = re.findall('\\[[^\\]]+\\]', line)
            if time_stamps:
                lyric = line
                for tplus in time_stamps:
                    lyric = lyric.replace(tplus, '')

                for tplus in time_stamps:
                    t = remove(tplus)
                    tag_flag = t.split(':')[0]
                    if not tag_flag.isdigit():
                        continue
                    time_lrc = int(tag_flag) * 60
                    time_lrc += int(t.split(':')[1].split('.')[0])
                    lrc_dict[time_lrc] = lyric

    return lrc_dict


def main():
    with open('3443588.lrc', 'r') as (F):
        lrc = F.read()
    lrc_dict = lrc2dict(lrc)
    for key in lrc_dict:
        print key, lrc_dict[key]


if __name__ == '__main__':
    main()