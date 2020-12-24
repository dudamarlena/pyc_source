# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\correspondence_tables\usepa_to_chemspyder.py
# Compiled at: 2020-01-19 12:24:29
# Size of source mod 2**32: 407 bytes
"""Generate the .ttl from the correspondence tables.
Handcrafted as not available elsewhere."""
import pandas as pd
from pathlib import Path
data_dir = Path.cwd() / 'data' / 'final_tables' / 'tables'

def generate_usepa_to_chemspyder_correspondence(output_base_dir):
    """handcrafted data to generate ttl from csv file"""
    print(f"files will be stored in {data_dir}")