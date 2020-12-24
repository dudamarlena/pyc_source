# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/getml/models/modutils.py
# Compiled at: 2020-03-16 07:21:38
# Size of source mod 2**32: 2895 bytes
import random, string

def _make_random_name():
    """Temporary name created for a :class:`pandas.DataFrame` during
    :meth:`~getml.models.MultirelModel._convert_population_table` and
    :meth:`~getml.models.MultirelModel._convert_peripheral_tables`.

    Returns:
        str:
            String consisting of "temp-" and 15 random ASCII letters.
    """
    return 'temp-' + ''.join((random.choice(string.ascii_letters) for i in range(15)))


def _print_time_taken(begin, end, msg):
    """Prints time required to fit a model.

    Args:
        begin (float): :func:`time.time` output marking the beginning
            of the training.
        end (float): :func:`time.time` output marking the end of the
            training.
        msg (str): Message to display along the duration.

    Raises:
        TypeError: If any of the input is not of proper type.

    """
    if type(begin) is not float:
        raise TypeError("'begin' must be a float as returned by time.time().")
    if type(end) is not float:
        raise TypeError("'end' must be a float as returned by time.time().")
    if type(msg) is not str:
        raise TypeError("'msg' must be a str.")
    seconds = end - begin
    hours = int(seconds / 3600)
    seconds -= float(hours * 3600)
    minutes = int(seconds / 60)
    seconds -= float(minutes * 60)
    seconds = round(seconds, 6)
    print(msg + str(hours) + 'h:' + str(minutes) + 'm:' + str(seconds))
    print('')