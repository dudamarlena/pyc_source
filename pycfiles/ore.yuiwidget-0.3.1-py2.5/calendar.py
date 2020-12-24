# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/yuiwidget/calendar.py
# Compiled at: 2008-09-11 20:30:06
from zope.app.form.browser.textwidgets import DateWidget
from zc.resourcelibrary import need
from datetime import datetime, timedelta

class CalendarWidget(DateWidget):
    mindate = (datetime.now() - timedelta(730)).strftime('%m/%d/%Y')
    maxdate = (datetime.now() + timedelta(730)).strftime('%m/%d/%Y')

    def getInputValue(self):
        return super(CalendarWidget, self).getInputValue()

    def __call__(self):
        need('yui-calendar')
        need('yui-container')
        need('yui-button')
        jsid = self.name.replace('.', '_')
        value = self._getFormValue()
        if value is None or value == self.context.missing_value:
            value = ''
        input_widget = '        \n        <div class="datefield">\n           <input id="%(name)s" name="%(name)s" type="text" value="%(value)s"/>\n           <button type="button" id="%(name)s-btn" title="Show Calendar"/>\n              <img src="/++resource++calbtn.gif" />\n            </button>\n        </div>\n        \n        <div id="%(name)s-container">\n           <div class="hd">Calendar</div>\n           <div class="bd">\n              <div id="%(name)s-caldiv"></div>\n           </div>\n        </div>\n        \n        <script language="javascript">\n           YAHOO.util.Event.onDOMReady(function(){\n           var dialog, calendar;\n           var curdate = "%(value)s";\n           \n           pad = function (value, length) {\n              value = String(value);\n              length = parseInt(length) || 2;\n              while (value.length < length)\n                  value = "0" + value;\n                  return value;\n           };\n           \n           calendar = new YAHOO.widget.Calendar("%(name)s-caldiv", {\n                    iframe:false,          // Turn iframe off, since container has iframe support.\n                    hide_blank_weeks:true,  // Enable, to demonstrate how we handle changing height, using changeContent\n                    mindate:"%(mindate)s",\n                    maxdate:"%(maxdate)s",\n                    navigator:true\n                    });\n           \n            function handle_cancel() {\n                this.hide();\n            }\n\n            function handle_ok() {\n                if ( calendar.getSelectedDates().length > 0) {\n                     var selDate = calendar.getSelectedDates()[0];\n                     var datestring = selDate.getFullYear() + "-" + pad( selDate.getMonth()+1, 2) + "-" + pad( selDate.getDate(), 2);\n                     document.getElementById("%(name)s").value = datestring;\n                };\n                this.hide();\n            }\n\n            dialog = new YAHOO.widget.Dialog("%(name)s-container", {\n                  context:["%(name)s-btn", "tl", "bl"],\n                  buttons:[ {text:"Select", isDefault:true, handler: handle_ok },\n                            {text:"Cancel", handler: handle_cancel}],\n                  width:"16em",  // Sam Skin dialog needs to have a width defined (7*2em + 2*1em = 16em).\n                  draggable:false,\n                  close:true\n                  });        \n\n\n            // calendar.select( "%(value)s" );\n            calendar.render();\n            dialog.render();\n            \n            // Using dialog.hide() instead of visible:false is a workaround for an IE6/7 container known issue with border-collapse:collapse.\n            dialog.hide();\n            \n            calendar.renderEvent.subscribe(function() {\n               dialog.fireEvent("changeContent");\n               });\n            YAHOO.util.Event.on("%(name)s-btn", "click", dialog.show, dialog, true);\n            });\n        </script>\n        ' % {'name': self.name, 'value': value, 'mindate': self.mindate, 'maxdate': self.maxdate}
        return input_widget