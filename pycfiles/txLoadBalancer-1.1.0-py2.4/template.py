# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/txlb/admin/template.py
# Compiled at: 2008-07-05 02:21:36
head = '\n    <html>\n    <head>\n    <title>%s</title>\n    <link rel=stylesheet type="text/css" href="/txlb.css">\n    %s\n    </head>\n    '
refresh = '\n    <META HTTP-EQUIV=Refresh CONTENT="%s; URL=%s">\n    '
message = '<p class="message">%s</p>'
header = head + '\n    <body>\n    <div class="title">%s version %s, running on host %s.</div>\n    '
footer = '\n    <div class="footer">\n    <a href="/">top</a>\n    <a href="all">all</a>\n    <a href="config.obj">running config</a>\n    <a href="config.xml">disk config</a>\n    <a href="%s">%s</a>\n    </div>\n    %s\n    </body>\n    </html>\n    '
startRefresh = '\n    <a class="button" href="/all?refresh=1&ignore=%s">Start\n    auto-refresh</a></p>\n    '
stopRefresh = '\n    <a class="button" href="/all?ignore=%s">Stop auto-refresh</a></p>\n    '
refreshButtons = '\n    <p><b>current config</b></p>\n    <p>last update at %s</p>\n    <p><a class="button" href="/all?ignore=%s">Refresh</a>\n    %s\n    '
serviceName = '\n    <table><tr><th align="left" colspan="1">Service: %s</th></tr>\n    '
listeningService = '\n    <tr><td colspan="1">Listening on %s</td></tr>\n    '
groupName = '\n    <tr class="%s"><td colspan="5" class="servHeader">%s\n    '
groupDescEnabled = '\n    <b>ENABLED</b>\n    '
groupDescDisabled = '\n    <a href="enableGroup?service=%s&group=%s">enable</a>\n    '
groupHeaderForm = '\n    </td><td valign="top" rowspan="2" class="addWidget">\n    <table class="addWidget">\n    <form method="GET" action="addHost">\n    <input type="hidden" name="service" value="%s">\n    <input type="hidden" name="group" value="%s">\n    <tr>\n        <td><div class="widgetLabel">name</div>\n        </td>\n        <td><input name="name" type="text" size="15">\n        </td>\n    </tr>\n    <tr>\n        <td><div class="widgetLabel">ip</div>\n        </td>\n        <td><input name="ip" type="text" size="15">\n        </td>\n    </tr>\n    <tr>\n        <td colspan=2 align="center"><input type="submit" value="add host">\n        </td>\n    </tr>\n    </form>\n    </table>\n    </td>\n    </tr>\n    <tr class="%s">\n    <th colspan="2">hosts</th><th>open</th><th>total</th><th>failed</th>\n    </tr>\n    '
hostInfo = '\n    <tr class="%s">\n    <td>%s</td><td><tt>%s</tt></td>\n    <td>%s</td><td>%s</td><td>%s</td>\n    <td><div class="deleteButton">\n    <a href="delHost?service=%s&group=%s&ip=%s">remove host</a>\n    </div></td>\n    </tr>\n    '
badHostGroup = '\n    <tr class="%s"><th colspan="2">disabled hosts</th>\n    <th>why</th><th>when</th></tr>\n    '
badHostInfo = '\n    <tr class="%s"><td>\n    %s</td><td><tt>%s</tt></td>\n    <td>%s</td><td>--</td>\n    </tr>\n    '
serviceClose = '\n    </table>\n    '
unauth = '\n    <html><body>Access Denied.</body></html>\n    '