# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/git_additions/__helpers.py
# Compiled at: 2018-12-29 08:10:59
import pathlib, time

def find_toplevel(path, last=None):
    path = pathlib.Path(path).absolute()
    if path == last:
        return None
    else:
        if (path / '.git').is_dir():
            return path
        return find_toplevel(path.parent, last=path)


def duration(commit1, commit2):
    start = commit1.commit_time
    end = commit2.commit_time
    d = divmod(end - start, 86400)
    h = divmod(d[1], 3600)
    m = divmod(h[1], 60)
    s = m[1]
    return (
     d[0], h[0], m[0], s)


def commit_date(commit):
    return time.ctime(commit.commit_time)


def normalize_duration(days, hours, minutes, seconds, total):
    minutes += int(seconds / 60)
    seconds = int(seconds % 60)
    hours += int(minutes / 60)
    minutes = int(minutes % 60)
    days += int(hours / 24)
    hours = int(hours % 24)
    if total == 'seconds':
        total_duration = days * 24 * 60 * 60 + hours * 60 * 60 + minutes * 60 + seconds
    elif total == 'minutes':
        total_duration = days * 24 * 60 + hours * 60 + minutes + seconds / 60
    elif total == 'hours':
        total_duration = days * 24 + hours + minutes / 60 + seconds / 3600
    elif total == 'days':
        total_duration = days + hours / 24 + minutes / 1440 + seconds / 86400
    else:
        total_duration = None
    return (days, hours, minutes, seconds, total_duration)