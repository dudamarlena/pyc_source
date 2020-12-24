# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nickdg/anaconda3/envs/dna2/lib/python3.7/site-packages/genomics_demo/scripts.py
# Compiled at: 2018-10-01 10:36:16
# Size of source mod 2**32: 443 bytes
from genomics_demo.dna import DNA
import click

@click.command()
@click.argument('seq', type=str)
@click.option('--reverse/--no-reverse', default=False, help='Whether to reverse or not')
def get_reverse_complement(seq, reverse=False):
    """Take a DNA sequence and returns its complement"""
    complement = str(DNA(seq).compliment())
    if reverse:
        complement = complement[::-1]
    click.echo(complement)


get_reverse_complement()