# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mike/PycharmProjects/bqtools/build/lib/bqtools/__init__.py
# Compiled at: 2020-01-05 15:42:01
# Size of source mod 2**32: 116942 bytes
__doc__ = 'bqtools-json a module for managing interaction between json data and big query.\n\nThis module provides utility functions for big query and specifically treating big query as json\ndocument database.\nSchemas can be defined in json and provides means to create such structures by reading or passing\njson structures.\n\n'
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import copy, json, logging, os, pprint, re, threading
try:
    import queue
except ImportError:
    import Queue as queue

from datetime import datetime, date, timedelta, time
from time import sleep
from google.cloud import bigquery, exceptions, storage
from jinja2 import Environment, select_autoescape, FileSystemLoader
INVALIDBQFIELDCHARS = re.compile('[^a-zA-Z0-9_]')
HEADVIEW = '#standardSQL\nSELECT\n  *\nFROM\n  `{0}.{1}.{2}`\nWHERE\n  _PARTITIONTIME = (\n  SELECT\n    MAX(_PARTITIONTIME)\n  FROM\n    `{0}.{1}.{2}`)'
_ROOT = os.path.abspath(os.path.dirname(__file__))
DSTABLELISTQUERY = 'SELECT\n  table_name\nFROM\n  {}.INFORMATION_SCHEMA.TABLES\nWHERE\n  table_type = "BASE TABLE"\nORDER BY\n  1'
DSVIEWLISTQUERY = 'SELECT\n  v.table_name,\n  v.use_standard_sql,\n  t.creation_time,\n  v.view_definition\nFROM\n  {0}.INFORMATION_SCHEMA.TABLES AS t\nJOIN\n  {0}.INFORMATION_SCHEMA.VIEWS AS v\nON\n  v.table_name = t.table_name\nWHERE\n  t.table_type = "VIEW"\nORDER BY\n  v.table_name'
DSVIEWORDER = 'SELECT\n  t.table_name\nFROM\n  {0}.INFORMATION_SCHEMA.TABLES AS t\nWHERE\n  t.table_type = "VIEW"\nORDER BY\n  creation_time'
TCMPDAYPARTITION = 'SELECT\n  FORMAT_TIMESTAMP("%Y%m%d", _PARTITIONTIME) AS partitionName,\n  COUNT(*) AS rowNum{extrafunctions}\nFROM\n  `{project}.{dataset}.{table_name}`\nGROUP BY\n  1\nORDER BY\n  1'
MAPBQREGION2KMSREGION = {'EU': 'europe'}

class BQJsonEncoder(json.JSONEncoder):
    """BQJsonEncoder"""

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        else:
            if isinstance(obj, date):
                return obj.isoformat()
            if isinstance(obj, timedelta):
                return (datetime.min + obj).time().isoformat()
            return super(BQJsonEncoder, self).default(obj)


class BQTError(Exception):
    """BQTError"""
    pass


class InconsistentJSONStructure(BQTError):
    """InconsistentJSONStructure"""
    CUSTOM_ERROR_MESSAGE = 'The json structure passed has inconsistent types for the same key {0} and thus cannot be made into a BQ schema or valid json new line for loading onto big query\n{1} type previously {2}'

    def __init__(self, resource_name, e, ttype):
        super(InconsistentJSONStructure, self).__init__(self.CUSTOM_ERROR_MESSAGE.format(resource_name, e, ttype))


class NotADictionary(BQTError):
    CUSTOM_ERROR_MESSAGE = 'The json structure passed is not a dictionary\n{1}'

    def __init__(self, resource_name):
        super(NotADictionary, self).__init__(self.CUSTOM_ERROR_MESSAGE.format(resource_name, e))


class UnexpectedType(BQTError):
    CUSTOM_ERROR_MESSAGE = 'The object type of \n{1} is nota type that bqutils knows how to handle'

    def __init__(self, resource_name):
        super(UnexpectedType, self).__init__(self.CUSTOM_ERROR_MESSAGE.format(resource_name, e))


class UnexpectedDict(BQTError):
    CUSTOM_ERROR_MESSAGE = 'The object is a dict and shoulld not be \n{0}'

    def __init__(self, resource_name):
        super(UnexpectedDict, self).__init__(self.CUSTOM_ERROR_MESSAGE.format(resource_name))


class SchemaMutationError(BQTError):
    """SchemaMutationError"""
    CUSTOM_ERROR_MESSAGE = 'Schema Mutation Error: unable to mutate object path {0} on keyi {1} object {2}'

    def __init__(self, objtomatch, keyi, path):
        super(SchemaMutationError, self).__init__(self.CUSTOM_ERROR_MESSAGE.format(objtomatch, keyi, path))


class BQQueryError(BQTError):
    """BQQueryError"""
    CUSTOM_ERROR_MESSAGE = 'GCP API Error: unable to processquery {0} from GCP:\n{1}'

    def __init__(self, query, desc, e):
        super(ApiExecutionError, self).__init__(self.CUSTOM_ERROR_MESSAGE.format(query, e))


def get_json_struct(jsonobj, template=None):
    """

    :param jsonobj: Object to parse and adjust so could be loaded into big query
    :param template:  An input object to use as abasis as a template defaullt no template provided
    :return:  A json object that is a template object. This can be used as input to
    get_bq_schema_from_json_repr
    """
    if template is None:
        template = {}
    for key in jsonobj:
        newkey = INVALIDBQFIELDCHARS.sub('_', key)
        if jsonobj[key] is None:
            pass
        else:
            if newkey not in template:
                value = None
                if isinstance(jsonobj[key], bool):
                    value = False
                else:
                    if isinstance(jsonobj[key], str):
                        value = ''
                    else:
                        if isinstance(jsonobj[key], unicode):
                            value = ''
                        else:
                            if isinstance(jsonobj[key], int) or isinstance(jsonobj[key], long):
                                value = 0
                            else:
                                if isinstance(jsonobj[key], float):
                                    value = 0.0
                                else:
                                    if isinstance(jsonobj[key], date):
                                        value = jsonobj[key]
                                    else:
                                        if isinstance(jsonobj[key], datetime):
                                            value = jsonobj[key]
                                        else:
                                            if isinstance(jsonobj[key], dict):
                                                value = get_json_struct(jsonobj[key])
                                            else:
                                                if isinstance(jsonobj[key], list):
                                                    value = [{}]
                                                    if len(jsonobj[key]) > 0:
                                                        if not isinstance(jsonobj[key][0], dict):
                                                            new_value = []
                                                            for vali in jsonobj[key]:
                                                                new_value.append({'value': vali})

                                                            jsonobj[key] = new_value
                                                        for list_item in jsonobj[key]:
                                                            value[0] = get_json_struct(list_item, value[0])

                                                else:
                                                    raise UnexpectedType(str(jsonobj[key]))
                template[newkey] = value
            elif isinstance(jsonobj[key], type(template[newkey])):
                if isinstance(jsonobj[key], dict):
                    template[key] = get_json_struct(jsonobj[key], template[newkey])
            else:
                if isinstance(jsonobj[key], list):
                    if len(jsonobj[key]) != 0:
                        if not isinstance(jsonobj[key][0], dict):
                            new_value = []
                            for vali in jsonobj[key]:
                                new_value.append({'value': vali})

                            jsonobj[key] = new_value
                        for list_item in jsonobj[key]:
                            template[newkey][0] = get_json_struct(list_item, template[newkey][0])

                    else:
                        newtype = ''
                        if isinstance(jsonobj[key], float):
                            if isinstance(template[newkey], int):
                                newtype = 0.0
                        if isinstance(jsonobj[key], datetime):
                            if isinstance(template[newkey], date):
                                newtype = jsonobj[key]
                        if not (isinstance(jsonobj[key], dict) or isinstance(jsonobj[key], list)):
                            if not (isinstance(template[newkey], list) or isinstance(template[newkey], dict)):
                                template[newkey] = newtype
                        raise InconsistentJSONStructure(key, str(jsonobj[key]), str(template[newkey]))

    return template


def clean_json_for_bq(anobject):
    """

    :param object to be converted to big query json compatible format:
    :return: cleaned object
    """
    newobj = {}
    if not isinstance(anobject, dict):
        raise NotADictionary(str(anobject))
    for key in anobject:
        newkey = INVALIDBQFIELDCHARS.sub('_', key)
        value = anobject[key]
        if isinstance(value, dict):
            value = clean_json_for_bq(value)
        if isinstance(value, list):
            if len(value) != 0:
                if not isinstance(value[0], dict):
                    new_value = []
                    for vali in value:
                        new_value.append({'value': vali})

                    value = new_value
                valllist = []
                for vali in value:
                    vali = clean_json_for_bq(vali)
                    valllist.append(vali)

                value = valllist
        newobj[newkey] = value

    return newobj


def get_bq_schema_from_json_repr(jsondict):
    """
    Generate fields structure of Big query resource if the input json structure is vallid
    :param jsondict:  a template object in json format to use as basis to create a big query
    schema object from
    :return: a big query schema
    """
    fields = []
    for key, data in jsondict.items():
        field = {'name': key}
        if isinstance(data, bool):
            field['type'] = 'BOOLEAN'
            field['mode'] = 'NULLABLE'
        else:
            if isinstance(data, str):
                field['type'] = 'STRING'
                field['mode'] = 'NULLABLE'
            else:
                if isinstance(data, unicode):
                    field['type'] = 'STRING'
                    field['mode'] = 'NULLABLE'
                else:
                    if isinstance(data, int):
                        field['type'] = 'INTEGER'
                        field['mode'] = 'NULLABLE'
                    else:
                        if isinstance(data, float):
                            field['type'] = 'FLOAT'
                            field['mode'] = 'NULLABLE'
                        else:
                            if isinstance(data, datetime):
                                field['type'] = 'DATETIME'
                                field['mode'] = 'NULLABLE'
                            else:
                                if isinstance(data, date):
                                    field['type'] = 'DATE'
                                    field['mode'] = 'NULLABLE'
                                else:
                                    if isinstance(data, time):
                                        field['type'] = 'TIME'
                                        field['mode'] = 'NULLABLE'
                                    else:
                                        if isinstance(data, bytes):
                                            field['type'] = 'BYTES'
                                            field['mode'] = 'NULLABLE'
                                        else:
                                            if isinstance(data, dict):
                                                field['type'] = 'RECORD'
                                                field['mode'] = 'NULLABLE'
                                                field['fields'] = get_bq_schema_from_json_repr(data)
                                            else:
                                                if isinstance(data, list):
                                                    field['type'] = 'RECORD'
                                                    field['mode'] = 'REPEATED'
                                                    field['fields'] = get_bq_schema_from_json_repr(data[0])
        fields.append(field)

    return fields


def generate_create_schema(resourcelist, file_handle):
    """
    Generates using a jinja template bash command using bq to for a set of schemas
    supports views, tables or exetrnal tables.
    The resource list is a list of tables as you would get from table.get from big query
    or generated by get_bq_schema_from_json_repr

    :param resourcelist: list of resources to genereate code for
    :param file_handle: file handle to output too expected to be utf-8
    :return: nothing
    """
    jinjaenv = Environment(loader=(FileSystemLoader(os.path.join(_ROOT, 'templates'))),
      autoescape=(select_autoescape(['html', 'xml'])),
      extensions=[
     'jinja2.ext.do', 'jinja2.ext.loopcontrols'])
    objtemplate = jinjaenv.get_template('bqschema.in')
    output = objtemplate.render(resourcelist=resourcelist)
    print((output.encode('utf-8')), file=file_handle)


