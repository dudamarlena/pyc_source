# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/prism_core/controllers.py
# Compiled at: 2013-05-07 22:27:45
__doc__ = '\nCore Controller.\n'
import logging
log = logging.getLogger('prism.core.controllers')

class CoreController(object):
    """
    Root manager class for managing all other controllers.
    """
    _db = None
    _controller_classes = {}

    def __init__(self, notify=None):
        self.notify = notify
        for name, cls in self._controller_classes.iteritems():
            setattr(self, name, cls(self, notify))

    @classmethod
    def _set_db(cls, session):
        if cls._db is None:
            cls._db = session
        return

    @classmethod
    def _get_db(cls):
        return cls._db

    db = property(_get_db, _set_db)

    @classmethod
    def register(cls, ctrlcls):
        assert ctrlcls.name != BaseController.name, 'Must set controller name'
        cls._controller_classes[ctrlcls.name] = ctrlcls
        return ctrlcls


register_controller = CoreController.register

class BaseController(object):
    """
    Base class for all controllers to inherit from.
    """
    name = 'base'

    def __init__(self, core, notify):
        self.core = core
        self.notify = notify

    def _set_db(self, value):
        self.core.db = value

    def _get_db(self):
        return self.core.db

    db = property(_get_db, _set_db)

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def getById(self, resource_id):
        raise NotImplementedError

    def delete(self, resource_id):
        raise NotImplementedError