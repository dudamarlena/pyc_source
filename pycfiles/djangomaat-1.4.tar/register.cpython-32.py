# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/germanoguerrini/Developer/github/django-maat/djangomaat/register.py
# Compiled at: 2015-02-03 06:23:21
from __future__ import unicode_literals
from django.db.models.base import ModelBase
try:
    from django.contrib.contenttypes.fields import GenericRelation
except ImportError:
    from django.contrib.contenttypes.generic import GenericRelation

from .exceptions import ModelNotRegistered, ModelAlreadyRegistered
from .models import MaatRanking

def get_handler_instance(model, handler_class, options):
    """ Returns an handler instance for the given *model*. """
    handler = handler_class(model)
    for key, value in options.items():
        setattr(handler, key, value)

    return handler


def contribute_to_class(model, related_name=None):
    """
    Adds a 'maat_ranking' attribute to each instance of model.
    The attribute is a generic relation to MaatRanking, used by the
    handler to retrieve the ordered queryset.
    """
    try:
        generic_relation = GenericRelation(MaatRanking, related_query_name=related_name)
    except TypeError:
        generic_relation = GenericRelation(MaatRanking, related_name=related_name)

    generic_relation.contribute_to_class(model, 'maat_ranking')


class MaatRegister(object):
    """
    Register class.
    """

    def __init__(self):
        self._registry = {}

    def get_handler_for_model(self, model):
        """
        Returns an handler for the given *model*. If the model has not been
        registered, it raises a *ModelNotRegistered* exception.
        """
        try:
            return self._registry[model]
        except KeyError:
            raise ModelNotRegistered('Model {} is not handled'.format(model))

    def get_registered_handlers(self):
        """ Returns a list of all the registered handlers. """
        return list(self._registry.values())

    def register(self, model_or_iterable, handler_class, **kwargs):
        """
        Registers a model or a list of models to be handled by *handler_class*.
        Once registered, a model gains a new attribute *maat* which can be
        used to retrieve an ordered queryset.

        Eg:

            from djangomaat.register import maat

            maat.register(Article, ArticleMaatHandler)

            ordered_article_list = Article.maat.ordered_by('popularity')

        Plus, the management command `populate_maat_ranking` will
        automatically process the model.
        """
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [
             model_or_iterable]
        for model in model_or_iterable:
            if model in self._registry:
                try:
                    model_name = model._meta.model_name
                except AttributeError:
                    model_name = model._meta.module_name

                raise ModelAlreadyRegistered('The model {} is already registered.'.format(model_name))
            handler = get_handler_instance(model, handler_class, kwargs)
            self._registry[model] = handler
            contribute_to_class(model, handler.related_name)

    def unregister(self, model_or_iterable):
        """ Do not use it. Just for testing, really. """
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [
             model_or_iterable]
        for model in model_or_iterable:
            if model in self._registry:
                del self._registry[model]
                continue


maat = MaatRegister()