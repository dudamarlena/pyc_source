# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\correspondence_tables\usepa_to_chemspyder.py
# Compiled at: 2020-01-19 12:24:29
# Size of source mod 2**32: 407 bytes
__doc__ = 'Generate the .ttl from the correspondence tables.\nHandcrafted as not available elsewhere.'
import pandas as pd
from pathlib import Path
data_dir = Path.cwd() / 'data' / 'final_tables' / 'tables'

def generate_usepa_to_chemspyder_correspondence(output_base_dir):
    """handcrafted data to generate ttl from csv file"""
    print(f"files will be stored in {data_dir}")