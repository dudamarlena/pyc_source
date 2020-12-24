# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cubicweb_postgis/views.py
# Compiled at: 2019-02-21 07:28:15
__doc__ = 'cubicweb-postgis views/forms/actions/components for web ui'
from cubicweb import tags, uilib
from cubicweb.utils import UStringIO
from cubicweb.web import formfields
from cubicweb.web import formwidgets
from cubicweb.view import EntityView
from cubicweb.predicates import match_kwargs
try:
    from shapely import wkb
except ImportError:
    wkb = None

formfields.FIELDS['Geometry'] = formfields.StringField
uilib.PRINTERS['Geometry'] = uilib.print_string
formfields.FIELDS['Geography'] = formfields.StringField
uilib.PRINTERS['Geography'] = uilib.print_string

class RefpointAttributeView(EntityView):
    __regid__ = 'refpointattr'
    __select__ = EntityView.__select__ & match_kwargs('rtype')

    def entity_call(self, entity, rtype, **kwargs):
        value = getattr(entity, rtype)
        if value:
            value = wkb.loads(value.decode('hex'))
            self.w('lat: %s, long: %s' % (value.x, value.y))


class RefpointWidget(formwidgets.TextInput):

    def _render(self, form, field, renderer):
        ustring = UStringIO()
        w = ustring.write
        value = self.values(form, field)[0]
        longitude = 0
        latitude = 0
        if value:
            value = wkb.loads(value.decode('hex'))
            longitude = value.x
            latitude = value.y
        w(tags.div(tags.label('longitude') + tags.input(type='text', value=longitude, name=field.input_name(form, 'longitude')), klass='form-group'))
        w(tags.div(tags.label('latitude') + tags.input(type='text', value=latitude, name=field.input_name(form, 'latitude')), klass='form-group'))
        return ustring.getvalue()

    def process_field_data(self, form, field):
        """Return process posted value(s) for widget and return something
        understandable by the associated `field`. That value may be correctly
        typed or a string that the field may parse.
        """
        posted = form._cw.form
        longitude = posted.get(field.input_name(form, 'longitude')).strip() or None
        latitude = posted.get(field.input_name(form, 'latitude')).strip() or None
        return 'POINT(%s %s)' % (longitude, latitude)