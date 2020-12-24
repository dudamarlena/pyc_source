# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fixture/loadable/google_datastore_loadable.py
# Compiled at: 2017-10-02 03:31:12
# Size of source mod 2**32: 2746 bytes
"""
Components for loading and unloading data using the Google App Engine `Datastore`_.

Added in version 1.1

.. _Datastore: http://code.google.com/appengine/docs/datastore/

"""
from fixture.loadable import EnvLoadableFixture

class EntityMedium(EnvLoadableFixture.StorageMediumAdapter):
    __doc__ = '\n    Adapts google.appengine.api.datastore.Entity objects and any \n    other object that is an instance of Entity\n    '

    def _entities_to_keys(self, mylist):
        """Converts an array of datastore objects to an array of keys.
        
        if the value passed in is not a list, this passes it through as is
        """
        if type(mylist) == type([]):
            if all(map(lambda x: hasattr(x, 'key'), mylist)):
                return [ent.key() for ent in mylist]
            else:
                return mylist
        else:
            return mylist

    def clear(self, obj):
        """Delete this entity from the Datastore"""
        obj.delete()

    def save(self, row, column_vals):
        """Save this entity to the Datastore"""
        gen = [(k, self._entities_to_keys(v)) for k, v in column_vals]
        entity = (self.medium)(**dict(gen))
        entity.put()
        return entity


class GoogleDatastoreFixture(EnvLoadableFixture):
    __doc__ = '\n    A fixture that knows how to load DataSet objects into Google Datastore `Entity`_ objects.\n    \n    >>> from fixture import GoogleDatastoreFixture\n    \n    See :ref:`Using Fixture With Google App Engine <using-fixture-with-appengine>` for a complete example.\n    \n    .. _Entity: http://code.google.com/appengine/docs/datastore/entitiesandmodels.html\n    \n    Keyword Arguments:\n    \n    ``style``\n        A :class:`Style <fixture.style.Style>` object to translate names with\n    \n    ``env``\n        A dict or module that contains Entity classes.  This will be searched when \n        :class:`Style <fixture.style.Style>` translates DataSet names into\n        storage media.  See :meth:`EnvLoadableFixture.attach_storage_medium <fixture.loadable.loadable.EnvLoadableFixture.attach_storage_medium>` for details on \n        how ``env`` works.\n    \n    ``dataclass``\n        :class:`SuperSet <fixture.dataset.SuperSet>` class to represent loaded data with\n    \n    ``medium``\n        A custom :class:`StorageMediumAdapter <fixture.loadable.loadable.StorageMediumAdapter>` \n        class to instantiate when storing a DataSet.\n        By default, an Entity adapter will be used so you should only set a custom medium \n        if you know what you doing.\n    \n    Added in version 1.1\n    '
    Medium = EntityMedium

    def commit(self):
        pass

    def rollback(self):
        pass