def generate_create_schema_file(filename, resourcelist):
    """
    Generates using a jinja template bash command using bq to for a set of schemas
    supports views, tables or exetrnal tables.
    The resource list is a list of tables as you would get from table.get from big query
    or generated by get_bq_schema_from_json_repr

    :param filename: filename to putput too
    :param resourcelist: list of resources to genereate code for
    :return:nothing
    """
    with open(filename, mode='wb+') as (file_handle):
        generate_create_schema(resourcelist, file_handle)


def dataset_exists(client, dataset_reference):
    """Return if a dataset exists.

    Args:
        client (google.cloud.bigquery.client.Client):
            A client to connect to the BigQuery API.
        dataset_reference (google.cloud.bigquery.dataset.DatasetReference):
            A reference to the dataset to look for.

    Returns:
        bool: ``True`` if the dataset exists, ``False`` otherwise.
    """
    from google.cloud.exceptions import NotFound
    try:
        client.get_dataset(dataset_reference)
        return True
    except NotFound:
        return False
    except exceptions.NotFound:
        return False


def table_exists(client, table_reference):
    """Return if a table exists.

    Args:
        client (google.cloud.bigquery.client.Client):
            A client to connect to the BigQuery API.
        table_reference (google.cloud.bigquery.table.TableReference):
            A reference to the table to look for.

    Returns:
        bool: ``True`` if the table exists, ``False`` otherwise.
    """
    from google.cloud.exceptions import NotFound
    try:
        client.get_table(table_reference)
        return True
    except NotFound:
        return False
    except exceptions.NotFound:
        return False


def create_schema(sobject, schema_depth=0, fname=None, dschema=None):
    schema = []
    if dschema is None:
        dschema = {}
    dummyfield = bigquery.SchemaField('xxxDummySchemaAsNoneDefinedxxx', 'STRING')
    if fname is not None:
        fname = INVALIDBQFIELDCHARS.sub('_', fname)
    if isinstance(sobject, list):
        tschema = []
        pdschema = dschema
        if fname is not None:
            if fname not in dschema:
                dschema[fname] = {}
                pdschema = dschema[fname]
        for i in sobject:
            if isinstance(sobject, dict) or isinstance(sobject, list):
                tschema.extend(create_schema(i, dschema=pdschema))

        if len(tschema) == 0:
            tschema.append(dummyfield)
        if fname is not None:
            recordschema = bigquery.SchemaField(fname, 'RECORD', mode='REPEATED', fields=tschema)
            schema.append(recordschema)
        else:
            schema = tschema
    else:
        if isinstance(sobject, dict):
            tschema = []
            if len(sobject) > 0:
                for j in sobject:
                    if j not in dschema:
                        dschema[j] = {}
                    if 'simple' not in dschema[j]:
                        fieldschema = create_schema((sobject[j]), fname=j, dschema=(dschema[j]))
                        if fieldschema is not None:
                            if fname is not None:
                                tschema.extend(fieldschema)
                            else:
                                schema.extend(fieldschema)

            else:
                if fname is not None:
                    tschema.append(dummyfield)
                else:
                    schema.append(dummyfield)
            if fname is not None:
                recordschema = bigquery.SchemaField(fname, 'RECORD', fields=tschema)
                schema = [recordschema]
        else:
            fieldschema = None
            if fname is not None:
                if isinstance(sobject, bool):
                    fieldschema = bigquery.SchemaField(fname, 'BOOLEAN')
                else:
                    if isinstance(sobject, int):
                        fieldschema = bigquery.SchemaField(fname, 'INTEGER')
                    else:
                        if isinstance(sobject, float):
                            fieldschema = bigquery.SchemaField(fname, 'FLOAT')
                        else:
                            if isinstance(sobject, datetime):
                                fieldschema = bigquery.SchemaField(fname, 'DATETIME')
                            else:
                                if isinstance(sobject, date):
                                    fieldschema = bigquery.SchemaField(fname, 'DATE')
                                else:
                                    if isinstance(sobject, time):
                                        fieldschema = bigquery.SchemaField(fname, 'TIME')
                                    else:
                                        if isinstance(sobject, str) or isinstance(sobject, unicode):
                                            fieldschema = bigquery.SchemaField(fname, 'STRING')
                                        else:
                                            if isinstance(sobject, bytes):
                                                fieldschema = bigquery.SchemaField(fname, 'BYTES')
                                            else:
                                                if isinstance(sobject, list):
                                                    if len(sobject) > 0:
                                                        fieldschema = bigquery.SchemaField(fname, 'RECORD')
                                                        fieldschema.mode = 'REPEATED'
                                                        mylist = sobject
                                                        head = mylist[0]
                                                        fieldschema.fields = create_schema(head, schema_depth + 1)
                                                else:
                                                    if isinstance(sobject, dict):
                                                        fieldschema = bigquery.SchemaField(fname, 'RECORD')
                                                        fieldschema.fields = create_schema(sobject, schema_depth + 1)
                                                    else:
                                                        raise UnexpectedType(str(type(sobject)))
                if dschema is not None:
                    dschema['simple'] = True
                return [fieldschema]
            else:
                return []
        return schema


def dict_plus_schema_2_tuple(data, schema):
    """
    :param data:
    :param schema:
    :return:
    """
    otuple = []
    for schema_item in schema:
        value = None
        if data is not None:
            if schema_item.name in data:
                value = data[schema_item.name]
        if schema_item.field_type == 'RECORD':
            ttuple = []
            if schema_item.mode != 'REPEATED' or value is None:
                value = [
                 value]
            for value_item in value:
                value = dict_plus_schema_2_tuple(value_item, schema_item.fields)
                ttuple.append(value)

            value = ttuple
        otuple.append(value)

    return tuple(otuple)


def tuple_plus_schema_2_dict(data, schema):
    """
    :param data:
    :param schema:
    :return:
    """
    rdata = {}
    for schema_item, value in zip(schema, data):
        if schema_item.field_type == 'RECORD':
            ldata = []
            if schema_item.mode == 'REPEATED':
                llist = value
            else:
                llist = [
                 value]
            for list_item in llist:
                ldata.append(tuple_plus_schema_2_dict(list_item, schema_item.fields))

            if schema_item.mode == 'REPEATED':
                value = ldata
            else:
                value = ldata[0]
        rdata[schema_item.name] = value

    return rdata


def gen_template_dict(schema):
    """

    :param schema: Take a rest representation of google big query table fields and create a
    template json object
    :return:
    """
    rdata = {}
    for schema_item in schema:
        value = None
        if schema_item.field_type == 'RECORD':
            tvalue = self.gen_template_dict(schema_item.fields)
            if schema_item.mode == 'REPEATED':
                value = [
                 tvalue]
            else:
                value = tvalue
        else:
            if schema_item.field_type == 'INTEGER':
                value = 0
            else:
                if schema_item.field_type == 'BOOLEAN':
                    value = False
                else:
                    if schema_item.field_type == 'FLOAT':
                        value = 0.0
                    else:
                        if schema_item.field_type == 'STRING':
                            value = ''
                        else:
                            if schema_item.field_type == 'DATETIME':
                                value = datetime.utcnow()
                            else:
                                if schema_item.field_type == 'DATE':
                                    value = date.today()
                                else:
                                    if schema_item.field_type == 'TIME':
                                        value = datetime.time()
                                    else:
                                        if schema_item.field_type == 'BYTES':
                                            value = '\x00'
                                        else:
                                            raise UnexpectedType(str(type(sobject)))
        rdata[schema_item.name] = value

    return rdata


def to_dict(schema):
    field_member = {'name':schema.name, 
     'type':schema.field_type, 
     'description':schema.description, 
     'mode':schema.mode, 
     'fields':None}
    if schema.fields is not None:
        fields_to_append = []
        for field_item in schema.fields:
            fields_to_append.append(to_dict(field_item))

        field_member['fields'] = fields_to_append
    return field_member


def calc_field_depth(fieldlist, depth=0):
    max_depth = depth
    recursive_depth = depth
    for i in fieldlist:
        if 'fields' in i:
            recursive_depth = calc_field_depth(i['fields'], depth + 1)
            if recursive_depth > max_depth:
                max_depth = recursive_depth

    return max_depth


def trunc_field_depth(fieldlist, maxdepth, depth=0):
    new_field = []
    if depth <= maxdepth:
        for i in fieldlist:
            new_field.append(i)
            if 'fields' in i:
                if depth == maxdepth:
                    i['type'] = 'STRING'
                    i.pop('fields', None)
                else:
                    i['fields'] = trunc_field_depth(i['fields'], maxdepth, depth + 1)

    return new_field


def match_and_addtoschema(objtomatch, schema, evolved=False, path='', logger=None):
    pretty_printer = pprint.PrettyPrinter(indent=4)
    poplist = {}
    for keyi in objtomatch:
        thekey = INVALIDBQFIELDCHARS.sub('_', keyi)
        if thekey != keyi:
            poplist[keyi] = thekey
        matchstruct = False
        do_bare_type_list(objtomatch, keyi, 'value')
        for schema_item in schema:
            if thekey == schema_item.name:
                if schema_item.field_type == 'RECORD':
                    if schema_item.mode == 'REPEATED':
                        subevolve = evolved
                        for listi in objtomatch[keyi]:
                            schema_item._fields = list(schema_item.fields)
                            tsubevolve = match_and_addtoschema(listi, (schema_item.fields), evolved=evolved,
                              path=(path + '.' + thekey))
                            if not subevolve and tsubevolve:
                                subevolve = tsubevolve

                        evolved = subevolve
                    else:
                        schema_item._fields = list(schema_item.fields)
                        evolved = match_and_addtoschema((objtomatch[keyi]), (schema_item.fields), evolved=evolved)
                matchstruct = True
                break

        if matchstruct:
            pass
        else:
            try:
                toadd = create_schema((objtomatch[keyi]), fname=keyi)
            except Exception as an_exception:
                raise SchemaMutationError(str(objtomatch), keyi, path)

        if toadd is not None:
            schema.extend(toadd)
            if logger is not None:
                logger.warning('Evolved path = {}, struct={}'.format(path + '.' + thekey, pretty_printer.pformat(objtomatch[keyi])))
            evolved = True

    if len(poplist):
        for pop_item in poplist:
            objtomatch[poplist[pop_item]] = objtomatch[pop_item]
            objtomatch.pop(pop_item, None)

    return evolved


def do_bare_type_list(adict, key, detail, logger=None):
    """
    Converts a list that is pointed to be a key in a dctionary from
    non dictionary object to dictionary object. We do this as bare types
    are not allowed in BQ jsons structures. So structures of type

    "foo":[ 1,2,3 ]

    to

    "foo":[{"detail":1},{"detail":2},{"detail":3}]

    Args:
        self: The gscanner object instance
        adict: The dictionary the key of the list object is in. This object is modified so mutated.
        key: The key name of the list if it does not exist this does nothing. if the item at the
        key is not a list it
        does nothing if length of list is 0 this does nothing
        detail: The name of the field in new sub dictionary of each object
        logerror: boolean if true and list objects are already a dictionary will log trace and
        key that ha dthe issue

    Returns:
        Nothing.

    Raises:
        Nothing
    """
    try:
        if key in adict:
            if key in adict:
                if isinstance(adict[key], list):
                    if len(adict[key]) > 0:
                        new_list = isinstance(adict[key][0], dict) or []
                        for list_item in adict[key]:
                            new_list.append({detail: list_item})

                        adict[key] = new_list
            elif logger is not None:
                tbs = traceback.extract_stack()
                tbsflat = '\n'.join(map(str, tbs))
                logger.error('Bare list for key {} in dict {} expected a basic type not converting {}'.format(key, str(adict), tbsflat))
    except Exception as an_exception:
        raise UnexpectedDict('Bare list for key {} in dict {} expected a basic type not converting'.format(key, str(adict)))


