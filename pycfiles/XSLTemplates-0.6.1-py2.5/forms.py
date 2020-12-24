# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/xsltemplates/ext/forms.py
# Compiled at: 2007-10-05 18:07:01
import amara
from Ft.Xml.XPath import Conversions
from Ft.Xml.Domlette import NonvalidatingReader
from datetime import datetime, date
XHTML_NS = 'http://www.w3.org/1999/xhtml'

def date_selection(context, syear, smonth, sday):
    doc = amara.create_document('select', XHTML_NS, attributes={'name': 'month'})
    for x in range(1, 12):
        gen = date(2007, x, 1)
        abbr, full = gen.strftime('%b'), gen.strftime('%B')
        option = doc.xml_create_element('option', XHTML_NS, attributes={'value': unicode(abbr)}, content=unicode(full))
        if smonth > 0 and smonth == x:
            option.xml_set_attribute('selected', 'true')
        doc.select.xml_append(option)

    month = NonvalidatingReader.parseString(doc.xml(), XHTML_NS)
    del doc
    doc = amara.create_document('select', XHTML_NS, attributes={'name': 'day'})
    for x in range(1, 31):
        option = doc.xml_create_element('option', XHTML_NS, attributes={'value': unicode(x)}, content=unicode(x))
        if sday > 0 and sday == x:
            option.xml_set_attribute('selected', 'true')
        doc.select.xml_append(option)

    day = NonvalidatingReader.parseString(doc.xml(), XHTML_NS)
    del doc
    gen = datetime.now()
    doc = amara.create_document('select', XHTML_NS, attributes={'name': 'year'})
    for x in range(gen.year - 20, gen.year + 20):
        option = doc.xml_create_element('option', XHTML_NS, attributes={'value': unicode(x)}, content=unicode(x))
        if x == gen.year or syear > 0 and syear == x:
            option.xml_set_attribute('selected', 'true')
        doc.select.xml_append(option)

    year = NonvalidatingReader.parseString(doc.xml(), XHTML_NS)
    del doc
    return [
     month, day, year]


def state_selection(content):
    states = '<select name="state" xmlns="%s">\n\t<option value="AL">Alabama</option>\n\t<option value="AK">Alaska</option>\n\t<option value="AZ">Arizona</option>\n\t<option value="AR">Arkansas</option>\n\t<option value="CA">California</option>\n\t<option value="CO">Colorado</option>\n\t<option value="CT">Connecticut</option>\n\t<option value="DE">Delaware</option>\n\t<option value="DC">District of Columbia</option>\n\t<option value="FL">Florida</option>\n\t<option value="GA">Georgia</option>\n\t<option value="HI">Hawaii</option>\n\t<option value="ID">Idaho</option>\n\t<option value="IL">Illinois</option>\n\t<option value="IN">Indiana</option>\n\t<option value="IA">Iowa</option>\n\t<option value="KS">Kansas</option>\n\t<option value="KY">Kentucky</option>\n\t<option value="LA">Louisiana</option>\n\t<option value="ME">Maine</option>\n\t<option value="MD">Maryland</option>\n\t<option value="MA">Massachusetts</option>\n\t<option value="MI">Michigan</option>\n\t<option value="MN">Minnesota</option>\n\t<option value="MS">Mississippi</option>\n\t<option value="MO">Missouri</option>\n\t<option value="MT">Montana</option>\n\t<option value="NE">Nebraska</option>\n\t<option value="NJ">New Jersey</option>\n\t<option value="NH">New Hampshire</option>\n\t<option value="NV">Nevada</option>\n\t<option value="NM">New Mexico</option>\n\t<option value="NY">New York</option>\n\t<option value="NC">North Carolina</option>\n\t<option value="ND">North Dakota</option>\n\t<option value="OH">Ohio</option>\n\t<option value="OK">Oklahoma</option>\n\t<option value="OR">Oregon</option>\n\t<option value="PA">Pennsylvania</option>\n\t<option value="RI">Rhode Island</option>\n\t<option value="SC">South Carolina</option>\n\t<option value="SD">South Dakota</option>\n\t<option value="TN">Tennessee</option>\n\t<option value="TX">Texas</option>\n\t<option value="UT">Utah</option>\n\t<option value="VT">Vermont</option>\n\t<option value="VA">Virginia</option>\n\t<option value="WA">Washington</option>\n\t<option value="WV">West Virginia</option>\n\t<option value="WI">Wisconsin</option>\n\t<option value="WY">Wyoming</option>\n</select>' % XHTML_NS
    return [NonvalidatingReader.parseString(str(states), XHTML_NS)]


extensions = [
 (
  'http://ionrock.org/ns/xsltemplate', 'date-selection', date_selection),
 (
  'http://ionrock.org/ns/xsltemplate', 'state-selection', state_selection)]