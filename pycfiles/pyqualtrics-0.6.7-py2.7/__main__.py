# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pyqualtrics\__main__.py
# Compiled at: 2017-06-01 23:29:10
import sys, os
from pyqualtrics import Qualtrics
if os.path.exists('.env'):
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

try:
    input = raw_input
except NameError:
    pass

def main(argv):
    kwargs = {}
    iterator = iter(argv)
    executable = next(iterator)
    try:
        command = next(iterator)
    except StopIteration:
        print 'The name of the API call to be made is required'
        return

    user = None
    if 'QUALTRICS_USER' not in os.environ:
        user = input('Enter Qualtrics username: ')
    token = None
    if 'QUALTRICS_TOKEN' not in os.environ:
        token = input('Enter Qualtrics token: ')
    qualtrics = Qualtrics(user, token)
    method = getattr(qualtrics, command)
    if not method:
        print '%s API call is not implement' % method
        return
    else:
        for option in argv:
            try:
                arg, value = option.split('=')
                kwargs[arg] = value
            except ValueError:
                pass

        return method(**kwargs)


if __name__ == '__main__':
    result = main(sys.argv)
    if result is None:
        print 'Error executing API Call'
    else:
        print 'Success: %s' % result