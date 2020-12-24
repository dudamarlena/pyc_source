# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\extra\django\_impl.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 7997 bytes
import unittest
from functools import partial
from typing import Type, Union
import django.db.models as dm
import django.forms as df
import django.test as dt
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import hypothesis.strategies._internal.core as st
from hypothesis import reject
from hypothesis.errors import InvalidArgument
from hypothesis.extra.django._fields import from_field
from hypothesis.utils.conventions import InferType, infer

class HypothesisTestCase:

    def setup_example(self):
        self._pre_setup()

    def teardown_example(self, example):
        self._post_teardown()

    def __call__(self, result=None):
        testMethod = getattr(self, self._testMethodName)
        if getattr(testMethod, 'is_hypothesis_test', False):
            return unittest.TestCase.__call__(self, result)
        return dt.SimpleTestCase.__call__(self, result)


class TestCase(HypothesisTestCase, dt.TestCase):
    pass


class TransactionTestCase(HypothesisTestCase, dt.TransactionTestCase):
    pass


@st.defines_strategy
def from_model(model: Type[dm.Model], **field_strategies: Union[(st.SearchStrategy, InferType)]) -> st.SearchStrategy:
    """Return a strategy for examples of ``model``.

    .. warning::
        Hypothesis creates saved models. This will run inside your testing
        transaction when using the test runner, but if you use the dev console
        this will leave debris in your database.

    ``model`` must be an subclass of :class:`~django:django.db.models.Model`.
    Strategies for fields may be passed as keyword arguments, for example
    ``is_staff=st.just(False)``.

    Hypothesis can often infer a strategy based the field type and validators,
    and will attempt to do so for any required fields.  No strategy will be
    inferred for an :class:`~django:django.db.models.AutoField`, nullable field,
    foreign key, or field for which a keyword
    argument is passed to ``from_model()``.  For example,
    a Shop type with a foreign key to Company could be generated with::

        shop_strategy = from_model(Shop, company=from_model(Company))

    Like for :func:`~hypothesis.strategies.builds`, you can pass
    :obj:`~hypothesis.infer` as a keyword argument to infer a strategy for
    a field which has a default value instead of using the default.
    """
    if not issubclass(model, dm.Model):
        raise InvalidArgument('model=%r must be a subtype of Model' % (model,))
    fields_by_name = {f:f.name for f in model._meta.concrete_fields}
    for name, value in sorted(field_strategies.items()):
        if value is infer:
            field_strategies[name] = from_field(fields_by_name[name])
    else:
        for name, field in sorted(fields_by_name.items()):
            if name not in field_strategies and not field.auto_created:
                if field.default is dm.fields.NOT_PROVIDED:
                    field_strategies[name] = from_field(field)

    for field in field_strategies:
        if model._meta.get_field(field).primary_key:
            kwargs = {field: field_strategies.pop(field)}
            kwargs['defaults'] = st.fixed_dictionaries(field_strategies)
            return _models_impl((st.builds)((model.objects.update_or_create), **kwargs))
        return _models_impl((st.builds)((model.objects.get_or_create), **field_strategies))


@st.composite
def _models_impl--- This code section failed: ---

 L. 117         0  SETUP_FINALLY        16  'to 16'

 L. 118         2  LOAD_FAST                'draw'
                4  LOAD_FAST                'strat'
                6  CALL_FUNCTION_1       1  ''
                8  LOAD_CONST               0
               10  BINARY_SUBSCR    
               12  POP_BLOCK        
               14  RETURN_VALUE     
             16_0  COME_FROM_FINALLY     0  '0'

 L. 119        16  DUP_TOP          
               18  LOAD_GLOBAL              IntegrityError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    40  'to 40'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L. 120        30  LOAD_GLOBAL              reject
               32  CALL_FUNCTION_0       0  ''
               34  POP_TOP          
               36  POP_EXCEPT       
               38  JUMP_FORWARD         42  'to 42'
             40_0  COME_FROM            22  '22'
               40  END_FINALLY      
             42_0  COME_FROM            38  '38'

Parse error at or near `POP_TOP' instruction at offset 26


@st.defines_strategy
def from_form(form: Type[df.Form], form_kwargs: dict=None, **field_strategies: Union[(st.SearchStrategy, InferType)]) -> st.SearchStrategy[df.Form]:
    """Return a strategy for examples of ``form``.

    ``form`` must be an subclass of :class:`~django:django.forms.Form`.
    Strategies for fields may be passed as keyword arguments, for example
    ``is_staff=st.just(False)``.

    Hypothesis can often infer a strategy based the field type and validators,
    and will attempt to do so for any required fields.  No strategy will be
    inferred for a disabled field or field for which a keyword argument
    is passed to ``from_form()``.

    This function uses the fields of an unbound ``form`` instance to determine
    field strategies, any keyword arguments needed to instantiate the unbound
    ``form`` instance can be passed into ``from_form()`` as a dict with the
    keyword ``form_kwargs``. E.g.::

        shop_strategy = from_form(Shop, form_kwargs={"company_id": 5})

    Like for :func:`~hypothesis.strategies.builds`, you can pass
    :obj:`~hypothesis.infer` as a keyword argument to infer a strategy for
    a field which has a default value instead of using the default.
    """
    form_kwargs = form_kwargs or {}
    if not issubclass(form, df.BaseForm):
        raise InvalidArgument('form=%r must be a subtype of Form' % (form,))
    unbound_form = form(**form_kwargs)
    fields_by_name = {}
    for name, field in unbound_form.fields.items():
        if isinstance(field, df.MultiValueField):
            for i, _field in enumerate(field.fields):
                fields_by_name['%s_%d' % (name, i)] = _field

        else:
            fields_by_name[name] = field
    else:
        for name, value in sorted(field_strategies.items()):
            if value is infer:
                field_strategies[name] = from_field(fields_by_name[name])
            for name, field in sorted(fields_by_name.items()):
                if name not in field_strategies:
                    field_strategies[name] = field.disabled or from_field(field)
                return _forms_impl(st.builds(partial(form, **form_kwargs),
                  data=(st.fixed_dictionaries(field_strategies))))


@st.composite
def _forms_impl--- This code section failed: ---

 L. 202         0  SETUP_FINALLY        12  'to 12'

 L. 203         2  LOAD_FAST                'draw'
                4  LOAD_FAST                'strat'
                6  CALL_FUNCTION_1       1  ''
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L. 204        12  DUP_TOP          
               14  LOAD_GLOBAL              ValidationError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    36  'to 36'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 205        26  LOAD_GLOBAL              reject
               28  CALL_FUNCTION_0       0  ''
               30  POP_TOP          
               32  POP_EXCEPT       
               34  JUMP_FORWARD         38  'to 38'
             36_0  COME_FROM            18  '18'
               36  END_FINALLY      
             38_0  COME_FROM            34  '34'

Parse error at or near `POP_TOP' instruction at offset 22