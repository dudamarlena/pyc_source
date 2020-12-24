# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cb/Projekter/stonebear/stonebear/deploy.py
# Compiled at: 2011-09-06 17:56:10
from build import build
from push import push
from clean import clean

def deploy(args, config):
    """
    convenience function that builds and pushes in one call
    """
    build(args, config)
    push(args, config)