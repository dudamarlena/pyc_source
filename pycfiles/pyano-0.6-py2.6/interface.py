# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pyano/interface.py
# Compiled at: 2010-11-11 19:59:33
from mod_python import util
from mod_python import apache
from validate import InputError
from config import ConfigError, conf, parse_config, NONE, RANDOM
from stats import stats, parse_stats, format_stats, uptime_sort
from security import SecurityError, check_ip
from mix import MixError

class Interface:

    def __call__(self, req):
        req.content_type = 'text/html'
        req.send_http_header()
        self.fs = util.FieldStorage(req, keep_blank_values=True)
        try:
            options = req.get_options()
            if 'config_file' in options:
                parse_config(options['config_file'])
            else:
                parse_config()
            self.main(req)
        except InputError, ie:
            req.write(self.html_fail(str(ie)))
        except SecurityError, he:
            req.write(self.html_fail(str(he)))
        except MixError, me:
            req.write(self.html_fail(str(me)))
        except ConfigError, ce:
            req.write(self.html_result('Configuration Error!', str(ce)))
        except Exception, ex:
            req.write(self.html_result('Unhandled Error!', str(ex)))

        return apache.OK

    def set_html_content(self, html, content):
        return html.replace('<!--CONTENT-->', content)

    def html_result(self, title, msg, print_back=True):
        out = '<h2>' + title + '</h2>\n'
        out += '<p>' + msg + '</p>\n'
        if print_back:
            out += "<p>Press your browser's back button to come back to the mixmaster web interface.</p>\n"
        return self.set_html_content(self.html(), out)

    def html_fail(self, msg, print_back=True):
        return self.html_result('Failure!', msg, print_back)

    def html_success(self, msg, print_back=True):
        return self.html_result('Success!', msg, print_back)


class MixInterface(Interface):

    def main(self, req):
        parse_stats()
        if len(self.fs) == 0:
            content = self.form()
            content = content.replace('PYANO_URI', str(req.uri))
            if stats:
                content = content.replace('PYANO_CHAIN', self.html_chain())
            else:
                content = content.replace('PYANO_CHAIN', '')
            content = content.replace('PYANO_COPIES', self.html_copies())
            html = self.set_html_content(self.html(), content)
            req.write(html)
        else:
            check_ip(req.get_remote_host(apache.REMOTE_NOLOOKUP))
            msg = self.process()
            req.write(self.html_success(msg))

    def html_chain(self):
        out = '\n'
        out += '      <tr id="chain">\n'
        out += '        <td><strong>Chain:</strong></td>\n'
        out += '        <td>\n'
        for i in range(0, conf.chain_max_length):
            out += '          <select name="chain' + str(i) + '">\n'
            out += '            <option value="' + NONE + '"></option>\n'
            out += '            <option value="' + RANDOM + '">Random</option>\n'
            for remailer in uptime_sort():
                out += '            <option value="' + remailer + '">' + format_stats(remailer).replace(' ', '&nbsp;') + '</option>\n'

            out += '          </select><br/>'

        out += '        </td>\n'
        out += '      </tr>\n'
        return out

    def html_copies(self):
        out = '          <select name="copies">\n'
        for i in range(0, conf.max_copies):
            out += '            <option value="' + str(i + 1) + '" >' + str(i + 1) + '</option>\n'

        out += '          </select>'
        return out