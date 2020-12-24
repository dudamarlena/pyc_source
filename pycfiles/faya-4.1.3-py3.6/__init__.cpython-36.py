# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/faya/__init__.py
# Compiled at: 2018-07-04 01:22:16
# Size of source mod 2**32: 1262 bytes
import click, sys, os
__p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if __p not in sys.path:
    sys.path.insert(0, p)
from .lib import __jp_dict
from .lib import __pixiv
from .lib import __nikkei
from .lib import __common
from .lib import __muti
from .lib import __wiki
pool = __muti.Multithread()

@click.group()
def faya():
    pass


@click.command()
@click.argument('word')
def jp(word):
    msg = __jp_dict.get(word)
    click.echo(msg)


@click.command()
@click.argument('key')
def wiki(key):
    msg = __wiki.get(key)
    click.echo(msg)


@click.command()
def pixiv():
    msg = __pixiv.get()
    click.echo(msg)


@click.command()
def nikkei():
    msg = __nikkei.get()
    click.echo(msg)


faya.add_command(jp)
faya.add_command(pixiv)
faya.add_command(nikkei)
faya.add_command(wiki)
faya.add_command(__common.md5)
faya.add_command(__common.roll)
faya.add_command(__common.cal)
faya.add_command(__common.unicodeDecode)
faya.add_command(__common.unicodeEncode)
faya.add_command(__common.greek)
if __name__ == '__main__':
    jp('眠い')