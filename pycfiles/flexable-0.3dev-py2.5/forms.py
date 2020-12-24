# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/flexable/forms.py
# Compiled at: 2007-06-22 03:57:57


def getlocalname(e):
    tag = e.tag
    splited = tag.split('}')
    if len(splited) == 2:
        return splited[1]
    else:
        return splited[0]


class FormCollection(object):

    def __init__(self, elements):
        self.forms = [ Form(e) for e in elements ]

    def __getitem__(self, i):
        return self.get(i)

    def get(self, i, default=None):
        if type(i) == str:
            return self.getByName(i, default)
        elif len(self.forms) > i:
            return self.forms[i]
        else:
            return default

    def getByName(self, name, default=None):
        for f in self.forms:
            if f.get('name') == name:
                return f

        return default

    def __len__(self):
        return len(self.forms)


class Form(object):

    def __init__(self, element):
        self.element = element

    def get(self, name):
        return self.element.get(name)

    def setOptions(self, selectElement, values):
        selected = values[0]
        optValues = values[1]
        prefix = selectElement.prefix
        ns = ''
        if prefix:
            ns = '{%s}' % selectElement.nsmap[prefix]
        for (optvalue, optlabel) in optValues:
            opt = selectElement.makeelement('%soption' % ns)
            if optvalue == selected:
                opt.set('selected', 'selected')
            opt.set('value', optvalue)
            opt.text = optlabel
            selectElement.append(opt)

    def setRadio(self, elements, values):
        checked = values[0]
        radioValues = values[1]
        if len(radioValues) != len(elements):
            raise Exception, 'Sorry and radio elements are not same length.'
        for (i, v) in enumerate(radioValues):
            e = elements[i]
            e.set('value', v[0])

    def _set_values(self, values):
        for (k, v) in values.iteritems():
            elements = self.element.xpath(".//*[@name='%s']" % k)
            etype = getlocalname(elements[0])
            if etype == 'input':
                etype = elements[0].get('type')
            if etype == 'radio':
                self.setRadio(elements, v)
                return
            for e in elements:
                if type(v) == str:
                    if etype in ('text', 'password'):
                        e.set('value', v)
                    elif etype == 'textarea':
                        e.text = v
                elif type(v) == tuple:
                    if etype == 'select':
                        self.setOptions(e, v)
                    if etype == 'checkbox':
                        if v[0]:
                            e.set('checked', 'checked')
                        else:
                            del e.attrib['checked']
                        e.set('value', v[1])
                else:
                    raise Exception

    def _get_values(self):
        values = dict()
        for e in self.element.xpath(".//*[local-name()='input']"):
            values[e.get('name')] = e.get('value')

        for e in self.element.xpath(".//*[local-name()='select']"):
            opts = e.xpath(".//*[local-name() = 'option']")
            selected = e.xpath(".//*[local-name() = 'option' and @selected='selected']")
            value = None
            if len(selected) > 0:
                value = selected[0].get('value')
            optvalues = [ o.get('value') for o in opts ]
            values[e.get('name')] = (
             value, optvalues)

        return values

    values = property(_get_values, _set_values)