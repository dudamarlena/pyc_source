# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-rpc7z9ca/catsoop/catsoop/__QTYPES__/pythonliteral/pythonliteral.py
# Compiled at: 2020-01-06 01:44:31
# Size of source mod 2**32: 1350 bytes
import ast
tutor.qtype_inherit('pythonic')
base, _ = tutor.question('pythonic')

def handle_submission(submissions, **info):
    sub = submissions[info['csq_name']].strip()
    inp = info['csq_input_check'](sub)
    if inp is not None:
        return {'score':0.0, 
         'msg':'<font color="red">%s</font>' % inp}
    try:
        x = ast.parse(sub).body[0].value
        assert not isinstance(x, ast.BinOp)
        ast.literal_eval(x)
    except:
        return {'score':0.0, 
         'msg':'Value must be a valid Python literal.'}
    else:
        return (base['handle_submission'])(submissions, **info)