# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/datagrid/grids.py
# Compiled at: 2019-06-12 01:17:17
"""Components for creating customizable datagrids from database data.

Datagrids are used to display a table-based view of data from a database,
complete with pagination, batch selection, sorting, and flexible column
rendering.

Datagrids have one or more :py:class:`Column` subclasses associated, which will
render the data. The datagrid may display a subset of the rendered columns,
and users can choose which of those columns they want displayed, and in which
order.

There are two main types of datagrids:

* :py:class:`DataGrid` is the base class for a datagrid, and will display
  the data with standard numerical page-based pagination.

* :py:class:`AlphanumericDataGrid` is similar, but uses a more specific
  paginator that allows the user to paginate by the first letter/number/symbol
  of the data in a given field. This is useful for lists of users, for
  example.

All datagrids are meant to be subclassed.
"""
from __future__ import unicode_literals
import logging, re, string, traceback, pytz
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.core.paginator import InvalidPage, QuerySetPaginator
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext, Context
from django.template.defaultfilters import date, timesince
from django.template.loader import get_template
from django.utils import six
from django.utils.cache import patch_cache_control
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
try:
    from django.contrib.auth.models import SiteProfileNotAvailable
except ImportError:

    class SiteProfileNotAvailable(Exception):
        pass


from djblets.template.context import get_default_template_context_processors
from djblets.db.query import chainable_select_related_queryset
from djblets.util.compat.django.template.loader import render_template, render_to_string
from djblets.util.decorators import cached_property
from djblets.util.http import get_url_params_except
logger = logging.getLogger(__name__)
_column_registry = {}

