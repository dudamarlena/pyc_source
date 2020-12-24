# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/drink/types.py
# Compiled at: 2011-04-12 18:10:07
__all__ = [
 '_Editable',
 'Text', 'TextArea', 'GroupListArea', 'GroupCheckBoxes',
 'Id', 'Int', 'Password', 'File']
import os, drink, datetime, transaction
from . import classes
from drink import template
from drink.zdb import DataBlob
from time import mktime, strptime
from persistent.dict import PersistentDict

class _Editable(object):
    form_attr = None

    def __init__(self, caption=None, group=None):
        self.caption = caption
        self.id = str(id(self))
        self.group = group if group else self.__class__.__name__

    def html(self, name, value, _template=None, no_label=False):
        d = self.__dict__.copy()
        d.update({'id': self.id, 'name': name, 'caption': self.caption or name, 'value': value})
        if no_label:
            pfx = '<div id="edit_%(name)s" class="editable">'
        else:
            pfx = '<div id="edit_%(name)s" class="editable">                <label class="autoform" for="%(id)s">%(caption)s:</label>'
        return (pfx + (_template or self._template) + '</div>') % d

    set = setattr


class EasyPermissions(_Editable):

    def html(self, name, value, _template=None):
        return '\n        <div class="option" onclick="$(\'#edit_read_groups input\').each( function() { $(this).attr(\'checked\', false ) } ) ; $(\'#edit_write_groups input\').each( function() { $(this).attr(\'checked\', false ) } )">\n        Private document</div>\n        <div class="option" onclick="$(\'#edit_read_groups input\').each( function() { $(this).attr(\'checked\', !! $(this).attr(\'value\').match(/^users|admin$/) ) } ) ; $(\'#edit_write_groups input\').each( function() { $(this).attr(\'checked\', false ) } ) ">\n        Users can only consult</div>\n        <div class="option" onclick="$(\'#edit_read_groups input\').each( function() { $(this).attr(\'checked\', !! $(this).attr(\'value\').match(/^users|admin$/) ) } ) ; $(\'#edit_write_groups input\').each( function() { $(this).attr(\'checked\', !! $(this).attr(\'value\').match(/^users|admin$/) ) } ) ">\n        Users can change content</div>\n        <div class="option" onclick="$(\'#edit_read_groups input\').each( function() { $(this).attr(\'checked\', !! $(this).attr(\'value\').match(/^users|anonymous|admin$/) ) } ) ">\n        Everybody can see</div>\n        '

    def set(self, obj, name, val):
        pass


class Text(_Editable):
    _template = '<input type="text" size="%(size)d" id="%(id)s" value="%(value)s" name="%(name)s" />'

    def __init__(self, caption=None, group=None, size=40):
        _Editable.__init__(self, caption, group)
        self.size = size


DATE_FMT = '%d/%m/%Y'

def dt2str(dt):
    try:
        return dt.strftime(DATE_FMT)
    except AttributeError:
        return dt


def dt2ts(dt):
    try:
        return int(mktime(dt.timetuple()))
    except AttributeError:
        return 0


def str2dt(text):
    try:
        return datetime.datetime(*strptime(text, DATE_FMT)[:6])
    except AttributeError:
        return text


def str2d(text):
    try:
        return datetime.date(*strptime(text, DATE_FMT)[:3])
    except AttributeError:
        return text


class Date(Text):
    _template = '<input class="auto_date" type="text" size="%(size)d" id="%(id)s" value="%(value)s" name="%(name)s" />'

    def __init__(self, caption=None, group=None, size=10):
        Text.__init__(self, caption, group, size)

    def set(self, obj, name, val):
        setattr(obj, name, str2d(val))

    def html(self, name, value, _template=None, no_label=False):
        return Text.html(self, name, dt2str(value), _template, no_label)


class TextArea(_Editable):
    _template = '<textarea rows="%(rows)s" cols="%(cols)s" id="%(id)s" name="%(name)s">%(value)s</textarea>'

    def __init__(self, caption=None, group=None, rows=None, cols=None):
        _Editable.__init__(self, caption, group)
        self._rows = rows
        self._cols = cols

    def html(self, name, value):
        r = self._rows
        c = self._cols
        if isinstance(value, basestring):
            length = value.count('\n')
        else:
            length = len(value)
        if c is None:
            self.cols = 50
        else:
            self.cols = c
        if r is None:
            self.rows = min(400, max(10, length))
        else:
            self.rows = r
        return _Editable.html(self, name, value)


class GroupListArea(TextArea):

    def html(self, name, value):
        self._cols = 30
        self._rows = len(value) + 2
        return TextArea.html(self, name, ('\n').join(group.id for group in value))

    def set(self, obj, name, val):
        groups = drink.db.db['groups']
        setattr(obj, name, set(groups[line.strip()] for line in val.split('\n') if line.strip() in groups))


class BoolOption(_Editable):

    def html(self, name, value):
        html = '<input type="checkbox" name=%(name)s value="%(name)s"' + ('checked="checked" />' if value else '/>') + '<span class="label' + (' selected' if value else '') + '">%(caption)s</span>'
        return _Editable.html(self, name, None, _template=html, no_label=True)

    def set(self, obj, name, val):
        setattr(obj, name, bool(val))


class CheckboxSet(_Editable):

    def __init__(self, caption=None, group=None, values=[]):
        """ values: set of valid Ids
                OR a callable returning this object """
        _Editable.__init__(self, caption, group)
        self.values = values

    @property
    def v(self):
        if callable(self.values):
            return self.values()
        return self.values

    def html(self, name, values):
        all_ids = self.v
        opts = [ '<input type="checkbox" name=%(name)s value="' + o + '" ' + ('checked="checked" />' if o in values else '/>') + '<span class="label' + (' selected' if o in values else '') + '">' + o + '</span>' for o in all_ids
               ]
        return _Editable.html(self, name, None, ('\n').join(opts))

    def set(self, obj, name, val):
        values = drink.request.forms.getall(name)
        all_values = set(self.v)
        all_values.intersection_update(values)
        setattr(obj, name, all_values)


class GroupCheckBoxes(CheckboxSet):

    def __init__(self, caption=None, group=None):
        CheckboxSet.__init__(self, caption, group, self._group_list)

    def _group_list(self):
        return drink.db.db['groups'].keys()


class Id(Text):

    def set(self, obj, name, val):
        parent = drink.get_object(drink.db, obj.rootpath)
        del parent[getattr(obj, name)]
        setattr(obj, name, val)
        parent[val] = obj


class Int(Text):

    def set(self, obj, name, val):
        setattr(obj, name, int(val))


class Float(Text):

    def set(self, obj, name, val):
        float(val)
        setattr(obj, name, val)


class Password(Text):
    _template = '<input type="password" size="%(size)d" id="%(id)s" name="%(name)s" value="%(value)s" />'


class File(_Editable):
    _template = '<input name="%(name)s" id="%(id)s" type="file" />'
    form_attr = 'enctype="multipart/form-data"'

    def set(self, obj, name, val):
        if val == '':
            return
        setattr(obj, name + '_name', val.filename)
        new_o = DataBlob()
        setattr(obj, name, new_o)
        o_fd = new_o.open('w')
        chunk_sz = 1048576
        while True:
            dat = val.file.read(chunk_sz)
            if not dat:
                break
            o_fd.write(dat)

        o_fd.close()