# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/brownant/dinergate.py
# Compiled at: 2014-10-08 06:38:51
from six import with_metaclass
from werkzeug.utils import cached_property
from brownant.pipeline.network import HTTPClientProperty

class DinergateType(type):
    """The metaclass of :class:`~brownant.dinergate.Dinergate` and its
    subclasses.

    This metaclass will give all members are instance of
    :class:`~werkzeug.utils.cached_property` default names. It is because many
    pipeline properties are subclasses of
    :class:`~werkzeug.utils.cached_property`, but them would not be created by
    decorating functions. They will has not built-in :attr:`__name__`, which
    may cause them could not cache values as expected.
    """

    def __new__(metacls, name, bases, members):
        cls = type.__new__(metacls, name, bases, members)
        for name in dir(cls):
            value = getattr(cls, name)
            if isinstance(value, cached_property) and not value.__name__:
                value.__name__ = name
                value.__module__ = cls.__module__

        return cls


class Dinergate(with_metaclass(DinergateType)):
    """The simple classify crawler.

    In order to work with unnamed properties such as the instances of
    :class:`~brownant.pipeline.base.PipelineProperty`, the meta class
    :class:`~brownant.dinergate.DinergateType` will scan subclasses of this
    class and name all unnamed members which are instances of
    :class:`~werkzeug.utils.cached_property`.

    :param request: the standard parameter passed by app.
    :type request: :class:`~brownant.request.Request`
    :param http_client: the session instance of python-requests.
    :type http_client: :class:`requests.Session`
    :param kwargs: other arguments from the URL pattern.
    """
    URL_TEMPLATE = None
    http_client = HTTPClientProperty()

    def __init__(self, request, http_client=None, **kwargs):
        self.request = request
        if http_client:
            self.http_client = http_client
        vars(self).update(kwargs)

    @property
    def url(self):
        """The fetching target URL.

        The default behavior of this property is build URL string with the
        :const:`~brownant.dinergate.Dinergate.URL_TEMPLATE`.

        The subclasses could override
        :const:`~brownant.dinergate.Dinergate.URL_TEMPLATE` or use a different
        implementation.
        """
        if not self.URL_TEMPLATE:
            raise NotImplementedError
        return self.URL_TEMPLATE.format(self=self)