class Column(object):
    """A column in a datagrid.

    The column is the primary component of the datagrid. It is used to
    display not only the column header but the HTML for the cell as well.

    Columns can be tied to database fields and can be used for sorting.
    Not all columns have to allow for this, though.

    Columns can have an image, text, or both in the column header. The
    contents of the cells can be instructed to link to the object on the
    row or the data in the cell.

    If a Column defines an :py:attr:`image_class`, then it will be assumed that
    the class represents an icon, perhaps as part of a spritesheet, and will
    display it in a ``<div>``. An :py:attr:`image_url` cannot also be defined.

    Attributes:
        cell_template (unicode):
            The path to a template. If this is not None, this will override
            the default cell_template for the DataGrid the column is in.
    """
    SORT_DESCENDING = 0
    SORT_ASCENDING = 1

    def __init__(self, label=None, id=None, detailed_label=None, detailed_label_html=None, field_name=None, db_field=None, image_url=None, image_class=None, image_width=None, image_height=None, image_alt=b'', shrink=False, expand=False, sortable=False, default_sort_dir=SORT_DESCENDING, link=False, link_func=None, link_css_class=None, cell_clickable=False, css_class=b''):
        """Initialize the column.

        When initializing a column as part of a :py:class:`DataGrid` subclass,
        a number of options can be provided.

        Args:
            id (unicode, optional):
                The unique ID of the column on the datagrid.

            label (unicode, optional):
                The label to show in the column header.

            detailed_label (unicode, optional):
                A detailed label to display in the column customization
                menu. Defaults to ``label``.

            detailed_label_html (unicode, optional):
                A detailed label in HTML form to display in the column
                customization menu. This takes precedence over
                ``detailed_label``.

            field_name (unicode, optional):
                The name of the field on the model containing the data to
                render.

            db_field (unicode, optional):
                The name of the database field containing the field used
                for sorting. Defaults to ``field_name``.

            image_url (unicode, optional):
                The URL to the image used in the header and navigation menu.
                This cannot be used with ``image_class``.

            image_class (unicode, optional):
                The CSS class of a spritesheet icon to use in the header
                and navigation menu. This cannot be used with ``image_url``.

            image_width (int, optional):
                The width of the image.

            image_height (int, optional):
                The height of the image.

            image_alt (unicode, optional):
                The alt text for the image.

            shrink (bool, optional):
                If ``True``, the column's width will be calculated to its
                minimum size.

            expand (bool, optional):
                If ``True``, the column's width will be calculated to its
                maximum size. If there are other expanded columns, they'll
                share the available width equally.

            sortable (bool, optional):
                If ``True``, the column can be sorted. This requires a
                ``db_field`` that allows for sorting.

            default_sort_dir (int, optional):
                The default sorting direction when the user activates sorting.
                Either :py:attr:`SORT_DESCENDING`
                or :py:attr:`SORT_ASCENDING`.

            link (bool, optional):
                If ``True``, the contents will be linked to the URL
                returned by ``link_func`` or
                :py:meth:`DataGrid.link_to_object`.

            link_func (callable, optional):
                Optional function that returns a URL for the link.

            link_css_class (unicode or callable, optional):
                The CSS class or classes to define on ``<a>`` for the link
                for the cell, if setting ``link=True``. This can be a
                function returning the classes.

            cell_clickable (bool, optional):
                If ``True``, clicking anywhere on the cell will navigate to
                the URL defined, if any.

            css_class (unicode, optional):
                The CSS class or classes to define on the cell. This can be
                a function returning the classes.
        """
        assert not (image_class and image_url)
        self.id = id
        self.field_name = field_name
        self.db_field = db_field or field_name
        self.label = label
        self.detailed_label = detailed_label or self.label
        self.detailed_label_html = detailed_label_html or self.detailed_label
        self.image_url = image_url
        self.image_class = image_class
        self.image_width = image_width
        self.image_height = image_height
        self.image_alt = image_alt
        self.shrink = shrink
        self.expand = expand
        self.sortable = sortable
        self.default_sort_dir = default_sort_dir
        self.cell_clickable = False
        self.link = link
        self.link_func = link_func or (lambda state, x, y: state.datagrid.link_to_object(state, x, y))
        self.link_css_class = link_css_class
        self.css_class = css_class
        self.cell_template = None
        return

    @cached_property
    def cell_template_obj(self):
        """Return the cell template, if it exists."""
        if self.cell_template:
            return get_template(self.cell_template)
        else:
            return

    def setup_state(self, state):
        """Set up any state that may be needed for the column.

        This is called once per column per datagrid instance.

        By default, no additional state is set up. Subclasses can override
        this to set any variables they may need.

        Args:
            state (StatefulColumn):
                The state for the DataGrid instance.
        """
        pass

    def get_sort_field(self, state):
        """Return the field used for sorting this column.

        By default, this uses the provided db_field.

        Args:
            state (StatefulColumn):
                The state for the DataGrid instance.

        Returns:
            unicode:
                The field on the model used for sorting. Defaults
                to ``db_field``.
        """
        return self.db_field

    def get_toggle_url(self, state):
        """Return a URL to toggle this column's visibility.

        Args:
            state (StatefulColumn):
                The state for the DataGrid instance.

        Returns:
            unicode: The URL used to toggle column visibility.
        """
        columns = [ column.id for column in state.datagrid.columns ]
        if state.active:
            try:
                columns.remove(self.id)
            except ValueError:
                pass

        else:
            columns.append(self.id)
        url_params = get_url_params_except(state.datagrid.request.GET, b'columns')
        if url_params:
            url_params = url_params + b'&'
        return b'?%scolumns=%s' % (url_params, (b',').join(columns))

    def get_header(self, state):
        """Render the header for the column.

        The column header will include the current sort indicator, if it
        belongs in the sort list. It will also be made clickable in order
        to modify the sort order appropriately, if sortable.

        Args:
            state (StatefulColumn):
                The state for the DataGrid instance.

        Returns:
            unicode: The HTML for the header.
        """
        datagrid = state.datagrid
        in_sort = False
        sort_direction = self.SORT_DESCENDING
        sort_primary = False
        sort_url = b''
        unsort_url = b''
        if self.sortable:
            sort_list = list(datagrid.sort_list)
            if sort_list:
                rev_column_id = b'-%s' % self.id
                new_column_id = self.id
                cur_column_id = b''
                if self.id in sort_list:
                    sort_direction = self.SORT_ASCENDING
                    cur_column_id = self.id
                    new_column_id = rev_column_id
                elif rev_column_id in sort_list:
                    sort_direction = self.SORT_DESCENDING
                    cur_column_id = rev_column_id
                    new_column_id = self.id
                if cur_column_id:
                    in_sort = True
                    sort_primary = sort_list[0] == cur_column_id
                    if not sort_primary:
                        new_column_id = cur_column_id
                    sort_list.remove(cur_column_id)
                sort_list.insert(0, new_column_id)
            else:
                sort_list = [self.id]
            del sort_list[2:]
            url_params = get_url_params_except(datagrid.request.GET, b'sort', b'datagrid-id', b'gridonly', b'columns')
            if url_params:
                url_params = url_params + b'&'
            url_prefix = b'?%ssort=' % url_params
            unsort_url = url_prefix + (b',').join(sort_list[1:])
            sort_url = url_prefix + (b',').join(sort_list)
        return render_template(datagrid.column_header_template_obj, {b'column': self, 
           b'column_state': state, 
           b'in_sort': in_sort, 
           b'sort_ascending': sort_direction == self.SORT_ASCENDING, 
           b'sort_primary': sort_primary, 
           b'sort_url': sort_url, 
           b'unsort_url': unsort_url})

    def collect_objects(self, state, object_list):
        """Iterate through the objects and builds a cache of data to display.

        This optimizes the fetching of data in the grid by grabbing all the
        IDs of related objects that will be queried for rendering, loading
        them all at once, and populating the cache.

        Args:
            state (StatefulColumn):
                The state for the DataGrid instance.

            object_list (list):
                The list of objects being rendered on the datagrid.
        """
        id_field = b'%s_id' % self.field_name
        ids = set()
        model = None
        for obj in object_list:
            if not hasattr(obj, id_field):
                return
            id_value = getattr(obj, id_field)
            if id_value is None:
                continue
            ids.add(id_value)
            if not model:
                field = getattr(obj.__class__, self.field_name).field
                try:
                    model = field.rel.to
                except AttributeError:
                    return

        if model and ids:
            for obj in model.objects.filter(pk__in=ids):
                state.data_cache[obj.pk] = obj

        return

    def render_cell(self, state, obj, render_context):
        """Render the table cell containing column data.

        Args:
            state (StatefulColumn):
                The state for the DataGrid instance.

            obj (object):
                The object being rendered for this row.

            render_context (Context):
                The shared context used for cell renders.

        Returns:
            unicode: The rendered cell as HTML.
        """
        try:
            rendered_data = self.render_data(state, obj)
        except Exception as e:
            logger.exception(b'Error when calling render_data for DataGrid Column %r: %s', self, e)
            rendered_data = b''

        url = b''
        css_class = b''
        link_css_class = b''
        if self.link:
            if self.link_func:
                try:
                    url = self.link_func(state, obj, rendered_data)
                except AttributeError:
                    pass

            elif render_context:
                url = render_context.get(b'_datagrid_object_url')
        if self.css_class:
            if six.callable(self.css_class):
                css_class = self.css_class(obj)
            else:
                css_class = self.css_class
        if self.link_css_class:
            if six.callable(self.link_css_class):
                link_css_class = self.link_css_class(obj)
            else:
                link_css_class = self.link_css_class
        key = b'%s:%s:%s:%s:%s' % (state.last, rendered_data, url, css_class,
         link_css_class)
        if key not in state.cell_render_cache:
            if url:
                css_class = b'%s has-link' % css_class
            ctx = {}
            if render_context:
                ctx.update(render_context)
            ctx.update({b'column': self, 
               b'column_state': state, 
               b'css_class': css_class.strip(), 
               b'link_css_class': link_css_class, 
               b'url': url, 
               b'data': mark_safe(rendered_data)})
            template = self.cell_template_obj
            if template is None:
                template = state.datagrid.cell_template_obj
            state.cell_render_cache[key] = render_template(template, ctx)
        return state.cell_render_cache[key]

    def render_data(self, state, obj):
        """Render the column data within the cell.

        Args:
            state (StatefulColumn):
                The state for the DataGrid instance.

            obj (object):
                The object being rendered for this row.

        Returns:
            unicode: The rendered data as HTML.
        """
        id_field = b'%s_id' % self.field_name
        if id_field in obj.__dict__:
            pk = obj.__dict__[id_field]
            if pk in state.data_cache:
                return state.data_cache[pk]
            value = getattr(obj, self.field_name)
            state.data_cache[pk] = escape(value)
            return value
        else:
            value = obj
            for field_name in self.field_name.split(b'.'):
                if field_name:
                    value = getattr(value, field_name)
                    if six.callable(value):
                        value = value()

            return escape(value)

    def augment_queryset(self, state, queryset):
        """Augment a queryset with new queries.

        Subclasses can override this to extend the queryset to provide
        additional information, usually using queryset.extra(). This must
        return a queryset based on the original queryset.

        This should not restrict the query in any way, or the datagrid may
        not operate properly. It must only add additional data to the
        queryset.

        Args:
            state (StatefulColumn):
                The state for the DataGrid instance.

            queryset (QuerySet):
                The queryset to augment.

        Returns:
            QuerySet: The resulting QuerySet.
        """
        return queryset