def recurse_and_add_to_schema(schema, oschema):
    changes = False
    wschema = copy.deepcopy(schema)
    for output_schema_item in oschema:
        nschema = []
        for new_schema_item in wschema:
            if output_schema_item['name'].lower() == new_schema_item.name.lower():
                if output_schema_item['type'] == 'RECORD':
                    rchanges, output_schema_item['fields'] = recurse_and_add_to_schema(new_schema_item.fields, output_schema_item['fields'])
                    if rchanges and not changes:
                        changes = rchanges
            else:
                nschema.append(new_schema_item)

        wschema = nschema

    for wsi in wschema:
        changes = True
        oschema.append(to_dict(wsi))

    return (
     changes, oschema)


FSLST = '#standardSQL\nSELECT \n     ut.*, \n     fls.firstSeenScanversion,\n     fls.lastSeenScanVersion,\n     fls.firstSeenTime,\n     fls.lastSeenTime,\n     fls.numSeen\nFROM `{0}.{1}.{2}` as ut\nJOIN (\n    SELECT \n       id,\n       {4} AS firstSeenTime,\n       {4} AS lastSeenTime,\n       COUNT(*) AS numSeen\n    FROM `{0}.{1}.{2}`\n    GROUP BY \n    1) AS fls\nON fls.id = ut.id AND fls.{3}  = {4}\n'
FSLSTDT = "View that shows {} captured values of underlying table for object of a given non repeating key of 'id' {}.{}.{}"

def gen_diff_views(project, dataset, table, schema, description='', intervals=None, update_only_fields=None, time_expr=None, fieldsappend=None):
    """

    :param project: google project id of underlying table
    :param dataset: google dataset id of underlying table
    :param table: the base table to do diffs (assumes each time slaice is a view of what data
    looked like))
    :param schema: the schema of the base table
    :param description: a base description for the views
    :param intervals: a list of form []
    :param update_only_fields:
    :param time_expr:
    :param fieldsappend:
    :return:
    """
    views = []
    fieldsnot4diff = []
    if intervals is None:
        intervals = [
         {'day': '1 DAY'}, {'week': '7 DAY'}, {'month': '30 DAY'},
         {'fortnight': '14 DAY'}]
    if time_expr is None:
        time_expr = '_PARTITIONTIME'
    fieldsnot4diff.append('scantime')
    if isinstance(fieldsappend, list):
        for fdiffi in fieldsappend:
            fieldsnot4diff.append(fdiffi)

    if update_only_fields is None:
        update_only_fields = [
         'creationTime',
         'usage',
         'title',
         'description',
         'preferred',
         'documentationLink',
         'discoveryLink',
         'numLongTermBytes',
         'detailedStatus',
         'lifecycleState',
         'size',
         'md5Hash',
         'crc32c',
         'timeStorageClassUpdated',
         'deleted',
         'networkIP',
         'natIP',
         'changePasswordAtNextLogin',
         'status',
         'state',
         'substate',
         'stateStartTime',
         'metricValue',
         'requestedState',
         'statusMessage',
         'numWorkers',
         'currentStateTime',
         'currentState',
         'lastLoginTime',
         'lastViewedByMeDate',
         'modifiedByMeDate',
         'etag',
         'servingStatus',
         'lastUpdated',
         'updateTime',
         'lastModified',
         'lastModifiedTime',
         'timeStorageClassUpdated',
         'updated',
         'numRows',
         'numBytes',
         'numUsers',
         'isoCountryCodes',
         'countries',
         'uriDescription']
    fqtablename = '{}.{}.{}'.format(project, dataset, table)
    basediffview = table + 'db'
    basefromclause = '\nfrom `{}` as {}'.format(fqtablename, 'ta' + table)
    baseselectclause = '#standardSQL\nSELECT\n    {} AS scantime'.format(time_expr)
    curtablealias = 'ta' + table
    fieldprefix = ''
    aliasstack = []
    fieldprefixstack = []
    fields4diff = []
    fields_update_only = []
    aliasnum = 1
    basedata = {'select':baseselectclause, 
     'from':basefromclause,  'aliasnum':aliasnum}

    def recurse_diff_base(schema, fieldprefix, curtablealias):
        pretty_printer = pprint.PrettyPrinter(indent=4)
        for schema_item in schema:
            skip = False
            for fndi in fieldsnot4diff:
                if schema_item.name == fndi:
                    skip = True
                    break

            if skip:
                pass
            else:
                if schema_item.field_type == 'STRING':
                    basefield = ',\n    ifnull({}.{},"None") as {}'.format(curtablealias, schema_item.name, fieldprefix + schema_item.name)
                else:
                    if schema_item.field_type == 'BOOLEAN':
                        basefield = ',\n    ifnull({}.{},False) as {}'.format(curtablealias, schema_item.name, fieldprefix + schema_item.name)
                    else:
                        if schema_item.field_type == 'INTEGER':
                            basefield = ',\n    ifnull({}.{},0) as {}'.format(curtablealias, schema_item.name, fieldprefix + schema_item.name)
                        else:
                            if schema_item.field_type == 'FLOAT':
                                basefield = ',\n    ifnull({}.{},0.0) as {}'.format(curtablealias, schema_item.name, fieldprefix + schema_item.name)
                            else:
                                if schema_item.field_type == 'DATE':
                                    basefield = ',\n    ifnull({}.{},DATE(1970,1,1)) as {}'.format(curtablealias, schema_item.name, fieldprefix + schema_item.name)
                                else:
                                    if schema_item.field_type == 'DATETIME':
                                        basefield = ',\n    ifnull({}.{},DATETIME(1970,1,1,0,0,0)) as {}'.format(curtablealias, schema_item.name, fieldprefix + schema_item.name)
                                    else:
                                        if schema_item.field_type == 'TIME':
                                            basefield = ',\n    ifnull({}.{},TIME(0,0,0)) as {}'.format(curtablealias, schema_item.name, fieldprefix + schema_item.name)
                                        else:
                                            if schema_item.field_type == 'BYTES':
                                                basefield = ',\n    ifnull({}.{},b"\x00") as {}'.format(curtablealias, schema_item.name, fieldprefix + schema_item.name)
                                            else:
                                                if schema_item.field_type == 'RECORD':
                                                    aliasstack.append(curtablealias)
                                                    fieldprefixstack.append(fieldprefix)
                                                    fieldprefix = fieldprefix + schema_item.name
                                                    if schema_item.mode == 'REPEATED':
                                                        oldalias = curtablealias
                                                        curtablealias = 'A{}'.format(basedata['aliasnum'])
                                                        basedata['aliasnum'] = basedata['aliasnum'] + 1
                                                        basedata['from'] = basedata['from'] + '\nLEFT JOIN UNNEST({}) as {}'.format(oldalias + '.' + schema_item.name, curtablealias)
                                                    else:
                                                        curtablealias = curtablealias + '.' + schema_item.name
                                                    recurse_diff_base(schema_item.fields, fieldprefix, curtablealias)
                                                    curtablealias = aliasstack.pop()
                                                    fieldprefix = fieldprefixstack.pop()
                                                    continue
                    update_only = False
                    for fndi in update_only_fields:
                        if schema_item.name == fndi:
                            update_only = True
                            break

                    if update_only:
                        fields_update_only.append(fieldprefix + schema_item.name)
                    else:
                        fields4diff.append(fieldprefix + schema_item.name)
            basedata['select'] = basedata['select'] + basefield

    recurse_diff_base(schema, fieldprefix, curtablealias)
    views.append({'name':basediffview,  'query':basedata['select'] + basedata['from'],  'description':'View used as basis for diffview:' + description})
    refbasediffview = '{}.{}.{}'.format(project, dataset, basediffview)
    diffviewselectclause = '#standardSQL\nSELECT\n    o.scantime as origscantime,\n    l.scantime as laterscantime,'
    diffieldclause = ''
    diffcaseclause = ''
    diffwhereclause = ''
    diffviewfromclause = '\n  FROM (SELECT\n     *\n  FROM\n    `{0}`\n  WHERE\n    scantime = (\n    SELECT\n      MAX({1})\n    FROM\n      `{2}.{3}.{4}`\n    WHERE\n      {1} < (\n      SELECT\n        MAX({1})\n      FROM\n        `{2}.{3}.{4}`)\n      AND\n      {1} < TIMESTAMP_SUB(CURRENT_TIMESTAMP(),INTERVAL %interval%) ) ) o\nFULL OUTER JOIN (\n  SELECT\n     *\n  FROM\n    `{0}`\n  WHERE\n    scantime =(\n    SELECT\n      MAX({1})\n    FROM\n      `{2}.{3}.{4}` )) l\nON\n'.format(refbasediffview, time_expr, project, dataset, table)
    for f4i in fields4diff:
        diffieldclause = diffieldclause + ',\n    o.{} as orig{},\n    l.{} as later{},\n    case when o.{} = l.{} then 0 else 1 end as diff{}'.format(f4i, f4i, f4i, f4i, f4i, f4i, f4i)
        if diffcaseclause == '':
            diffcaseclause = "\n    CASE\n    WHEN o.{} IS NULL THEN 'Added'\n    WHEN l.{} IS NULL THEN 'Deleted'\n    WHEN o.{} = l.{} ".format(f4i, f4i, f4i, f4i)
        else:
            diffcaseclause = diffcaseclause + 'AND o.{} = l.{} '.format(f4i, f4i)
        if diffwhereclause == '':
            diffwhereclause = '    l.{} = o.{}'.format(f4i, f4i)
        else:
            diffwhereclause = diffwhereclause + '\n    AND l.{}=o.{}'.format(f4i, f4i)

    for f4i in fields_update_only:
        diffieldclause = diffieldclause + ',\n    o.{} as orig{},\n    l.{} as later{},\n    case when o.{} = l.{} then 0 else 1 end as diff{}'.format(f4i, f4i, f4i, f4i, f4i, f4i, f4i)
        diffcaseclause = diffcaseclause + 'AND o.{} = l.{} '.format(f4i, f4i)

    diffcaseclause = diffcaseclause + "THEN 'Same'\n    ELSE 'Updated'\n  END AS action"
    for intervali in intervals:
        for keyi in intervali:
            viewname = table + 'diff' + keyi
            viewdescription = 'Diff of {} of underlying table {} description: {}'.format(keyi, table, description)
            views.append({'name':viewname,  'query':diffviewselectclause + diffcaseclause + diffieldclause + diffviewfromclause.replace('%interval%', intervali[keyi]) + diffwhereclause, 
             'description':viewdescription})

    for i in schema:
        if i.name == 'id':
            fsv = FSLST.format(project, dataset, table, 'firstSeenTime', time_expr)
            fsd = FSLSTDT.format('first', project, dataset, table)
            lsv = FSLST.format(project, dataset, table, 'lastSeenTime', time_expr)
            lsd = FSLSTDT.format('last', project, dataset, table)
            views.append({'name':table + 'fs',  'query':fsv, 
             'description':fsd})
            views.append({'name':table + 'ls',  'query':lsv, 
             'description':lsd})
            break

    return views


