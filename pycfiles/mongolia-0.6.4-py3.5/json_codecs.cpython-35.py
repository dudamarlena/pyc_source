# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mongolia/json_codecs.py
# Compiled at: 2017-02-10 15:15:18
# Size of source mod 2**32: 2080 bytes
import datetime, dateutil, json
from bson import ObjectId
OBJECTID_IDENTIFIER = '$oid'
ISO_8601_IDENTIFIER = '$iso'

class MongoliaJSONEncoder(json.JSONEncoder):
    __doc__ = '\n    Adds the ability to serialize python ObjectId and datetime.datetime objects\n    when included in json.dumps(). The results are json objects with their\n    respective identifiers as keys and their serialized values as values.\n    \n    ObjectId objects are serialized as strings, and datetime.datetime objects\n    are serialized to the standard ISO 8601 format.\n    \n    >>> json.dumps(ObjectId(\'5717fc0d78ba2f1d6c41919a\'), cls=MongoliaJSONEncoder)\n    \'{OBJECTID_IDENTIFIER: "5717fc0d78ba2f1d6c41919a"}\'\n    \n    >>> json.dumps(datetime.datetime(2016, 4, 20, 18, 28, 12), cls=MongoliaJSONEncoder)\n    \'{ISO_8601_IDENTIFIER: "2016-04-20T18:28:12"}\'\n    '

    def default(self, o):
        if isinstance(o, ObjectId):
            return {OBJECTID_IDENTIFIER: str(o)}
        if isinstance(o, datetime.date) or isinstance(o, datetime.datetime):
            return {ISO_8601_IDENTIFIER: o.isoformat()}
        return super(MongoliaJSONEncoder, self).default(o)


class MongoliaJSONDecoder(json.JSONDecoder):
    __doc__ = '\n    Adds the ability to deserialize Mongolia\'s json representations of python\n    ObjectId and datetime.datetime objects when included in json.loads().\n    \n    >>> json.loads(\'{OBJECTID_IDENTIFIER: "5717fc0d78ba2f1d6c41919a"}\', cls=MongoliaJSONDecoder)\n    ObjectId(\'5717fc0d78ba2f1d6c41919a\')\n    \n    >>> json.loads(\'{ISO_8601_IDENTIFIER: "2016-04-20T18:28:12"}\', cls=MongoliaJSONDecoder)\n    datetime.datetime(2016, 4, 20, 18, 28, 12)\n    '

    def __init__(self, *args, **kwargs):
        super(MongoliaJSONDecoder, self).__init__(*args, **kwargs)

    def convert(self, o):
        if OBJECTID_IDENTIFIER in o:
            return ObjectId(o[OBJECTID_IDENTIFIER])
        if ISO_8601_IDENTIFIER in o:
            return dateutil.parser.parse(o[ISO_8601_IDENTIFIER])
        return o