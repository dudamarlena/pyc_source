# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vermeul/openbis/obis/src/python/obis/scripts/click_util.py
# Compiled at: 2018-09-27 20:05:19
# Size of source mod 2**32: 490 bytes
import click
from datetime import datetime

def click_echo(message, with_timestamp=True):
    if with_timestamp:
        timestamp = datetime.now().strftime('%H:%M:%S')
        click.echo('{} {}'.format(timestamp, message))
    else:
        click.echo(message)


def check_result(command, result):
    if result.failure():
        click_echo('Could not {}:\n{}'.format(command, result.output))
    else:
        if len(result.output) > 0:
            click_echo(result.output)
    return result.returncode