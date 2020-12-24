# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/tests/learners/dp_learner_many_test.py
# Compiled at: 2018-07-18 16:52:13
# Size of source mod 2**32: 1344 bytes
import platform, subprocess, sys

def dp_learner_many_test():
    """
    Used to test the data poisoning learners.
    Use like - python3 adlib/tests/learners/dp_learner_many_test.py 30 label-flipping
    to run 30 tests of label flipping, writing the results to the CWD.
    """
    if 'window' in platform.system().lower():
        print('Cannot use this script to automate testing on Windows.')
        exit(1)
    try:
        subprocess.run(['unbuffer', 'echo'])
    except:
        print('Need command unbuffer - install expect package.')
        exit(1)

    num_runs = int(sys.argv[1]) if len(sys.argv) >= 2 else 30
    attacker = sys.argv[2].lower() if len(sys.argv) == 3 else 'dummy'
    for i in range(num_runs):
        print('START run:', i + 1)
        command = ['unbuffer', 'python3', 'adlib/tests/learners/dp_learner_test.py', attacker]
        ps = subprocess.Popen(command, stdout=(subprocess.PIPE), stderr=(subprocess.STDOUT))
        subprocess.check_output(['tee', './dp-' + attacker + '-' + str(i + 1) + '.txt'], stdin=(ps.stdout))
        ps.wait()
        print('END run:', i + 1)


if __name__ == '__main__':
    dp_learner_many_test()