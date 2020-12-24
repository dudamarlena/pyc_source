# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_forms/djinn_forms/widgets/datetimewidget.py
# Compiled at: 2015-11-16 04:46:43
from base import BaseWidget
from datetime import datetime
from django.forms import Media

class DateTimeWidget(BaseWidget):
    """
    Widget that renders the datetime as two separate boxes, using jQuery
    to bind the appropriate client side widgets.
    The following attrs are supported:

     * date_format Defaults to dd-mm-YYYY
     * time_format Defaults to hh:mm
    """

    def _media(self):
        """ Add JS for TinyMCE """
        return Media(js=('js/djinn_forms_datetimedirect.js', ))

    def _template_name(self):
        if self.attrs.get('direct'):
            Templ = 'djinn_forms/snippets/datetimedirectwidget.html'
        else:
            Templ = 'djinn_forms/snippets/datetimewidget.html'
        return Templ

    media = property(_media)
    template_name = property(_template_name)
    defaults = {'date_format': '%d-%m-%Y', 'time_format': '%H:%M'}

    def build_attrs(self, extra_attrs=None, **kwargs):
        final_attrs = super(DateTimeWidget, self).build_attrs(extra_attrs=extra_attrs, **kwargs)
        if kwargs.get('value'):
            if kwargs.get('value') == 'errorDirect':
                final_attrs['direct'] = ''
                final_attrs['notdirect'] = 'checked'
            else:
                final_attrs['date_value'] = kwargs['value'].strftime(self.attrs['date_format'])
                final_attrs['time_value'] = kwargs['value'].strftime(self.attrs['time_format'])
        else:
            final_attrs['date_value'] = ''
            final_attrs['time_value'] = ''
            final_attrs['direct'] = 'checked'
            final_attrs['notdirect'] = ''
        return final_attrs

    def value_from_datadict(self, data, files, name):
        value = None
        if data.get('%s_date' % name):
            value_str = data[('%s_date' % name)]
            format_str = self.attrs['date_format']
            if data.get('%s_time' % name):
                value_str = '%s %s' % (value_str, data[('%s_time' % name)])
                format_str = '%s %s' % (format_str, self.attrs['time_format'])
            value = datetime.strptime(value_str, format_str)
        elif name == 'publish_from' and data.get('radiodirect') == 'NotDirect':
            value = 'errorDirect'
        return value