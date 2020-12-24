# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rmcgover/src/pushsource/src/pushsource/_impl/source.py
# Compiled at: 2020-02-03 19:38:52
# Size of source mod 2**32: 5510 bytes
import inspect, functools
from six.moves.urllib import parse

class Source(object):
    __doc__ = 'A source of push items.\n\n    This base class defines the interface for all pushsource backends.\n    Instances of a specific backend can be obtained using\n    the :meth:`~pushsource.Source.get` method.\n    '
    _BACKENDS = {}

    def __iter__(self):
        """Iterate over the push items contained within this source.

        Yields a series of :class:`~pushsource.PushItem` instances.
        """
        raise NotImplementedError()

    @classmethod
    def get(cls, source_url, **kwargs):
        """Obtain a push source from the given URL.

        Parameters:
            source_url (str)
                Specifies a push source backend and associated arguments.
                For information about push source URLs, see
                :ref:`urls`.

            kwargs (dict)
                Any additional keyword arguments to be passed into
                the backend.

        Returns:
            :class:`~pushsource.Source`
                A new Source instance initialized with the given arguments.
        """
        return (cls.get_partial)(source_url, **kwargs)()

    @classmethod
    def get_partial(cls, source_url, **kwargs):
        """Obtain a push source constructor from the given URL and arguments.

        This method returns a constructor for a push source (rather than a push source
        instance directly) so that additional arguments may be provided later.

        One of the primary uses of this method is to provide your own preconfigured
        aliases for existing backends, as described in :ref:`binding`.

        Parameters:
            source_url (str)
                Specifies a push source backend and associated arguments.
                For information about push source URLs, see
                :ref:`urls`.

            kwargs (dict)
                Any additional keyword arguments to be passed into
                the backend.

        Returns:
            callable
                A callable which accepts any number of keyword arguments
                and returns a :class:`~pushsource.Source`.
        """
        parsed = parse.urlparse(source_url)
        scheme = parsed.scheme
        klass = cls._BACKENDS[scheme]
        query = parsed.query
        if not query:
            if not parsed.netloc:
                if '=' in parsed.path:
                    query = parsed.path
        url_kwargs = parse.parse_qs(query)
        for key in url_kwargs.keys():
            value = url_kwargs[key]
            if isinstance(value, list) and len(value) == 1:
                url_kwargs[key] = value[0]

        getargspec = inspect.getfullargspec if hasattr(inspect, 'getfullargspec') else inspect.getargspec
        sig = getargspec(klass)
        if 'url' in sig.args:
            if parsed.path is not query:
                url_kwargs['url'] = parsed.path
        for key, converter in [
         (
          'threads', int),
         (
          'timeout', int)]:
            if key in url_kwargs:
                url_kwargs[key] = converter(url_kwargs[key])

        url_kwargs.update(kwargs)
        return (functools.partial)(klass, **url_kwargs)

    @classmethod
    def register_backend(cls, name, factory):
        """Register a new pushsource backend.

        This method allows registering additional backends beyond those
        shipped with the pushsource library. See :ref:`implementing` for
        more information.

        Parameters:
            name (str)
                The name of a backend. This should be a brief unique identifying
                string.

                If a backend of the given name is already registered, it will be
                overwritten.

            factory (callable)
                A callable used to create new instances of the backend.
                When invoked, this callable must return an object which implements
                the :class:`~pushsource.Source` interface.

        Raises:
            TypeError
                If ``factory`` is not callable.
        """
        if not callable(factory):
            raise TypeError('expected callable, got: %s' % repr(factory))
        cls._BACKENDS[name] = factory