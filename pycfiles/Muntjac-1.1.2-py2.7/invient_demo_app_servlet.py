# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/addon/invient/demo/invient_demo_app_servlet.py
# Compiled at: 2013-04-04 15:36:37
from muntjac.terminal.gwt.server.application_servlet import ApplicationServlet

class InvientChartsDemoAppServlet(ApplicationServlet):

    def writeAjaxPageHtmlMuntjacScripts(self, window, themeName, application, page, appUrl, themeUri, appId, request):
        page.write('<script type="text/javascript">\n')
        page.write('//<![CDATA[\n')
        page.write('document.write("<script language=\'javascript\' src=\'./jquery/jquery-1.4.4.min.js\'><\\/script>");\n')
        page.write('document.write("<script language=\'javascript\' src=\'./js/highcharts.js\'><\\/script>");\n')
        page.write('document.write("<script language=\'javascript\' src=\'./js/modules/exporting.js\'><\\/script>");\n')
        page.write('//]]>\n</script>\n')
        super(InvientChartsDemoAppServlet, self).writeAjaxPageHtmlMuntjacScripts(window, themeName, application, page, appUrl, themeUri, appId, request)