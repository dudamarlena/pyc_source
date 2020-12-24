# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/jik/.virtualenvs/coal-mine/lib/python3.6/site-packages/coal_mine/abstract_store.py
# Compiled at: 2016-08-09 17:39:55
# Size of source mod 2**32: 3427 bytes
__doc__ = '\nAbstract store for Coal Mine\n\nSubclass for a specific storage engine.\n'
from abc import ABCMeta, abstractmethod

class AbstractStore(object, metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, *args, **kwargs):
        """Args and behavior are dependent on the storage engine."""
        raise NotImplementedError('__init__')

    @abstractmethod
    def create(self, canary):
        """Make sure you copy the data in `canary` rather than storing the dict
        internally."""
        raise NotImplementedError('create')

    @abstractmethod
    def update(self, identifier, updates):
        raise NotImplementedError('update')

    @abstractmethod
    def get(self, identifier):
        """Should raise KeyError if not found, or return a dict with these keys: id,
        name, description, slug, periodicity, emails, late, paused, deadline,
        history. History should be a list of tuples, each of which contains a
        naive UTC timestamp and a possibly empty comment, sorted from most to
        least recent. Deadline should be a naive UTC timestamp.

        NOTE: The caller could modify the dict you return, so don't return
        anything you have a pointer to internally! If you need to return a dict
        which you're also using internally, then deepcopy it."""
        raise NotImplementedError('get')

    @abstractmethod
    def list(self, *, verbose=False, paused=None, late=None, search=None):
        """Return an iterator which yields dicts (but see the note on get()). If
        verbose is False, then the dicts contain only name and id, otherwise,
        all fields (same as returned by get()) are returned. If paused, late,
        and/or search are specified, they are used to filter the results. The
        latter is a regular expression (string, not regular expression object),
        which is matched against the name, slug, and id of canaries and only
        matches are returned."""
        raise NotImplementedError('list')

    @abstractmethod
    def upcoming_deadlines(self):
        """Return an iterator which yields canaries (same as returned by get(); see in
        particular the note there) that are unpaused and not yet late, sorted
        by deadline in increasing order, i.e., the canary that will pass its
        deadline soonest is returned first."""
        raise NotImplementedError('upcoming_deadlines')

    @abstractmethod
    def delete(self, identifier):
        """Raise KeyError if a canary with the specified identifier
        doesn't exist."""
        raise NotImplementedError('delete')

    @abstractmethod
    def find_identifier(self, slug):
        """Should raise KeyError if a canary with the specified slug
        does not exist, or return the identifier string."""
        raise NotImplementedError('find_identifier')