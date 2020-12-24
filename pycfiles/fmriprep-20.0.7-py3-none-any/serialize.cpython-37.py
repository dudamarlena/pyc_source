# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-vxs8l7gu/pip/pip/_vendor/cachecontrol/serialize.py
# Compiled at: 2020-05-05 12:41:36
# Size of source mod 2**32: 7091 bytes
import base64, io, json, zlib
from pip._vendor import msgpack
from pip._vendor.requests.structures import CaseInsensitiveDict
from .compat import HTTPResponse, pickle, text_type

def _b64_decode_bytes(b):
    return base64.b64decode(b.encode('ascii'))


def _b64_decode_str(s):
    return _b64_decode_bytes(s).decode('utf8')


class Serializer(object):

    def dumps(self, request, response, body=None):
        response_headers = CaseInsensitiveDict(response.headers)
        if body is None:
            body = response.read(decode_content=False)
            response._fp = io.BytesIO(body)
        data = {'response': {'body':body, 
                      'headers':dict(((text_type(k), text_type(v)) for k, v in response.headers.items())), 
                      'status':response.status, 
                      'version':response.version, 
                      'reason':text_type(response.reason), 
                      'strict':response.strict, 
                      'decode_content':response.decode_content}}
        data['vary'] = {}
        if 'vary' in response_headers:
            varied_headers = response_headers['vary'].split(',')
            for header in varied_headers:
                header = text_type(header).strip()
                header_value = request.headers.get(header, None)
                if header_value is not None:
                    header_value = text_type(header_value)
                data['vary'][header] = header_value

        return (b',').join([b'cc=4', msgpack.dumps(data, use_bin_type=True)])

    def loads(self, request, data):
        if not data:
            return
        try:
            ver, data = data.split(b',', 1)
        except ValueError:
            ver = b'cc=0'

        if ver[:3] != b'cc=':
            data = ver + data
            ver = b'cc=0'
        ver = ver.split(b'=', 1)[(-1)].decode('ascii')
        try:
            return getattr(self, '_loads_v{}'.format(ver))(request, data)
        except AttributeError:
            return

    def prepare_response(self, request, cached):
        """Verify our vary headers match and construct a real urllib3
        HTTPResponse object.
        """
        if '*' in cached.get('vary', {}):
            return
            for header, value in cached.get('vary', {}).items():
                if request.headers.get(header, None) != value:
                    return

            body_raw = cached['response'].pop('body')
            headers = CaseInsensitiveDict(data=(cached['response']['headers']))
            if headers.get('transfer-encoding', '') == 'chunked':
                headers.pop('transfer-encoding')
        else:
            cached['response']['headers'] = headers
            try:
                body = io.BytesIO(body_raw)
            except TypeError:
                body = io.BytesIO(body_raw.encode('utf8'))

        return HTTPResponse(body=body, preload_content=False, **cached['response'])

    def _loads_v0(self, request, data):
        pass

    def _loads_v1(self, request, data):
        try:
            cached = pickle.loads(data)
        except ValueError:
            return
        else:
            return self.prepare_response(request, cached)

    def _loads_v2(self, request, data):
        try:
            cached = json.loads(zlib.decompress(data).decode('utf8'))
        except (ValueError, zlib.error):
            return
        else:
            cached['response']['body'] = _b64_decode_bytes(cached['response']['body'])
            cached['response']['headers'] = dict(((_b64_decode_str(k), _b64_decode_str(v)) for k, v in cached['response']['headers'].items()))
            cached['response']['reason'] = _b64_decode_str(cached['response']['reason'])
            cached['vary'] = dict(((_b64_decode_str(k), _b64_decode_str(v) if v is not None else v) for k, v in cached['vary'].items()))
            return self.prepare_response(request, cached)

    def _loads_v3(self, request, data):
        pass

    def _loads_v4(self, request, data):
        try:
            cached = msgpack.loads(data, raw=False)
        except ValueError:
            return
        else:
            return self.prepare_response(request, cached)