# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\widgets\big_widgets.py
# Compiled at: 2011-07-14 09:28:11
"""The bigger TurboGears widgets"""
__all__ = [
 'CalendarDatePicker', 'CalendarDateTimePicker', 'AutoCompleteField', 'AutoCompleteTextField', 'LinkRemoteFunction', 'RemoteForm', 'AjaxGrid', 'URLLink']
import itertools
from datetime import datetime
from turbogears import validators, expose
from turbojson import jsonify
from turbogears.widgets.base import CSSLink, JSLink, CSSSource, JSSource, Widget, WidgetsList, static, mochikit, CoreWD
from turbogears.widgets.i18n import CalendarLangFileLink
from turbogears.widgets.forms import FormField, CompoundFormField, TextField, HiddenField, TableForm, CheckBox, RadioButtonList
from turbogears.widgets.rpc import RPC

class CalendarDatePicker(FormField):
    """Use a Javascript calendar system to allow picking of calendar dates."""
    __module__ = __name__
    template = '\n    <span xmlns:py="http://genshi.edgewall.org/" class="${field_class}">\n    <input type="text" id="${field_id}" class="${field_class}" name="${name}" value="${strdate}" py:attrs="attrs"/>\n    <input type="button" id="${field_id}_trigger" class="date_field_button" value="${button_text}"/>\n    <script type="text/javascript">\n    Calendar.setup({\n        inputField: \'${field_id}\',\n        ifFormat: \'${format}\',\n        button: \'${field_id}_trigger\'\n        <span py:if="picker_shows_time" py:replace="\', showsTime : true\'"/>\n    });\n    </script>\n    </span>\n    '
    params = [
     'attrs', 'skin', 'picker_shows_time', 'button_text', 'format', 'calendar_lang']
    params_doc = {'attrs': 'Extra attributes', 'skin': 'For alternate skins, such as "calendar-blue" or "skins/aqua/theme"', 'picker_shows_time': 'Whether the calendar should let you pick a time, too', 'button_text': 'Text for the button that will show the calendar picker', 'format': 'The date format (default is mm/dd/yyyy)', 'calendar_lang': 'The language to be used in the calendar picker.'}
    attrs = {}
    skin = 'calendar-system'
    picker_shows_time = False
    button_text = 'Choose'
    format = '%m/%d/%Y'
    calendar_lang = None
    _default = None

    def __init__(self, name=None, default=None, not_empty=True, calendar_lang=None, validator=None, format=None, **kw):
        super(CalendarDatePicker, self).__init__(name, **kw)
        self.not_empty = not_empty
        if default is not None or not self.not_empty:
            self._default = default
        if format is not None:
            self.format = format
        if validator is None:
            self.validator = validators.DateTimeConverter(format=self.format, not_empty=self.not_empty)
        else:
            self.validator = validator
        if calendar_lang:
            self.calendar_lang = calendar_lang
        javascript = [
         JSLink(static, 'calendar/calendar.js'), JSLink(static, 'calendar/calendar-setup.js')]
        javascript.append(CalendarLangFileLink(static, language=self.calendar_lang))
        self.javascript = self.javascript + javascript
        if self.skin:
            css = [
             CSSLink(static, 'calendar/%s.css' % self.skin)]
            self.css = self.css + css
        return

    @property
    def default(self):
        if self._default is None and self.not_empty:
            return datetime.now()
        return self._default

    def update_params(self, d):
        super(CalendarDatePicker, self).update_params(d)
        if hasattr(d['value'], 'strftime'):
            d['strdate'] = d['value'].strftime(d['format'])
        else:
            d['strdate'] = d['value']


class CalendarDatePickerDesc(CoreWD):
    __module__ = __name__
    name = 'Calendar'
    for_widget = CalendarDatePicker('date_picker')


class CalendarDateTimePicker(CalendarDatePicker):
    """Javascript calendar system to allow picking of dates with times."""
    __module__ = __name__
    format = '%Y/%m/%d %H:%M'
    picker_shows_time = True


class CalendarDateTimePickerDesc(CoreWD):
    __module__ = __name__
    name = 'Calendar with time'
    for_widget = CalendarDateTimePicker('datetime_picker')


