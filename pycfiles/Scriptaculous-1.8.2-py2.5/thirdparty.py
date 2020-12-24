# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scriptaculous/thirdparty.py
# Compiled at: 2008-06-15 15:56:09
import itertools
from widgets import prototype_js, scriptaculous_js
from turbogears import expose
from turbogears.widgets import PasswordField, CSSLink, JSLink, JSSource
from turbogears.widgets.base import CompoundWidget, Widget, CoreWD
idcounter = itertools.count()

class PasswordStrengthField(PasswordField):
    """A standard, single-line password field with strength meter."""
    template = 'scriptaculous.templates.password_strength_field'
    css = [CSSLink('scriptaculous', 'css/thirdparty/password_strength.css')]
    javascript = [prototype_js, scriptaculous_js,
     JSLink('scriptaculous', 'javascript/thirdparty/password_strength.js')]


class PasswordStrengthFieldDesc(CoreWD):
    name = 'Scriptaculous Password Strength Field'
    show_separately = True
    template = '\n    <div>\n        Password:<br/>\n        ${for_widget.display()}\n    </div>\n    '
    full_class_name = 'scriptaculous.thirdparty.PasswordStrengthField'

    def __init__(self, *args, **kw):
        super(PasswordStrengthFieldDesc, self).__init__(*args, **kw)
        self.for_widget = PasswordStrengthField(label='password')


class Tabber(Widget):
    """This widget includes the tabber js and css into your rendered
    page so you can create tabbed DIVs by assigning them the 'panel' class
    and invoking ProtoTabs() on yout tabSet UL.
    """
    css = [
     CSSLink('scriptaculous', 'css/thirdparty/tabs.css')]
    javascript = [prototype_js, scriptaculous_js,
     JSLink('scriptaculous', 'javascript/thirdparty/prototabs.js')]


tabberWidget = Tabber()

class TabberDesc(CoreWD):
    name = 'Scriptaculous/Prototabs Tabber'
    show_separately = True
    for_widget = Tabber()
    full_class_name = 'scriptaculous.thirdparty.Tabber'
    template = '<div>\n\t<script>\n\t\tEvent.observe(window, \'load\', function(){\n\t\t\tvar tabSet1 = new ProtoTabs(\'tabSet1\', {defaultPanel: \'mytab2\', ajaxUrls: {\n\t\t\t\t\tmytab3: \'scriptaculous.thirdparty.Tabber/dynamic_tab_content\',\n\t\t\t\t}\n\t\t\t});\n\t\t});\n\t</script>\n\t<div class="tabs10">\n\t\t<ul id="tabSet1">\n\t\t\t<li><a href="#mytab1"><span>static</span></a></li>\n\t\t\t<li><a href="#mytab2"><span>default</span></a></li>\n\t\t\t<li><a href="#mytab3"><span>asynchronous</span></a></li>\n\t\t</ul>\n\t</div>\n\t<div id="mytab1" class="panel">\n\t\tTab with static content. E.g., from your controller.\n\t</div>\n\t<div id="mytab2" class="panel">\n\t\tTab which is shown first. I.e., by definition.\n\t</div>\n\t<div id="mytab3" class="panel">\n\t\tThis gets overriden by the AJAX request beingt invoked each time this one gets selected.\n\t</div></div>'

    @expose()
    def dynamic_tab_content(self):
        return 'This text has been <em>dynamically</em> loaded by an AJAX request.'


class Rating(Widget):
    """This widget includes the unobtrusive CSS based rating widget.
    For a more detailed description please see:
    http://livepipe.net/projects/control_rating/
    """
    css = [
     CSSLink('scriptaculous', 'css/thirdparty/control.rating.css')]
    javascript = [prototype_js, scriptaculous_js,
     JSLink('scriptaculous', 'javascript/thirdparty/control.rating.js')]


