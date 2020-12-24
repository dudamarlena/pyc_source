# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__QTYPES__/number/number.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 1127 bytes
tutor.qtype_inherit('expression')
defaults['csq_render_result'] = False

def _input_check(src, tree):
    if tree[0] == 'NUMBER':
        return
    if tree[0] == '/':
        if tree[1][0] == 'NUMBER':
            if tree[2][0] == 'NUMBER':
                return
    return 'Your input must be a single number or simple fraction.'


defaults['csq_input_check'] = _input_check