class AutoComplete(Widget):
    """Mixin class for autocomplete fields.

    Performs Ajax-style autocompletion by requesting search
    results from the server as the user types.

    """
    __module__ = __name__
    javascript = [
     mochikit, JSLink(static, 'autocompletefield.js')]
    css = [CSSLink(static, 'autocompletefield.css')]
    params = ['search_controller', 'search_param', 'result_name', 'attrs', 'only_suggest', 'complete_delay', 'take_focus', 'min_chars', 'show_spinner']
    params_doc = {'attrs': 'Extra attributes', 'search_controller': 'Name of the controller returning the auto completions', 'search_param': 'Name of the search parameter ("*" passes all form fields)', 'result_name': 'Name of the result list returned by the controller', 'only_suggest': 'If true, pressing enter does not automatically submit the first list item.', 'complete_delay': 'Delay (in seconds) before loading new auto completions', 'take_focus': 'If true, take focus on load.', 'min_chars': 'Minimum number of characters to type before autocomplete activates', 'show_spinner': 'If false, the spinner (load indicator) is not shown.'}
    attrs = {}
    search_controller = ''
    search_param = 'searchString'
    result_name = 'textItems'
    only_suggest = False
    complete_delay = 0.2
    take_focus = False
    min_chars = 1
    show_spinner = True


class AutoCompleteField(CompoundFormField, AutoComplete):
    """Text field with auto complete functionality and hidden key field."""
    __module__ = __name__
    template = '\n    <span xmlns:py="http://genshi.edgewall.org/" id="${field_id}" class="${field_class}">\n    <script type="text/javascript">\n        AutoCompleteManager${field_id} = new AutoCompleteManager(\'${field_id}\',\n        \'${text_field.field_id}\', \'${hidden_field.field_id}\',\n        \'${search_controller}\', \'${search_param}\', \'${result_name}\',${str(only_suggest).lower()},\n        \'${show_spinner and tg.url([tg.widgets, \'turbogears.widgets/spinner.gif\']) or None}\',\n        ${complete_delay}, ${str(take_focus).lower()}, ${min_chars});\n        addLoadEvent(AutoCompleteManager${field_id}.initialize);\n    </script>\n    ${text_field.display(value_for(text_field), **params_for(text_field))}\n    <img py:if="show_spinner" id="autoCompleteSpinner${field_id}"\n        src="${tg.url([tg.widgets, \'turbogears.widgets/spinnerstopped.png\'])}" alt=""/>\n    <span class="autoTextResults" id="autoCompleteResults${field_id}"/>\n    ${hidden_field.display(value_for(hidden_field), **params_for(hidden_field))}\n    </span>\n    '
    member_widgets = [
     'text_field', 'hidden_field']
    text_field = TextField(name='text')
    hidden_field = HiddenField(name='hidden')


class AutoCompleteFieldDesc(CoreWD):
    __module__ = __name__
    name = 'AutoCompleteField'
    codes = ('AK AL AR AS AZ CA CO CT DC DE FL FM GA GU HI IA ID IL IN KS\n        KY LA MA MD ME MH MI MN MO MP MS MT NC ND NE NH NJ NM NV NY OH\n        OK OR PA PR PW RI SC SD TN TX UM UT VA VI VT WA WI WV WY').split()
    states = ('Alaska Alabama Arkansas American_Samoa Arizona\n        California Colorado Connecticut District_of_Columbia\n        Delaware Florida Federated_States_of_Micronesia Georgia Guam\n        Hawaii Iowa Idaho Illinois Indiana Kansas Kentucky Louisiana\n        Massachusetts Maryland Maine Marshall_Islands Michigan\n        Minnesota Missouri Northern_Mariana_Islands Mississippi\n        Montana North_Carolina North_Dakota Nebraska New_Hampshire\n        New_Jersey New_Mexico Nevada New_York Ohio Oklahoma Oregon\n        Pennsylvania Puerto_Rico Palau Rhode_Island South_Carolina\n        South_Dakota Tennessee Texas U.S._Minor_Outlying_Islands\n        Utah Virginia Virgin_Islands_of_the_U.S. Vermont Washington\n        Wisconsin West_Virginia Wyoming').split()
    states = map(lambda s: s.replace('_', ' '), states)
    state_code = dict(zip(codes, states))
    template = '\n    <form xmlns:py="http://genshi.edgewall.org/" onsubmit="if (\n        this.elements[0].value &amp;&amp; this.elements[1].value)\n        alert(\'The alpha code for \'+this.elements[0].value\n        +\' is \'+this.elements[1].value+\'.\');return false"><table>\n        <tr><th>State</th><td py:content="for_widget.display()"/>\n        <td><input type="submit" value="Show alpha code"/></td></tr>\n    </table></form>\n    '
    full_class_name = 'turbogears.widgets.AutoCompleteField'

    def __init__(self, *args, **kw):
        super(AutoCompleteFieldDesc, self).__init__(*args, **kw)
        self.for_widget = AutoCompleteField(name='state_and_code', search_controller='%s/search' % self.full_class_name, search_param='state', result_name='states')

    @expose('json')
    def search(self, state):
        states = []
        code = state.upper()
        if code in self.state_code:
            states.append((self.state_code[code], code))
        else:
            states.extend([ s for s in zip(self.states, self.codes) if s[0].lower().startswith(state.lower()) ])
        return dict(states=states)