class RatingDesc(CoreWD):
    name = 'Scriptaculous Control.Rating'
    show_separately = True
    for_widget = Rating()
    full_class_name = 'scriptaculous.thirdparty.Rating'
    template = '<div>\n    <table width="100%" cellpadding="0" cellspacing="0" class="api_table">\n\t\t<thead>\n\t\t\t<tr><td width="300">Example</td><td class="right">Options</td></tr>\n\t\t</thead>\n\t\t<tbody>\n\t\t\t<tr>\n\t\t\t\t<td><div id="rating_one" class="rating_container">\n\t\t\t\t\t<a href="#" class="rating_on"></a>\n\t\t\t\t\t<a href="#" class="rating_on"></a>\n\t\t\t\t\t<a href="#" class="rating_half"></a>\n\t\t\t\t\t<a href="#" class="rating_off"></a>\n\t\t\t\t\t<a href="#" class="rating_off"></a>\n\t\t\t\t</div></td>\n\t\t\t\t<td class="right">{}</td>\n\t\t\t</tr>\n\t\t\t<tr>\n\t\t\t\t<td><div id="rating_two" class="rating_container"></div></td>\n\t\t\t\t<td class="right">{value: 2.4}</td>\n\t\t\t</tr>\n\t\t\t<tr>\n\t\t\t\t<td><div id="rating_four" class="rating_container"></div></td>\n\t\t\t\t<td class="right">{value: 4, rated: true}</td>\n\t\t\t</tr>\n\t\t\t<tr>\n\t\t\t\t<td><div id="rating_five" class="rating_container"></div></td>\n\t\t\t\t<td class="right">{value: 6, rated: false, max:9}</td>\n\t\t\t</tr>\n\t\t\t<tr>\n\t\t\t\t<td><div id="rating_six" class="rating_container"></div></td>\n\t\t\t\t<td class="right">{value: 6, rated: false, min: 3, max: 12, multiple: true, reverse: true}</td>\n\t\t\t</tr>\n\t\t\t<tr>\n\t\t\t\t<td><div id="rating_seven" class="rating_container"></div><input id="rating_seven_input" value="2" style="width:50px;"/></td>\n\t\t\t\t<td class="right">{input: \'rating_seven_input\', multiple: true}</td>\n\t\t\t</tr>\n\t\t\t<tr>\n\t\t\t\t<td><div id="rating_eight" class="rating_container"></div>\n\t\t\t\t<select id="rating_eight_select">\n\t\t\t\t\t<option value="1">Bad</option>\n\t\t\t\t\t<option value="2">Good</option>\n\t\t\t\t\t<option value="3">Great</option>\n\t\t\t\t\t<option value="4">Excellent</option>\n\t\t\t\t\t<option value="5">Really Excellent</option>\n\t\t\t\t</select></td>\n\t\t\t\t<td class="right">{input: \'rating_eight_select\', multiple: true}</td>\n\t\t\t</tr>\n\t\t</tbody>\n\t</table>\n\t<script>\n\t\tvar rating_one = new Control.Rating(\'rating_one\');\n\t\tvar rating_two = new Control.Rating(\'rating_two\',{value: 2.4});\n\t\tvar rating_four = new Control.Rating(\'rating_four\',{value: 4,rated: true});\n\t\tvar rating_five = new Control.Rating(\'rating_five\',{value: 6,rated: false,max:9});\n\t\tvar rating_six = new Control.Rating(\'rating_six\',{\n\t\t\tvalue: 6,\n\t\t\trated: false,\n\t\t\tmin: 3,\n\t\t\tmax: 12,\n\t\t\tmultiple: true,\n\t\t\treverse: true\n\t\t});\n\t\tvar rating_seven = new Control.Rating(\'rating_seven\',{\n\t\t\tinput: \'rating_seven_input\',\n\t\t\tmultiple: true\n\t\t});\n\t\tvar rating_eight = new Control.Rating(\'rating_eight\',{\n\t\t\tinput: \'rating_eight_select\',\n\t\t\tmultiple: true\n\t\t});\n\n\t</script></div>'


class ModalBox(Widget):
    css = [
     CSSLink('scriptaculous', 'css/thirdparty/modalbox.css')]
    javascript = [prototype_js, scriptaculous_js,
     JSLink('scriptaculous', 'javascript/thirdparty/modalbox.js')]


modalbox = ModalBox()

class ModalBoxDesc(CoreWD):
    name = 'Scriptaculous ModalBox'
    show_separately = True
    for_widget = modalbox
    full_class_name = 'scriptaculous.thirdparty.ModalBox'
    template = '<div>\n    <ul>\n\t<li><a href="javascript:Modalbox.MessageBox.alert(\'Example Alert\', \'Some text as body.\')"><code>Modalbox.MessageBox.alert</code></a></li>\n\t<li><a href="javascript:Modalbox.MessageBox.prompt(\'Example Prompt\', \'Please enter something:\', \'nothing\', function(btn, value){alert(\'Button: \'+btn+\' Value: \'+value)})"><code>Modalbox.MessageBox.prompt</code></a></li>\n\t<li><a href="javascript:Modalbox.MessageBox.confirm(\'Example Confirm Dialog\', \'Are you unsure you are sure?\', function(value){alert(value)})"><code>Modalbox.MessageBox.confirm</code></a></li>\n    </ul>\n    </div>'