def evolve_schema(insertobj, table, client, bigquery, logger=None):
    """

    :param insertobj: json object that represents schema expected
    :param table: a table object from python api thats been git through client.get_table
    :param client: a big query client object
    :param bigquery: big query service as created with google discovery discovery.build(
    "bigquery","v2")
    :param logger: a google logger class
    :return: evolved True or False
    """
    schema = list(table.schema)
    tablechange = False
    evolved = match_and_addtoschema(insertobj, schema)
    if evolved:
        if logger is not None:
            logger.warning('Evolving schema as new field(s) on {}:{}.{} views with * will need reapplying'.format(table.project, table.dataset_id, table.table_id))
        treq = bigquery.tables().get(projectId=(table.project), datasetId=(table.dataset_id), tableId=(table.table_id))
        table_data = treq.execute()
        oschema = table_data.get('schema')
        tablechange, pschema = recurse_and_add_to_schema(schema, oschema['fields'])
        update = {'schema': {'fields': pschema}}
        preq = bigquery.tables().patch(projectId=(table.project), datasetId=(table.dataset_id), tableId=(table.table_id),
          body=update)
        preq.execute()
        client.get_table(table)
    return evolved


def create_default_bq_resources(template, basename, project, dataset, location):
    """

    :param template: a template json object to create a big query schema for
    :param basename: a base name of the table to create that will also be used as a basis for views
    :param project: the project to create resources in
    :param dataset: the datasets to create them in
    :param location: The locatin
    :return: a list of big query table resources as dicionaries that can be passe dto code
    genearteor or used in rest
    calls
    """
    resourcelist = []
    table = {'type':'TABLE', 
     'location':location, 
     'tableReference':{'projectId':project, 
      'datasetId':dataset, 
      'tableId':basename}, 
     'timePartitioning':{'type':'DAY', 
      'expirationMs':'94608000000'}, 
     'schema':{}}
    table['schema']['fields'] = get_bq_schema_from_json_repr(template)
    resourcelist.append(table)
    views = gen_diff_views(project, dataset, basename, create_schema(template))
    table = {'type':'VIEW', 
     'tableReference':{'projectId':project, 
      'datasetId':dataset, 
      'tableId':'{}head'.format(basename)}, 
     'view':{'query':HEADVIEW.format(project, dataset, basename), 
      'useLegacySql':False}}
    resourcelist.append(table)
    for view_item in views:
        table = {'type':'VIEW',  'tableReference':{'projectId':project, 
          'datasetId':dataset, 
          'tableId':view_item['name']}, 
         'view':{'query':view_item['query'], 
          'useLegacySql':False}}
        resourcelist.append(table)

    return resourcelist


class ViewCompiler(object):

    def __init__(self):
        self.view_depth_optimiser = []

    def compile(self, dataset, name, sql):
        standard_sql = True
        compiled_sql = sql
        prefix = ''
        if sql.strip().lower().find('#standardsql') == 0:
            prefix = '#standardSQL\n'
        else:
            standard_sql = False
            prefix = '#legacySQL\n'
        prefix = prefix + '\n-- ===================================================================================\n-- \n--                             ViewCompresser Output\n--     \n--                      \\/\\/\\/\\/\\/\\/Original SQL Below\\/\\/\\/\\/\n'
        for line in sql.splitlines():
            prefix = prefix + '-- ' + line + '\n'

        prefix = prefix + '\n-- \n--                      /\\/\\/\\/\\/\\/\\Original SQL Above/\\/\\/\\/\\\n--                      \n--                            Compiled SQL below\n-- ===================================================================================\n'
        for i in self.view_depth_optimiser:
            if not standard_sql:
                compiled_sql = compiled_sql.replace('[' + i + ']', '( /* flattened view [-' + i + '-]*/ ' + self.view_depth_optimiser[i]['unnested'] + ')')
            else:
                compiled_sql = compiled_sql.replace('`' + i.replace(':', '.') + '`', '( /* flattened view `-' + i + '-`*/ ' + self.view_depth_optimiser[i]['unnested'] + ')')

        self.view_depth_optimiser[dataset.project + ':' + dataset.dataset_id + '.' + name] = {'raw':sql,  'unnested':compiled_sql}
        if len(prefix + compiled_sql) > 256000:
            if standard_sql:
                prefix = '#standardSQL\n'
            else:
                prefix = '#legacySQL\n'
            if len(prefix + compiled_sql) > 256000:
                nsql = ''
                for line in compiled_sql.split('\n').trim():
                    if line[:2] != '--':
                        ' '.join(line.split())
                        nsql = nsql + '\n' + line

                compiled_sql = nsql
                if len(prefix + compiled_sql) > 256000:
                    if len(sql) > 256000:
                        nsql = ''
                        for line in origsql.split('\n').trim():
                            if line[:1] != '#':
                                ' '.join(line.split())
                                nsql = nsql + '\n' + line
                                compiled_sql = nsql

                    else:
                        compiled_sql = sql
        return prefix + compiled_sql


def compute_region_equals_bqregion(compute_region, bq_region):
    if compute_region == bq_region or compute_region.lower() == bq_region.lower():
        bq_compute_region = bq_region.lower()
    else:
        bq_compute_region = MAPBQREGION2KMSREGION.get(bq_region, bq_region.lower())
    return compute_region.lower() == bq_compute_region


def run_query(client, query, logger, desctext='', location=None, max_results=10000):
    """
    Runa big query query and yield on each row returned as a generator
    :param client: The BQ client to use to run the query
    :param query: The query text assumed standardsql unless starts with #legcaySQL
    :param desctext: Some descriptive text to put out if in debug mode
    :return: nothing
    """
    use_legacy_sql = False
    if query.lower().find('#legacysql') == 0:
        use_legacy_sql = True
    job_config = bigquery.QueryJobConfig()
    job_config.maximum_billing_tier = 10
    job_config.use_legacy_sql = use_legacy_sql
    query_job = client.query(query, job_config=job_config, location=location)
    pretty_printer = pprint.PrettyPrinter(indent=4)
    results = False
    while 1:
        query_job.reload()
        if query_job.state == 'DONE':
            if query_job.error_result:
                errtext = 'Query error {}{}'.format(pretty_printer.pformat(query_job.error_result), pretty_printer.pformat(query_job.errors))
                logger.error(errtext, exc_info=True)
                raise BQQueryError(query, desctext, errtext)
            else:
                results = True
                break

    if results:
        for irow in query_job.result():
            yield irow


