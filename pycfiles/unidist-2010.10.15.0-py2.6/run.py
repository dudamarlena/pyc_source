# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/unidist/run.py
# Compiled at: 2010-10-14 14:04:23
"""
Simple, non-threaded, run command.  Stores command in sharedstate for internal
inspection in bucket "__internals.run".  Can use this for cache.  Value of
state bucket key is:  (occurred_time, status, output, output_error)
"""
import subprocess, logging, time
from log import log
import sharedstate

def Run(command, env=None):
    """Actually run the command on the local machine.  Blocks until complete.
  
  Args:
    command: string, command to run in shell
    env: dict, values to set as environment variables for this command
  """
    output_error = ''
    pipe = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env=env)
    status = pipe.wait()
    output = pipe.stdout.read()
    output_error = pipe.stderr.read()
    pipe.stderr.close()
    pipe.stdout.close()
    if status != 0:
        log('Non-Zero Exit Code: %s: %s: %s' % (status, command, output_error), logging.INFO)
    if not command.startswith('rrdtool'):
        sharedstate.Set('__internals.run', command, (time.time(), status, output, output_error))
    return (status, output, output_error)


def OutputParsePrepare(output):
    """Any script that needs parsing may be helped by having all tabs converted to
  spaces and all duplicate spaces converted to tabs.
  
  Returns: list of strings, the parse-ready output, returns as a list of lines
  
  TODO(g): Respect quotes, as an option.  Right now all quoted strings will
      still be compressed, and optionally, this might be something we dont want.
  """
    output = output.replace('\t', ' ')
    while '  ' in output:
        output = output.replace('  ', ' ')

    lines = output.split('\n')
    return lines


def MakePathSafeToCreate(text, replace_char='_'):
    """Converts any unsafe characters in the text to path safe characters.
  
  Returns: string, safe for saving as a path name
  """
    replace_needed = '-+=\\|/[]{}()!@#$%^&*();:`~'
    for char in replace_needed:
        while char in text:
            text = text.replace(char, replace_char)

    return text