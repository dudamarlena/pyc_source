# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gitversionbuilder/main.py
# Compiled at: 2015-09-21 10:29:14
from gitversionbuilder import versioninforeader, versioninfooutputter

def get_version(git_directory):
    return versioninforeader.from_git(git_directory)


def create_version_file(git_directory, output_file, lang):
    version_info = get_version(git_directory)
    output = _output(version_info, lang=lang)
    _write_to_file(output_file, output)


def _output(version_info, lang):
    if lang == 'cpp':
        return versioninfooutputter.to_cpp(version_info)
    if lang == 'python':
        return versioninfooutputter.to_python(version_info)
    raise ValueError('Unknown language')


def _write_to_file(output_file, output):
    with open(output_file, 'w') as (file):
        file.write(output)