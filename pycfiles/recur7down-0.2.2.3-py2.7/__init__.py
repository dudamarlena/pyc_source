# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/recur7down/__init__.py
# Compiled at: 2018-01-23 16:24:09
from .base import Collect
from .products import product_main
from .diary import diary_main
from .transaction import transaction_main
from .html import html_main
from .parse_diary import parse_diary_main
import sys

def main():
    """
    entrypoint, if with first input 'raw', then taking input instead of read
    get product(p) or diary(d) or transaction(t) or html(h) or parse diary(pd):  
p/d/t/h/pd? 
    """
    try:
        if sys.argv[1] == 'raw':
            c = str(sys.argv[2]).strip()
        else:
            c = raw_input('get product(p) or diary(d) or transaction(t) or html(h) or parse diary(pd):  \np/d/t/h/pd? ')
    except:
        c = raw_input('get product(p) or diary(d) or transaction(t) or html(h) or parse diary(pd):  \np/d/t/h/pd? ')

    if c.lower() == 'p':
        product_main()
    elif c.lower() == 'd':
        diary_main()
    elif c.lower() == 't':
        transaction_main()
    elif c.lower() == 'h':
        html_main()
    elif c.lower() == 'pd':
        parse_diary_main()