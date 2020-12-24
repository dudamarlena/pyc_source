# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.6/site-packages/filabel/utils.py
# Compiled at: 2018-12-29 18:37:27
# Size of source mod 2**32: 315 bytes


def parse_labels(cfg):
    """
    Parse labels to dict where label is key and list
    of patterns is corresponding value

    cfg: ConfigParser with loaded configuration of labels
    """
    return {label:list(filter(None, cfg['labels'][label].splitlines())) for label in cfg['labels']}