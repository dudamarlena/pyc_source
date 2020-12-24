# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/me/projects/keystone.git/tmp/keystone.git/llvm/utils/llvm-build/llvmbuild/configutil.py
# Compiled at: 2016-06-04 06:22:29
"""
Defines utilities useful for performing standard "configuration" style tasks.
"""
import re, os

def configure_file(input_path, output_path, substitutions):
    """configure_file(input_path, output_path, substitutions) -> bool

    Given an input and output path, "configure" the file at the given input path
    by replacing variables in the file with those given in the substitutions
    list. Returns true if the output file was written.

    The substitutions list should be given as a list of tuples (regex string,
    replacement), where the regex and replacement will be used as in 're.sub' to
    execute the variable replacement.

    The output path's parent directory need not exist (it will be created).

    If the output path does exist and the configured data is not different than
    it's current contents, the output file will not be modified. This is
    designed to limit the impact of configured files on build dependencies.
    """
    f = open(input_path, 'rb')
    try:
        data = f.read()
    finally:
        f.close()

    for regex_string, replacement in substitutions:
        regex = re.compile(regex_string)
        data = regex.sub(replacement, data)

    output_parent_path = os.path.dirname(os.path.abspath(output_path))
    if not os.path.exists(output_parent_path):
        os.makedirs(output_parent_path)
    if os.path.exists(output_path):
        current_data = None
        try:
            f = open(output_path, 'rb')
            try:
                current_data = f.read()
            except:
                current_data = None

            f.close()
        except:
            current_data = None

        if current_data is not None and current_data == data:
            return False
    f = open(output_path, 'wb')
    try:
        f.write(data)
    finally:
        f.close()

    return True