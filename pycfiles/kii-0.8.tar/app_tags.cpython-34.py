# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/app/templatetags/app_tags.py
# Compiled at: 2015-01-18 07:28:37
# Size of source mod 2**32: 1737 bytes
from django import template
from django.db import models
from django.core.urlresolvers import NoReverseMatch
register = template.Library()

@register.assignment_tag
def node_url(node, **kwargs):
    """
    Typical usage (look at ``kii/glue/templates/default/glue/menu_node.html``
    for a real example):

    .. code-block:: html+django

        {% load app_tags %}

        {% with node=app.menu %}

            {% node_url node as url %}
            <a href="{{ url }}">My app root menu node</a>

            {% for child_node in node.children %}

                {% node_url child_node as child_url %}
                <a href="{{ child_url }}">A child node</a>

            {% endfor %}
        {% endwith %}

    :param node: a :py:class:`kii.app.menu.MenuNode` instance
    :param kwargs: kwargs that will be passed to the :py:func:`reverse`    function
    :return: the target URL of the menu node
    """
    return node.url(**kwargs)


@register.assignment_tag
def model_url(model, suffix, **kwargs):
    """
    Return a model-related URL. Usage:

    .. code-block:: html+django

        {% load app_tags %}

        {% model_url my_object "delete" as url %}
        {% if url %}
            {{ url }}
        {% endif %}
        
    Will ouptut something like ``/myapp/mymodel/12/delete`` if the URL exists.

    Model can be an instance or a :py:class:`Model` subclass.

    This tag will fail silently if the URL is not foun and return an empty string.
    """
    try:
        if isinstance(model, models.Model):
            return model.reverse(suffix, **kwargs)
        if issubclass(model, models.Model):
            return model.class_reverse(suffix, **kwargs)
    except NoReverseMatch:
        return ''