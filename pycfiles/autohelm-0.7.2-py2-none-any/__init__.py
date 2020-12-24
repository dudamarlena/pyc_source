# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/circleci/autohelm/autohelm/__init__.py
# Compiled at: 2018-11-27 14:02:40
import subprocess, logging
from exception import AutoHelmCommandException

class Response(object):
    """
    Description:
    - Utility class to simplify the results from call()

    Arguments: 
    - stdout(string) 
    - stderr (string)
    - exitcode (sting,int) 

    Attributes:
    - stdout
    - stderr
    - exitcode

    Returns:
    - Instance of Response() is truthy where Reponse.exitcode == 0  
    - Instance Response() is falsey where Reponse.exitcode != 0
    """

    def __init__(self, stdout, stderr, exitcode):
        self._dict = {}
        self._dict['stdout'] = stdout
        self._dict['stderr'] = stderr
        self._dict['exitcode'] = exitcode

    def __getattr__(self, name):
        return self._dict.get(name)

    def __str__(self):
        return str(self._dict)

    def __bool__(self):
        return not self._dict['exitcode']

    def __eq__(self, other):
        return self._dict == other._dict


def call(args):
    """
    Description:
    - Wrapper for subprocess.Popen. Joins `args` and passes
    to `subprocess.Popen`

    Arguments: 
    - args (list)

    Returns:
    - Instance of Response()
    """
    logging.debug((' ').join(args))
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    exitcode = p.returncode
    if exitcode > 0:
        raise AutoHelmCommandException(('Error with subprocess call: {}').format((' ').join(args)), stdout, stderr, exitcode)
    return Response(stdout, stderr, exitcode)