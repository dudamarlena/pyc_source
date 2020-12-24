# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/GitHub/MetaWards/build/lib.macosx-10.9-x86_64-3.7/metawards/utils/_read_done_file.py
# Compiled at: 2020-04-15 04:10:58
# Size of source mod 2**32: 567 bytes
__all__ = ['read_done_file']

def read_done_file(filename: str):
    """This function reads the 'done_file' from 'filename' returning the list
       of seeded nodes
    """
    try:
        print(f"{filename} -- ")
        nodes_seeded = []
        with open(filename, 'r') as (FILE):
            line = FILE.readline()
            nodes_seeded.append(float(line.strip()))
        return nodes_seeded
    except Exception as e:
        try:
            raise ValueError(f"Possible corruption of {filename}: {e}")
        finally:
            e = None
            del e