class DefaultBQSyncDriver(object):
    """DefaultBQSyncDriver"""
    threadLocal = threading.local()

    def __init__(self, srcproject, srcdataset, dstdataset, dstproject=None, srcbucket=None, dstbucket=None, remove_deleted_tables=True, copy_data=True, copy_views=True, check_depth=-1):
        """
        Constructor for base copy driver all other drivers should inherit from this
        :param srcproject: The project that is the source for the copy (note all actions are done inc ontext of source project)
        :param srcdataset: The source dataset
        :param dstdataset: The destination dataset
        :param dstproject: The source project if None assumed to be source project
        :param srcbucket:  The source bucket when copying cross region data is extracted to this bucket rewritten to destination bucket
        :param dstbucket: The destination bucket where data is loaded from
        :param remove_deleted_tables: If table exists in destination but not in source should it be deleted
        :param copy_data: Copy data or just do schema
        :param copy_views: Copy views not just tables attempts to rewrite views into context of destination failures are logged but continues
        """
        if dstproject is None:
            dstproject = srcproject
        else:
            self._remove_deleted_tables = remove_deleted_tables
            if not srcproject != dstproject:
                if not srcdataset != dstdataset:
                    raise AssertionError('Source and destination datasets cannot be the same')
            self._source_project = srcproject
            self._source_dataset = srcdataset
            self._destination_project = dstproject
            self._destination_dataset = dstdataset
            self._copy_data = copy_data
            self._http = None
            self._DefaultBQSyncDriver__copy_q = None
            self._DefaultBQSyncDriver__schema_q = None
            self._DefaultBQSyncDriver__jobs = []
            self._DefaultBQSyncDriver__copy_views = copy_views
            self.reset_stats()
            self._DefaultBQSyncDriver__logger = logging
            self._DefaultBQSyncDriver__check_depth = check_depth
            assert dataset_exists(self.source_client, self.source_client.dataset(self.source_dataset)), 'Source dataset does not exist %r' % self.source_dataset
            assert dataset_exists(self.destination_client, self.destination_client.dataset(self.destination_dataset)), 'Destination dataset does not exists %r' % self.destination_dataset
            source_dataset_impl = self.source_dataset_impl
            destination_dataset_impl = self.destination_dataset_impl
            self._same_region = source_dataset_impl.location == destination_dataset_impl.location
            self._source_location = source_dataset_impl.location
            self._destination_location = destination_dataset_impl.location
            if not self.same_region:
                if not srcbucket is not None:
                    raise AssertionError('Being asked to copy datasets across region but no source bucket is defined these must be in same region as source dataset')
                else:
                    if not isinstance(srcbucket, basestring):
                        raise AssertionError('Being asked to copy datasets across region but no source bucket is not a string')
                    else:
                        self._source_bucket = srcbucket
                        assert dstbucket is not None, 'Being asked to copy datasets across region but no destination bucket is defined these must be in same region as destination dataset'
                        assert isinstance(dstbucket, basestring), 'Being asked to copy datasets across region but destination bucket is not a string'
                    self._destination_bucket = dstbucket
                    client = storage.Client(project=(self.source_project))
                    src_bucket = client.get_bucket(self.source_bucket)
                    assert compute_region_equals_bqregion(src_bucket.location, source_dataset_impl.location), 'Source bucket location is not same as source dataset location'
                dst_bucket = client.get_bucket(self.destination_bucket)
                assert compute_region_equals_bqregion(dst_bucket.location, destination_dataset_impl.location), 'Destination bucket location is not same as destination dataset location'

    def reset_stats(self):
        self._DefaultBQSyncDriver__bytes_synced = 0
        self._DefaultBQSyncDriver__rows_synced = 0
        self._DefaultBQSyncDriver__bytes_avoided = 0
        self._DefaultBQSyncDriver__rows_avoided = 0
        self._DefaultBQSyncDriver__tables_synced = 0
        self._DefaultBQSyncDriver__views_synced = 0
        self._DefaultBQSyncDriver__views_failed_sync = 0
        self._DefaultBQSyncDriver__tables_failed_sync = 0
        self._DefaultBQSyncDriver__tables_avoided = 0
        self._DefaultBQSyncDriver__view_avoided = 0
        self._DefaultBQSyncDriver__extract_fails = 0
        self._DefaultBQSyncDriver__load_fails = 0
        self._DefaultBQSyncDriver__copy_fails = 0

    @property
    def copy_fails(self):
        return self._DefaultBQSyncDriver__copy_fails

    def increment_copy_fails(self):
        self._DefaultBQSyncDriver__copy_fails += 1

    @property
    def load_fails(self):
        return self._DefaultBQSyncDriver__load_fails

    def increment_load_fails(self):
        self._DefaultBQSyncDriver__load_fails += 1

    @property
    def extract_fails(self):
        return self._DefaultBQSyncDriver__extract_fails

    def increment_extract_fails(self):
        self._DefaultBQSyncDriver__extract_fails += 1

    @property
    def check_depth(self):
        return self._DefaultBQSyncDriver__check_depth

    @check_depth.setter
    def check_depth(self, value):
        self._DefaultBQSyncDriver__check_depth = value

    @property
    def views_failed_sync(self):
        return self._DefaultBQSyncDriver__views_failed_sync

    def increment_views_failed_sync(self):
        self._DefaultBQSyncDriver__views_failed_sync += 1

    @property
    def tables_failed_sync(self):
        return self._DefaultBQSyncDriver__tables_failed_sync

    def increment_tables_failed_sync(self):
        self._DefaultBQSyncDriver__tables_failed_sync += 1

    @property
    def tables_avoided(self):
        return self._DefaultBQSyncDriver__tables_avoided

    def increment_tables_avoided(self):
        self._DefaultBQSyncDriver__tables_avoided += 1

    @property
    def view_avoided(self):
        return self._DefaultBQSyncDriver__view_avoided

    def increment_view_avoided(self):
        self._DefaultBQSyncDriver__view_avoided += 1

    @property
    def bytes_synced(self):
        return self._DefaultBQSyncDriver__bytes_synced

    @property
    def copy_views(self):
        return self._DefaultBQSyncDriver__copy_views

    def add_bytes_synced(self, bytes):
        self._DefaultBQSyncDriver__bytes_synced += bytes

    @property
    def rows_synced(self):
        return self._DefaultBQSyncDriver__rows_synced

    def add_rows_synced(self, rows):
        self._DefaultBQSyncDriver__rows_synced += rows

    @property
    def bytes_avoided(self):
        return self._DefaultBQSyncDriver__bytes_avoided

    def add_bytes_avoided(self, bytes):
        self._DefaultBQSyncDriver__bytes_avoided += bytes

    @property
    def rows_avoided(self):
        return self._DefaultBQSyncDriver__rows_avoided

    def add_rows_avoided(self, rows):
        self._DefaultBQSyncDriver__rows_avoided += rows

    @property
    def tables_synced(self):
        return self._DefaultBQSyncDriver__tables_synced

    @property
    def views_synced(self):
        return self._DefaultBQSyncDriver__views_synced

    def increment_tables_synced(self):
        self._DefaultBQSyncDriver__tables_synced += 1

    def increment_views_synced(self):
        self._DefaultBQSyncDriver__views_synced += 1

    @property
    def copy_q(self):
        return self._DefaultBQSyncDriver__copy_q

    @copy_q.setter
    def copy_q(self, value):
        self._DefaultBQSyncDriver__copy_q = value

    @property
    def schema_q(self):
        return self._DefaultBQSyncDriver__schema_q

    @schema_q.setter
    def schema_q(self, value):
        self._DefaultBQSyncDriver__schema_q = value

    @property
    def source_location(self):
        return self._source_location

    @property
    def destination_location(self):
        return self._destination_location

    @property
    def source_bucket(self):
        return self._source_bucket

    @property
    def destination_bucket(self):
        return self._destination_bucket

    @property
    def same_region(self):
        return self._same_region

    @property
    def source_dataset_impl(self):
        source_datasetref = self.source_client.dataset(self.source_dataset)
        return self.source_client.get_dataset(source_datasetref)

    @property
    def destination_dataset_impl(self):
        destination_datasetref = self.destination_client.dataset(self.destination_dataset)
        return self.destination_client.get_dataset(destination_datasetref)

    @property
    def source_client(self):
        """
        Obtains a source client in the current thread only constructs a client once per thread
        :return:
        """
        source_client = getattr(DefaultBQSyncDriver.threadLocal, self.source_project + self._source_dataset, None)
        if source_client is None:
            setattr(DefaultBQSyncDriver.threadLocal, self.source_project + self._source_dataset, bigquery.Client(project=(self.source_project), _http=(self.http)))
        return getattr(DefaultBQSyncDriver.threadLocal, self.source_project + self._source_dataset, None)

    @property
    def http(self):
        """
        Allow override of http transport per client
        usefule for proxy handlng but should be handled by sub-classes default is do nothing
        :return:
        """
        self._http

    @property
    def destination_client(self):
        """
        Obtains a s destination client in current thread only constructs a client once per thread
        :return:
        """
        source_client = getattr(DefaultBQSyncDriver.threadLocal, self.destination_project + self.destination_dataset, None)
        if source_client is None:
            setattr(DefaultBQSyncDriver.threadLocal, self.destination_project + self.destination_dataset, bigquery.Client(project=(self.destination_project), _http=(self.http)))
        return getattr(DefaultBQSyncDriver.threadLocal, self.destination_project + self.destination_dataset, None)

    @property
    def source_project(self):
        return self._source_project

    @property
    def source_dataset(self):
        return self._source_dataset

    @property
    def jobs(self):
        return self._DefaultBQSyncDriver__jobs

    def add_job(self, job):
        self._DefaultBQSyncDriver__jobs.append(job)

    @property
    def destination_project(self):
        return self._destination_project

    @property
    def destination_dataset(self):
        return self._destination_dataset

    @property
    def remove_deleted_tables(self):
        return self._remove_deleted_tables

    def day_partition_deep_check(self):
        """

        :return: True if should check rows and bytes counts False if notrequired
        """
        return True

    def extra_dp_compare_functions(self, table):
        """
        Function to allow record comparison checks for a day partition
        These shoul dbe aggregates for the partition i..e max, min, avg
        Override when row count if not sufficient. Row count works for
        tables where rows only added non deleted or removed
        :return: a comma seperated extension of functions
        """
        default = ''
        SCHEMA = list(table.schema)
        expression_list = []
        for field in SCHEMA:
            if self.check_depth >= 0 or self.check_depth >= -1 and (re.search('update.*time', field.name.lower()) or re.search('modifi.*time', field.name.lower()) or re.search('creat.*time', field.name.lower())):
                if field.field_type == 'STRING':
                    expression_list.append("IFNULL(`{0}`,'')".format(field.name))
                else:
                    if field.field_type == 'TIMESTAMP':
                        expression_list.append("CAST(IFNULL(`{0}`,TIMESTAMP('1970-01-01')) AS STRING)".format(field.name))
                    else:
                        if field.field_type == 'INTEGER' or field.field_type == 'INT64':
                            expression_list.append('CAST(IFNULL(`{0}`,0) AS STRING)'.format(field.name))
                        else:
                            if field.field_type == 'FLOAT' or field.field_type == 'FLOAT64' or field.field_type == 'NUMERIC':
                                expression_list.append('CAST(IFNULL(`{0}`,0.0) AS STRING)'.format(field.name))
                            else:
                                if field.field_type == 'BOOL' or field.field_type == 'BOOLEAN':
                                    expression_list.append('CAST(IFNULL(`{0}`,false) AS STRING)'.format(field.name))
                                elif field.field_type == 'BYTES':
                                    expression_list.append("CAST(IFNULL(`{0}`,'') AS STRING)".format(field.name))

        if len(expression_list) > 0:
            default = ',\nAVG(FARM_FINGERPRINT(CONCAT({0}))) as avgFingerprint,\nSTDDEV_POP(FARM_FINGERPRINT(CONCAT({0}))) as stdDvPopFingerprint,'.format(','.join(expression_list))
        return default

    @property
    def copy_data(self):
        """
        True if to copy data not just structure
        False just keeps structure in sync
        :return:
        """
        return self._copy_data

    def table_data_change(self, srctable, dsttable):
        """
        Method to allow customisation of detecting if table differs
        default method is check rows, numberofbytes and last modified time
        this exists to allow something like a query to do comparison
        if you want to force a copy this should retrn True
        :param srctable:
        :param dsttable:
        :return:
        """
        return False

    def fault_barrier(self, function, *args):
        """
        A fault barrie here to ensure functions called in thread
        do n9t exit prematurely
        :param function: A function to call
        :param args: The functions arguments
        :return:
        """
        try:
            function(*args)
        except Exception as e:
            self.get_logger().exception(str(e))

    def update_source_view_definition(self, view_definition, use_standard_sql):
        view_definition = view_definition.replace('`{}.{}.'.format(self.source_project, self.source_dataset), '`{}.{}.'.format(self.destination_project, self.destination_dataset))
        view_definition = view_definition.replace('[{}:{}.'.format(self.source_project, self.source_dataset), '[{}:{}.'.format(self.destination_project, self.destination_dataset))
        view_definition = view_definition.replace('[{}.{}.'.format(self.source_project, self.source_dataset), '[{}:{}.'.format(self.destination_project, self.destination_dataset))
        return view_definition

    @property
    def logger(self):
        return self._DefaultBQSyncDriver__logger

    @logger.setter
    def logger(self, alogger):
        self._DefaultBQSyncDriver__logger = alogger

    def get_logger(self):
        """
        Returns the python logger to use for logging errors and issues
        :return:
        """
        return self._DefaultBQSyncDriver__logger


class MultiBQSyncCoordinator(object):
    """MultiBQSyncCoordinator"""

    def __init__(self, srcproject_and_dataset_list, dstproject_and_dataset_list, srcbucket=None, dstbucket=None, remove_deleted_tables=True, copy_data=True, copy_views=True, check_depth=-1):
        if not len(srcproject_and_dataset_list) == len(dstproject_and_dataset_list):
            raise AssertionError('Source and destination lists must be same length')
        elif not len(srcproject_and_dataset_list) > 0:
            raise AssertionError('Fro multi copy we need at least 1 source and 1 destination')
        self._MultiBQSyncCoordinator__copy_drivers = []
        self._MultiBQSyncCoordinator__check_depth = check_depth
        for itemnum, src_project_dataset in enumerate(srcproject_and_dataset_list):
            dst_project_dataset = dstproject_and_dataset_list[itemnum]
            copy_driver = MultiBQSyncDriver((src_project_dataset.split('.')[0]), (src_project_dataset.split('.')[1]),
              (dst_project_dataset.split('.')[1]),
              dstproject=(dst_project_dataset.split('.')[0]),
              srcbucket=srcbucket,
              dstbucket=dstbucket,
              remove_deleted_tables=remove_deleted_tables,
              copy_data=copy_data,
              copy_views=copy_views,
              check_depth=(self._MultiBQSyncCoordinator__check_depth),
              coordinator=self)
            self._MultiBQSyncCoordinator__copy_drivers.append(copy_driver)

    @property
    def logger(self):
        return self._MultiBQSyncCoordinator__copy_drivers[0].logger

    @property
    def check_depth(self):
        self._MultiBQSyncCoordinator__check_depth

    @check_depth.setter
    def check_depth(self, value):
        self._MultiBQSyncCoordinator__check_depth = value
        for copy_driver in self._MultiBQSyncCoordinator__copy_drivers:
            copy_driver.check_depth = self._MultiBQSyncCoordinator__check_depth

    @logger.setter
    def logger(self, value):
        for copy_driver in self._MultiBQSyncCoordinator__copy_drivers:
            copy_driver.logger = value

    @property
    def tables_synced(self):
        total = 0
        for copy_driver in self._MultiBQSyncCoordinator__copy_drivers:
            total += copy_driver.tables_synced

        return total

    @property
    def views_synced(self):
        total = 0
        for copy_driver in self._MultiBQSyncCoordinator__copy_drivers:
            total += copy_driver.views_synced

        return total

    @property
    def rows_synced(self):
        total = 0
        for copy_driver in self._MultiBQSyncCoordinator__copy_drivers:
            total += copy_driver.rows_synced

        return total

    @property
    def rows_avoided(self):
        total = 0
        for copy_driver in self._MultiBQSyncCoordinator__copy_drivers:
            total += copy_driver.rows_avoided

        return total

    @property
    def views_failed_sync(self):
        total = 0
        for copy_driver in self._MultiBQSyncCoordinator__copy_drivers:
            total += copy_driver.views_failed_sync

        return total

    @property
    def tables_failed_sync(self):
        total = 0
        for copy_driver in self._MultiBQSyncCoordinator__copy_drivers:
            total += copy_driver.tables_failed_sync

        return total

    @property
    def tables_avoided(self):
        total = 0
        for copy_driver in self._MultiBQSyncCoordinator__copy_drivers:
            total += copy_driver.tables_avoided

        return total

    @property
    def view_avoided(self):
        total = 0
        for copy_driver in self._MultiBQSyncCoordinator__copy_drivers:
            total += copy_driver.view_avoided

        return total

    @property
    def extract_fails(self):
        total = 0
        for copy_driver in self._MultiBQSyncCoordinator__copy_drivers:
            total += copy_driver.extract_fails

        return total

    @property
    def load_fails(self):
        total = 0
        for copy_driver in self._MultiBQSyncCoordinator__copy_drivers:
            total += copy_driver.load_fails

        return total

    @property
    def copy_fails(self):
        total = 0
        for copy_driver in self._MultiBQSyncCoordinator__copy_drivers:
            total += copy_driver.copy_fails

        return total

    def sync(self):
        """
        Synchronise all the datasets in the driver
        :return:
        """
        for copy_driver in self._MultiBQSyncCoordinator__copy_drivers:
            sync_bq_datset(copy_driver)

    def update_source_view_definition(self, view_definition, use_standard_sql):
        for copy_driver in self._MultiBQSyncCoordinator__copy_drivers:
            view_definition = copy_driver.real_update_source_view_definition(view_definition, use_standard_sql)

        return view_definition


