# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nowandnext/digiguide/categories.py
# Compiled at: 2009-05-11 19:02:39
STRCATS = 'Adult Entertainment\n Animation\n Arts\n Business and Finance\n Chat Show\n Childrens\n Comedy\n Consumer\n Cookery\n DIY\n Documentary\n Drama\n Education\n Entertainment\n Fashion\n Film\n Game Show\n Gardening\n Health\n History Documentary\n Kids Drama\n Magazine Programme\n Motoring\n Music\n Nature\n News\n Political\n Quiz Show\n Reality Show\n Religious\n Science Fiction Series\n Scientific Documentary\n Series\n Sitcom\n Soap\n Special Interest\n Sport\n Talk Show\n Technology\n Travel'
CATEGORIES = [ a.strip().upper() for a in STRCATS.split('\n') ]
if __name__ == '__main__':
    import pprint
    pprint.pprint(CATEGORIES)