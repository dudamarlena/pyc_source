# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/transmart/api/v2/constraints/composite.py
# Compiled at: 2019-08-27 08:40:44
# Size of source mod 2**32: 16794 bytes
"""
* Copyright (c) 2015-2017 The Hyve B.V.
* This code is licensed under the GNU General Public License,
* version 3.
"""
import json, abc, arrow
from functools import wraps
from . import atomic
from ..widgets import ConceptPicker, ConstraintWidget
from ...commons import INPUT_DATE_FORMATS, input_check

class InvalidConstraint(Exception):
    pass


def bind_widget_tuple(target, pos):
    """
    :param target: widget to bind to.
    :param pos: position in tuple.
    """

    def bind_decorator(func):

        @wraps(func)
        def wrapper(self, value):
            try:
                try:
                    if value is not None:
                        w = getattr(self._details_widget, target)
                        with w.hold_sync():
                            state = list(w.value)
                            state[pos] = value
                            w.value = tuple(state)
                except AttributeError:
                    pass

            finally:
                return

            return func(self, value)

        return wrapper

    return bind_decorator


def bind_widget_factory(callable_):

    def bind_widget_type(target, *args):

        def bind_decorator(func):

            @wraps(func)
            def wrapper(self, value):
                try:
                    try:
                        w = getattr(self._details_widget, target)
                        with w.hold_sync():
                            w.value = callable_(value, *args)
                    except AttributeError:
                        pass

                finally:
                    return

                return func(self, value)

            return wrapper

        return bind_decorator

    return bind_widget_type