class MultiBQSyncDriver(DefaultBQSyncDriver):

    def __init__(self, srcproject, srcdataset, dstdataset, dstproject=None, srcbucket=None, dstbucket=None, remove_deleted_tables=True, copy_data=True, copy_views=True, check_depth=-1, coordinator=None):
        DefaultBQSyncDriver.__init__(self, srcproject, srcdataset, dstdataset, dstproject, srcbucket, dstbucket, remove_deleted_tables, copy_data, copy_views, check_depth)
        self._MultiBQSyncDriver__coordinater = coordinator

    @property
    def coordinater(self):
        return self._MultiBQSyncDriver__coordinater

    @coordinater.setter
    def coordinater(self, value):
        self._MultiBQSyncDriver__coordinater = value

    def real_update_source_view_definition(self, view_definition, use_standard_sql):
        view_definition = view_definition.replace('`{}.{}.'.format(self.source_project, self.source_dataset), '`{}.{}.'.format(self.destination_project, self.destination_dataset))
        view_definition = view_definition.replace('[{}:{}.'.format(self.source_project, self.source_dataset), '[{}:{}.'.format(self.destination_project, self.destination_dataset))
        view_definition = view_definition.replace('[{}.{}.'.format(self.source_project, self.source_dataset), '[{}:{}.'.format(self.destination_project, self.destination_dataset))
        return view_definition

    def update_source_view_definition(self, view_definition, use_standard_sql):
        return self.coordinater.update_source_view_definition(view_definition, use_standard_sql)


def create_and_copy_table(copy_driver, table_name):
    """
    Function to create table in destination dataset and copy all data
    Only called for brand new tables

    :param copy_driver: Has checked source dest all exist
    :param table_name: The table name we are copying from source
    :return: None
    """
    if not isinstance(copy_driver, DefaultBQSyncDriver):
        raise AssertionError('Copy driver has to be a subclass of DefaultCopy Driver')
    else:
        dst_dataset_impl = copy_driver.destination_dataset_impl
        srctable_ref = copy_driver.source_client.dataset(copy_driver.source_dataset).table(table_name)
        srctable = copy_driver.source_client.get_table(srctable_ref)
        NEW_SCHEMA = list(srctable.schema)
        destination_table_ref = copy_driver.destination_client.dataset(copy_driver.destination_dataset).table(table_name)
        destination_table = bigquery.Table(destination_table_ref, schema=NEW_SCHEMA)
        destination_table.description = srctable.description
        destination_table.friendly_name = srctable.friendly_name
        destination_table.labels = srctable.labels
        destination_table.partitioning_type = srctable.partitioning_type
        if srctable.partition_expiration is not None:
            destination_table.partition_expiration = srctable.partition_expiration
        destination_table.expires = srctable.expires
        if getattr(srctable, 'require_partition_filter', None):
            destination_table.require_partition_filter = srctable.require_partition_filter
        if getattr(srctable, 'range_partitioning', None):
            destination_table.range_partitioning = srctable.range_partitioning
        if getattr(srctable, 'time_partitioning', None):
            destination_table.time_partitioning = srctable.time_partitioning
        if getattr(srctable, 'clustering_fields', None):
            destination_table.clustering_fields = srctable.clustering_fields
        encryption_config = srctable.encryption_configuration
        if encryption_config is not None:
            if copy_driver.same_region or encryption_config.kms_key_name.find('/locations/global/') != -1:
                destination_table.encryption_config = encryption_config
            else:
                parts = encryption_config.kms_key_name.split('/')
                parts[3] = MAPBQREGION2KMSREGION.get(dst_dataset_impl.location, dst_dataset_impl.location.lower())
                destination_table.encryption_config = '/'.join(parts)
        try:
            copy_driver.destination_client.create_table(destination_table)
        except Exception:
            copy_driver.increment_tables_failed_sync()
            raise

        copy_driver.get_logger().info('Created table {}.{}.{}'.format(copy_driver.destination_project, copy_driver.destination_dataset, table_name))
        if srctable.num_rows != 0:
            copy_driver.add_bytes_synced(srctable.num_bytes)
            copy_driver.add_rows_synced(srctable.num_rows)
            copy_driver.copy_q.put((-1 * srctable.num_rows,
             (copy_table_data,
              [
               copy_driver, table_name, srctable.partitioning_type, 0,
               srctable.num_rows])))


def compare_schema_patch_ifneeded(copy_driver, table_name):
    """
    Compares schemas and patches if needed and copies data
    :param copy_driver:
    :param table_name:
    :return:
    """
    srctable_ref = copy_driver.source_client.dataset(copy_driver.source_dataset).table(table_name)
    srctable = copy_driver.source_client.get_table(srctable_ref)
    dsttable_ref = copy_driver.destination_client.dataset(copy_driver.destination_dataset).table(table_name)
    dsttable = copy_driver.source_client.get_table(dsttable_ref)
    NEW_SCHEMA = list(srctable.schema)
    OLD_SCHEMA = list(dsttable.schema)
    fields = []
    if dsttable.description != srctable.description:
        dsttable.description = srctable.description
        fields.append('description')
    if dsttable.friendly_name != srctable.friendly_name:
        dsttable.friendly_name = srctable.friendly_name
        fields.append('friendly_name')
    if dsttable.labels != srctable.labels:
        dsttable.labels = srctable.labels
        fields.append('labels')
    if dsttable.partition_expiration != srctable.partition_expiration:
        dsttable.partition_expiration = srctable.partition_expiration
        fields.append('partition_expiration')
    if dsttable.expires != srctable.expires:
        dsttable.expires = srctable.expires
        fields.append('expires')
    else:

        def compare_and_merge_schema_fields(input):
            working_schema = []
            changes = 0
            field_names_found = {}
            for schema_item in input['oldchema']:
                match = False
                for tgt_schema_item in input['newschema']:
                    if tgt_schema_item.name == schema_item.name:
                        field_names_found[schema_item.name] = True
                        match = True
                        if tgt_schema_item.field_type != schema_item.field_type:
                            changes += 1
                            input['workingchema'] = working_schema
                            input['changes'] = changes
                            input['deleteandrecreate'] = True
                            return input
                        if tgt_schema_item.description != schema_item.description:
                            changes += 1
                        if tgt_schema_item.field_type != 'RECORD':
                            working_schema.append(tgt_schema_item)
                        else:
                            if tgt_schema_item.mode != schema_item.mode:
                                changes += 1
                                input['workingchema'] = working_schema
                                input['changes'] = changes
                                input['deleteandrecreate'] = True
                                return input
                            else:
                                output = compare_and_merge_schema_fields({'oldchema':list(schema_item.fields), 
                                 'newschema':list(tgt_schema_item.fields)})
                                changes += output['changes']
                                if output['changes'] > 0:
                                    newfields = []
                                    for schema_item in output['workingchema']:
                                        newfields.append(schema_item.to_api_repr())

                                    tmp_work = tgt_schema_item.to_api_repr()
                                    tmp_work['fields'] = newfields
                                    working_schema.append(bigquery.SchemaField.from_api_repr(tmp_work))
                                else:
                                    working_schema.append(tgt_schema_item)
                            if 'deleteandrecreate' in output:
                                if output['deleteandrecreate']:
                                    input['deleteandrecreate'] = output['deleteandrecreate']
                                    return input
                            break

            if not match:
                working_schema.append(schema_item)
            for tgt_schema_item in input['newschema']:
                if tgt_schema_item.name not in field_names_found:
                    working_schema.append(tgt_schema_item)
                    changes += 1

            if len(working_schema) < len(input['newschema']):
                pass
            input['workingchema'] = working_schema
            input['changes'] = changes
            return input

        output = compare_and_merge_schema_fields({'oldchema':OLD_SCHEMA,  'newschema':NEW_SCHEMA})
        if 'deleteandrecreate' in output:
            remove_deleted_destination_table(copy_driver, table_name)
            create_and_copy_table(copy_driver, table_name)
        elif output['changes'] > 0:
            dsttable.schema = output['workingchema']
            fields.append('schema')
        else:
            if len(fields) > 0:
                try:
                    copy_driver.destination_client.update_table(dsttable, fields)
                except Exception:
                    copy_driver.increment_tables_failed_sync()
                    raise

                dsttable = copy_driver.source_client.get_table(dsttable_ref)
                copy_driver.get_logger().info('Patched table {}.{}.{} {}'.format(copy_driver.destination_project, copy_driver.destination_dataset, table_name, ','.join(fields)))
            else:
                copy_driver.increment_tables_avoided()
            copy_driver.add_bytes_synced(srctable.num_bytes)
            copy_driver.add_rows_synced(srctable.num_rows)
            if dsttable.num_rows != srctable.num_rows or dsttable.num_bytes != srctable.num_bytes or srctable.modified >= dsttable.modified or copy_driver.table_data_change(srctable, dsttable):
                copy_driver.copy_q.put((-1 * srctable.num_rows,
                 (copy_table_data,
                  [
                   copy_driver, table_name, srctable.partitioning_type,
                   dsttable.num_rows, srctable.num_rows])))
            else:
                copy_driver.add_bytes_avoided(srctable.num_bytes)
                copy_driver.add_rows_avoided(srctable.num_rows)