class StatefulColumn(object):
    """A stateful wrapper for a Column instance.

    Columns must be stateless, as they are shared across all instances of
    a particular DataGrid. However, some state is needed for columns, such
    as their widths or active status.

    StatefulColumn wraps a :py:class:`Column` instance and provides state
    storage, and also provides a convenient way to call methods on a Column and
    pass the state.

    Attributes owned by the Column can be accessed directly through the
    StatefulColumn.

    Likewise, any functions owned by the Column can be accessed as well.
    The function will be invoked with this StatefulColumn as the first
    parameter passed.
    """

    def __init__(self, datagrid, column):
        """Initialize the column state.

        Args:
            datagrid (DataGrid):
                The DataGrid instance owning this column state.

            column (Column):
                The column instance this state is associated with.
        """
        self.datagrid = datagrid
        self.column = column
        self.active = False
        self.last = False
        self.width = 0
        self.data_cache = {}
        self.cell_render_cache = {}
        try:
            column.setup_state(self)
        except Exception as e:
            logger.exception(b'Error when calling setup_state for DataGrid Column %r: %s', self.column, e)

    @property
    def toggle_url(self):
        """The visibility toggle URL of the column.

        This is a convenience used by templates to call
        :py:meth:`Column.get_toggle_url` with the current state.
        """
        return self.column.get_toggle_url(self)

    @property
    def header(self):
        """The header of the column.

        This is a convenience used by templates to call
        :py:meth:`Column.get_header` with the current state.
        """
        return self.column.get_header(self)

    def __getattr__(self, name):
        """Returns an attribute from the parent Column.

        This is called when accessing an attribute not found directly on
        StatefulColumn. The attribute will be fetched from the Column
        (if it exists there).

        In the case of accessing a function, a wrapper will be returned
        that will automatically pass this StatefulColumn instance as the
        first parameter.

        Args:
            name (unicode): The attribute to fetch from the column.

        Returns:
            The attribute value from the column.
        """
        result = getattr(self.column, name)
        if callable(result):
            return lambda *args, **kwargs: result(self, *args, **kwargs)
        return result


