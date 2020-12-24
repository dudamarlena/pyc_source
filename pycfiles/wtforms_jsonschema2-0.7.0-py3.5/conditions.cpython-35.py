# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wtforms_jsonschema2/conditions.py
# Compiled at: 2018-10-15 04:56:42
# Size of source mod 2**32: 3069 bytes
from collections import OrderedDict
from .utils import _get_related_view_property
from flask_appbuilder.views import BaseView
import inspect, logging
log = logging.getLogger(__name__)

class ViewCondition:
    __doc__ = '\n    Base class for view conditions.\n    '

    def __init__(self, conditions):
        self.conditions = conditions
        self.affected_views = []

    def get_json_schema(self, view):
        """Return the JSON Schema version of this condition."""
        raise NotImplementedError('get_json_schema is not implemented on {}'.format(self.__class__))


class oneOf(ViewCondition):
    __doc__ = '\n    A wtforms version of the jsonschema oneOf attribute that allows you to\n    specify that onlye one of a set of related views should be filled in, based\n    on the values of other fields.\n\n    It should receive a dictionary where the keys are related views\n    and the value is a dictionary of property/value combinations that\n    when satisfied, mean that related view should be required\n    (and not the others).\n    '

    def __init__(self, conditions):
        super().__init__(conditions)
        for k in conditions.keys():
            if inspect.isclass(k) and issubclass(k, BaseView):
                self.affected_views.append(k)

    def get_json_schema(self, view, converter):
        """Return the JSON Schema version of this condition."""
        schema = []
        for rel_view, condition in self.conditions.items():
            schema_cond = OrderedDict([('properties', OrderedDict()),
             (
              'required', [])])
            for fieldname, val in condition.items():
                form = converter._get_form(view, 'add')()
                field, req = converter.convert_field(getattr(form, fieldname))
                if not isinstance(val, list):
                    val = [
                     val]
                if 'enum' in field.keys():
                    newvals = []
                    for v in val:
                        log.debug('val: {}'.format(v))
                        log.debug('enum: {}'.format(field['enum']))
                        for c in field['enum']:
                            if isinstance(c, dict) and (c['id'] == v or c['label'] == v):
                                newvals.append(c)
                            elif c == v:
                                newvals.append(c)

                    log.debug('newvals: {}'.format(newvals))
                    val = newvals
                schema_cond['properties'][fieldname] = {'enum': val}
                schema_cond['required'].append(fieldname)

            for field in rel_view.datamodel.get_related_fks([view]):
                defin = _get_related_view_property(view, rel_view, field)
                schema_cond['properties'][field] = defin
                schema_cond['required'].append(field)

            schema.append(schema_cond)

        return (
         'oneOf', schema)