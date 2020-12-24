# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/victor/Documents/Experiments/test-sphynx/v5/PROJECT/moduleD/classif/ds.py
# Compiled at: 2018-02-20 08:47:55
# Size of source mod 2**32: 426 bytes
"""
Woaw ce module est trop stylé, je me demande bien qui a pu écrire un si
beau code
"""

def get_bad_guy(ds, model):
    """Returns whether or not the person in the ds is a wrongdoer

    Args:
        ds (str): ds text
        model (code.Model): model to perform inference with

    Returns:
        bool: blabla
    """
    print(ds, model)
    return ds == model


if __name__ == '__main__':
    get_bad_guy(1, '3')