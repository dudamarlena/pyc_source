# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cookiecutter/mkpregen.py
# Compiled at: 2017-02-26 17:11:47
# Size of source mod 2**32: 954 bytes
import sys, json
from pathlib import Path

def write_cc_yaml(cc_json, pre_template):
    with open(str(cc_json)) as (fp):
        data = json.loads(fp.read())
    with open(str(pre_template)) as (fp):
        line = fp.readline()
        while line:
            if line.strip() != '@USER_CONFIG@':
                print(line.rstrip())
            else:
                print('default_context:')
                for k in sorted(data.keys()):
                    if not k.startswith('_'):
                        val = data[k]
                        if isinstance(val, list):
                            val = val[0]
                        print('{ident}{key}: "{{{{ cookiecutter.{key} }}}}"'.format(ident='    ',
                          key=k))
                    else:
                        line = fp.readline()


if __name__ == '__main__':
    cc_json = sys.argv[1]
    pre_template = sys.argv[2]
    write_cc_yaml(Path(cc_json), Path(pre_template))