def remove_deleted_destination_table(copy_driver, table_name):
    """
    Removes tables/views deleted on source dataset but that exist on destination dataset
    :param copy_driver:
    :param table_name:
    :return:
    """
    if copy_driver.remove_deleted_tables:
        table_ref = copy_driver.destination_dataset_impl.table(table_name)
        table = copy_driver.destination_client.get_table(table_ref)
        copy_driver.destination_client.delete_table(table)
        copy_driver.get_logger().info('Deleted table/view {}.{}.{}'.format(copy_driver.destination_project, copy_driver.destination_dataset, table_name))


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def copy_table_data(copy_driver, table_name, partitioning_type, dst_rows, src_rows):
    """
    Function copies data assumes schemas are identical
    :param copy_driver:
    :param table_name:
    :return:
    """
    if not copy_driver.copy_data:
        return
    else:
        src_query = None
        dst_query = None
        if partitioning_type == 'DAY':
            bqclient = copy_driver.source_client
            srctable_ref = bqclient.dataset(copy_driver.source_dataset).table(table_name)
            srctable = bqclient.get_table(srctable_ref)
            extrafields = copy_driver.extra_dp_compare_functions(srctable)
            src_query = TCMPDAYPARTITION.format(project=(copy_driver.source_project), dataset=(copy_driver.source_dataset),
              extrafunctions=extrafields,
              table_name=table_name)
            dst_query = TCMPDAYPARTITION.format(project=(copy_driver.destination_project), dataset=(copy_driver.destination_dataset),
              extrafunctions=extrafields,
              table_name=table_name)
        if copy_driver.same_region:
            jobs = []
            if partitioning_type != 'DAY' or dst_rows == 0 or src_rows <= 5000:
                jobs.append(in_region_copy(copy_driver, table_name))
            else:
                source_ended = False
                destination_ended = False
                source_generator = run_query((copy_driver.source_client), src_query, (copy_driver.get_logger()),
                  'List source data per partition',
                  location=(copy_driver.source_location))
                try:
                    source_row = next(source_generator)
                except StopIteration:
                    source_ended = True

                destination_generator = run_query((copy_driver.destination_client), dst_query, (copy_driver.get_logger()),
                  'List destination data per partition',
                  location=(copy_driver.destination_location))
                try:
                    destination_row = next(destination_generator)
                except StopIteration:
                    destination_ended = True

                while not source_ended or not destination_ended:
                    if not destination_ended and not source_ended and destination_row['partitionName'] == source_row['partitionName']:
                        diff = False
                        rowdict = dict(list(source_row.items()))
                        for key in rowdict:
                            if source_row[key] != destination_row[key] and (not isinstance(source_row[key], float) or not isclose(source_row[key], destination_row[key])):
                                diff = True
                                break

                        if diff:
                            jobs.append(in_region_copy(copy_driver, '{}${}'.format(table_name, source_row['partitionName'])))
                        try:
                            source_row = next(source_generator)
                        except StopIteration:
                            source_ended = True

                        try:
                            destination_row = next(destination_generator)
                        except StopIteration:
                            destination_ended = True

                    else:
                        if destination_ended or source_row['partitionName'] < destination_row['partitionName']:
                            jobs.append(in_region_copy(copy_driver, '{}${}'.format(table_name, source_row['partitionName'])))
                            try:
                                source_row = next(source_generator)
                            except StopIteration:
                                source_ended = True

                    if source_ended or source_row['partitionName'] > destination_row['partitionName']:
                        remove_deleted_destination_table(copy_driver, '{}${}'.format(table_name, destination_row['partitionName']))
                        try:
                            destination_row = next(destination_generator)
                        except StopIteration:
                            destination_ended = True

            def copy_complete_callback(job):
                if job.error_result is not None:
                    copy_driver.increment_copy_fails()

            callbacks = {}
            for job in jobs:
                callbacks[job.job_id] = copy_complete_callback

            wait_for_jobs(jobs, (copy_driver.logger), desc='Wait for copy jobs', call_back_on_complete=callbacks)
        else:
            if partitioning_type != 'DAY':
                cross_region_copy(copy_driver, table_name)
            else:
                source_ended = False
                destination_ended = False
                source_generator = run_query((copy_driver.source_client), src_query, (copy_driver.get_logger()),
                  'List source data per partition',
                  location=(copy_driver.source_location))
                try:
                    source_row = next(source_generator)
                except StopIteration:
                    source_ended = True

                destination_generator = run_query((copy_driver.destination_client), dst_query, (copy_driver.get_logger()),
                  'List destination data per partition',
                  location=(copy_driver.destination_location))
                try:
                    destination_row = next(destination_generator)
                except StopIteration:
                    destination_ended = True

                while not source_ended or not destination_ended:
                    if not destination_ended and not source_ended and destination_row['partitionName'] == source_row['partitionName']:
                        diff = False
                        rowdict = dict(list(source_row.items()))
                        for key in rowdict:
                            if source_row[key] != destination_row[key] and (not isinstance(source_row[key], float) or not isclose(source_row[key], destination_row[key])):
                                diff = True
                                break

                        if diff:
                            copy_driver.copy_q.put((-1 * source_row['rowNum'],
                             (cross_region_copy,
                              [
                               copy_driver,
                               '{}${}'.format(table_name, source_row['partitionName'])])))
                        else:
                            copy_driver.add_rows_avoided(source_row['rowNum'])
                        try:
                            source_row = next(source_generator)
                        except StopIteration:
                            source_ended = True

                        try:
                            destination_row = next(destination_generator)
                        except StopIteration:
                            destination_ended = True

                    else:
                        if destination_ended or source_row['partitionName'] < destination_row['partitionName']:
                            copy_driver.copy_q.put((-1 * source_row['rowNum'],
                             (cross_region_copy,
                              [
                               copy_driver,
                               '{}${}'.format(table_name, source_row['partitionName'])])))
                            try:
                                source_row = next(source_generator)
                            except StopIteration:
                                source_ended = True

                    if source_ended or source_row['partitionName'] > destination_row['partitionName']:
                        remove_deleted_destination_table(copy_driver, '{}${}'.format(table_name, destination_row['partitionName']))
                        try:
                            destination_row = next(destination_generator)
                        except StopIteration:
                            destination_ended = True


def cross_region_copy(copy_driver, table_name):
    """
    Copy data acoss region each table is
    Extracted out to avro file to cloud storage src
    Data is loaded into new dataset
    Deleted from destination
    :param copy_driver:
    :param table_name:
    :return:
    """
    bqclient = copy_driver.source_client
    blobname = '{}-{}-{}-{}-{}*.avro'.format(table_name, copy_driver.source_project, copy_driver.source_dataset, copy_driver.destination_project, copy_driver.destination_dataset)
    src_uri = 'gs://{}/{}'.format(copy_driver.source_bucket, blobname)
    srctable = bqclient.dataset(copy_driver.source_dataset).table(table_name)
    job_config = bigquery.ExtractJobConfig()
    job_config.destination_format = bigquery.job.DestinationFormat.AVRO
    job_config.compression = bigquery.job.Compression.DEFLATE
    job = bqclient.extract_table(srctable, [src_uri], job_config=job_config, location=(copy_driver.source_location))

    def cross_region_rewrite(job):
        if job.error_result:
            copy_driver.increment_extract_fails()
        else:
            blob_uris = int(job._job_statistics().get('destinationUriFileCounts')[0])
            client = storage.Client(project=(copy_driver.source_project))
            src_bucket = client.get_bucket(copy_driver.source_bucket)
            dst_bucket = client.get_bucket(copy_driver.destination_bucket)
            for blob_num in range(blob_uris):
                ablobname = blobname.replace('*', '{:012d}'.format(blob_num))
                src_blob = storage.blob.Blob(ablobname, src_bucket)
                dst_blob = storage.blob.Blob(ablobname, dst_bucket)
                token, bytes_rewritten, total_bytes = dst_blob.rewrite(src_blob)
                while token is not None:
                    token, bytes_rewritten, total_bytes = dst_blob.rewrite(src_blob, token=token)

                src_blob.delete()

            dst_uri = 'gs://{}/{}'.format(copy_driver.destination_bucket, blobname)
            bqclient = copy_driver.destination_client
            dsttable = bqclient.dataset(copy_driver.destination_dataset).table(table_name)
            job_config = bigquery.LoadJobConfig()
            job_config.source_format = bigquery.job.SourceFormat.AVRO
            job_config.compression = bigquery.job.Compression.DEFLATE
            job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
            job = bqclient.load_table_from_uri([dst_uri], dsttable, job_config=job_config, location=(copy_driver.destination_location))

        def delete_blob(job):
            if job.error_result:
                copy_driver.increment_load_fails()
            else:
                client = storage.Client(project=(copy_driver.source_project))
                dst_bucket = client.get_bucket(copy_driver.destination_bucket)
                for blob_num in range(blob_uris):
                    ablobname = blobname.replace('*', '{:012d}'.format(blob_num))
                    dst_blob = storage.blob.Blob(ablobname, dst_bucket)
                    dst_blob.delete()

        callbackobj = {job.job_id: delete_blob}
        wait_for_jobs([job], (copy_driver.get_logger()), desc=('Wait for load job for table {}'.format(table_name)),
          call_back_on_complete=callbackobj)

    callbackobj = {job.job_id: cross_region_rewrite}
    wait_for_jobs([job], (copy_driver.get_logger()), desc=('Wait for extract job for table {}'.format(table_name)), call_back_on_complete=callbackobj)


def in_region_copy(copy_driver, table_name):
    bqclient = copy_driver.source_client
    srctable = bqclient.dataset(copy_driver.source_dataset).table(table_name)
    dsttable = bqclient.dataset(copy_driver.destination_dataset).table(table_name)
    job_config = bigquery.CopyJobConfig()
    job_config.write_disposition = 'WRITE_TRUNCATE'
    job_config.create_disposition = 'CREATE_IF_NEEDED'
    job = bqclient.copy_table(srctable,
      dsttable, job_config=job_config)
    return job


def sync_bq_processor(stop_event, copy_driver, q):
    """
    Main background thread driver loop for copying
    :param copy_driver: Basis of copy
    :param q: The work queue tasks are put in
    :return: None
    """
    if not isinstance(copy_driver, DefaultBQSyncDriver):
        raise AssertionError('Copy driver has to be a subclass of DefaultCopy Driver')
    elif not isinstance(q, queue.Queue):
        raise AssertionError('Must be passed a queue for background thread Driver')
    while not stop_event.isSet():
        try:
            _, task = q.get(timeout=1)
            if task is None:
                continue
            function, args = task
            (copy_driver.fault_barrier)(function, *args)
            q.task_done()
        except queue.Empty:
            pass


def wait_for_jobs(jobs, logger, desc='', sleepTime=0.1, call_back_on_complete=None):
    """
    Wait for a list of big query jobs to complete
    :param jobs: The array of jobs to wait for
    :param desc: A descriptive text of jobs waiting for
    :param sleepTime: How long to sleep between checks of jobs
    :param logger: A logger to use for output
    :return:
    """
    while len(jobs) > 0:
        didnothing = True
        for job in jobs:
            if job is not None:
                if job.done():
                    didnothing = False
                    if job.error_result:
                        logger.error('{}:Error BQ {} Job {} error {}'.format(desc, job.job_type, job.job_id, str(job.error_result)))
                    else:
                        if job.job_type == 'load':
                            if job.output_rows is not None:
                                logger.info('{}:BQ {} Job completed:{} rows {}ed {:,d}'.format(desc, job.job_type, job.job_id, job.job_type, job.output_rows))
                    if call_back_on_complete is not None and job.job_id in call_back_on_complete:
                        call_back_on_complete[job.job_id](job)
            else:
                didnothing = False
                logger.debug('{}:BQ {} Job completed:{}'.format(desc, job.job_type, job.job_id))

        if didnothing:
            sleep(sleepTime)
        else:
            jobs = [x for x in jobs if x.job_id is not None if not x.state == 'DONE']


