# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysmvt/htmltable.py
# Compiled at: 2010-05-30 13:30:03
"""
    Example:
    
    t = Table()
    t.name = Link('Name', 'contentbase:AttributeCategoriesUpdate', 'id')
    t.display = Col('Display')
    t.inactive = YesNo('Active', reverse=True)
    t.created = DateTime('Created')
    t.last_edited = DateTime('Last Updated')
    t.render(dic_or_list)
"""
from pysmvt.utils import OrderedProperties, isurl
from pysmvt.routing import url_for
from webhelpers.html import HTML, literal
from webhelpers.html.tags import link_to
from webhelpers.containers import NotGiven

class StringIndentHelper(object):

    def __init__(self):
        self.output = []
        self.level = 0
        self.indent_with = '    '

    def dec(self, value):
        self.level -= 1
        return self.render(value)

    def inc(self, value):
        self.render(value)
        self.level += 1

    def __call__(self, value, **kwargs):
        self.render(value)

    def render(self, value, **kwargs):
        self.output.append('%s%s' % (self.indent(**kwargs), value))

    def indent(self, level=None):
        if level == None:
            return self.indent_with * self.level
        else:
            return self.indent_with * self.level
            return

    def get(self):
        retval = ('\n').join(self.output)
        self.output = []
        return retval


class HtmlAttributeHolder(object):

    def __init__(self, **kwargs):
        self._cleankeys(kwargs)
        self.attributes = kwargs

    def set_attrs(self, **kwargs):
        self._cleankeys(kwargs)
        self.attributes.update(kwargs)

    setAttributes = set_attrs

    def set_attr(self, key, value):
        if key.endswith('_'):
            key = key[:-1]
        self.attributes[key] = value

    setAttribute = set_attr

    def add_attr(self, key, value):
        """
            Creates a space separated string of attributes.  Mostly for the
            "class" attribute.
        """
        if key.endswith('_'):
            key = key[:-1]
        if self.attributes.has_key(key):
            self.attributes[key] = self.attributes[key] + ' ' + value
        else:
            self.attributes[key] = value

    def del_attr(self, key):
        if key.endswith('_'):
            key = key[:-1]
        del self.attributes[key]

    def get_attrs(self):
        return self.attributes

    getAttributes = get_attrs

    def get_attr(self, key, defaultval=NotGiven):
        try:
            if key.endswith('_'):
                key = key[:-1]
            return self.attributes[key]
        except KeyError:
            if defaultval is not NotGiven:
                return defaultval
            raise

    getAttribute = get_attr

    def _cleankeys(self, dict):
        """
            When using kwargs, some attributes can not be sent directly b/c
            they are Python key words (i.e. "class") so that have to be sent
            in with an underscore at the end (i.e. "class_").  We want to
            remove the underscore before saving
        """
        for (key, val) in dict.items():
            if key.endswith('_'):
                del dict[key]
                dict[key[:-1]] = val


class Table(OrderedProperties):

    def __init__(self, row_dec=None, **kwargs):
        if not kwargs.has_key('summary'):
            kwargs['summary'] = ''
        if not kwargs.has_key('cellpadding'):
            kwargs['cellpadding'] = 0
        if not kwargs.has_key('cellspacing'):
            kwargs['cellspacing'] = 0
        self.attrs = kwargs
        self.row_dec = row_dec
        OrderedProperties.__init__(self)

    def render(self, iterable):
        ind = StringIndentHelper()
        if len(iterable) > 0:
            ind.inc(HTML.table(_closed=False, **self.attrs))
            ind.inc('<thead>')
            ind.inc('<tr>')
            for (name, col) in self._data.items():
                ind(col.render_th())

            ind.dec('</tr>')
            ind.dec('</thead>')
            ind.inc('<tbody>')
            for (row_num, value) in enumerate(iterable):
                row_attrs = HtmlAttributeHolder()
                if self.row_dec:
                    self.row_dec(row_num + 1, row_attrs, value)
                ind.inc(HTML.tr(_closed=False, **row_attrs.attributes))
                for (name, col) in self._data.items():
                    ind(col.render_td(value, name))

                ind.dec('</tr>')

            ind.dec('</tbody>')
            ind.dec('</table>')
            return ind.get()
        else:
            return ''


