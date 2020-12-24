# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/bots/discord/config.py
# Compiled at: 2020-03-23 07:40:05
# Size of source mod 2**32: 339 bytes
import os
signal = os.getenv('DISCORD_SIGNAL_CHAR') or '!'
max_workers = os.getenv('DISCORD_MAX_WORKERS', 10)
public_ip = os.getenv('PUBLIC_ADDRESS', None)
public_path = os.getenv('PUBLIC_DATA_PATH', None)