# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/jquery/ajax.py
# Compiled at: 2008-02-08 10:22:36
from turbogears.widgets import Widget
from widgets import jquery

class FormRemote(Widget):
    """
    form_remote_tag is an ajax helper

    While target link is clicked, submit form in json format

    """
    name = 'form_remote_tag'
    javascript = [jquery]
    template = '\n        <script type="text/javascript">\n        $(function(){$(\'form.${target}\').submit(function(){ \n            $.ajax({url: "${href}",\n            data: $(this.elements).serialize(), \n            success: function(response){\n                $("#${update}").html(response);\n                },\n                dataType: "html"}); return false;\n            });\n        }); \n        </script>\n    '
    params = ['target', 'update', 'href']
    params_doc = {'target': 'the link id', 'update': 'div to be replaced', 
       'href': 'remote method href'}


form_remote_tag = FormRemote()

class LinkRemote(Widget):
    """
    link_to_remote is an ajax helper

    While target link is clicked,
    use XMLHttpRequest to get a response from a remote method

    this widget has no call back.
    """
    name = 'link_to_remote'
    javascript = [jquery]
    template = '\n        <script type="text/javascript">\n        $(function(){$(\'#${target}\').click(function(){\n            $.ajax({url: "${href}",\n                success: function(response){\n                    $("#${update}").html(response);\n                    ${callback}\n                },\n                dataType: "html"\n            });\n            return false;\n        });});\n        </script>\n    '
    params = ['target', 'update', 'href', 'callback']
    params_doc = {'target': 'the link id', 'update': 'div to be replaced', 
       'href': 'remote method href', 
       'callback': 'call back functions, default is Null'}
    callback = ''


link_to_remote = LinkRemote()

class PeriodicallyCallRemote(Widget):
    """
    periodically_call_remote  is an ajax helper

    Fetch data from server periodically
    """
    name = 'periodically_call_remote'
    javascript = [jquery]
    template = '\n        <script type="text/javascript">\n        $(document).ready(function() {\n            setInterval(function() {\n                $.ajax({url: "${href}",\n                    success: function(response){\n                        $("#${update}").html(response);\n                    },\n                    dataType: "html"\n                })\n            },${interval})\n        });\n        </script>\n    '
    params = ['update', 'href', 'interval']
    params_doc = {'update': 'div to be replaced', 'href': 'remote method href', 
       'interval': 'update time interval, default is 1000(ms)'}
    interval = 1000


periodically_call_remote = PeriodicallyCallRemote
addCallback = link_to_remote
addFormback = form_remote_tag
addPeriodback = periodically_call_remote