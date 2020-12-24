# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/nspanti/workspace/rqlcontroller/cubicweb_rqlcontroller/views.py
# Compiled at: 2020-03-20 10:33:28
# Size of source mod 2**32: 6343 bytes
__doc__ = 'cubicweb-rqlcontroller views/forms/actions/components for web ui'
import json, re
from six import string_types
from cubicweb.predicates import ExpectedValuePredicate, match_form_params, match_http_method
from cubicweb.uilib import exc_message
from cubicweb.utils import json_dumps
from cubicweb.web import RemoteCallFailed, DirectResponse
from cubicweb.web.controller import Controller
from cubicweb.web.views.urlrewrite import rgx_action, SchemaBasedRewriter
from cubicweb import Binary
ARGRE = re.compile('__r(?P<ref>\\d+)$')
DATARE = re.compile('__f(?P<ref>.+)$')

def rewrite_args(args, output, form):
    for k, v in args.items():
        if not isinstance(v, string_types):
            continue
        match = ARGRE.match(v)
        if match:
            numref = int(match.group('ref'))
            if 0 <= numref <= len(output):
                rset = output[numref]
                if not rset:
                    raise Exception('%s references empty result set %s' % (
                     v, rset))
                if len(rset) > 1:
                    raise Exception('%s references multi lines result set %s' % (
                     v, rset))
                row = rset.rows[0]
                if len(row) > 1:
                    raise Exception('%s references multi column result set %s' % (v, rset))
                args[k] = row[0]
                continue
            match = DATARE.match(v)
            if match:
                args[k] = Binary(form[v][1].read())


class match_request_content_type(ExpectedValuePredicate):
    """match_request_content_type"""

    def _get_value(self, cls, req, **kwargs):
        header = req.get_header('Content-Type', None)
        if header is not None:
            header = header.split(';', 1)[0].strip()
        return header


class RqlIOController(Controller):
    """RqlIOController"""
    __regid__ = 'rqlio'
    __select__ = match_http_method('POST') & match_request_content_type('application/json', 'multipart/form-data', mode='any') & match_form_params('version')

    def json(self):
        contenttype = self._cw.get_header('Content-Type', raw=False)
        if (contenttype.mediaType, contenttype.mediaSubtype) == ('application', 'json'):
            encoding = contenttype.params.get('charset', 'utf-8')
            content = self._cw.content
        else:
            encoding = 'utf-8'
            content = self._cw.form['json'][1]
        try:
            args = json.loads(content.read().decode(encoding))
        except ValueError as exc:
            try:
                raise RemoteCallFailed(exc_message(exc, self._cw.encoding))
            finally:
                exc = None
                del exc

        if not isinstance(args, (list, tuple)):
            args = (
             args,)
        return args

    def publish(self, rset=None):
        self._cw.ajax_request = True
        self._cw.set_content_type('application/json')
        version = self._cw.form['version']
        if version not in ('1.0', '2.0'):
            raise RemoteCallFailed('unknown rqlio version %r', version)
        args = self.json()
        try:
            result = (self.rqlio)(version, *args)
        except (RemoteCallFailed, DirectResponse):
            raise
        except Exception as exc:
            try:
                raise RemoteCallFailed(exc_message(exc, self._cw.encoding))
            finally:
                exc = None
                del exc

        if result is None:
            return ''
        return json_dumps(result).encode(self._cw.encoding)

    def rqlio(self, version, *rql_args):
        try:
            output = self._rqlio(rql_args)
        except Exception:
            self._cw.cnx.rollback()
            raise
        else:
            self._cw.cnx.commit()
        if version == '2.0':
            return [{'rows':o.rows,  'variables':o.variables} for o in output]
        return [o.rows for o in output]

    def _rqlio(self, rql_args):
        output = []
        for rql, args in rql_args:
            if args is None:
                args = {}
            rewrite_args(args, output, self._cw.form)
            output.append(self._cw.execute(rql, args))

        return output


class RQLIORewriter(SchemaBasedRewriter):
    rules = [
     (
      re.compile('/rqlio/(?P<version>.+)$'),
      rgx_action(controller='rqlio', formgroups=('version', )))]