class CheckboxColumn(Column):
    """A column that renders a checkbox.

    The :py:meth:`is_selectable` and :py:meth:`is_selected` functions can be
    overridden to control whether a checkbox is displayed in a row and whether
    that checkbox is initially checked.

    The checkboxes have a ``data-object-id`` attribute that contains the ID of
    the object that row represents. This allows the JavaScript code to
    determine which rows have been checked, and operate on that
    accordingly.

    The checkboxes also have a ``data-checkbox-name`` attribute that
    contains the value passed in to the ``checkbox_name`` parameter of its
    constructor.
    """

    def __init__(self, checkbox_name=b'select', shrink=True, show_checkbox_header=True, detailed_label=_(b'Select Rows'), *args, **kwargs):
        """Initialize the column.

        Args:
            checkbox_name (unicode):
                The name set in ``data-checkbox-name``.

            shrink (bool):
                If ``True``, the column's width will be calculated to its
                minimum size.

            show_checkbox_header (bool):
                If ``True``, a checkbox will be used for the column header.
        """
        super(CheckboxColumn, self).__init__(shrink=shrink, label=format_html(b'<input class="datagrid-header-checkbox" type="checkbox" data-checkbox-name="{0}" />', checkbox_name), detailed_label=detailed_label, detailed_label_html=format_html(b'<input type="checkbox" /> {0}', detailed_label), *args, **kwargs)
        self.show_checkbox_header = show_checkbox_header
        self.checkbox_name = checkbox_name
        self.cell_template = b'datagrid/cell_no_link.html'

    def render_data(self, state, obj):
        if self.is_selectable(state, obj):
            checked = b''
            if self.is_selected(state, obj):
                checked = mark_safe(b'checked="true"')
            return format_html(b'<input type="checkbox" data-object-id="{0}" data-checkbox-name="{1}" {2} />', obj.pk, self.checkbox_name, checked)
        else:
            return b''

    def is_selectable(self, state, obj):
        """Returns whether an object can be selected.

        If this returns False, no checkbox will be rendered for this item.
        """
        return True

    def is_selected(self, state, obj):
        """Returns whether an object has been selected.

        If this returns True, the checkbox will be checked.
        """
        return False


class DateTimeColumn(Column):
    """A column that renders a date or time."""

    def __init__(self, label, format=None, sortable=True, timezone=pytz.utc, *args, **kwargs):
        super(DateTimeColumn, self).__init__(label, sortable=sortable, *args, **kwargs)
        self.format = format
        self.timezone = timezone

    def render_data(self, state, obj):
        datetime = getattr(obj, self.field_name)
        if settings.USE_TZ:
            datetime = pytz.utc.normalize(datetime).astimezone(self.timezone)
        return date(datetime, self.format)


class DateTimeSinceColumn(Column):
    """A column that renders a date or time relative to now."""

    def __init__(self, label, sortable=True, timezone=pytz.utc, *args, **kwargs):
        super(DateTimeSinceColumn, self).__init__(label, sortable=sortable, *args, **kwargs)

    def render_data(self, state, obj):
        return _(b'%s ago') % timesince(getattr(obj, self.field_name))


