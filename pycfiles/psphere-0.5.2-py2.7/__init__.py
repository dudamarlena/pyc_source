# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/psphere/__init__.py
# Compiled at: 2013-04-04 22:30:59
import logging, time
from suds import MethodNotFound
logger = logging.getLogger(__name__)
__version__ = '0.5.2'
__released__ = '0.5.2'

class cached_property(object):
    """Decorator for read-only properties evaluated only once within TTL period.

    It can be used to created a cached property like this::

        import random

        # the class containing the property must be a new-style class
        class MyClass(object):
            # create property whose value is cached for ten minutes
            @cached_property(ttl=600)
            def randint(self):
                # will only be evaluated every 10 min. at maximum.
                return random.randint(0, 100)

    The value is cached  in the '_cache' attribute of the object instance that
    has the property getter method wrapped by this decorator. The '_cache'
    attribute value is a dictionary which has a key for every property of the
    object which is wrapped by this decorator. Each entry in the cache is
    created only when the property is accessed for the first time and is a
    two-element tuple with the last computed property value and the last time
    it was updated in seconds since the epoch.

    The default time-to-live (TTL) is 300 seconds (5 minutes). Set the TTL to
    zero for the cached value to never expire.

    To expire a cached property value manually just do::
    
        del instance._cache[<property name>]

    """

    def __init__(self, fget, doc=None):
        self.ttl = 300
        self.fget = fget
        self.__doc__ = doc or fget.__doc__
        self.__name__ = fget.__name__
        self.__module__ = fget.__module__

    def __get__(self, inst, owner):
        now = time.time()
        try:
            value, last_update = inst._cache[self.__name__]
            logger.info('Found cached value for %s', self.__name__)
            if self.ttl > 0 and now - last_update > self.ttl:
                logger.info('Cached value has exceeded TTL')
                raise AttributeError
        except (KeyError, AttributeError):
            logger.info('%s is not cached.', self.__name__)
            value = self.fget(inst)
            try:
                cache = inst._cache
            except AttributeError:
                cache = inst._cache = {}

            cache[self.__name__] = (
             value, now)

        return value


