# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/geats/exceptions.py
# Compiled at: 2013-12-22 08:30:04


class AlreadyExistsException(RuntimeError):
    """
    Generated on a .create() DB call where the key already
    exists.
    """
    pass


class InvalidVMDefinition(RuntimeError):
    """
    The VM definition was deemed invalid either by the
    Manager or by the VM instance.
    """
    pass


class UnsupportedVMType(RuntimeError):
    """
    The supplied vm_type is not supported or unknown.
    """
    pass


class UnsupportedStorageType(RuntimeError):
    """
    The supplied type for a storage volume was not found
    or is not supported for this vm_type.
    """
    pass


class VMException(RuntimeError):
    """
    An arbitrary exception while performing a VM action.
    It's expected that the exception message can be returned
    directly to the user.
    """
    pass


class FailedToAcquireLockException(VMException):
    """
    Each VM has a lockfile that prevents multiple operations
    being performed on it simultaneously.
    """
    pass


class VMLockedException(VMException):
    """
    VMLockedException means that VM.is_locked() returned True
    for an operation that requires it to be false.
    Most commonly, this is to prevent a VM being accidently
    undefine'd.
    """
    pass