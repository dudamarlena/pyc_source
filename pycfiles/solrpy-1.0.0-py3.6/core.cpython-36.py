# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solr/core.py
# Compiled at: 2020-05-13 01:59:13
# Size of source mod 2**32: 39830 bytes
from __future__ import print_function
import sys, socket, codecs, datetime, logging, six, base64
from xml.sax import make_parser
from xml.sax.handler import ContentHandler
from xml.sax.saxutils import escape, quoteattr
from xml.dom.minidom import parseString
from past.builtins import long, unicode, basestring, PY3
from future.utils import iteritems
from six import BytesIO as StringIO
import six.moves.http_client as httplib, six.moves.urllib.parse as urlparse, six.moves.urllib.parse as urllib
__all__ = [
 'SolrException', 'Solr', 'SolrConnection',
 'Response', 'SearchHandler']
_python_version = sys.version_info[0] + sys.version_info[1] / 10.0

class SolrException(Exception):
    __doc__ = 'An exception thrown by solr connections.\n\n    Detailed information is provided in attributes of the exception object.\n    '
    httpcode = 400
    reason = None
    body = None

    def __init__(self, httpcode=None, reason=None, body=None):
        self.httpcode = httpcode
        self.reason = reason
        self.body = body

    def __repr__(self):
        return 'HTTP code=%s, Reason=%s, body=%s' % (
         self.httpcode, self.reason, self.body)

    def __str__(self):
        return 'HTTP code=%s, reason=%s' % (self.httpcode, self.reason)


def committing(function=None):

    def wrapper(self, *args, **kw):
        commit = kw.pop('commit', False)
        optimize = kw.pop('optimize', False)
        query = {}
        if commit or optimize:
            if optimize:
                query['optimize'] = 'true'
            else:
                if commit:
                    query['commit'] = 'true'
            wait_searcher = kw.pop('wait_searcher', True)
            wait_flush = kw.pop('wait_flush', True)
            if not wait_searcher:
                query['waitSearcher'] = 'false'
            if not wait_flush:
                query['waitFlush'] = 'false'
                query['waitSearcher'] = 'false'
        else:
            if 'wait_flush' in kw:
                raise TypeError('wait_flush cannot be specified without commit or optimize')
            else:
                if 'wait_searcher' in kw:
                    raise TypeError('wait_searcher cannot be specified without commit or optimize')
        content = function(self, *args, **kw)
        if content:
            return self._update(content, query)

    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper


class Solr:

    def __init__(self, url, persistent=True, timeout=None, ssl_key=None, ssl_cert=None, http_user=None, http_pass=None, post_headers={}, max_retries=3, debug=False):
        """
            url -- URI pointing to the Solr instance. Examples:

                http://localhost:8080/solr
                https://solr-server/solr

                Your python install must be compiled with SSL support for the
                https:// schemes to work. (Most pre-packaged pythons are.)

            persistent -- Keep a persistent HTTP connection open.
                Defaults to true

            timeout -- Timeout, in seconds, for the server to response.
                By default, use the python default timeout (of none?)

            ssl_key, ssl_cert -- If using client-side key files for
                SSL authentication,  these should be, respectively,
                your PEM key file and certificate file.

            http_user, http_pass -- If given, include HTTP Basic authentication 
                in all request headers.

        """
        self.scheme, self.host, self.path = urlparse.urlparse(url, 'http')[:3]
        self.url = url
        assert self.scheme in ('http', 'https')
        self.persistent = persistent
        self.reconnects = 0
        self.timeout = timeout
        self.ssl_key = ssl_key
        self.ssl_cert = ssl_cert
        self.max_retries = int(max_retries)
        if not self.max_retries >= 0:
            raise AssertionError
        else:
            kwargs = {}
            if self.timeout:
                if _python_version >= 2.6:
                    if _python_version < 3:
                        kwargs['timeout'] = self.timeout
            if self.scheme == 'https':
                self.conn = (httplib.HTTPSConnection)(self.host, key_file=ssl_key, 
                 cert_file=ssl_cert, **kwargs)
            else:
                self.conn = (httplib.HTTPConnection)((self.host), **kwargs)
        self.response_version = 2.2
        self.encoder = codecs.getencoder('utf-8')
        self.decoder = codecs.getdecoder('utf-8')
        if self.timeout and _python_version < 2.6:
            self.conn.connect()
            if self.scheme == 'http':
                self.conn.sock.settimeout(self.timeout)
            elif self.scheme == 'https':
                self.conn.sock.sock.settimeout(self.timeout)
        self.xmlheaders = {'Content-Type': 'text/xml; charset=utf-8'}
        self.xmlheaders.update(post_headers)
        if not self.persistent:
            self.xmlheaders['Connection'] = 'close'
        else:
            self.form_headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'}
            self.form_headers.update(post_headers)
            if http_user is not None:
                if http_pass is not None:
                    http_auth = http_user + ':' + http_pass
                    if six.PY3:
                        http_auth = http_auth.strip().encode('utf-8')
                    http_auth = 'Basic ' + base64.b64encode(http_auth)
                    self.auth_headers = {'Authorization': http_auth}
            self.auth_headers = {}
        if not self.persistent:
            self.form_headers['Connection'] = 'close'
        self.debug = debug
        self.select = SearchHandler(self, '/select')

    def close(self):
        """Close the underlying HTTP(S) connection."""
        self.conn.close()

    @committing
    def delete(self, id=None, ids=None, queries=None):
        """
        Delete documents by ids or queries.

        Any or all of `id`, `ids`, or `queries` may be given; all
        provided will be used.  If none are provided, no request will be
        sent to Solr.

        `id` is a single value for the schema's unique id field.  `ids`
        is an iterable of unique ids.

        `queries` is an iterable of standard-syntax queries.
        Supports commit-control arguments.
        """
        return self._delete(id=id, ids=ids, queries=queries)

    @committing
    def delete_many(self, ids):
        """
        Delete documents using an iterable of ids.

        This is equivalent to ``delete(ids=[ids])``.
        Supports commit-control arguments.
        """
        return self._delete(ids=ids)

    @committing
    def delete_query(self, query):
        """
        Delete all documents identified by a query.

        This is equivalent to ``delete(queries=[query])``.
        Supports commit-control arguments.
        """
        return self._delete(queries=[query])

    @committing
    def add(self, doc):
        """
        Add a document to the Solr server.  Document fields
        should be specified as arguments to this function

        Example::

            doc = {"id": "mydoc", "author": "Me"}
            connection.add(doc)

        Supports commit-control arguments.
        """
        lst = [
         '<add>']
        self._Solr__add(lst, doc)
        lst.append('</add>')
        return ''.join(lst)

    @committing
    def add_many(self, docs):
        """
        Add several documents to the Solr server.

        `docs`
            An iterable of document dictionaries.

        Supports commit-control arguments.
        """
        lst = [
         '<add>']
        for doc in docs:
            self._Solr__add(lst, doc)

        lst.append('</add>')
        return ''.join(lst)

    def commit(self, wait_flush=True, wait_searcher=True, _optimize=False):
        """
        Issue a commit command to the Solr server.

        `wait_flush` and `wait_searcher` have the same interpretations as
        the like-name `commit-control arguments`_.

        """
        return self._commit('commit', wait_flush, wait_searcher)

    def optimize(self, wait_flush=True, wait_searcher=True):
        """
        Issue an optimize command to the Solr server.

        `wait_flush` and `wait_searcher` have the same interpretations as
        the like-name `commit-control arguments`_.

        """
        return self._commit('optimize', wait_flush, wait_searcher)

    def _commit(self, verb, wait_flush, wait_searcher):
        if not wait_searcher:
            if not wait_flush:
                options = 'waitFlush="false" waitSearcher="false"'
            else:
                options = 'waitSearcher="false"'
        else:
            options = ''
        xstr = '<%s %s/>' % (verb, options)
        return self._update(xstr)

    def _update(self, request, query=None):
        selector = '%s/update%s' % (self.path, qs_from_items(query))
        try:
            rsp = self._post(selector, request, self.xmlheaders)
            data = rsp.read()
        finally:
            if not self.persistent:
                self.close()

        if PY3:
            data = data.decode('utf-8')
        starts = data.startswith
        if starts('<result status="'):
            if not starts('<result status="0"'):
                data = self.decoder(data)[0]
                parsed = parseString(data)
                status = parsed.documentElement.getAttribute('status')
                if status != 0:
                    reason = parsed.documentElement.firstChild.nodeValue
                    raise SolrException(rsp.status, reason)
        return data

    def __add(self, lst, fields):
        lst.append('<doc>')
        for field, value in iteritems(fields):
            if not isinstance(value, (list, tuple, set)):
                values = [
                 value]
            else:
                values = value
            for value in values:
                if value == None:
                    pass
                else:
                    if isinstance(value, datetime.datetime):
                        value = utc_to_string(value)
                    else:
                        if isinstance(value, datetime.date):
                            value = datetime.datetime.combine(value, datetime.time(tzinfo=(UTC())))
                            value = utc_to_string(value)
                        else:
                            if isinstance(value, bool):
                                value = value and 'true' or 'false'
                    elem = FieldElement()
                    elem['name'] = quoteattr(field)
                    elem['value'] = escape(unicode(value))
                    lst.append(unicode(elem))

        lst.append('</doc>')

    def _delete(self, id=None, ids=None, queries=None):
        """
        Delete a specific document by id.
        """
        if not ids:
            ids = []
        else:
            if id:
                ids.insert(0, id)
            lst = []
            for id in ids:
                lst.append('<id>%s</id>\n' % escape(unicode(id)))

            for query in queries or ():
                lst.append('<query>%s</query>\n' % escape(unicode(query)))

            if lst:
                lst.insert(0, '<delete>\n')
                lst.append('</delete>')
                return ''.join(lst)

    def __repr__(self):
        return '<%s (url=%s, persistent=%s, post_headers=%s, reconnects=%s)>' % (
         self.__class__.__name__,
         self.url, self.persistent,
         self.xmlheaders, self.reconnects)

    def _reconnect(self):
        self.reconnects += 1
        self.close()
        self.conn.connect()
        if self.timeout:
            if _python_version < 2.6:
                if self.scheme == 'http':
                    self.conn.sock.settimeout(self.timeout)
                elif self.scheme == 'https':
                    self.conn.sock.sock.settimeout(self.timeout)

    def _post(self, url, body, headers):
        _headers = self.auth_headers.copy()
        _headers.update(headers)
        attempts = self.max_retries + 1
        while attempts > 0:
            try:
                self.conn.request('POST', url, body.encode('UTF-8'), _headers)
                return check_response_status(self.conn.getresponse())
            except (socket.error, httplib.ImproperConnectionState,
             httplib.BadStatusLine):
                self._reconnect()
                attempts -= 1
                if attempts <= 0:
                    raise