ossdl_js = JSLink('scriptaculous', 'javascript/thirdparty/ossdl.js')
ossdl_css = CSSLink('scriptaculous', 'css/thirdparty/ossdl.css')

class AJAJForm(Widget):
    css = [
     ossdl_css]
    javascript = [prototype_js, ossdl_js]


ajaj_form = AJAJForm()

class AJAJFormDesc(CoreWD):
    name = 'Scriptaculous/OSSDL AJAJForms'
    show_separately = True
    for_widget = ajaj_form
    full_class_name = 'scriptaculous.thirdparty.AJAJForm'
    template = '<div>\n    <form method="post" action="scriptaculous.thirdparty.AJAJForm/proceed_form" onsubmit="return false;" class="AJAJForm">\n\t<table>\n\t    <tr><td class="label"><label for="user_name">${_("Your full name:")}</label></td>\n\t\t<td class="field"><input type="text" id="user_name" name="user_name"/></td>\n\t    </tr>\n\t    <tr><td class="label"><label for="user_age">${_("Your age:")}</label></td>\n\t\t<td class="field"><input type="text" id="user_age" name="user_age"/></td>\n\t    </tr>\n\t    <tr>\n\t\t<td colspan="2" class="buttons"><input type="submit" name="auth" value="${_(\'confess\')}"/></td>\n\t    </tr>\n\t</table>\n    </form>\n    <script type="text/javascript">\n        AJAJForms.decorateForms();\n    </script>\n    </div>\n    '

    @expose('json')
    def proceed_form(self, user_name, user_age):
        import cherrypy
        if user_name != 'Monty Python':
            cherrypy.response.status = 400
            return {'fielderrors': {'user_name': _("Your name must be 'Monty Python'!")}}
        return {}


class PaginationBar(Widget):
    css = [
     ossdl_css]
    javascript = [prototype_js, ossdl_js]
    params = ['attrs']
    attrs = {}
    template = '<div xmlns:py="http://purl.org/kid/ns#"><div class="paginationBar" py:attrs="attrs"></div>\n    <script type="text/javascript">\n\tPaginationBar.decoratePagingBars();\n    </script></div>\n    '


pagination_bar = PaginationBar()

class PaginationBarDesc(CoreWD):
    name = 'Scriptaculous/OSSDL Pagination Bar'
    show_separately = True
    for_widget = PaginationBar(attrs={'id': 'mybar'})
    full_class_name = 'scriptaculous.thirdparty.PaginationBar'
    template = '<div>\n    ${for_widget.display()}\n    <ul>\n\t<li><a href="javascript:PaginationBar.lock(\'mybar\')">${_("Lock")}</a></li>\n\t<li><a href="javascript:PaginationBar.unlock(\'mybar\')">${_("Unlock")}</a></li>\n    </ul>\n    <script type="text/javascript">\n\tvar bar = "mybar";\n\tPaginationBar.setMaxPage(bar, 4);\n\tPaginationBar.decoratedBars[bar].callbackGotoPage = function(page) {alert(\'callbackGotoPage(\'+page+\')\')};\n\tPaginationBar.decoratedBars[bar].callbackReload = function() {alert(\'You clicked on reload.\')};\n    </script></div>\n    '


class PagingDataGrid(CompoundWidget):
    css = [
     ossdl_css]
    javascript = [prototype_js, ossdl_js]
    params = ['attrs', 'id', 'data_url', 'property_url']
    id = lambda : 'grid_%d' % idcounter.next()
    attrs = {}
    member_widgets = ['pbar']
    pbar = pagination_bar
    template = '\n\t<div xmlns:py="http://purl.org/kid/ns#" py:strip="">\n\t<div id="${id}" py:attrs="attrs"></div>\n\t<script type="text/javascript">\n\t\tPagingDataGrid.init(\'${id}\', \'${data_url}\', \'${property_url}\');\n\t</script></div>'


paging_data_grid = PagingDataGrid()