# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/app/menu.py
# Compiled at: 2015-01-18 07:28:37
from django.core.urlresolvers import reverse

class MenuNode(object):
    """
    Describe a menu element, and may be attached to an
    :py:class:`App <kii.app.core.App>` instance (via the :py:attr:`menu
    <kii.app.core.App.menu>` attribute) for automatic inclusion in templates.
    """
    route = '#'
    reverse = True
    parent = None
    weight = 0
    require_authentication = True
    reverse_kwargs = []

    def __init__(self, **kwargs):
        """
        :param str route: Either a relative URL, absolute URL or a django URL        name, such as ``kii:myapp:index``. Defaults to ``#``.
        :param bool reverse: Wether the given route should be reversed using        django's :py:func:`reverse` or returned 'as is'. Defaults to ``True``.
        :param parent: TODO, seems useless
        :param int weight: Indicate the importance of the node. Higher is more        important, default to ``0``.
        :param bool require_authentication: Used to determine if the node        should be shown to unauthenticated users. Defaults to ``True``.
        :param list reverse_kwargs: A list of strings that the route will        accept when reversing. Defaults to ``[]``
        :param list children: A list of children :py:class:`MenuNode` instances        that will be considered as submenus of this instance.        Defaults to ``[]``.
        :param icon: TODO, seems useless.
        
        """
        self.reverse = kwargs.get('reverse', self.reverse)
        self.route = kwargs.get('route', self.route)
        self.label = kwargs.get('label', self.route)
        self.parent = kwargs.get('parent', self.parent)
        self.title = kwargs.get('title', self.label)
        self.weight = kwargs.get('weight', self.weight)
        self.require_authentication = kwargs.get('require_authentication', self.require_authentication)
        self.icon = kwargs.get('icon', None)
        self.reverse_kwargs = kwargs.get('reverse_kwargs', self.reverse_kwargs)
        self.children = []
        for item in kwargs.get('children', []):
            self.add(item)

        return

    def url(self, **kwargs):
        """
        :param kwargs: a dictionary of values that will be used for reversing,        if the corresponding key is present in :py:attr:`self.reverse_kwargs        <MenuNode.reverse_kwargs>`
        :return: The target URL of the node, after reversing (if needed)
        """
        if self.reverse:
            expected_kwargs = {key:value for key, value in kwargs.items() if key in self.reverse_kwargs}
            return reverse(self.route, kwargs=expected_kwargs)
        return self.route

    def add(self, item):
        """
        Add a new node to the instance children and sort them by weight.

        :param item: A menu node instance
        """
        self.children.append(item)
        self.children = sorted(self.children, key=lambda i: i.weight, reverse=True)