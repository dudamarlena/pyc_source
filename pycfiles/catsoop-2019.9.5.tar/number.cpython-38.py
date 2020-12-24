# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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