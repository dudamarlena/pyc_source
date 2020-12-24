# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/commandline/randomize_option.py
# Compiled at: 2009-10-07 18:08:46
import parsing
parsing.parser.add_option('--randomize-order', action='store_true', help='Randomize the test order')
parsing.parser.add_option('--randomize-seed', metavar='SEED', type='int', help='Seed for randomizing the test order, implies --randomize-order')

def non_negative_seed():
    """
    Returns a non-negative int as seed, based on time.time

    The seed is based on time.time, os.urandom may be used in the
    future (like it is in module 'random')
    """
    import time
    while True:
        result = hash(time.time())
        if result >= 0:
            return result


def randomize_order(seed):
    if seed is None:
        seed = non_negative_seed()
    import sys
    print >> sys.stderr, 'seed=%s' % seed
    from testoob import extracting
    parsing.kwargs['extraction_decorators'].append(extracting.randomize(seed))
    return


def process_options(options):
    if options.randomize_order is not None or options.randomize_seed is not None:
        randomize_order(options.randomize_seed)
    return


parsing.option_processors.append(process_options)