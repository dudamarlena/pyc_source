# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tbielawa/rhat/release-engine/re-client/src/reclient/utils.py
# Compiled at: 2015-01-27 15:32:52
import os
from subprocess import call
import tempfile, json, yaml, logging
from reclient.colorize import colorize
from prettytable import PrettyTable
out = logging.getLogger('reclient')

def cooked_input(msg=''):
    """We need this to test user prompt"""
    return raw_input(msg)


def user_prompt_yes_no(prompt_str=''):
    """Simple re-useable prompt for action confirmation. Adds [y/n]
    suffix automatically.

    Returns True if Yes, False if No
    """
    ret = None
    while ret is None:
        ans = cooked_input(prompt_str + '[y/n]: ')
        if ans == 'y' or ans == 'Y':
            ret = True
        elif ans == 'n' or ans == 'N':
            ret = False
        else:
            continue

    return ret


def serialize(blob, format):
    """
    Serializes a structure.
    """
    if format == 'json':
        return json.dumps(blob, indent=4)
    return yaml.safe_dump(blob)


def deserialize(blob, format):
    """
    Retutns a deserialized structure.
    """
    if format == 'json':
        return json.loads(blob)
    return yaml.safe_load(blob)


def save_playbook(blob, dest, format):
    """Save the temporary playbook, `source` at `path`"""
    with open(dest, 'w') as (_dest):
        try:
            del blob['id']
        except KeyError:
            pass

        if format == 'json':
            json.dump(blob, _dest, indent=4)
        else:
            yaml.safe_dump(blob, _dest)


def temp_blob(data, format):
    """data is either a string or a hash. Function will 'do the right
thing' either way

format is the format to write with.
"""
    out.debug('tmp_blob received [%s]: %s' % (type(data), str(data)))
    if type(data) in [unicode, str]:
        data = json.loads(data)
    elif type(data) == dict or type(data) == list:
        pass
    else:
        raise ValueError("This isn't something I can work with")
    tmpfile = tempfile.NamedTemporaryFile(mode='w', suffix='.%s' % format, prefix='reclient-')
    if format == 'json':
        json.dump(data, tmpfile, indent=4)
    else:
        yaml.safe_dump(data, tmpfile)
    tmpfile.flush()
    return tmpfile


def edit_playbook(blob, format):
    """Edit the playbook object 'blob'.

If 'blob' is an unserialized string, then it is serialized and dumped
(with indenting) out to a temporary file.

If 'blob' is a serialized hash is is dumped out (with indenting) to a
temporary file.

If 'blob' is a file object (like you would get from 'temp_blob')
it is flush()'d.

'format' is either json or yaml.

Once all that is complete, an editor is opened pointing at the path to
the temporary file. After the editor is closed the original (or
instantiated) file handle is returned."""
    VISUAL = os.environ.get('VISUAL', None)
    if VISUAL is None:
        EDITOR = os.environ.get('EDITOR', 'emacs')
    else:
        EDITOR = VISUAL
    callcmd = [
     EDITOR]
    tmpfile = blob
    if isinstance(blob, tempfile._TemporaryFileWrapper):
        blob.flush()
    else:
        tmpfile = temp_blob(blob, format)
    try:
        out.debug('Editing with EDITOR=%s' % EDITOR)
        if EDITOR == 'emacs':
            callcmd.extend(['-nw', tmpfile.name])
        else:
            callcmd.append(tmpfile.name)
        out.debug('Going to launch editor with args: %s' % str(callcmd))
        call(callcmd)
    except OSError:
        out.debug("First call to EDITOR failed. Trying 'vi' explicitly")
        try:
            fallback_call = ['vi', tmpfile.name]
            call(fallback_call)
        except OSError:
            out.debug("Second call to EDITOR failed. Trying 'vim' explicitly")
            try:
                fallback_back_call = [
                 'vim', tmpfile.name]
                call(fallback_back_call)
            except OSError:
                out.info('Could not launch any editors. Tried: %s, vi, and vim' % EDITOR)
                return False

    return tmpfile


def less_file(path):
    call(['less', '-X', path])


def read_dynamic_args():
    """Prompt the user for dynamic arguments

An empty key name ends the prompt"""
    dynamic_args = {}
    while True:
        argname = cooked_input(colorize('Argument name: ', color='yellow'))
        if argname == '':
            break
        else:
            argvalue = cooked_input(colorize('Argument value: ', color='yellow'))
            try:
                argvalue = int(argvalue)
            except ValueError:
                pass

            dynamic_args[argname] = argvalue

    return dynamic_args


def dynamic_args_table(dargs):
    """Build a nice table of collected dynamic args"""
    t = PrettyTable(['Arg Name', 'Value'])
    t.header_style = 'upper'
    if dargs == {}:
        return ''
    for k, v in dargs.iteritems():
        t.add_row([k, v])

    return t