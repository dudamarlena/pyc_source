# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/site/urlresolvers.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django.core.urlresolvers import NoReverseMatch, reverse

def local_site_reverse(viewname, request=None, local_site_name=None, local_site=None, args=None, kwargs=None, *func_args, **func_kwargs):
    """Reverse a URL name and return a working URL.

    This works much like Django's :py:func:`~django.core.urlresolvers.reverse`,
    but handles returning a LocalSite version of a URL when invoked with one of
    the following:

    * A ``request`` argument, representing an HTTP request to a URL within a
      LocalSite.
    * A ``local_site_name`` argument, indicating the name of the local site.
    * A ``local_site`` argument.

    Args:
        viewname (unicode):
            The name of the view to generate a URL for.

        request (django.http.HttpRequest, optional):
            The current HTTP request. The current local site can be extracted
            from this.

        local_site_name (unicode, optional):
            The name of the local site.

        local_site (reviewboard.site.models.LocalSite, optional):
            The local site.

        args (list, optional):
            Positional arguments to use for reversing in
            :py:func:`~django.core.urlresolvers.reverse`.

        kwargs (dict, optional):
            Keyword arguments to use for reversing in
             :py:func:`~django.core.urlresolvers.reverse`.

        func_args (tuple, optional):
            Additional positional arguments to pass to
            :py:func:`~django.core.urlresolvers.reverse`.

        func_kwargs (dict, optional):
            Additional keyword arguments to pass to
            :py:func:`~django.core.urlresolvers.reverse`.

    Returns:
        unicode:
        The reversed URL.

    Raises:
        django.core.urlresolvers.NoReverseMatch:
            Raised when there is no URL matching the view and arguments.
    """
    assert not (local_site_name and local_site)
    if request or local_site_name or local_site:
        if local_site:
            local_site_name = local_site.name
        elif request and not local_site_name:
            local_site_name = getattr(request, b'_local_site_name', None)
        if local_site_name:
            if args:
                new_args = [
                 local_site_name] + list(args)
                new_kwargs = kwargs
            else:
                new_args = args
                new_kwargs = {b'local_site_name': local_site_name}
                if kwargs:
                    new_kwargs.update(kwargs)
                try:
                    return reverse(viewname, args=new_args, kwargs=new_kwargs, *func_args, **func_kwargs)
                except NoReverseMatch:
                    pass

    return reverse(viewname, args=args, kwargs=kwargs, *func_args, **func_kwargs)