# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/split_select_date_time_widget.py
# Compiled at: 2014-08-27 19:26:12
from signalbox.select_time_widget import SelectTimeWidget
from django.forms.widgets import MultiWidget
from django.forms.extras.widgets import SelectDateWidget

class SplitSelectDateTimeWidget(MultiWidget):
    """
    MultiWidget = A widget that is composed of multiple widgets.

    This class combines SelectTimeWidget and SelectDateWidget so we have something 
    like SpliteDateTimeWidget (in django.forms.widgets), but with Select elements.
    """

    def __init__(self, attrs=None, hour_step=None, minute_step=None, second_step=None, twelve_hr=None, years=None):
        """ pass all these parameters to their respective widget constructors..."""
        widgets = (
         SelectDateWidget(attrs=attrs, years=years), SelectTimeWidget(attrs=attrs, hour_step=hour_step, minute_step=minute_step, second_step=second_step, twelve_hr=twelve_hr))
        super(SplitSelectDateTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.date(), value.time().replace(microsecond=0)]
        else:
            return [
             None, None]

    def format_output(self, rendered_widgets):
        """
        Given a list of rendered widgets (as strings), it inserts an HTML
        linebreak between them.
        
        Returns a Unicode string representing the HTML for the whole lot.
        """
        rendered_widgets.insert(-1, '<br/>')
        return ('').join(rendered_widgets)