class SolrConnection(Solr):
    __doc__ = '\n    Represents a Solr connection.\n\n    Designed to work with the 2.2 response format (Solr 1.2+),\n    though will likely work with 2.1 responses as well.\n    '

    def add(self, _commit=False, **fields):
        """
        Add or update a single document with field values given by
        keyword arguments.

        The `_commit` argument is treated specially, causing an immediate
        commit if present.  It may be specified either positionally or as
        a keyword.  If `_commit` is true, the commit will be issued as
        part of the same HTTP request to the Solr server.

        Example::

            connection.add(id="mydoc", author="Me")

        This is equialent to ``solr.Solr.add(fields, commit=_commit)``.
        """
        return Solr.add_many(self, [fields], commit=_commit)

    def add_many(self, docs, _commit=False):
        """
        Add or update multiple documents. with field values for each given
        by dictionaries in the sequence `docs`.

        The `_commit` argument is treated specially, causing an immediate
        commit if present.  It may be specified either positionally or as
        a keyword.  If `_commit` is true, the commit will be issued as
        part of the same HTTP request to the Solr server.

        Example::

            doc1 = {...}
            doc2 = {...}
            connection.add_many([doc1, doc2], _commit=True)

        This is equialent to ``solr.Solr.add_many(docs, commit=_commit)``.
        """
        return Solr.add_many(self, docs, commit=_commit)

    def query(self, *args, **params):
        return (self.select)(*args, **params)

    def raw_query(self, **params):
        return (self.select.raw)(**params)


