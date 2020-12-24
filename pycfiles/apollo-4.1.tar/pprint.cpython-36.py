# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/apogee/utils/pprint.py
# Compiled at: 2019-06-15 16:47:39
# Size of source mod 2**32: 1794 bytes
import numpy as np

class Colors:
    HEADER = '\x1b[95m'
    OKBLUE = '\x1b[94m'
    OKGREEN = '\x1b[92m'
    WARNING = '\x1b[93m'
    FAIL = '\x1b[91m'
    ENDC = '\x1b[0m'
    BOLD = '\x1b[1m'
    UNDERLINE = '\x1b[4m'


def pprint_marginals(network, marginals, n=4, percent=True):
    for variable, marginal in marginals.items():
        print('=' * 50)
        if len(network[variable].parents) > 0:
            print(variable, '|', ', '.join(network[variable].parents))
        else:
            print(variable)
        print('-' * 50)
        probs = np.asarray(list(marginal.values()))
        if percent:
            statement = lambda x, y: ('{0}: {1:.' + str(n) + '}%').format(x, y * 100)
        else:
            statement = lambda x, y: ('{0}: {1:.' + str(n) + '}').format(x, y)
        if np.max(probs) == 1.0:
            idx = np.argmax(probs)
            for i, (state, prob) in enumerate(marginal.items()):
                if i == idx:
                    print(Colors.BOLD + Colors.OKGREEN + statement(state, prob) + Colors.ENDC)
                else:
                    print(Colors.FAIL + statement(state, prob) + Colors.ENDC)

        elif (np.allclose)(*probs):
            for i, (state, prob) in enumerate(marginal.items()):
                print(Colors.OKBLUE + statement(state, prob) + Colors.ENDC)

        else:
            idx = np.argmax(probs)
            for i, (state, prob) in enumerate(marginal.items()):
                if i == idx:
                    print(Colors.OKGREEN + statement(state, prob) + Colors.ENDC)
                else:
                    print(Colors.OKBLUE + statement(state, prob) + Colors.ENDC)

    print('-' * 50)