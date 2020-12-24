# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/factotum/diceware.py
# Compiled at: 2017-01-20 23:06:59
# Size of source mod 2**32: 478 bytes
import sys, random, re
from pkg_resources import resource_filename, Requirement

def generatePhrase(numWords):
    phrase = re.compile('[0-9]+\t(.*)')
    path_to_diceware = resource_filename('factotum', 'diceware.wordlist.asc')
    with open(path_to_diceware, 'r') as (diceware):
        password = diceware.readlines()
        password = [m.group(1) for l in password if m for m in [phrase.search(l)]]
        random.SystemRandom().shuffle(password)
        return ' '.join(password[0:numWords])