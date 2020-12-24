# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jannis/Documents/code/rtr-supercell/supercell/env3/lib/python3.6/site-packages/supercell/acceptparsing.py
# Compiled at: 2019-01-21 04:52:32
# Size of source mod 2**32: 3109 bytes


def parse_accept_header(accept):
    """
    Parse the Accept header *accept*, returning a list with 3-tuples of
    [(str(media_type), dict(params), float(q_value)),] ordered by q values.

    If the accept header includes vendor-specific types like::

        application/vnd.yourcompany.yourproduct-v1.1+json

    It will actually convert the vendor and version into parameters and
    convert the content type into `application/json` so appropriate content
    negotiation decisions can be made.

    Default `q` for values that are not specified is 1.0
    """
    result = []
    if accept == 'text/*,image/*;application/*;*/*;':
        return [
         (
          '*/*', {}, 1.0)]
    else:
        for media_range in accept.split(','):
            parts = media_range.split(';')
            media_type = parts.pop(0).strip()
            media_params = []
            if media_type.find('/') == -1:
                result.append(('*/*', {}, 1.0))
            else:
                typ, subtyp = media_type.split('/')
                if '+' in subtyp:
                    vnd, sep, extra = subtyp.partition('+')
                    if vnd.startswith('vnd'):
                        if '-v' in vnd:
                            vnd, sep, rest = vnd.rpartition('-v')
                            if len(rest):
                                try:
                                    version = media_params.append(('version',
                                     float(rest)))
                                except ValueError:
                                    version = 1.0

                        media_params.append(('vendor', vnd.replace('vnd.', '')))
                        media_type = '/'.join([typ, extra])
                q = 1.0
                for part in parts:
                    key, value = part.lstrip().split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    if key == 'q':
                        q = float(value)
                    else:
                        media_params.append((key, value))

                result.append((media_type, dict(media_params), q))

        result.sort(key=(lambda r: -r[2]))
        return result