# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/services/versionning/check.py
# Compiled at: 2010-05-21 08:57:51


def check_tube(repository, tube, variant=None):
    repository.check_item(tube)
    if variant is not None:
        for layer in tube.get_ordered_layers(variant=variant):
            repository.check_item(layer)

    return


def check_descriptor(repository, descriptor):
    repository.check_item(descriptor)


def check_dispatch(repository, dispatch, variant=None):
    check_tube(repository, dispatch.tube, variant=variant)
    check_descriptor(repository, dispatch.descriptor)