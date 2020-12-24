# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/fedor/Documents/dev/assnake-core-preprocessing/assnake_core_preprocessing/remove_human_bbmap/init_remove_human_bbmap.py
# Compiled at: 2020-02-20 15:42:38
# Size of source mod 2**32: 430 bytes
import assnake.api.loaders, assnake.api.sample_set
from tabulate import tabulate
import click

@click.command('remove_human_bbmap', short_help='Count number of reads and basepairs in fastq file')
@click.pass_obj
def init_remove_human_bbmap(config):
    """
    Will download masked human genome and save it fasta directory.
    """
    pass