class ManagedObject(object):
    """The base class which all managed object's derive from.
    
   :param mo_ref: The managed object reference used to create this instance
   :type mo_ref: ManagedObjectReference
   :param client: A reference back to the psphere client object, which    we use to make calls.
   :type client: Client

    """
    _valid_attrs = set([])

    def __init__(self, mo_ref, client):
        self._cache = {}
        logger.debug('===== Have been passed %s as mo_ref: ', mo_ref)
        self._mo_ref = mo_ref
        self._client = client

    def _get_dataobject(self, name, multivalued):
        """This function only gets called if the decorated property
        doesn't have a value in the cache."""
        logger.debug('Querying server for uncached data object %s', name)
        self.update_view_data(properties=[name])
        return self._cache[name][0]

    def _get_mor(self, name, multivalued):
        """This function only gets called if the decorated property
        doesn't have a value in the cache."""
        logger.debug('Querying server for uncached MOR %s', name)
        logger.debug('Getting view for MOR')
        self.update(properties=[name])
        return self._cache[name][0]

    def flush_cache(self, properties=None):
        """Flushes the cache being held for this instance.

        :param properties: The list of properties to flush from the cache.
        :type properties: list or None (default). If None, flush entire cache.

        """
        if hasattr(self, '_cache'):
            if properties is None:
                del self._cache
            else:
                for prop in properties:
                    if prop in self._cache:
                        del self._cache[prop]

        return

    def update(self, properties=None):
        """Updates the properties being held for this instance.

        :param properties: The list of properties to update.
        :type properties: list or None (default). If None, update all
        currently cached properties.

        """
        if properties is None:
            try:
                self.update_view_data(properties=self._cache.keys())
            except AttributeError:
                pass

        else:
            self.update_view_data(properties=properties)
        return

    def _get_properties(self, properties=None):
        """Retrieve the requested properties from the server.

        :param properties: The list of properties to update.
        :type properties: list or None (default).

        """
        pass

    def update_view_data(self, properties=None):
        """Update the local object from the server-side object.
        
        >>> vm = VirtualMachine.find_one(client, filter={"name": "genesis"})
        >>> # Update all properties
        >>> vm.update_view_data()
        >>> # Update the config and summary properties
        >>> vm.update_view_data(properties=["config", "summary"]

        :param properties: A list of properties to update.
        :type properties: list

        """
        if properties is None:
            properties = []
        logger.info('Updating view data for object of type %s', self._mo_ref._type)
        property_spec = self._client.create('PropertySpec')
        property_spec.type = str(self._mo_ref._type)
        if properties is None:
            properties = []
        elif properties == 'all':
            logger.debug('Retrieving all properties')
            property_spec.all = True
        else:
            logger.debug('Retrieving %s properties', len(properties))
            property_spec.all = False
            property_spec.pathSet = properties
        object_spec = self._client.create('ObjectSpec')
        object_spec.obj = self._mo_ref
        pfs = self._client.create('PropertyFilterSpec')
        pfs.propSet = [property_spec]
        pfs.objectSet = [object_spec]
        pc = self._client.sc.propertyCollector
        object_content = pc.RetrieveProperties(specSet=pfs)[0]
        if not object_content:
            logger.error('Nothing returned from RetrieveProperties!')
        self._set_view_data(object_content)
        return

    def preload(self, name, properties=None):
        """Pre-loads the requested properties for each object in the "name"
        attribute.

        :param name: The name of the attribute containing the list to
        preload.
        :type name: str
        :param properties: The properties to preload on the objects or the
        string all to preload all properties.
        :type properties: list or the string "all"
        
        """
        if properties is None:
            raise ValueError('You must specify some properties to preload. To preload all properties use the string "all".')
        if not getattr(self, name):
            return
        else:
            mo_refs = []
            for item in getattr(self, name):
                if isinstance(item, ManagedObject) is False:
                    raise ValueError("Only ManagedObject's can be pre-loaded.")
                mo_refs.append(item._mo_ref)

            views = self._client.get_views(mo_refs, properties)
            self._cache[name] = (
             views, time.time())
            return

    def _set_view_data(self, object_content):
        """Update the local object from the passed in object_content."""
        logger.info('Setting view data for a %s', self.__class__)
        self._object_content = object_content
        for dynprop in object_content.propSet:
            if dynprop.name not in self._valid_attrs:
                logger.error("Server returned a property '%s' but the object hasn't defined it so it is being ignored." % dynprop.name)
                continue
            try:
                if not len(dynprop.val):
                    logger.info('Server returned empty value for %s', dynprop.name)
            except TypeError:
                logger.info('%s of type %s has no len!', dynprop.name, type(dynprop.val))

            try:
                cache = self._cache
            except AttributeError:
                cache = self._cache = {}

            if dynprop.val.__class__.__name__.startswith('Array'):
                logger.info('Setting value of an Array* property')
                logger.debug('%s being set to %s', dynprop.name, dynprop.val[0])
                now = time.time()
                cache[dynprop.name] = (dynprop.val[0], now)
            else:
                logger.info('Setting value of a single-valued property')
                logger.debug('DynamicProperty value is a %s: ', dynprop.val.__class__.__name__)
                logger.debug('%s being set to %s', dynprop.name, dynprop.val)
                now = time.time()
                cache[dynprop.name] = (dynprop.val, now)

    def __getattr__(self, name):
        """Overridden so that SOAP methods can be proxied.

        The magic contained here allows us to automatically access vSphere
        SOAP methods through the Python object, like:
        >>> client.si.content.rootFolder.CreateFolder(name="foo")

        This is achieved by asking the underlying SOAP service if the
        requested name is a valid method. If the method name is not valid
        then we pass the attribute retrieval back to __getattribute__
        which will use the default behaviour (i.e. just get the attribute).

        TODO: There's no checking if the SOAP method is valid for the type
        of object being called. e.g. You could do folder.Login() which would
        be totally bogus.
        
        :param name: The name of the method to call.
        :param type: str

        """
        logger.debug('Entering overridden built-in __getattr__ with %s' % name)
        client = object.__getattribute__(self, '_client')
        try:
            getattr(client.service, name)
        except MethodNotFound:
            return object.__getattribute__(self, name)

        logger.debug('Constructing proxy method %s for a %s', name, self._mo_ref._type)

        def func(**kwargs):
            result = self._client.invoke(name, _this=self._mo_ref, **kwargs)
            logger.debug('Invoke returned %s', result)
            return result

        return func