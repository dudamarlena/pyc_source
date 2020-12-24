# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\test\_write_stds.py
# Compiled at: 2017-01-26 21:08:30
# Size of source mod 2**32: 3476 bytes
"""Snippets for what a particular dataset (including nested sequences)
should look like after writing in different expl/impl Vr and endian combos,
as well as undefined length sequences and items
"""
impl_LE_deflen_std_hex = '10 00 10 00 0c 00 00 00 4e 61 6d 65 5e 50 61 74 69 65 6e 74 06 30 39 00 5a 00 00 00 fe ff 00 e0 52 00 00 00 06 30 40 00 4a 00 00 00 fe ff 00 e0 1a 00 00 00 06 30 48 00 02 00 00 00 31 20 06 30 50 00 08 00 00 00 32 5c 34 5c 38 5c 31 36 fe ff 00 e0 20 00 00 00 06 30 48 00 02 00 00 00 32 20 06 30 50 00 0e 00 00 00 33 32 5c 36 34 5c 31 32 38 5c 31 39 36 20 '
impl_BE_deflen_std_hex = '00 10 00 10 00 00 00 0c 4e 61 6d 65 5e 50 61 74 69 65 6e 74 30 06 00 39 00 00 00 5a ff fe e0 00 00 00 00 52 30 06 00 40 00 00 00 4a ff fe e0 00 00 00 00 1a 30 06 00 48 00 00 00 02 31 20 30 06 00 50 00 00 00 08 32 5c 34 5c 38 5c 31 36 ff fe e0 00 20 00 00 00 30 06 00 48 00 00 00 02 32 20 30 06 00 50 00 00 00 0e 33 32 5c 36 34 5c 31 32 38 5c 31 39 36 20 '