class Col(object):

    def __init__(self, header, extractor=None, th_decorator=None, **kwargs):
        self.attrs_td = dict([ (k[:-3], v) for (k, v) in kwargs.items() if k.endswith('_td') ])
        self.attrs_th = dict([ (k[:-3], v) for (k, v) in kwargs.items() if k.endswith('_th') ])
        self.header = header
        self.crow = None
        self.extractor = extractor
        self.th_decorator = th_decorator
        return

    def render_th(self):
        thcontent = self.header
        if self.th_decorator:
            thcontent = self.th_decorator(thcontent)
        return HTML.th(thcontent, **self.attrs_th)

    def render_td(self, row, key):
        self.crow = row
        contents = self.process(key)
        return HTML.td(contents, **self.attrs_td)

    def extract(self, name):
        """ extract a value from the current row """
        if self.extractor:
            return self.extractor(self.crow)
        try:
            return self.crow[name]
        except TypeError:
            pass

        try:
            return getattr(self.crow, name)
        except AttributeError, e:
            if "object has no attribute '%s'" % name not in str(e):
                raise

        raise TypeError('could not retrieve value from row, unrecognized row type')

    def process(self, key):
        return self.extract(key)


class Link(Col):
    """
        Examples:
        
        Link( 'Referred By',
            validate_url=False,
            urlfrom=lambda row: url_for('module:ReferringObjectDetail', id=row[referred_by_id]) if row[referred_by_id] else None
        )
    """

    def __init__(self, header, urlfrom='url', require_tld=True, validate_url=True, **kwargs):
        Col.__init__(self, header, **kwargs)
        self.urlfrom = urlfrom
        self._link_attrs = {}
        self.require_tld = require_tld
        self.validate_url = validate_url

    def process(self, key):
        try:
            url = self.urlfrom(self.crow)
        except TypeError, e:
            if 'is not callable' not in str(e):
                raise
            url = self.extract(self.urlfrom)

        if url is not None and (not self.validate_url or isurl(url, require_tld=self.require_tld)):
            return link_to(self.extract(key), url, **self._link_attrs)
        else:
            return self.extract(key)

    def attrs(self, **kwargs):
        self._link_attrs = kwargs
        return self


class Links(Col):

    def __init__(self, header, *args, **kwargs):
        Col.__init__(self, header, **kwargs)
        self.aobjs = args

    def process(self, key):
        return literal(('').join([ a.process(key, self.extract) for a in self.aobjs ]))


class A(object):
    """ a container class used by Links """

    def __init__(self, endpoint, *args, **kwargs):
        self.endpoint = endpoint
        if kwargs.has_key('label'):
            self.label = kwargs['label']
            del kwargs['label']
        else:
            self.label = NotGiven
        self.url_arg_keys = args
        self.attrs = kwargs

    def process(self, name, extract):
        url_args = dict([ (key, extract(key)) for key in self.url_arg_keys ])
        url = url_for(self.endpoint, **url_args)
        if self.label is NotGiven:
            label = extract(name)
        else:
            label = self.label
        return link_to(label, url, **self.attrs)


class YesNo(Col):

    def __init__(self, header, reverse=False, yes='yes', no='no', **kwargs):
        Col.__init__(self, header, **kwargs)
        self.reversed = reverse
        self.yes = yes
        self.no = no

    def process(self, key):
        value = self.extract(key)
        if self.reversed:
            value = not value
        if value:
            return self.yes
        else:
            return self.no


class TrueFalse(YesNo):

    def __init__(self, header, reverse=False, true='true', false='false', **kwargs):
        YesNo.__init__(self, header, reverse, true, false, **kwargs)


class DateTime(Col):

    def __init__(self, header, format='%m/%d/%y %H:%M', on_none='', **kwargs):
        Col.__init__(self, header, **kwargs)
        self.format = format
        self.on_none = on_none

    def process(self, key):
        value = self.extract(key)
        if value == None:
            return self.on_none
        else:
            return value.strftime(self.format)