class AutoCompleteTextField(TextField, AutoComplete):
    """Text field with auto complete functionality."""
    __module__ = __name__
    template = '\n    <span xmlns:py="http://genshi.edgewall.org/" class="${field_class}">\n    <script type="text/javascript">\n        AutoCompleteManager${field_id} = new AutoCompleteManager(\'${field_id}\', \'${field_id}\', null,\n        \'${search_controller}\', \'${search_param}\', \'${result_name}\', ${str(only_suggest).lower()},\n        \'${show_spinner and tg.url([tg.widgets, \'turbogears.widgets/spinner.gif\']) or None}\',\n        ${complete_delay}, ${str(take_focus).lower()}, ${min_chars});\n        addLoadEvent(AutoCompleteManager${field_id}.initialize);\n    </script>\n    <input type="text" name="${name}" class="${field_class}" id="${field_id}"\n        value="${value}" py:attrs="attrs"/>\n    <img py:if="show_spinner" id="autoCompleteSpinner${field_id}"\n        src="${tg.url([tg.widgets, \'turbogears.widgets/spinnerstopped.png\'])}" alt=""/>\n    <span class="autoTextResults" id="autoCompleteResults${field_id}"/>\n    </span>\n    '


class AutoCompleteTextFieldDesc(CoreWD):
    __module__ = __name__
    name = 'AutoCompleteTextField'
    states = AutoCompleteFieldDesc.states
    state_code = AutoCompleteFieldDesc.state_code
    template = '\n    <table xmlns:py="http://genshi.edgewall.org/">\n        <tr><th>State</th><td py:content="for_widget.display()"/></tr>\n    </table>\n    '
    full_class_name = 'turbogears.widgets.AutoCompleteTextField'

    def __init__(self, *args, **kw):
        super(AutoCompleteTextFieldDesc, self).__init__(*args, **kw)
        self.for_widget = AutoCompleteTextField(name='state_only', search_controller='%s/search' % self.full_class_name, search_param='state', result_name='states')

    @expose('json')
    def search(self, state):
        states = []
        code = state.upper()
        if code in self.state_code:
            states.append(self.state_code[code])
        else:
            states.extend([ s for s in self.states if s.lower().startswith(state.lower()) ])
        return dict(states=states)


class LinkRemoteFunction(RPC):
    """Link with remote execution.

    Returns a link that executes a POST asynchronously
    and updates a DOM Object with the result of it.

    """
    __module__ = __name__
    template = '\n    <a xmlns:py="http://genshi.edgewall.org/" name="${name}"\n        py:attrs="attrs" py:content="value" onclick="${js}" href="#"/>\n    '
    params = [
     'attrs']
    attrs = {}


class LinkRemoteFunctionDesc(CoreWD):
    __module__ = __name__
    name = 'AJAX remote function'
    states = AutoCompleteFieldDesc.states
    template = '\n    <div id="items">\n        ${for_widget.display("States starting with the letter \'N\'", update="items")}\n    </div>\n    '
    full_class_name = 'turbogears.widgets.LinkRemoteFunction'

    def __init__(self, *args, **kw):
        super(LinkRemoteFunctionDesc, self).__init__(*args, **kw)
        self.for_widget = LinkRemoteFunction(name='linkrf', action='%s/search_linkrf' % self.full_class_name, data=dict(state_starts_with='N'))

    @expose()
    def search_linkrf(self, state_starts_with):
        return ('<br/>').join([ s for s in self.states if s.startswith(state_starts_with) ])


