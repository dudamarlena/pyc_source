# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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