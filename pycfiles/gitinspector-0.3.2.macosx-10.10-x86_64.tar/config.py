# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/gitinspector/lib/python2.7/site-packages/gitinspector/config.py
# Compiled at: 2015-08-05 12:31:15
from __future__ import unicode_literals
import extensions, filtering, format, interval, optval, os, subprocess

def __read_git_config__(repo, variable):
    previous_directory = os.getcwd()
    os.chdir(repo)
    setting = subprocess.Popen(b'git config inspector.' + variable, shell=True, bufsize=1, stdout=subprocess.PIPE).stdout
    os.chdir(previous_directory)
    try:
        setting = setting.readlines()[0]
        setting = setting.decode(b'utf-8', b'replace').strip()
    except IndexError:
        setting = b''

    return setting


def __read_git_config_bool__(repo, variable):
    try:
        variable = __read_git_config__(repo, variable)
        return optval.get_boolean_argument(False if variable == b'' else variable)
    except optval.InvalidOptionArgument:
        return False


def __read_git_config_string__(repo, variable):
    string = __read_git_config__(repo, variable)
    if len(string) > 0:
        return (True, string)
    else:
        return (False, None)


def init(run):
    var = __read_git_config_string__(run.repo, b'file-types')
    if var[0]:
        extensions.define(var[1])
    var = __read_git_config_string__(run.repo, b'exclude')
    if var[0]:
        filtering.add(var[1])
    var = __read_git_config_string__(run.repo, b'format')
    if var[0] and not format.select(var[1]):
        raise format.InvalidFormatError(_(b'specified output format not supported.'))
    run.hard = __read_git_config_bool__(run.repo, b'hard')
    run.list_file_types = __read_git_config_bool__(run.repo, b'list-file-types')
    run.localize_output = __read_git_config_bool__(run.repo, b'localize-output')
    run.metrics = __read_git_config_bool__(run.repo, b'metrics')
    run.responsibilities = __read_git_config_bool__(run.repo, b'responsibilities')
    run.useweeks = __read_git_config_bool__(run.repo, b'weeks')
    var = __read_git_config_string__(run.repo, b'since')
    if var[0]:
        interval.set_since(var[1])
    var = __read_git_config_string__(run.repo, b'until')
    if var[0]:
        interval.set_until(var[1])
    run.timeline = __read_git_config_bool__(run.repo, b'timeline')
    if __read_git_config_bool__(run.repo, b'grading'):
        run.hard = True
        run.list_file_types = True
        run.metrics = True
        run.responsibilities = True
        run.timeline = True
        run.useweeks = True