class SearchHandler(object):

    def __init__(self, conn, relpath='/select', arg_separator='_'):
        self.conn = conn
        self.selector = conn.path + relpath
        self.arg_separator = arg_separator

    def __call__(self, q=None, fields=None, highlight=None, score=True, sort=None, sort_order='asc', **params):
        """
        q is the query string.

        fields is an optional list of fields to include. It can
        be either a string in the format that SOLR expects, or
        a python list/tuple of field names.   Defaults to
        all fields. ("*")

        score indicates whether "score" should be included
        in the field list.  Note that if you explicitly list
        "score" in your fields value, then score is
        effectively ignored.  Defaults to true.

        highlight indicates whether highlighting should be included.
        highlight can either be False, indicating "No" (the default),
        a list of fields in the same format as "fields" or True, indicating
        to highlight any fields included in "fields". If True and no "fields"
        are given, raise a ValueError.

        sort is a list of fields to sort by. See "fields" for
        formatting. Each sort element can have be in the form
        "fieldname asc|desc" as specified by SOLR specs.

        sort_order is the backward compatible way to add the same ordering
        to all the sort field when it is not specified.

        Optional parameters can also be passed in.  Many SOLR
        parameters are in a dotted notation (e.g., hl.simple.post).
        For such parameters, replace the dots with underscores when
        calling this method. (e.g., hl_simple_post='</pre'>)

        Returns a Response instance.
        """
        if highlight:
            params['hl'] = 'true'
            if not isinstance(highlight, (bool, int, float)):
                if not isinstance(highlight, basestring):
                    highlight = ','.join(highlight)
                params['hl_fl'] = highlight
            else:
                raise fields or ValueError('highlight is True and no fields were given')
        else:
            if isinstance(fields, basestring):
                params['hl_fl'] = [
                 fields]
            else:
                params['hl_fl'] = ','.join(fields)
            if q is not None:
                params['q'] = q
            if fields:
                if not isinstance(fields, basestring):
                    fields = ','.join(fields)
            if not fields:
                fields = '*'
            if sort:
                if not sort_order or sort_order not in ('asc', 'desc'):
                    raise ValueError("sort_order must be 'asc' or 'desc'")
                if isinstance(sort, basestring):
                    sort = [f.strip() for f in sort.split(',')]
                sorting = []
                for e in sort:
                    if not (e.endswith('asc') or e.endswith('desc')):
                        sorting.append('%s %s' % (e, sort_order))
                    else:
                        sorting.append(e)

                sort = ','.join(sorting)
                params['sort'] = sort
            if score:
                if 'score' not in fields.replace(',', ' ').split():
                    fields += ',score'
            params['fl'] = fields
            params['version'] = self.conn.response_version
            params['wt'] = 'xml'
            json = (self.raw)(**params)
            if PY3:
                if type(json) == str:
                    json = json.encode('utf-8')
        return parse_query_response('XML', StringIO(json), params, self)

    def raw(self, **params):
        """
        Issue a query against a SOLR server.

        Return the raw result.  No pre-processing or post-processing
        happens to either input parameters or responses.
        """
        query = []
        for key, value in iteritems(params):
            key = key.replace(self.arg_separator, '.')
            if isinstance(value, (list, tuple)):
                query.extend([(key, strify(v)) for v in value])
            else:
                query.append((key, strify(value)))

        request = urllib.urlencode(query, doseq=True)
        conn = self.conn
        if conn.debug:
            logging.info('solrpy request: %s' % request)
        try:
            rsp = conn._post(self.selector, request, conn.form_headers)
            data = rsp.read()
            if conn.debug:
                logging.info('solrpy got response: %s' % data)
        finally:
            if not conn.persistent:
                conn.close()

        return data


def strify(s):
    if isinstance(s, unicode):
        return s.encode('utf-8')
    else:
        return s


