# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/musicbot/commands/music.py
# Compiled at: 2020-04-15 22:39:47
# Size of source mod 2**32: 504 bytes
import logging, click
from musicbot import helpers
from musicbot.music.file import File
from musicbot.music.fingerprint import acoustid_api_key_option
logger = logging.getLogger(__name__)

@click.group(help='Music file', cls=(helpers.GroupWithHelp))
def cli():
    pass


@cli.command(help='Print music fingerprint')
@click.argument('path')
@helpers.add_options(acoustid_api_key_option)
def fingerprint(path, acoustid_api_key):
    f = File(path)
    print(f.fingerprint(acoustid_api_key))