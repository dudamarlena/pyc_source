# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/machin/.virtualenvs/twine/lib/python2.7/site-packages/gerritclient/common/utils.py
# Compiled at: 2017-08-20 02:55:20
import functools, json, os, six, yaml
from gerritclient import error
SUPPORTED_FILE_FORMATS = ('json', 'yaml')

def get_display_data_single(fields, data, missing_field_value=None):
    """Performs slicing of data by set of given fields.

    :param fields: Iterable containing names of fields to be retrieved
                   from data
    :param data:   Collection of JSON objects representing some
                   external entities
    :param missing_field_value: the value will be used for all missing fields

    :return:       List containing the collection of values of the
                   supplied attributes
    """
    return [ data.get(field, missing_field_value) for field in fields ]


def get_display_data_multi(fields, data, sort_by=None):
    """Performs slice of data by set of given fields for multiple objects.

    :param fields:  Iterable containing names of fields to be retrieved
                    from data
    :param data:    Collection of JSON objects representing some
                    external entities
    :param sort_by: List of fields to sort by. By default no sorting

    :return:        List containing the collection of values of the
                    supplied attributes
    """
    data = [ get_display_data_single(fields, elem) for elem in data ]
    if sort_by:
        s_col_ids = [ fields.index(col) for col in sort_by ]
        data.sort(key=lambda x: [ x[s_col_id] for s_col_id in s_col_ids ])
    return data


def safe_load(data_format, stream):
    loaders = {'json': safe_deserialize(json.load), 'yaml': safe_deserialize(yaml.safe_load)}
    if data_format not in loaders:
        raise ValueError(('Unsupported data format. Available formats are: {0}').format(SUPPORTED_FILE_FORMATS))
    loader = loaders[data_format]
    return loader(stream)


def safe_dump(data_format, stream, data):
    yaml_dumper = lambda data, stream: yaml.safe_dump(data, stream, default_flow_style=False)
    json_dumper = lambda data, stream: json.dump(data, stream, indent=4)
    dumpers = {'json': json_dumper, 'yaml': yaml_dumper}
    if data_format not in dumpers:
        raise ValueError(('Unsupported data format. Available formats are: {0}').format(SUPPORTED_FILE_FORMATS))
    dumper = dumpers[data_format]
    dumper(data, stream)


def read_from_file(file_path):
    data_format = os.path.splitext(file_path)[1].lstrip('.')
    with open(file_path, 'r') as (stream):
        return safe_load(data_format, stream)


def write_to_file(file_path, data):
    data_format = os.path.splitext(file_path)[1].lstrip('.')
    with open(file_path, 'w') as (stream):
        safe_dump(data_format, stream, data)


def safe_deserialize(loader):
    """Wrapper for deserializers.

    Exceptions are raising during deserialization will be transformed into
    BadDataException

    :param loader: deserializer function
    :return: wrapped loader
    """

    @functools.wraps(loader)
    def wrapper(data):
        try:
            return loader(data)
        except (ValueError, TypeError, yaml.error.YAMLError) as e:
            raise error.BadDataException(('{0}: {1}').format(e.__class__.__name__, six.text_type(e)))

    return wrapper


def file_exists(path):
    """Checks if file exists

    :param str path: path to the file
    :returns: True if file exists, False otherwise
    """
    return os.path.lexists(path)


def urljoin(*args):
    """Joins given arguments into an URL.

    Trailing, but not leading slashes are stripped for each argument.
    """
    return ('/').join(map(lambda x: str(x).rstrip('/'), args))