class Response(object):
    __doc__ = '\n    A container class for a\n\n    A Response object will have the following properties:\n\n          header -- a dict containing any responseHeader values\n\n          results -- a list of matching documents. Each list item will\n              be a dict.\n    '

    def __init__(self, query):
        self.header = {}
        self.results = []
        self._query = query
        self._params = {}

    def _set_numFound(self, value):
        self._numFound = long(value)

    def _get_numFound(self):
        return self._numFound

    def _del_numFound(self):
        del self._numFound

    numFound = property(_get_numFound, _set_numFound, _del_numFound)

    def _set_start(self, value):
        self._start = long(value)

    def _get_start(self):
        return self._start

    def _del_start(self):
        del self._start

    start = property(_get_start, _set_start, _del_start)

    def _set_maxScore(self, value):
        self._maxScore = float(value)

    def _get_maxScore(self):
        return self._maxScore

    def _del_maxScore(self):
        del self._maxScore

    maxScore = property(_get_maxScore, _set_maxScore, _del_maxScore)

    def __len__(self):
        """
        Return the number of matching documents contained in this set.
        """
        return len(self.results)

    def __iter__(self):
        """
        Return an iterator of matching documents.
        """
        return iter(self.results)

    def next_batch(self):
        """
        Load the next set of matches.

        By default, Solr returns 10 at a time.
        """
        try:
            start = int(self.results.start)
        except AttributeError:
            start = 0

        start += len(self.results)
        params = dict(self._params)
        params['start'] = start
        q = params['q']
        del params['q']
        return (self._query)(q, **params)

    def previous_batch(self):
        """
        Return the previous set of matches
        """
        try:
            start = int(self.results.start)
        except AttributeError:
            start = 0

        if not start:
            return
        else:
            rows = int(self.header.get('rows', len(self.results)))
            start = max(0, start - rows)
            params = dict(self._params)
            params['start'] = start
            params['rows'] = rows
            q = params['q']
            del params['q']
            return (self._query)(q, **params)


def parse_query_response(data_type, data, params, query):
    """
    Parse the XML results of a /select call.
    """
    if data_type == 'XML':
        parser = make_parser()
        handler = ResponseContentHandler()
        parser.setContentHandler(handler)
        parser.parse(data)
        if handler.stack[0].children:
            response = handler.stack[0].children[0].final
            response._params = params
            response._query = query
            return response
        else:
            return
    elif data_type == 'JSON':
        pass


class ResponseContentHandler(ContentHandler):
    __doc__ = '\n    ContentHandler for the XML results of a /select call.\n    (Versions 2.2 (and possibly 2.1))\n    '

    def __init__(self):
        self.stack = [Node(None, {})]
        self.in_tree = False

    def startElement(self, name, attrs):
        if not self.in_tree:
            if name != 'response':
                raise SolrException('Unknown XML response from server: <%s ...' % name)
            self.in_tree = True
        element = Node(name, attrs)
        self.stack.append(element)
        self.stack[(-2)].children.append(element)

    def characters(self, ch):
        self.stack[(-1)].chars.append(ch)

    def endElement(self, name):
        node = self.stack.pop()
        name = node.name
        value = ''.join(node.chars)
        if name == 'int':
            node.final = int(value.strip())
        else:
            if name == 'str':
                node.final = value
            else:
                if name == 'null':
                    node.final = None
                else:
                    if name == 'long':
                        node.final = long(value.strip())
                    else:
                        if name == 'bool':
                            node.final = value.strip().lower().startswith('t')
                        else:
                            if name == 'date':
                                node.final = utc_from_string(value.strip())
                            else:
                                if name in ('float', 'double', 'status', 'QTime'):
                                    node.final = float(value.strip())
                                else:
                                    if name == 'response':
                                        node.final = response = Response(self)
                                        for child in node.children:
                                            name = child.attrs.get('name', child.name)
                                            if name == 'responseHeader':
                                                name = 'header'
                                            else:
                                                if child.name == 'result':
                                                    name = 'results'
                                                    for attr_name in child.attrs.getNames():
                                                        if attr_name != 'name':
                                                            setattr(response, attr_name, child.attrs.get(attr_name))

                                            setattr(response, name, child.final)

                                    else:
                                        if name in ('lst', 'doc'):
                                            node.final = dict([(cnode.attrs['name'], cnode.final) for cnode in node.children])
                                        else:
                                            if name in ('arr', ):
                                                node.final = [cnode.final for cnode in node.children]
                                            else:
                                                if name == 'result':
                                                    node.final = Results([cnode.final for cnode in node.children])
                                                else:
                                                    if name in ('responseHeader', ):
                                                        node.final = dict([(cnode.name, cnode.final) for cnode in node.children])
                                                    else:
                                                        raise SolrException('Unknown tag: %s' % name)
        for attr, val in iteritems(node.attrs):
            if attr != 'name':
                setattr(node.final, attr, val)


