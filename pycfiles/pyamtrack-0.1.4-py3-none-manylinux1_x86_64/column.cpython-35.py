# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_table/column.py
# Compiled at: 2020-01-08 07:16:58
# Size of source mod 2**32: 14604 bytes
__doc__ = 'PyAMS_table.column module\n\nThis module provides base classes and adapters for table columns management.\n'
import html
from urllib.parse import urlencode
from zope.dublincore.interfaces import IZopeDublinCore
from zope.interface import implementer
from zope.location import Location
from zope.security.interfaces import Unauthorized
from pyams_table.interfaces import IColumn, IColumnHeader, INoneCell
from pyams_utils.date import EXT_DATETIME_FORMAT, format_datetime
from pyams_utils.traversing import get_name
from pyams_utils.url import absolute_url
__docformat__ = 'reStructuredText'
from pyams_table import _

def add_column(self, class_, name, cell_renderer=None, head_cell_renderer=None, colspan=None, weight=None, header=None, css_classes=None, **kws):
    """Column creation helper, mainly used for testing"""
    if not IColumn.implementedBy(class_):
        raise ValueError('class_ %s must implement IColumn.' % class_)
    column = class_(self.context, self.request, self)
    column.__parent__ = self
    column.__name__ = name
    if cell_renderer is not None:
        column.render_cell = cell_renderer
    if head_cell_renderer is not None:
        column.render_head_cell = head_cell_renderer
    if colspan is not None:
        column.colspan = colspan
    if weight is not None:
        column.weight = weight
    if header is not None:
        column.header = header
    if css_classes is not None:
        column.css_classes = css_classes
    for key, value in kws.items():
        setattr(column, key, value)

    return column


def safe_get_attr(obj, attr, default):
    """Safe attribute getter"""
    try:
        return getattr(obj, attr, default)
    except Unauthorized:
        return default


@implementer(IColumn)
class Column(Location):
    """Column"""
    id = None
    colspan = 0
    weight = 0
    header = ''
    css_classes = {}

    def __init__(self, context, request, table):
        self.__parent__ = context
        self.context = context
        self.request = request
        self.table = table

    def update(self):
        """Update column"""
        pass

    def get_colspan(self, item):
        """Returns the colspan value."""
        return self.colspan

    def get_sort_key(self, item):
        """Returns the sort key used for column sorting."""
        return self.render_cell(item)

    def render_head_cell(self):
        """Header cell content."""
        registry = self.request.registry
        header = registry.queryMultiAdapter((self.context, self.request, self.table, self), IColumnHeader)
        if header:
            header.update()
            return header.render()
        translate = self.request.localizer.translate
        return html.escape(translate(self.header))

    def render_cell(self, item):
        """Cell content."""
        raise NotImplementedError('Subclass must implement render_cell')

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.__name__)


@implementer(INoneCell)
class NoneCell(Column):
    """NoneCell"""

    def get_colspan(self, item):
        return 0

    def render_head_cell(self):
        return ''

    def render_cell(self, item):
        return ''


class NameColumn(Column):
    """NameColumn"""
    header = _('Name')

    def render_cell(self, item):
        return html.escape(get_name(item))


class RadioColumn(Column):
    """RadioColumn"""
    header = _('X')

    @property
    def selected_item(self):
        """Get selected item"""
        items = self.table.selected_items
        if len(items) > 0:
            return list(items).pop()

    @selected_item.setter
    def selected_item(self, value):
        """Set selected item value"""
        self.table.selected_items = [
         value]

    def get_sort_key(self, item):
        """Get item sort key"""
        return get_name(item)

    def get_item_key(self, item):
        """Get item key"""
        return '%s-selected-item' % self.id

    @staticmethod
    def get_item_value(item):
        """Get item value"""
        return get_name(item)

    def update(self):
        """Column update"""
        items = [item for item in self.table.values if self.get_item_value(item) in self.request.params.get(self.get_item_key(item), [])]
        if len(items) > 0:
            self.selected_item = items.pop()

    def render_cell(self, item):
        """Render column cell"""
        selected = ''
        if item == self.selected_item:
            selected = ' checked="checked"'
        return '<input type="radio" class="%s" name="%s" value="%s"%s />' % (
         'radio-widget',
         html.escape(self.get_item_key(item)),
         html.escape(self.get_item_value(item)),
         selected)


class CheckBoxColumn(Column):
    """CheckBoxColumn"""
    header = _('X')
    weight = 10

    @property
    def selected_items(self):
        """Get list of selected items"""
        return self.table.selected_items

    @selected_items.setter
    def selected_items(self, values):
        """Set values of selected items"""
        self.table.selected_items = values

    def get_sort_key(self, item):
        """Get item sort key"""
        return get_name(item)

    def get_item_key(self, item):
        """Get item key"""
        return '%s-selected-items' % self.id

    def get_item_value(self, item):
        """Get item value"""
        return get_name(item)

    def is_selected(self, item):
        """Test if item is selected"""
        value = self.request.params.get(self.get_item_key(item), [])
        value = ensure_list(value)
        if self.get_item_value(item) in value:
            return True
        return False

    def update(self):
        """Update column"""
        self.selected_items = [item for item in self.table.values if self.is_selected(item)]

    def render_cell(self, item):
        """Render column cell"""
        selected = ''
        if item in self.selected_items:
            selected = ' checked="checked"'
        return '<input type="checkbox" class="{}" name="{}" value="{}"{} />'.format('checkbox-widget', html.escape(self.get_item_key(item)), html.escape(self.get_item_value(item)), selected)


