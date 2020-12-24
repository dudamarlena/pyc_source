# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/otest/aus/preproc/logs.py
# Compiled at: 2017-02-08 10:11:16
# Size of source mod 2**32: 1060 bytes
preline = '<h3>A list of {} that are saved on disk for this {}:</h3>'

def display_log(logs, issuer, profile, base):
    el = []
    if issuer:
        if profile:
            el.append(preline.format('tests', 'profile'))
        else:
            el.append(preline.format('profiles', 'issuer'))
    else:
        el.append(preline.format('issuers', 'test server'))
    el.append('<ul>')
    if profile:
        for name, path in logs:
            el.append('<li><a href="{}{}" download="{}.html">{}</a>'.format(base, path, name, name))

    else:
        for name, path in logs:
            _tarfile = '{}{}.tar'.format(base, path.replace('log', 'tar'))
            el.append('<li><a href="{}{}">{}</a> tar file:<a href="{}">'.format(base, path, name, _tarfile))
            el.append('Download logs</a>')

    el.append('</ul>')
    return '\n'.join(el)