class Results(list):
    __doc__ = '\n    Convenience class containing <result> items\n    '


class Node(object):
    __doc__ = '\n    A temporary object used in XML processing. Not seen by end user.\n    '

    def __init__(self, name, attrs):
        """
        Final will eventually be the "final" representation of
        this node, whether an int, list, dict, etc.
        """
        self.chars = []
        self.name = name
        self.attrs = attrs
        self.final = None
        self.children = []

    def __repr__(self):
        return '<%s val="%s" %s>' % (
         self.name,
         ''.join(self.chars).strip(),
         ' '.join(['%s="%s"' % (attr, val) for attr, val in iteritems(self.attrs)]))


class FieldElement:

    def __init__(self):
        self.attrs = {}

    def __setitem__(self, key, value):
        self.attrs[key] = unicode(value)
        if key == 'value':
            if value.startswith("{'"):
                tmp = eval(value)
                allow_keys = ['add', 'set', 'inc']
                if len(tmp) > 1:
                    raise NotFieldOption('Only one option is available.')
                first_key = tmp.popitem()
                if first_key[0] not in allow_keys:
                    raise NotFieldOption('This option is not allowed.')
                self.attrs['update'] = '"{0}"'.format(first_key[0])
                if type(first_key[1]) == list:
                    self.attrs['multi_value'] = first_key[1]
                self.attrs['value'] = unicode(first_key[1])

    def get_attr(self):
        attrs = ['{0}={1}'.format(attr_name, attr_value) for attr_name, attr_value in self.attrs.items() if attr_name not in ('value',
                                                                                                                              'multi_value')]
        return ' '.join(attrs)

    def __unicode__(self):
        if 'multi_value' in self.attrs:
            res_fields = []
            for entry in self.attrs['multi_value']:
                res_fields.append('<field{0}>{1}</field>'.format(' {0}'.format(self.get_attr()), unicode(entry)))

            return '\n'.join(res_fields)
        else:
            return '<field{0}>{1}</field>'.format(' {0}'.format(self.get_attr()), self.attrs['value'])

    def __str__(self):
        return self.__unicode__()


class NotFieldOption(Exception):
    pass


def check_response_status(response):
    if response.status != 200:
        ex = SolrException(response.status, response.reason)
        try:
            ex.body = response.read()
            print(ex.body)
        except:
            pass

        raise ex
    return response


class UTC(datetime.tzinfo):
    __doc__ = '\n    UTC timezone.\n    '

    def utcoffset(self, dt):
        return datetime.timedelta(0)

    def tzname(self, dt):
        return 'UTC'

    def dst(self, dt):
        return datetime.timedelta(0)


utc = UTC()

def utc_to_string(value):
    """
    Convert datetimes to the subset of ISO 8601 that Solr expects.
    """
    value = value.astimezone(utc).isoformat()
    if '+' in value:
        value = value.split('+')[0]
    value += 'Z'
    return value


def utc_from_string(value):
    """
    Parse a string representing an ISO 8601 date.
    Note: this doesn't process the entire ISO 8601 standard,
    onle the specific format Solr promises to generate.
    """
    try:
        if not value.endswith('Z'):
            if value[10] == 'T':
                raise ValueError(value)
        year = int(value[0:4])
        month = int(value[5:7])
        day = int(value[8:10])
        hour = int(value[11:13])
        minute = int(value[14:16])
        microseconds = int(float(value[17:-1]) * 1000000.0)
        second, microsecond = divmod(microseconds, 1000000)
        return datetime.datetime(year, month, day, hour, minute, second, microsecond, utc)
    except ValueError:
        raise ValueError("'%s' is not a valid ISO 8601 Solr date" % value)


def qs_from_items(query):
    qs = ''
    if query:
        sep = '?'
        for k, v in iteritems(query):
            k = urllib.quote(k)
            if isinstance(v, basestring):
                v = [
                 v]
            for s in v:
                qs += '%s%s=%s' % (sep, k, urllib.quote_plus(s))
                sep = '&'

    return qs