bind_widget_list = bind_widget_factory(lambda x: if x is None:
() # Avoid dead code: tuple(x))
bind_widget_date = bind_widget_factory(lambda x: arrow.get(x, INPUT_DATE_FORMATS).date())

class Queryable(abc.ABC):

    @abc.abstractmethod
    def json(self):
        pass


class Grouper(abc.ABC):

    def __and__(self, other):
        return self._Grouper__grouper_logic(other, is_and=True)

    def __or__(self, other):
        return self._Grouper__grouper_logic(other, is_and=False)

    def __grouper_logic(self, other, is_and):
        """ ObsConstraint """
        my_type, not_my_type = ('and', 'or') if is_and else ('or', 'and')
        if isinstance(other, Grouper):
            return GroupConstraint([self, other], my_type)
        if isinstance(other, GroupConstraint):
            if other.group_type == my_type:
                other.items.append(self)
                return other
            if other.group_type == not_my_type:
                return GroupConstraint([self, other], my_type)


class GroupConstraint(Queryable):
    __doc__ = '\n    Group constraint combines ObservationConstraints and results in a\n    subject set. It operates using and/or.\n    '

    def __init__(self, items, group_type):
        self.items = items
        self.group_type = group_type

    def __str__(self):
        return json.dumps(self.json())

    def __repr__(self):
        return '{}({})'.format(self.group_type, self.items)

    def __and__(self, other):
        return self._GroupConstraint__grouper_logic(other, is_and=True)

    def __or__(self, other):
        return self._GroupConstraint__grouper_logic(other, is_and=False)

    def __grouper_logic(self, other, is_and):
        my_type, not_my_type = ('and', 'or') if is_and else ('or', 'and')
        if isinstance(other, Grouper):
            if self.group_type == my_type:
                return GroupConstraint(self.items.copy() + [other], my_type)
            return GroupConstraint([self, other], my_type)
        else:
            if isinstance(other, self.__class__):
                if other.group_type == my_type:
                    return GroupConstraint(other.items.copy() + [self], my_type)
                if other.group_type == not_my_type:
                    if self.group_type == my_type:
                        return GroupConstraint(self.items.copy() + [other], my_type)
                return GroupConstraint([self, other], my_type)

    def subselect(self, dimension='patient'):
        return {'type':'subselection',  'dimension':dimension, 
         'constraint':self.json()}

    def json(self):
        return {'type':self.group_type, 
         'args':[item.subselect() for item in self.items]}


def _find_query_methods(obj):
    for method_name in dir(obj):
        if method_name.startswith('__'):
            continue
        method = getattr(obj, method_name)
        if getattr(method, '__query_method__', False):
            yield (
             method_name, method)


def override_defaults(method, **defaults):

    @wraps(method)
    def wrapper(*args, **kwargs):
        return method(args, **defaults, **kwargs)

    return wrapper


class ObservationConstraint(Queryable, Grouper):
    __doc__ = '\n    Represents constraints on observation level. This is the set of\n    observations that adhere to all criteria specified. A patient set\n    based on these constraints can be combined with other sets to\n    create complex queries.\n    '
    params = {'concept':atomic.ConceptCodeConstraint,  'study':atomic.StudyConstraint, 
     'trial_visit':atomic.TrialVisitConstraint, 
     'min_value':atomic.MinValueConstraint, 
     'max_value':atomic.MaxValueConstraint, 
     'min_date_value':atomic.MinDateValueConstraint, 
     'max_date_value':atomic.MaxDateValueConstraint, 
     'value_list':atomic.ValueListConstraint, 
     'min_start_date':atomic.StartTimeAfterConstraint, 
     'max_start_date':atomic.StartTimeBeforeConstraint, 
     'subject_set_id':atomic.SubjectSetConstraint}

    def __init__(self, concept: str=None, study: str=None, trial_visit: list=None, min_value=None, max_value=None, value_list=None, min_start_date=None, max_start_date=None, min_date_value=None, max_date_value=None, subject_set_id=None, subselection=None, api=None):
        """
        Represents constraints on observation level. This is the set of
        observations that adhere to all criteria specified. A patient set
        based on these constraints can be combined with other sets to
        create complex queries.

        :param concept:
        :param study:
        :param trial_visit:
        :param min_value:
        :param max_value:
        :param min_date_value:
        :param max_date_value:
        :param min_start_date:
        :param max_start_date:
        :param subject_set_id:
        :param subselection:
        :param api:
        """
        self._ObservationConstraint__concept = None
        self._ObservationConstraint__trial_visit = None
        self._ObservationConstraint__value_list = None
        self._ObservationConstraint__min_value = None
        self._ObservationConstraint__max_value = None
        self._ObservationConstraint__min_start_date = None
        self._ObservationConstraint__max_start_date = None
        self._ObservationConstraint__min_date_value = None
        self._ObservationConstraint__max_date_value = None
        self._ObservationConstraint__subject_set_id = None
        self._ObservationConstraint__subselection = None
        self._dimension_elements = None
        self._aggregates = None
        self.study = None
        self.api = api
        if api is not None:
            self._details_widget = ConstraintWidget(self)
            for name, method in _find_query_methods(api):
                self.__dict__[name] = self._constraint_method_factory(method)

        self.concept = concept
        self.trial_visit = trial_visit
        self.value_list = value_list
        self.study = study
        self.min_value = min_value
        self.max_value = max_value
        self.min_start_date = min_start_date
        self.max_start_date = max_start_date
        self.min_date_value = min_date_value
        self.max_date_value = max_date_value
        self.subject_set_id = subject_set_id
        self.subselection = subselection

    def __len__(self):
        len_ = 0
        for arg in self.params.keys():
            if getattr(self, arg) is not None:
                len_ += 1

        return len_

    def __repr__(self):
        arguments = []
        for arg in self.params.keys():
            if getattr(self, arg) is not None:
                arguments.append('{}={}'.format(arg, repr(getattr(self, arg))))

        return '{}({})'.format(self.__class__.__name__, ', '.join(arguments))

    def __str__(self):
        return json.dumps(self.json())

    def json(self):
        args = []
        if len(self) == 0:
            args.append({'type': 'true'})
        else:
            for param, constraint in self.params.items():
                attr = getattr(self, param)
                if attr is not None:
                    args.append(constraint(attr).json())

            if len(self) > 1:
                constraint = dict()
                constraint['args'] = args
                constraint['type'] = 'and'
            else:
                constraint = args.pop()
        if self.subselection is not None:
            return dict(type='subselection', dimension=(self.subselection),
              constraint=constraint)
        return constraint

    def subselect(self, dimension='patient'):
        """
        Query that represents all dimension elements that adhere to the
        observation constraints, e.g. all patients that have observations
        for which the criteria apply.

        :param dimension: only patients is supported for now.
        :return: criteria dictionary.
        """
        current = self.subselection
        try:
            self.subselection = dimension
            return self.json()
        finally:
            self.subselection = current

    def _constraint_method_factory(self, method):

        @wraps(method)
        def wrapper(*args, **kwargs):
            func = override_defaults(method, api=(self.api), constraint=self)
            return func(*args, **kwargs)

        for name, child in _find_query_methods(method):
            wrapper.__dict__[name] = override_defaults(child, api=(self.api), constraint=self)

        return wrapper

    @property
    def trial_visit(self):
        """
        List of trial visits by id.
        """
        return self._ObservationConstraint__trial_visit

    @trial_visit.setter
    @input_check((list,))
    @bind_widget_list('trial_visit_select')
    def trial_visit(self, value):
        self._ObservationConstraint__trial_visit = value

    @property
    def value_list(self):
        """
        List of categorical options.
        """
        return self._ObservationConstraint__value_list

    @value_list.setter
    @input_check((list,))
    @bind_widget_list('categorical_select')
    def value_list(self, value):
        self._ObservationConstraint__value_list = value

    @property
    def min_value(self):
        """
        Minimum value for numerical concepts, int or float.
        """
        return self._ObservationConstraint__min_value

    @min_value.setter
    @input_check((int, float))
    @bind_widget_tuple('numeric_range', 0)
    def min_value(self, value):
        self._ObservationConstraint__min_value = value

    @property
    def max_value(self):
        """
        Maximum value for numerical concepts, int or float.
        """
        return self._ObservationConstraint__max_value

    @max_value.setter
    @input_check((int, float))
    @bind_widget_tuple('numeric_range', 1)
    def max_value(self, value):
        self._ObservationConstraint__max_value = value

    @property
    def min_date_value(self):
        """
        Minimum value for date concepts, formatted as 'D-M-YYYY', or 'YYYY-M-D'.
        """
        return self._ObservationConstraint__min_date_value

    @min_date_value.setter
    @input_check((str,))
    @bind_widget_date('date_value_min')
    def min_date_value(self, value):
        self._ObservationConstraint__min_date_value = value

    @property
    def max_date_value(self):
        """
        Maximum value for date concepts, formatted as 'D-M-YYYY', or 'YYYY-M-D'.
        """
        return self._ObservationConstraint__max_date_value

    @max_date_value.setter
    @input_check((str,))
    @bind_widget_date('date_value_max')
    def max_date_value(self, value):
        self._ObservationConstraint__max_date_value = value

    @property
    def concept(self):
        return self._ObservationConstraint__concept

    @concept.setter
    def concept(self, value):
        self._ObservationConstraint__concept = value

    @property
    def max_start_date(self):
        return self._ObservationConstraint__max_start_date

    @max_start_date.setter
    @input_check((str,))
    @bind_widget_date('max_start_before')
    def max_start_date(self, value):
        self._ObservationConstraint__max_start_date = value

    @property
    def min_start_date(self):
        return self._ObservationConstraint__min_start_date

    @min_start_date.setter
    @input_check((str,))
    @bind_widget_date('max_start_since')
    def min_start_date(self, value):
        self._ObservationConstraint__min_start_date = value

    @property
    def subject_set_id(self):
        return self._ObservationConstraint__subject_set_id

    @subject_set_id.setter
    @input_check((int,))
    def subject_set_id(self, value):
        self._ObservationConstraint__subject_set_id = value

    @property
    def subselection(self):
        return self._ObservationConstraint__subselection

    @subselection.setter
    @input_check((str,))
    def subselection(self, value):
        self._ObservationConstraint__subselection = value

    @classmethod
    def from_tree_node(cls, constraints):
        c = cls()
        c.apply_tree_node_constraints(constraints)
        return c

    def apply_tree_node_constraints(self, constraints):
        """
        Reset current argument and apply those from a tree node constraints dict.

        :param constraints: constraints from tree node.
        """
        keyword_map = [
         ('concept', 'conceptCode'),
         ('study', 'studyId')]
        if not constraints:
            raise ValueError('Expected dict, got {!r}'.format(type(constraints)))
        for arg in self.params.keys():
            setattr(self, arg, None)

        try:
            constraint_list = constraints['args']
        except KeyError:
            constraint_list = [
             constraints]

        for c in constraint_list:
            for kw in keyword_map:
                if c.get(kw[1]):
                    setattr(self, kw[0], c.get(kw[1]))

        if self.api is not None:
            self.fetch_updates()

    def _dimension_elements_watcher(self):

        def watcher(key, value):
            if value is None:
                return
            elif key == 'trial visit':
                self._details_widget.update_trial_visits(value)
            else:
                if key == 'start time':
                    self._details_widget.update_start_time(value)

        class DictWatcher(dict):

            def __setitem__(self, key, value):
                watcher(key, value)
                super().__setitem__(key, value)

        return DictWatcher()

    def fetch_updates(self):
        if self.api is not None:
            if self.api.interactive:
                self._details_widget.disable_all()
                self._details_widget.update_obs_repr()
                agg_response = self.api.observations.aggregates_per_concept(self)
                self._aggregates = agg_response.get('aggregatesPerConcept', {}).get(self.concept, {})
                self._details_widget.update_from_aggregates(self._aggregates)
                self._dimension_elements = self._dimension_elements_watcher()
                for dimension in ('trial visit', 'start time'):
                    self._dimension_elements[dimension] = self.api.dimension_elements(dimension, self).get('elements')

    def find_concept(self, search_string: str=None):
        """

        :param search_string: Optionally pre-fill the search field
        :return:
        """
        if self.api is None:
            raise AttributeError('{}.api not set. Cannot be interactive.'.format(self.__class__))
        cp = ConceptPicker(target=(self.apply_tree_node_constraints), api=(self.api))
        if search_string is not None:
            cp.search_bar.value = str(search_string)
        return cp.get()

    def interact(self):
        return self._details_widget.get()


class RelationConstraint(Queryable, Grouper):
    __doc__ = '\n    Query that operates on relationships between subject sets.\n    '

    def __init__(self, constraint, type_label):
        self.constraint = constraint
        self.type_label = type_label

    def json(self):
        return {'type':'subselection', 
         'dimension':'patient', 
         'constraint':{'type':'relation', 
          'relatedSubjectsConstraint':self.constraint.json(), 
          'relationTypeLabel':self.type_label}}

    def subselect(self):
        return self.json()