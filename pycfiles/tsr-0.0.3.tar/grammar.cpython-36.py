# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marx/venv3/lib/python3.6/site-packages/tsr/modules/grammar.py
# Compiled at: 2018-05-13 09:02:24
# Size of source mod 2**32: 642 bytes
try:
    import inflect
    use_inflect = True
except ImportError:
    use_inflect = False

if use_inflect:
    inflect_engine = inflect.engine()

def singular_noun(word):
    if use_inflect:
        try:
            return inflect_engine.singular_noun(word)
        except:
            pass

    return word


def singular_verb(word):
    if use_inflect:
        try:
            return inflect_engine.singular_verb(word)
        except:
            pass

    return word


def singularise(word):
    x = singular_noun(word)
    if type(x).__name__ == 'str':
        return x
    else:
        return word