class DataGrid(object):
    """A paginated table of data based on queries from a database.

    A datagriad represents a list of objects, sorted and organized by
    columns. The sort order and column lists can be customized. allowing
    users to view this data however they prefer.

    This is meant to be subclassed for specific uses. The subclasses are
    responsible for defining one or more column types. It can also set
    one or more of the following optional variables:

    Attributes:
        title (unicode):
            The title of the grid.

        profile_sort_field (unicode):
            The variable name in the user profile where the sort order can be
            loaded and saved.

        profile_columns_field (unicode):
            The variable name in the user profile where the columns list can be
            loaded and saved.

        paginate_by (int):
            The number of items to show on each page of the grid. The default
            is 50.

        paginate_orphans (int):
            If this number of objects or fewer are on the last page, it will be
            rolled into the previous page. The default is 3.

        page (int):
            The page to display. If this is not specified, the ``?page=``
            variable passed in the URL will be used, or 1 if that is not
            specified.

        listview_template (unicode):
            The template used to render the list view. The default is
            :file:`datagrid/listview.html`.

        column_header_template (unicode):
            The template used to render each column header. The default is
            :file:`datagrid/column_header.html`.

        cell_template (unicode):
            The template used to render a cell of data. The default is
            :file:`datagrid/cell.html`.

        optimize_sorts (bool):
            Whether or not to optimize queries when using multiple sorts. This
            can offer a speed improvement, but may need to be turned off for
            more advanced querysets (such as when using ``extra()``).
            The default is ``True``.
    """
    _columns = None

    @classmethod
    def add_column(cls, column):
        """Add a new column for this datagrid.

        This can be used to add columns to a DataGrid subclass after
        the subclass has already been defined.

        The column added must have a unique ID already set.

        Args:
            column (Column):
                The column to add.
        """
        cls._populate_columns()
        if not column.id:
            raise KeyError(b'Custom datagrid columns must have a unique id attribute.')
        if column.id in _column_registry[cls]:
            raise KeyError(b'"%s" is already a registered column for %s' % (
             column.id, cls.__name__))
        _column_registry[cls][column.id] = column

    @classmethod
    def remove_column(cls, column):
        """Remove a column from this datagrid.

        This can be used to remove columns previously added through
        :py:meth:`add_column`.

        Args:
            column (Column):
                The column to remove.
        """
        cls._populate_columns()
        try:
            del _column_registry[cls][column.id]
        except KeyError:
            raise KeyError(b'"%s" is not a registered column for %s' % (
             column.id, cls.__name__))

    @classmethod
    def get_column(cls, column_id):
        """Return the column with the given ID.

        If not found, this will return None.

        Args:
            column_id (int):
                The index of the column to return.

        Returns:
            Column: The resulting column at the given index.
        """
        cls._populate_columns()
        return _column_registry[cls].get(column_id)

    @classmethod
    def get_columns(cls):
        """Return the list of registered columns for this datagrid.

        Returns:
            list of Column: The list of columns registered on this datagrid.
        """
        cls._populate_columns()
        return six.itervalues(_column_registry[cls])

    @classmethod
    def _populate_columns(cls):
        """Populate the default list of columns for the datagrid.

        The default list contains all columns added in the class definition.
        """
        if cls not in _column_registry:
            _column_registry[cls] = {}
            for key in dir(cls):
                column = getattr(cls, key)
                if isinstance(column, Column):
                    column.id = key
                    if not column.field_name:
                        column.field_name = column.id
                    if not column.db_field:
                        column.db_field = column.field_name
                    cls.add_column(column)

    def __init__(self, request, queryset=None, title=b'', extra_context={}, optimize_sorts=True, model=None):
        """Initialize the datagrid.

        Args:
            request (HttpRequest):
                The HTTP request from the client.

            queryset (QuerySet):
                A QuerySet returning the objects to render in the grid.

            title (unicode):
                The displayed title of the datagrid.

            extra_context (dict):
                Extra context variables to render on the datagrid template.

            optimize_sorts (bool):
                If ``True``, sorting will be optimized, reducing the
                complexity of the queries. This is the default.

            model (Model):
                The model for the objects in the datagrid. Defaults to the
                model associated with ``queryset``.
        """
        self.request = request
        self.queryset = queryset
        self.rows = []
        self.columns = []
        self.column_map = {}
        self.id_list = []
        self.paginator = None
        self.page = None
        self.sort_list = None
        self.state_loaded = False
        self.page_num = 0
        self.id = None
        self.extra_context = dict(extra_context)
        self.optimize_sorts = optimize_sorts
        self.special_query_args = []
        self._model = model
        if not hasattr(request, b'datagrid_count'):
            request.datagrid_count = 0
        self.id = b'datagrid-%s' % request.datagrid_count
        request.datagrid_count += 1
        self.title = title
        self.profile_sort_field = None
        self.profile_columns_field = None
        self.paginate_by = 50
        self.paginate_orphans = 3
        self.listview_template = b'datagrid/listview.html'
        self.column_header_template = b'datagrid/column_header.html'
        self.cell_template = b'datagrid/cell.html'
        self.paginator_template = b'datagrid/paginator.html'
        return

    @cached_property
    def cell_template_obj(self):
        """The rendered template used for cells on this datagrid.

        This will only be generated once, and reused for all cells.
        """
        obj = get_template(self.cell_template)
        if not obj:
            logger.error(b"Unable to load template '%s' for datagrid cell. This may be an installation issue.", self.cell_template, request=self.request)
        return obj

    @cached_property
    def column_header_template_obj(self):
        """The rendered template used for column headers on this datagrid.

        This will only be generated once, and reused for all headers.
        """
        obj = get_template(self.column_header_template)
        if not obj:
            logger.error(b"Unable to load template '%s' for datagrid column headers. This may be an installation issue.", self.column_header_template, request=self.request)
        return obj

    @property
    def all_columns(self):
        """All columns in the datagrid, sorted by label."""
        return [ self.get_stateful_column(column) for column in sorted(self.get_columns(), key=lambda x: x.detailed_label)
               ]

    @property
    def model(self):
        """The model representing the objects shown in the grid."""
        if self._model is None:
            return self.queryset.model
        else:
            return self._model

    def get_stateful_column(self, column):
        """Return a StatefulColumn for the given Column instance.

        If one has already been created, it will be returned.

        Args:
            column (Column):
                The column associated with the stateful column.

        Returns:
            StatefulColumn: The column state associated with the column.
        """
        if column not in self.column_map:
            self.column_map[column] = StatefulColumn(self, column)
        return self.column_map[column]

    def load_state(self, render_context=None):
        """Load the state of the datagrid.

        This will retrieve the user-specified or previously stored
        sorting order and columns list, as well as any state a subclass
        may need.

        Args:
            render_context (Context):
                Common template variable context to render on the datagrid.
        """
        if self.state_loaded:
            return
        else:
            profile_sort_list = None
            profile_columns_list = None
            profile = None
            profile_dirty = False
            if self.request.user.is_authenticated():
                profile = self.get_user_profile()
                if profile:
                    if self.profile_sort_field:
                        profile_sort_list = getattr(profile, self.profile_sort_field, None)
                    if self.profile_columns_field:
                        profile_columns_list = getattr(profile, self.profile_columns_field, None)
            colnames = self.request.GET.get(b'columns', profile_columns_list) or b''
            columns = filter(None, [ self.get_column(colname) for colname in colnames.split(b',')
                                   ])
            if not columns:
                colnames = (b',').join(self.default_columns)
                columns = [ self.get_column(colname) for colname in self.default_columns
                          ]
            expand_columns = []
            normal_columns = []
            for column_def in columns:
                column = self.get_stateful_column(column_def)
                self.columns.append(column)
                column.active = True
                if column.expand:
                    expand_columns.append(column)
                elif column.shrink:
                    column.width = 0
                else:
                    normal_columns.append(column)

            self.columns[(-1)].last = True
            total_pct = 100
            normal_column_width = total_pct / (len(self.columns) + len(expand_columns))
            for column in normal_columns:
                column.width = normal_column_width
                total_pct -= normal_column_width

            if len(expand_columns) > 0:
                expanded_column_width = total_pct / len(expand_columns)
            else:
                expanded_column_width = 0
            for column in expand_columns:
                column.width = expanded_column_width

            sort_str = self.request.GET.get(b'sort', profile_sort_list)
            if sort_str:
                self.sort_list = []
                for sort_item in sort_str.split(b','):
                    if sort_item[0] == b'-':
                        base_sort_item = sort_item[1:]
                    else:
                        base_sort_item = sort_item
                    column = self.get_column(base_sort_item)
                    if column and column.sortable:
                        self.sort_list.append(sort_item)

            else:
                self.sort_list = self.default_sort
                sort_str = (b',').join(self.sort_list)
            if self.load_extra_state(profile):
                profile_dirty = True
            if profile:
                if self.profile_columns_field and colnames != profile_columns_list:
                    setattr(profile, self.profile_columns_field, colnames)
                    profile_dirty = True
                if self.profile_sort_field and sort_str != profile_sort_list:
                    setattr(profile, self.profile_sort_field, sort_str)
                    profile_dirty = True
                if profile_dirty:
                    profile.save()
            self.state_loaded = True
            self.precompute_objects(render_context)
            return

    def get_user_profile(self):
        """Return the object, if any, to use for the user profile state.

        Returns:
            The object, if any, used to store and retrieve persistent
            profile state for the datagrid.
        """
        if hasattr(self.request.user, b'get_profile'):
            try:
                return self.request.user.get_profile()
            except ObjectDoesNotExist:
                pass
            except SiteProfileNotAvailable:
                pass

        return

    def load_extra_state(self, profile):
        """Load any extra state needed for this grid.

        This is used by subclasses that may have additional data to load
        and save.

        Args:
            profile (Model):
                The profile model instance to load from, if any.

        Returns:
            bool:
                Subclasses must return ``True`` if any profile-stored
                state has changed, or ``False`` otherwise.
        """
        return False

    def precompute_objects(self, render_context=None):
        """Pre-compute all objects used to render the datagrid.

        This builds the queryset and stores the list of objects for use in
        rendering the datagrid. It takes into consideration sorting,
        the current page, and augmented queries from columns.

        Args:
            render_context (Context):
                The common template variable context to render on the datagrid,
                provided in the constructor.
        """
        query = self.queryset
        use_select_related = False
        sort_list = []
        for sort_item in self.sort_list:
            if sort_item[0] == b'-':
                base_sort_item = sort_item[1:]
                prefix = b'-'
            else:
                base_sort_item = sort_item
                prefix = b''
            if sort_item:
                column = self.get_column(base_sort_item)
                if not column:
                    logger.warning(b'Skipping non-existing sort column "%s"', base_sort_item, request=self.request)
                    continue
                elif not column.sortable:
                    logger.warning(b'Skipping column "%s" which is not sortable', base_sort_item, request=self.request.user.username)
                    continue
                stateful_column = self.get_stateful_column(column)
                if stateful_column:
                    try:
                        sort_field = stateful_column.get_sort_field()
                    except Exception as e:
                        logger.exception(b'Error when calling get_sort_field for DataGrid Column %r: %s', column, e, request=self.request)
                        continue

                    if sort_field:
                        sort_list.append(prefix + sort_field)
                    if b'.' in sort_field:
                        use_select_related = True

        if sort_list:
            query = query.order_by(*sort_list)
        query = self.post_process_queryset(query)
        if hasattr(query, b'distinct'):
            query = query.distinct()
        self.paginator = self.build_paginator(query)
        page_num = self.request.GET.get(b'page', 1)
        if page_num == b'last':
            page_num = self.paginator.num_pages
        try:
            self.page = self.paginator.page(page_num)
        except InvalidPage:
            raise Http404

        self.id_list = []
        if self.optimize_sorts and len(sort_list) > 0:
            if hasattr(self.page.object_list, b'values_list'):
                self.id_list = list(self.page.object_list.values_list(b'pk', flat=True))
            else:
                self.id_list = [ int(obj.pk) for obj in self.page.object_list ]
            self.page.object_list = self.post_process_queryset(self.model.objects.filter(pk__in=self.id_list).order_by())
        if use_select_related:
            self.page.object_list = self.page.object_list.select_related(depth=1)
        if self.id_list:
            index = dict([ (id, pos) for pos, id in enumerate(self.id_list) ])
            object_list = [None] * len(self.id_list)
            for obj in list(self.page.object_list):
                object_list[index[obj.pk]] = obj

        else:
            object_list = list(self.page.object_list)
        for column in self.columns:
            column.collect_objects(object_list)

        if render_context is None:
            render_context = self._build_render_context()
        try:
            self.rows = []
            for obj in object_list:
                if obj is None:
                    continue
                if hasattr(obj, b'get_absolute_url'):
                    obj_url = obj.get_absolute_url()
                else:
                    obj_url = None
                render_context[b'_datagrid_object_url'] = obj_url
                self.rows.append({b'object': obj, 
                   b'cells': [ column.render_cell(obj, render_context) for column in self.columns
                           ]})

        except Exception as e:
            logger.exception(b'Error when calling render_cell for DataGrid Column %r: %s', column, e)

        return

    def post_process_queryset(self, queryset):
        """Add column-specific data to the queryset.

        Individual columns can define additional joins and extra info to add on
        to the queryset. This handles adding all of those.

        Args:
            queryset (django.db.models.query.QuerySet):
                The queryset to augment.

        Returns:
            django.db.models.query.QuerySet:
            The resulting augmented QuerySet.
        """
        queryset = chainable_select_related_queryset(queryset)
        for column in self.columns:
            try:
                queryset = column.augment_queryset(queryset)
            except Exception as e:
                logger.exception(b'Error when calling augment_queryset for DataGrid Column %r: %s', column, e)

        return queryset

    def render_listview(self, render_context=None):
        """Render the standard list view of the grid.

        This can be called from templates.

        Args:
            render_context (Context):
                The common template variable context to render on the datagrid,
                provided in the constructor.

        Returns:
            unicode: The rendered HTML for the datagrid page.
        """
        try:
            if render_context is None:
                render_context = self._build_render_context()
            self.load_state(render_context)
            context = {b'datagrid': self}
            context.update(self.extra_context)
            context.update(render_context)
            return render_to_string(self.listview_template, context)
        except Exception:
            trace = traceback.format_exc()
            logger.exception(b'Failed to render datagrid:\n%s', trace, request=self.request)
            return format_html(b'<pre>{0}</pre>', trace)

        return

    def render_listview_to_response(self, request=None, render_context=None):
        """Render the listview to a response.

        The rendered result will not be cached by the browser.

        Args:
            request (HttpRequest):
                The HTTP request from the client.

            render_context (Context):
                The common template variable context to render on the datagrid,
                provided in the constructor.

        Returns:
            HttpResponse: The HTTP response to send to the client.
        """
        response = HttpResponse(six.text_type(self.render_listview(render_context)))
        patch_cache_control(response, no_cache=True, no_store=True, max_age=0, must_revalidate=True)
        return response

    def render_to_response(self, template_name, extra_context={}):
        """Render the entire datagrid page to a response.

        This will render the entire page, given the specified template, with
        the datagrid as a part of it. This is the primary function a view
        will be using to render the page.

        Args:
            template_name (unicode):
                The template for the page.

            extra_context (dict):
                Extra context variables to use in the template.

        Returns:
            HttpResponse: The HTTP response to send to the client.
        """
        render_context = self._build_render_context()
        self.load_state(render_context)
        if self.request.GET.get(b'gridonly', False) and self.request.GET.get(b'datagrid-id', None) == self.id:
            return self.render_listview_to_response(render_context=render_context)
        else:
            context = {b'datagrid': self}
            context.update(extra_context)
            context.update(render_context)
            return render_to_response(template_name, Context(context))

    def render_paginator(self, adjacent_pages=3):
        """Render the paginator for the datagrid.

        This can be called from templates.

        Args:
            adjacent_pages (int):
                The number of adjacent page numbers to show in the
                paginator.

        Returns:
            unicode: The paginator as HTML.
        """
        extra_query = get_url_params_except(self.request.GET, b'page', b'gridonly', *self.special_query_args)
        page_nums = range(max(1, self.page.number - adjacent_pages), min(self.paginator.num_pages, self.page.number + adjacent_pages) + 1)
        if extra_query:
            extra_query += b'&'
        context = {b'is_paginated': self.page.has_other_pages(), 
           b'hits': self.paginator.count, 
           b'results_per_page': self.paginate_by, 
           b'page': self.page.number, 
           b'pages': self.paginator.num_pages, 
           b'page_numbers': page_nums, 
           b'has_next': self.page.has_next(), 
           b'has_previous': self.page.has_previous(), 
           b'show_first': 1 not in page_nums, 
           b'show_last': self.paginator.num_pages not in page_nums, 
           b'extra_query': extra_query}
        if self.page.has_next():
            context[b'next'] = self.page.next_page_number()
        else:
            context[b'next'] = None
        if self.page.has_previous():
            context[b'previous'] = self.page.previous_page_number()
        else:
            context[b'previous'] = None
        context.update(self.extra_context)
        return render_to_string(self.paginator_template, context)

    def build_paginator(self, queryset):
        """Build the paginator for the datagrid.

        This can be overridden to use a special paginator or to perform
        any kind of processing before passing on the query.

        Args:
            queryset (object):
                A queryset-compatible object.

        Returns:
            A populated paginator object.
        """
        return QuerySetPaginator(queryset, self.paginate_by, self.paginate_orphans)

    def _build_render_context(self):
        """Build a dictionary containing RequestContext contents.

        A RequestContext can be expensive, so it's best to reuse the
        contents of one when possible. This is not easy with a standard
        RequestContext, but it's possible to build one and then pull out
        the contents into a dictionary.
        """
        request = self.request
        render_context = {}
        for context_processor in get_default_template_context_processors():
            render_context.update(context_processor(request))

        return render_context

    @staticmethod
    def link_to_object(state, obj, value):
        """Return a URL for the given object.

        This defaults to calling ``obj.get_absolute_url``.

        Returns:
            unicode: The URL for the object.
        """
        return obj.get_absolute_url()

    @staticmethod
    def link_to_value(state, obj, value):
        """Return a URL for the given value.

        This defaults to calling ``value.get_absolute_url``.

        Returns:
            unicode: The URL for the value.
        """
        return value.get_absolute_url()


