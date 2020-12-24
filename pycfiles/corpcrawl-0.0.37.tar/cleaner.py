# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/workspace/corpcrawl_env/corpcrawl/corpcrawl/util/cleaner.py
# Compiled at: 2013-03-11 23:30:36
import re

def clean_name(name):
    if name:
        remove = [
         '(Filer)']
    for r in remove:
        name = name.replace(r, '')

    name = name.strip()
    name = first_letter_caps(name)
    return name


def clean_addr(addr):
    return first_letter_caps(addr)


def first_letter_caps(word):

    def repl(m):
        return m.group(0).upper()

    return re.sub('^[a-z]|\\s[a-z]', repl, word.lower())