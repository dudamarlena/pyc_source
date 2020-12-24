# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wtforms_jsonschema2/geofab.py
# Compiled at: 2018-10-15 04:56:42
# Size of source mod 2**32: 3418 bytes
import logging
from .base import converts
from .fab import FABConverter
from wtforms.form import Form
from wtforms.fields import FormField
from fab_addon_geoalchemy.fields import PointField
from copy import deepcopy
log = logging.getLogger(__name__)

class GeoFABConverter(FABConverter):
    __doc__ = '\n    Extends the FABConverter with GeoAlchemy2 support for geographic data.\n    '

    def convert(self, views, form_type='add'):
        log.debug('Calling GeoFABConverter.convert')
        if not isinstance(views, list) and (isinstance(views, Form) or issubclass(views, Form)):
            return super(FABConverter, self).convert(views)
        newviews = []
        try:
            iter(views)
        except TypeError:
            views = [
             views]

        for view in views:
            log.debug('Got view {}'.format(view))
            if isinstance(view, Form):
                log.debug('Got a form')
                form = view
                newviews.append(view)
            else:
                log.debug('Got a view')
                view = view()
                log.debug('Unbound fields: {}'.format(view.add_form._unbound_fields))
                newviews.append(view)
                form = self._get_form(view, form_type)

            class newForm(Form):
                pass

            newfields = []
            for field in form():
                fname = field.name
                if fname.startswith('_'):
                    pass
                else:
                    if fname in self.skip_fields:
                        pass
                    else:
                        field = getattr(form, fname)
                        if not hasattr(field, '_formfield'):
                            pass
                        else:
                            log.debug('Checking field {}'.format(fname))
                            if hasattr(field, 'field_class') and field.field_class == PointField:
                                log.debug('{} is a pointfield'.format(fname))
                                latfield = deepcopy(field)
                                latfield.args = ['Latitude'] + list(field.args)[1:]
                                latfield.kwargs['coordinate_type'] = 'latitude'
                                lonfield = deepcopy(field)
                                lonfield.args = ['Longitude'] + list(field.args)[1:]
                                lonfield.kwargs['coordinate_type'] = 'longitude'

                                class subform(Form):
                                    pass

                                subform.lat = latfield
                                subform.lon = lonfield
                                field = FormField(subform)
                            setattr(newForm, fname, field)
                            newfields.append((fname, field))

            newForm._unbound_fields = newfields
            setattr(view, '{}_form'.format(form_type), newForm)
            log.debug('NewFields: {}'.format(newfields))
            log.debug('Fields: {}'.format([f.name for f in self._get_form(view, form_type)()]))

        return super().convert(newviews, form_type)

    @converts(PointField)
    def convert_point_field(self, field):
        fieldtype = 'string'
        options = {'format': 'coordinate_point_{}'.format(field.coordinate_type)}
        vals = dict([(v.__class__, v) for v in field.validators])
        required = self._is_required(vals)
        return (
         fieldtype, options, required)