class GetAttrColumn(Column):
    """GetAttrColumn"""
    attr_name = None
    default_value = ''

    def get_value(self, obj):
        """Get object attribute value"""
        if obj is not None and self.attr_name is not None:
            return safe_get_attr(obj, self.attr_name, self.default_value)
        return self.default_value

    def render_cell(self, item):
        """Render column cell"""
        return self.get_value(item)


class GetItemColumn(Column):
    """GetItemColumn"""
    idx = None
    default_value = ''

    def get_value(self, obj):
        """Get object value"""
        if obj is not None and self.idx is not None:
            try:
                return obj[self.idx]
            except (KeyError, IndexError):
                return self.default_value

            return self.default_value

    def render_cell(self, item):
        """Render column cell"""
        return self.get_value(item)


class I18nGetAttrColumn(GetAttrColumn):
    """I18nGetAttrColumn"""

    def render_cell(self, item):
        """Render column cell"""
        translate = self.request.localizer.translate
        return translate(self.get_value(item))


class FormatterColumn(Column):
    """FormatterColumn"""
    formatter = format_datetime
    format_string = EXT_DATETIME_FORMAT

    def get_formatted_value(self, value):
        """Get formatted value"""
        return self.__class__.formatter(value, self.format_string, self.request)


class GetAttrFormatterColumn(FormatterColumn, GetAttrColumn):
    """GetAttrFormatterColumn"""

    def render_cell(self, item):
        """Render column cell"""
        value = self.get_value(item)
        if value:
            value = self.get_formatted_value(value)
        return value


class CreatedColumn(FormatterColumn, GetAttrColumn):
    """CreatedColumn"""
    header = _('Created')
    weight = 100
    attr_name = 'created'

    def render_cell(self, item):
        """Render column cell"""
        zdc = IZopeDublinCore(item, None)
        if zdc is not None:
            value = self.get_value(zdc)
            if value:
                value = self.get_formatted_value(value)
            return value
        return ''


class ModifiedColumn(FormatterColumn, GetAttrColumn):
    """ModifiedColumn"""
    header = _('Modified')
    weight = 110
    attr_name = 'modified'

    def render_cell(self, item):
        """Render column cell"""
        zdc = IZopeDublinCore(item, None)
        if zdc is not None:
            value = self.get_value(zdc)
            if value:
                value = self.get_formatted_value(value)
            return value
        return ''


class LinkColumn(Column):
    """LinkColumn"""
    header = _('Name')
    link_name = None
    link_target = None
    link_content = None
    link_css = None
    link_title = None

    def get_link_url(self, item):
        """Get link URL"""
        if self.link_name is not None:
            return '%s/%s' % (absolute_url(item, self.request), self.link_name)
        return absolute_url(item, self.request)

    def get_link_css(self, item):
        """Setup link CSS"""
        if self.link_css:
            return ' class="%s"' % self.link_css
        return ''

    def get_link_title(self, item):
        """Get link title"""
        if self.link_title:
            return ' title="%s"' % html.escape(self.link_title)
        return ''

    def get_link_target(self, item):
        """Get link target"""
        if self.link_target:
            return ' target="%s"' % self.link_target
        return ''

    def get_link_content(self, item):
        """Get link content"""
        if self.link_content:
            translate = self.request.localizer.translate
            return translate(self.link_content)
        return get_name(item)

    def render_cell(self, item):
        """Render column cell"""
        return '<a href="%s"%s%s%s>%s</a>' % (html.escape(self.get_link_url(item)),
         self.get_link_target(item),
         self.get_link_css(item),
         self.get_link_title(item),
         html.escape(self.get_link_content(item)))


class EMailColumn(LinkColumn, GetAttrColumn):
    """EMailColumn"""
    header = _('E-Mail')
    attr_name = None
    default_value = ''
    link_content = None

    def get_link_url(self, item):
        """Get item URL"""
        return 'mailto:%s' % self.get_value(item)

    def get_link_content(self, item):
        """Get link content"""
        if self.link_content:
            translate = self.request.localizer.translate
            return translate(self.link_content)
        return self.get_value(item)

    def render_cell(self, item):
        """Render column cell"""
        value = self.get_value(item)
        if value is self.default_value or value is None:
            return self.default_value
        return super(EMailColumn, self).render_cell(item)


def ensure_list(item):
    """Convert given item to list"""
    if not isinstance(item, (list, tuple)):
        return [item]
    return item


class SelectedItemColumn(LinkColumn):
    """SelectedItemColumn"""
    selected_item = None

    @property
    def view_url(self):
        """Get base target URL"""
        return '%s/%s' % (absolute_url(self.context, self.request), self.table.__name__)

    def get_item_key(self, item):
        """Get item key"""
        return '%s-selected-items' % self.id

    def get_item_value(self, item):
        """Get item value"""
        return get_name(item)

    def get_sort_key(self, item):
        """Returns the sort key used for column sorting"""
        return self.get_link_content(item)

    def get_link_content(self, item):
        """Get link content"""
        return self.link_content or get_name(item)

    def get_link_url(self, item):
        """Get link URL"""
        return '%s?%s' % (self.view_url,
         urlencode({self.get_item_key(item): self.get_item_value(item)}))

    def update(self):
        """Update column"""
        items = [item for item in self.table.values if self.get_item_value(item) in ensure_list(self.request.params.get(self.get_item_key(item), []))]
        if len(items) > 0:
            self.selected_item = items.pop()
            self.table.selected_items = [self.selected_item]


class ContentsLinkColumn(LinkColumn):
    """ContentsLinkColumn"""
    link_name = 'contents.html'


class IndexLinkColumn(LinkColumn):
    """IndexLinkColumn"""
    link_name = 'index.html'


class EditLinkColumn(LinkColumn):
    """EditLinkColumn"""
    link_name = 'edit.html'