def wait_for_queue(q, desc=None, sleepTime=0.1, logger=None):
    """
    Wit for background queue to finish
    :param q: The q to wiat for
    :return:
    """
    while q.qsize() > 0:
        qsize = q.qsize()
        if qsize > 0:
            if logger is None:
                if desc is None:
                    logger.info('Waiting for {} tasks {} to start'.format(qsize, desc))
            sleep(sleepTime)

    if logger is None:
        if desc is None:
            logger.info('Waiting for tasks {} to complete'.format(qsize, desc))
    q.join()
    if logger is None:
        if desc is None:
            logger.info('All tasks {} now complete'.format(qsize, desc))


def create_destination_view(copy_driver, table_name, view_input):
    """
    Create a view assuming it does not exist
    If error happens on creation logs but swallows error on
    basis order application is not perfect
    :param copy_driver:
    :param table_name: name of the view
    :param view_input: A dictionary of form {
        "use_standard_sql":bool,
        "view_definition":sql}
    :return:
    """
    srctable_ref = copy_driver.source_client.dataset(copy_driver.source_dataset).table(table_name)
    srctable = copy_driver.source_client.get_table(srctable_ref)
    use_legacy_sql = True
    if view_input['use_standard_sql'] == 'YES':
        use_legacy_sql = False
    destination_table_ref = copy_driver.destination_client.dataset(copy_driver.destination_dataset).table(table_name)
    destination_table = bigquery.Table(destination_table_ref)
    destination_table.description = srctable.description
    destination_table.friendly_name = srctable.friendly_name
    destination_table.labels = srctable.labels
    destination_table.view_use_legacy_sql = use_legacy_sql
    destination_table.view_query = view_input['view_definition']
    try:
        copy_driver.destination_client.create_table(destination_table)
        copy_driver.get_logger().info('Created view {}.{}.{}'.format(copy_driver.destination_project, copy_driver.destination_dataset, table_name))
    except exceptions.PreconditionFailed as e:
        copy_driver.increment_views_failed_sync()
        copy_driver.get_logger().exception('Pre conditionfailed creating view {}:{}'.format(table_name, view_input['view_definition']))
    except exceptions.BadRequest as e:
        copy_driver.increment_views_failed_sync()
        copy_driver.get_logger().exception('Bad request creating view {}:{}'.format(table_name, view_input['view_definition']))
    except exceptions.NotFound as e:
        copy_driver.increment_views_failed_sync()
        copy_driver.get_logger().exception('Not Found creating view {}:{}'.format(table_name, view_input['view_definition']))


def patch_destination_view(copy_driver, table_name, view_input):
    """
    Patch a view assuming it does  exist
    If error happens on creation logs but swallows error on
    basis order application is not perfect
    :param copy_driver:
    :param table_name: name of the view
    :param view_input: A dictionary of form {
        "use_standard_sql":bool,
        "view_definition":sql}
    :return:
    """
    srctable_ref = copy_driver.source_client.dataset(copy_driver.source_dataset).table(table_name)
    srctable = copy_driver.source_client.get_table(srctable_ref)
    dsttable_ref = copy_driver.destination_client.dataset(copy_driver.destination_dataset).table(table_name)
    dsttable = copy_driver.source_client.get_table(dsttable_ref)
    use_legacy_sql = True
    if view_input['use_standard_sql'] == 'YES':
        use_legacy_sql = False
    fields = []
    if dsttable.description != srctable.description:
        dsttable.description = srctable.description
        fields.append('description')
    if dsttable.friendly_name != srctable.friendly_name:
        dsttable.friendly_name = srctable.friendly_name
        fields.append('friendly_name')
    if dsttable.labels != srctable.labels:
        dsttable.labels = srctable.labels
        fields.append('labels')
    if dsttable.view_use_legacy_sql != use_legacy_sql:
        dsttable.view_use_legacy_sql = use_legacy_sql
        fields.append('use_legacy_sql')
    if dsttable.view_query != view_input['view_definition']:
        dsttable.view_query = view_input['view_definition']
        fields.append('view_query')
    try:
        if len(fields) > 0:
            copy_driver.destination_client.update_table(dsttable, fields)
            copy_driver.get_logger().info('Patched view {}'.format(table_name))
        else:
            copy_driver.increment_view_avoided()
    except exceptions.PreconditionFailed as e:
        copy_driver.increment_views_failed_sync()
        copy_driver.get_logger().exception('Pre conditionfailed patching view {}'.format(table_name))
    except exceptions.BadRequest as e:
        copy_driver.increment_views_failed_sync()
        copy_driver.get_logger().exception('Bad request patching view {}'.format(table_name))
    except exceptions.NotFound as e:
        copy_driver.increment_views_failed_sync()
        copy_driver.get_logger().exception('Not Found patching view {}'.format(table_name))


def sync_bq_datset(copy_driver, schema_threads=10, copy_data_threads=50):
    """
    Function to use copy driver  to copy tables from 1 dataset to another
    :param copy_driver:
    :return: Nothing
    """
    if not isinstance(copy_driver, DefaultBQSyncDriver):
        raise AssertionError('Copy driver has to be a subclass of DefaultCopy Driver')
    else:
        schema_q = queue.PriorityQueue()
        copy_driver.schema_q = schema_q
        thread_list = []
        stop_event = threading.Event()
        for i in range(schema_threads):
            t = threading.Thread(target=sync_bq_processor, name='copyschemabackgroundthread', args=[
             stop_event, copy_driver, schema_q])
            t.daemon = True
            t.start()
            thread_list.append(t)

        copy_q = queue.PriorityQueue()
        copy_driver.copy_q = copy_q
        for i in range(copy_data_threads):
            t = threading.Thread(target=sync_bq_processor, name='copydatabackgroundthread', args=[
             stop_event, copy_driver, copy_q])
            t.daemon = True
            t.start()
            thread_list.append(t)

        source_query = DSTABLELISTQUERY.format(copy_driver.source_dataset)
        destination_query = DSTABLELISTQUERY.format(copy_driver.destination_dataset)
        source_ended = False
        destination_ended = False
        source_generator = run_query((copy_driver.source_client), source_query, 'List source tables', (copy_driver.get_logger()), location=(copy_driver.source_location))
        try:
            source_row = next(source_generator)
        except StopIteration:
            source_ended = True

        destination_generator = run_query((copy_driver.destination_client), destination_query, (copy_driver.get_logger()), 'List destination tables',
          location=(copy_driver.destination_location))
        try:
            destination_row = next(destination_generator)
        except StopIteration:
            destination_ended = True

        while not source_ended or not destination_ended:
            if not destination_ended and not source_ended and destination_row['table_name'] == source_row['table_name']:
                copy_driver.increment_tables_synced()
                schema_q.put((0, (compare_schema_patch_ifneeded, [copy_driver, source_row['table_name']])))
                try:
                    source_row = next(source_generator)
                except StopIteration:
                    source_ended = True

                try:
                    destination_row = next(destination_generator)
                except StopIteration:
                    destination_ended = True

            else:
                if destination_ended or source_row['table_name'] < destination_row['table_name']:
                    schema_q.put((0, (create_and_copy_table, [copy_driver, source_row['table_name']])))
                    try:
                        source_row = next(source_generator)
                    except StopIteration:
                        source_ended = True

            if source_ended or source_row['table_name'] > destination_row['table_name']:
                copy_driver.increment_tables_synced()
                schema_q.put((0,
                 (
                  remove_deleted_destination_table, [copy_driver, destination_row['table_name']])))
                try:
                    destination_row = next(destination_generator)
                except StopIteration:
                    destination_ended = True

        wait_for_queue(schema_q, 'Table schemas sychronization', 0.1, copy_driver.get_logger())
        if copy_driver.copy_views:
            view_order = []
            views_to_apply = {}
            view_order_query = DSVIEWORDER.format(copy_driver.source_dataset)
            for viewrow in run_query((copy_driver.source_client), view_order_query, (copy_driver.get_logger()),
              'List views in apply order',
              location=(copy_driver.source_location)):
                view_order.append(viewrow['table_name'])

            source_view_query = DSVIEWLISTQUERY.format(copy_driver.source_dataset)
            destination_view_query = DSVIEWLISTQUERY.format(copy_driver.destination_dataset)
            source_ended = False
            destination_ended = False
            source_generator = run_query((copy_driver.source_client), source_view_query, 'List source views',
              (copy_driver.get_logger()), location=(copy_driver.source_location))
            try:
                source_row = next(source_generator)
            except StopIteration:
                source_ended = True

            destination_generator = run_query((copy_driver.destination_client), destination_view_query, (copy_driver.get_logger()),
              'List destination views',
              location=(copy_driver.destination_location))
            try:
                destination_row = next(destination_generator)
            except StopIteration:
                destination_ended = True

            while not source_ended or not destination_ended:
                if not destination_ended and not source_ended and destination_row['table_name'] == source_row['table_name']:
                    copy_driver.increment_views_synced()
                    expected_definition = copy_driver.update_source_view_definition(source_row['view_definition'], source_row['use_standard_sql'])
                    if expected_definition != destination_row['view_definition']:
                        views_to_apply[source_row['table_name']] = {'use_standard_sql':source_row['use_standard_sql'],  'view_definition':expected_definition, 
                         'action':'patch_view'}
                    else:
                        copy_driver.increment_view_avoided()
                    try:
                        source_row = next(source_generator)
                    except StopIteration:
                        source_ended = True

                    try:
                        destination_row = next(destination_generator)
                    except StopIteration:
                        destination_ended = True

                else:
                    if destination_ended or source_row['table_name'] < destination_row['table_name']:
                        copy_driver.increment_views_synced()
                        expected_definition = copy_driver.update_source_view_definition(source_row['view_definition'], source_row['use_standard_sql'])
                        views_to_apply[source_row['table_name']] = {'use_standard_sql':source_row['use_standard_sql'], 
                         'view_definition':expected_definition, 
                         'action':'create_view'}
                        try:
                            source_row = next(source_generator)
                        except StopIteration:
                            source_ended = True

                if source_ended or source_row['table_name'] > destination_row['table_name']:
                    schema_q.put((0,
                     (
                      remove_deleted_destination_table,
                      [
                       copy_driver, destination_row['table_name']])))
                    try:
                        destination_row = next(destination_generator)
                    except StopIteration:
                        destination_ended = True

            for view in view_order:
                if view in views_to_apply:
                    if views_to_apply[view]['action'] == 'create_view':
                        create_destination_view(copy_driver, view, views_to_apply[view])
                    else:
                        patch_destination_view(copy_driver, view, views_to_apply[view])

            wait_for_queue(schema_q, 'View schemas sychronization', 0.1, copy_driver.get_logger())
        wait_for_queue(copy_q, 'Table copying', 0.1, copy_driver.get_logger())
        stop_event.set()
        copy_driver.schema_q = None
        copy_driver.copy_q = None
        if len(copy_driver.jobs) > 0:
            wait_for_jobs((copy_driver.jobs), (copy_driver.get_logger()),
              desc='Table copying',
              sleepTime=0.1)