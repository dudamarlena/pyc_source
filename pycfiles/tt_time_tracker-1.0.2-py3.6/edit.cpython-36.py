# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tt/actions/write/edit.py
# Compiled at: 2020-03-25 12:46:18
# Size of source mod 2**32: 1006 bytes
import yaml, os, tempfile, subprocess
from tt.exceptz.exceptz import InvalidYAML
from tt.exceptz.exceptz import NoEditor
from tt.dataaccess.utils import get_data_store

def action_edit():
    if 'EDITOR' not in os.environ:
        raise NoEditor("Please set the 'EDITOR' environment variable")
    store = get_data_store()
    data = store.load()
    yml = yaml.safe_dump(data, default_flow_style=False, allow_unicode=True)
    cmd = os.getenv('EDITOR')
    fd, temp_path = tempfile.mkstemp(suffix='.yml', prefix='tt.')
    with open(temp_path, 'r+') as (f):
        f.write(yml.replace('\n- ', '\n\n- '))
        f.seek(0)
        subprocess.check_call((cmd + ' ' + temp_path), shell=True)
        yml = f.read()
        f.truncate()
        f.close
    os.close(fd)
    os.remove(temp_path)
    try:
        data = yaml.load(yml, Loader=(yaml.SafeLoader))
    except yaml.YAMLError as exc:
        raise InvalidYAML("Oops, that YAML doesn't appear to be valid!")

    store.dump(data)