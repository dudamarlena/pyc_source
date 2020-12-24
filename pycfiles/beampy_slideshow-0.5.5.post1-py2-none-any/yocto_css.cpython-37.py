# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/developpement/python/libperso/beampy/scour/yocto_css.py
# Compiled at: 2018-07-04 13:16:55
# Size of source mod 2**32: 3033 bytes


def parseCssString(str):
    rules = []
    chunks = str.split('}')
    for chunk in chunks:
        bits = chunk.split('{')
        if len(bits) != 2:
            continue
        rule = {}
        rule['selector'] = bits[0].strip()
        bites = bits[1].strip().split(';')
        if len(bites) < 1:
            continue
        props = {}
        for bite in bites:
            nibbles = bite.strip().split(':')
            if len(nibbles) != 2:
                continue
            props[nibbles[0].strip()] = nibbles[1].strip()

        rule['properties'] = props
        rules.append(rule)

    return rules