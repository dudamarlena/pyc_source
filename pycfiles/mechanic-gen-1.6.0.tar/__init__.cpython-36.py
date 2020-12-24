# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zackschrag/fctn/mechanic/mechanic/__init__.py
# Compiled at: 2018-03-19 16:00:43
# Size of source mod 2**32: 319 bytes
import sys, logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)