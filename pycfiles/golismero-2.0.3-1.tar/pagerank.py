# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/thirdparty/pagerank/pagerank.py
# Compiled at: 2013-12-09 06:41:17
import urllib

def get_pagerank(url):
    _ = 'http://toolbarqueries.google.com/tbr?client=navclient-auto&features=Rank&ch=%s&q=info:%s' % (check_hash(hash_url(url)), urllib.quote(url))
    try:
        f = urllib.urlopen(_)
        rank = f.read().strip()[9:]
    except Exception:
        rank = 'N/A'
    else:
        rank = '0' if not rank or not rank.isdigit() else rank

    return rank


def int_str(string_, integer, factor):
    for i in xrange(len(string_)):
        integer *= factor
        integer &= 4294967295
        integer += ord(string_[i])

    return integer


def hash_url(string_):
    c1 = int_str(string_, 5381, 33)
    c2 = int_str(string_, 0, 65599)
    c1 >>= 2
    c1 = c1 >> 4 & 67108800 | c1 & 63
    c1 = c1 >> 4 & 4193280 | c1 & 1023
    c1 = c1 >> 4 & 245760 | c1 & 16383
    t1 = (c1 & 960) << 4
    t1 |= c1 & 60
    t1 = t1 << 2 | c2 & 3855
    t2 = (c1 & 4294950912) << 4
    t2 |= c1 & 15360
    t2 = t2 << 10 | c2 & 252641280
    return t1 | t2


def check_hash(hash_int):
    hash_str = '%u' % hash_int
    flag = 0
    check_byte = 0
    i = len(hash_str) - 1
    while i >= 0:
        byte = int(hash_str[i])
        if 1 == flag % 2:
            byte *= 2
            byte = byte / 10 + byte % 10
        check_byte += byte
        flag += 1
        i -= 1

    check_byte %= 10
    if 0 != check_byte:
        check_byte = 10 - check_byte
        if 1 == flag % 2:
            if 1 == check_byte % 2:
                check_byte += 9
            check_byte >>= 1
    return '7' + str(check_byte) + hash_str