class RemoteForm(RPC, TableForm):
    """AJAX table form.

    A TableForm that submits the data asynchronously and loads the resulting
    HTML into a DOM object

    """
    __module__ = __name__

    def update_params(self, d):
        super(RemoteForm, self).update_params(d)
        d['form_attrs']['onSubmit'] = "return !remoteFormRequest(this, '%s', %s);" % (d.get('update', ''), jsonify.encode(self.get_options(d)))


class RemoteFormDesc(CoreWD):
    __module__ = __name__
    name = 'AJAX Form'
    template = '\n    <div>\n        ${for_widget.display()}\n        <div id="post_data">&nbsp;</div>\n    </div>\n    '
    full_class_name = 'turbogears.widgets.RemoteForm'

    class TestFormFields(WidgetsList):
        __module__ = __name__
        name = TextField()
        age = TextField()
        check = CheckBox()
        radio = RadioButtonList(options=list(enumerate(('Python Java Pascal Ruby').split())), default=3)

    def __init__(self, *args, **kw):
        super(RemoteFormDesc, self).__init__(*args, **kw)
        self.for_widget = RemoteForm(fields=self.TestFormFields(), name='remote_form', update='post_data', action='%s/post_data_rf' % self.full_class_name, before="alert('pre-hook')", confirm='Confirm?')

    @expose()
    def post_data_rf(self, **kw):
        return 'Received data:<br/>%r' % kw


ajaxgridcounter = itertools.count()

class AjaxGrid(Widget):
    """AJAX updateable datagrid based on widget.js grid"""
    __module__ = __name__
    template = '<div id="${id}" xmlns:py="http://genshi.edgewall.org/">\n    <a py:if="refresh_text"\n       href="#"\n       onclick="javascript:${id}_AjaxGrid.refresh(${defaults});return false;">\n       ${refresh_text}\n    </a>\n    <div id="${id}_update"></div>\n    <script type="text/javascript">\n        addLoadEvent(partial(${id}_AjaxGrid.refresh, ${defaults}));\n    </script>\n    </div>\n    '
    params = [
     'refresh_text', 'id', 'defaults']
    defaults = {}
    refresh_text = 'Update'
    id = 'ajaxgrid_%d' % ajaxgridcounter.next()

    def __init__(self, refresh_url, *args, **kw):
        super(AjaxGrid, self).__init__(*args, **kw)
        target = '%s_update' % self.id
        self.javascript = [mochikit, JSLink('turbogears', 'js/widget.js'), JSLink(static, 'ajaxgrid.js'), JSSource("\n                %(id)s_AjaxGrid = new AjaxGrid('%(refresh_url)s', '%(target)s');\n            " % dict(id=self.id, refresh_url=refresh_url, target=target))]

    def update_params(self, d):
        super(AjaxGrid, self).update_params(d)
        d['defaults'] = jsonify.encode(d['defaults'])


class AjaxGridDesc(CoreWD):
    __module__ = __name__
    name = 'AJAX Grid'
    full_class_name = 'turbogears.widgets.AjaxGrid'

    @staticmethod
    def facgen(n):
        total = 1
        yield (0, 1)
        for k in xrange(1, n + 1):
            total *= k
            yield (k, total)

    def __init__(self, *args, **kw):
        super(AjaxGridDesc, self).__init__(*args, **kw)
        self.for_widget = AjaxGrid(refresh_url='%s/update' % self.full_class_name, defaults=dict())
        self.update_count = itertools.count()

    @expose('json')
    def update(self):
        return dict(headers=['N', 'fact(N)'], rows=list(self.facgen(self.update_count.next())))


class URLLink(FormField):
    """Hyperlink"""
    __module__ = __name__
    template = '\n    <a xmlns:py="http://genshi.edgewall.org/"\n       href="$link"\n       target="$target"\n       py:attrs="attrs"\n    >$text</a>\n    '
    params = [
     'target', 'text', 'link', 'attrs']
    attrs = {}
    params_doc = {'link': 'Hyperlink', 'target': 'Specify where the link should be opened', 'text': 'The message to be shown for the link', 'attrs': 'Extra attributes'}