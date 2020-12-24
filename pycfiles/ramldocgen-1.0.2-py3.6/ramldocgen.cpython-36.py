# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ramldocgen\ramldocgen.py
# Compiled at: 2017-06-28 07:33:00
# Size of source mod 2**32: 282 bytes
import click
from .generator import Generator

@click.group()
def cli():
    pass


@cli.command()
@click.argument('infile')
@click.argument('outfile')
def generate(infile, outfile):
    g = Generator(infile)
    with open(outfile, 'w') as (target):
        target.write(g.generate())