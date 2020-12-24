# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomislav/dev/seveno_pyutil/build/lib/seveno_pyutil/collections_utilities.py
# Compiled at: 2019-01-18 04:39:44
# Size of source mod 2**32: 1247 bytes
import itertools

def in_batches(iterable, of_size=1):
    """
    Generator that yields generator slices of iterable.

    Since it is elegant and working flawlessly, it is shameles C/P from
    https://stackoverflow.com/questions/8991506/iterate-an-iterator-by-chunks-of-n-in-python/8998040#8998040

    Warning:
        Each returned batch should be completely consumed before next batch
        is yielded. See example below to better understand what that means.

    Example::

        from seveno_pyutil import in_batches

        g = (o for o in range(10))
        for batch in in_batches(g, of_size=3):
            print(list(batch))
        # [0, 1, 2]
        # [3, 4, 5]
        # [6, 7, 8]
        # [9]

        # And don't consume whole batch before yielding another one...
        g = list(range(10))
        for batch in in_batches(g, of_size=3):
            print( [next(batch), next(batch)] )
        # [0, 1]
        # [2, 3]
        # [4, 5]
        # [6, 7]
        # [8, 9]
    """
    it = iter(iterable)
    while True:
        chunk_it = itertools.islice(it, of_size)
        try:
            first_el = next(chunk_it)
        except StopIteration:
            return
        else:
            yield itertools.chain((first_el,), chunk_it)