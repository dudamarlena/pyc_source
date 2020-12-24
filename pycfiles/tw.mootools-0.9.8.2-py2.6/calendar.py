# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tw/mootools/calendar.py
# Compiled at: 2009-11-30 09:56:23
from tw.api import Widget, JSLink, CSSLink, CSSSource
from genshi.template.text import TextTemplate
import tw.forms
from tw.mootools.base import moo_core_js_compressed, moo_more_js_compressed
calendar_js = JSLink(modname=__name__, filename='static/calendar/mooECal.js', javascript=[])
calendar_css = CSSLink(modname=__name__, filename='static/calendar/style.css', javascript=[])

class CalendarWidget(Widget):
    """
    To use this calendar, just instanciate it. This is a prototype, so no advanced options available.
    Value should be an array of dictionnary including :
    * "title" (string)
    * "start" (date or datetime)
    * "end" (date or datetime)
    * "location" (string)
    * "url" (string, optionnal)
    Example of use :
    ${CalendarWidget().display([
        {
            'title':'Get Groceries',
            'start':date(2008,12,05),
            'end':date(2008,12,06),
            'location':'Store',
            'url':'http://www.myshoppingmal.com/'
        },
        {
            'title':'Goin Cow Tip',
            'start':datetime(2008,12,20,23,30),
            'end':'datetime(2008,12,20,23,45),
            'location':'',
            'url':'/ive-won/'
        },
        {
            'title':'Hair Cut',
            'start':datetime(2008,12,22,10,0),
            'end':datetime(2008,12,22,11,0),
            'location':'at the hair-dresser'
        }
    ])}
    """
    template = 'genshi:tw.mootools.templates.calendar'
    javascript = [
     moo_core_js_compressed, moo_more_js_compressed, calendar_js]
    css = [calendar_css]