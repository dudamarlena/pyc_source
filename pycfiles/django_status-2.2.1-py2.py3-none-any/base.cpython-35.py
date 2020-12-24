# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/perdy/Development/django-status/status/providers/base.py
# Compiled at: 2016-09-29 07:57:11
# Size of source mod 2**32: 2219 bytes
import importlib
from status import settings
__all__ = [
 'Provider', 'Resource']

class Provider:
    __doc__ = '\n    Wrapper that handles a check provider, giving easy access to them with dynamic imports from string.\n    '

    def __init__(self, name, provider, args, kwargs):
        """
        Create a provider.

        :param name: Provider name.
        :param provider: Provider function or string.
        :param args: Provider args.
        :param kwargs: Provider kwargs.
        """
        self.name = name
        if isinstance(provider, str):
            provider_module, provider_func = provider.rsplit('.', 1)
            module = importlib.import_module(provider_module)
            self.provider = getattr(module, provider_func, None)
            if self.provider is None:
                raise ValueError('Provider not found: %s' % (provider,))
        else:
            self.provider = provider
        self.args = args or ()
        self.kwargs = kwargs or {}

    def __call__(self, *args, **kwargs):
        """
        Return provider results.

        :param args: Provider args.
        :param kwargs: Provider kwargs
        :return: Results after evaluates provider.
        """
        if not args:
            args = self.args
        if not kwargs:
            kwargs = self.kwargs
        return self.provider(*args, **kwargs)


class Resource:
    __doc__ = '\n    Wrapper that handles a whole resource with its providers.\n    '

    def __init__(self, name):
        """
        Create a resource and all its providers.

        :param name: Resource name
        """
        self.name = name
        try:
            self.providers = {name:Provider(name=name, provider=provider, args=args, kwargs=kwargs) for name, provider, args, kwargs in settings.PROVIDERS[self.name]}
        except KeyError:
            raise ValueError("Resource doesn't exists: %s" % (self.name,))

    def __call__(self, *args, **kwargs):
        """
        Return results from all providers of this resource.

        :return: Results after evaluate each provider.
        """
        return {name:provider() for name, provider in self.providers.items()}