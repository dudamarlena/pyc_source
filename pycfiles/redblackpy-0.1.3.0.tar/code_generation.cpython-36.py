# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/HYPOTHETICAL/Documents/GitHubRepos/Intuition/RedBlackPy/rbp_setup_tools/code_generation.py
# Compiled at: 2018-08-15 11:46:31
# Size of source mod 2**32: 498 bytes


def generate_from_cython_src(input_file, output_file, list_of_types, from_str):
    src = input_file.readlines()[from_str:]
    for dtype in list_of_types:
        for line in src:
            new_line = line.format(DTYPE=dtype, key='{key}', value='{value}',
              map_kwargs='{}')
            output_file.write(new_line)