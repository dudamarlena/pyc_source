# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ice/control/repl/browser/repl.py
# Compiled at: 2010-08-27 06:32:04
from zope.component import getUtility
from zope.session.interfaces import ISession
from zope.traversing.browser.absoluteurl import absoluteURL
from ice.control.repl.interfaces import IDispatcher
PREFIX = 'ice.control.repl.'

def prepare_output(source):
    source = source.replace('<', '&lt;')
    source = source.replace('>', '&gt;')
    return source


class REPL:

    def session_data(self):
        session = ISession(self.request)
        absolute_url = absoluteURL(self.context, self.request)
        return session[(PREFIX + absolute_url)]

    def get_repl(self):
        dispatcher = getUtility(IDispatcher)
        data = self.session_data()
        credentials = (data.get('id'), data.get('password'))
        session = dispatcher.get_session(*credentials)
        if session:
            return session
        credentials = dispatcher.set_session(self.context)
        (data['id'], data['password']) = credentials
        return dispatcher.get_session(*credentials)

    def clear(self):
        dispatcher = getUtility(IDispatcher)
        data = self.session_data()
        try:
            dispatcher.del_session(data['id'], data['password'])
        except KeyError:
            pass

    def interact(self):
        self.request.response.setHeader('Content-Type', 'text/xml')
        source = self.request.get('source')
        repl = self.get_repl()
        (result, output) = repl.run(source)
        output_xml = [ '<line><![CDATA[%s]]></line>\n' % prepare_output(x) for x in output
                     ]
        response_xml = '<?xml version="1.0" ?>\n'
        response_xml += '<doc>\n'
        response_xml += '<output>%s</output>\n' % ('').join(output_xml)
        response_xml += '<result>%s</result>\n' % int(result)
        response_xml += '</doc>\n'
        return response_xml

    def get_history(self):
        self.request.response.setHeader('Content-Type', 'text/xml')
        response_xml = '<?xml version="1.0" ?>\n'
        response_xml += '<doc>\n'
        for x in self.get_repl().get_history():
            response_xml += '<line>%s</line>\n' % x

        response_xml += '</doc>\n'
        return response_xml