class AlphanumericDataGrid(DataGrid):
    """A DataGrid subclass for an alphanumerically-paginated datagrid.

    This is useful for datasets that need to be queried alphanumerically,
    according to the starting character of their ``sortable`` column.
    """

    def __init__(self, request, queryset, sortable_column, extra_regex=b'^[0-9].*', *args, **kwargs):
        """Initialize the datagrid.

        Args:
            request (HttpRequest):
                The HTTP request from the client.

            queryset (QuerySet):
                A QuerySet returning the objects to render in the grid.

            sortable_column (unicode):
                The model field used for the alphanumeric prefixes.

            extra_regex (unicode):
                A regex used for matching the beginning of entries in
                ``sortable_column``.
        """
        self.current_letter = request.GET.get(b'letter', b'all')
        regex_match = re.compile(extra_regex)
        if self.current_letter == b'all':
            pass
        elif self.current_letter.isalpha():
            queryset = queryset.filter(**{sortable_column + b'__istartswith': self.current_letter})
        elif regex_match.match(self.current_letter):
            queryset = queryset.filter(**{sortable_column + b'__regex': extra_regex})
        else:
            raise Http404
        super(AlphanumericDataGrid, self).__init__(request, queryset, *args, **kwargs)
        self.extra_context[b'current_letter'] = self.current_letter
        self.extra_context[b'letters'] = [b'all', b'0'] + list(string.ascii_uppercase)
        self.special_query_args.append(b'letter')
        self.paginator_template = b'datagrid/alphanumeric_paginator.html'