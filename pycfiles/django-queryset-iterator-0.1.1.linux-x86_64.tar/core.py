# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gxx/projects/queryset_iterator/virtualenv/lib/python2.7/site-packages/queryset_iterator/core.py
# Compiled at: 2014-09-14 06:11:29
"""
Contains the queryset_iterator function.
This function is useful for iterating over large querysets with Django.
"""
import gc
GC_COLLECT_BATCH = 1
GC_COLLECT_END = 2

def queryset_iterator(queryset, batchsize=500, gc_collect=GC_COLLECT_BATCH):
    """Iterate over a Django queryset in efficient batches

    :param queryset: The queryset to iterate over in batches.
    :type queryset: QuerySet
    :param batchsize: The batch size used to process the queryset. Defaults to 500.
    :type batchsize: int
    :param gc_collect: Whether to garbage collect between batches, at end or not at all.
        Defaults to GC_COLLECT_BATCH.
    :type gc_collect: int
    :yield: Items within the queryset, one at a time, transparently from batches.
    """
    if batchsize < 1:
        raise ValueError('Batch size must be above 0')
    if not isinstance(batchsize, int):
        raise TypeError('batchsize must be an integer')
    iterator = queryset.values_list('pk', flat=True).distinct().iterator()
    while True:
        pk_buffer = []
        try:
            try:
                while len(pk_buffer) < batchsize:
                    pk_buffer.append(iterator.next())

            except StopIteration:
                break

        finally:
            for result in queryset.filter(pk__in=pk_buffer).iterator():
                yield result

            if gc_collect == GC_COLLECT_BATCH and pk_buffer:
                gc.collect()

    if gc_collect == GC_COLLECT_END:
        gc.collect()