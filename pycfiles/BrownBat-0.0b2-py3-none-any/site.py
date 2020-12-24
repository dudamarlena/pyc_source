# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/brownant/site.py
# Compiled at: 2014-10-08 05:32:06
from __future__ import absolute_import, unicode_literals

class Site(object):
    """The site supported object which could be mounted to app instance.

    :param name: the name of the supported site.
    """

    def __init__(self, name):
        self.name = name
        self.actions = []

    def record_action(self, method_name, *args, **kwargs):
        """Record the method-calling action.

        The actions expect to be played on an target object.

        :param method_name: the name of called method.
        :param args: the general arguments for calling method.
        :param kwargs: the keyword arguments for calling method.
        """
        self.actions.append((method_name, args, kwargs))

    def play_actions(self, target):
        """Play record actions on the target object.

        :param target: the target which recive all record actions, is a brown
                       ant app instance normally.
        :type target: :class:`~brownant.app.Brownant`
        """
        for method_name, args, kwargs in self.actions:
            method = getattr(target, method_name)
            method(*args, **kwargs)

    def route(self, host, rule, **options):
        """The decorator to register wrapped function as the brown ant app.

        All optional parameters of this method are compatible with the
        :meth:`~brownant.app.Brownant.add_url_rule`.

        Registered functions or classes must be import-able with its qualified
        name. It is different from the :class:`~flask.Flask`, but like a
        lazy-loading mode. Registered objects only be loaded before the first
        using.

        The right way::

            @site.route("www.example.com", "/item/<int:item_id>")
            def spam(request, item_id):
                pass

        The wrong way::

            def egg():
                # the function could not be imported by its qualified name
                @site.route("www.example.com", "/item/<int:item_id>")
                def spam(request, item_id):
                    pass

            egg()

        :param host: the limited host name.
        :param rule: the URL path rule as string.
        :param options: the options to be forwarded to the
                        :class:`werkzeug.routing.Rule` object.
        """

        def decorator(func):
            endpoint = (b'{func.__module__}:{func.__name__}').format(func=func)
            self.record_action(b'add_url_rule', host, rule, endpoint, **options)
            return func

        return decorator