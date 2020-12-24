# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kghose/.venvs/benten/lib/python3.7/site-packages/benten/000.package.data/create-schema.py
# Compiled at: 2019-08-23 14:36:21
# Size of source mod 2**32: 1401 bytes
"""Short script that uses schema-salad to generate and post-process the CWL yml document into
a JSON format that is read in by Benten and converted into a set of Python classes for CWL types"""
import sys, subprocess, json

def remove_uris(d):
    if isinstance(d, dict):
        for k, v in d.items():
            d[k] = remove_uris(v)

        return d
    elif isinstance(d, list):
        return [remove_uris(v) for v in d]
        if not isinstance(d, str) or d.startswith('https://w3id.org') or d.startswith('http://www.w3.org'):
            _v = d.split('#')[1]
            if '/' in _v:
                _v = _v.split('/')[1]
    else:
        return _v
    return d


def main():
    print(sys.argv)
    if len(sys.argv) != 3:
        print('python create-schema.py <input.yml> <output.json>\ne.g. python create-schema.py CommonWorkflowLanguage.yml schema-v1.0.json')
        return
    subprocess.call(f"schema-salad-tool --print-avro {sys.argv[1]} > {sys.argv[2]}", shell=True)
    with open(sys.argv[2], 'r') as (f):
        d = json.load(f)
        d = remove_uris(d)
    with open(sys.argv[2], 'w') as (f):
        json.dump(d, f, indent=2)


if __name__ == '__main__':
    main()