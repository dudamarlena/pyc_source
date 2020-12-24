# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/victorng/.virtualenvs/taar/lib/python3.5/site-packages/taar_loader/filters.py
# Compiled at: 2018-02-01 11:30:18
# Size of source mod 2**32: 2153 bytes
import boto3

def filterDateAndClientID(row_jstr):
    row, jstr = row_jstr
    import dateutil.parser
    try:
        assert row.client_id is not None
        dateutil.parser.parse(row.subsession_start_date)
        return True
    except Exception:
        return False


def list_transformer(row_jsonstr):
    row, json_str = row_jsonstr
    import json, dateutil.parser
    client_id = row.client_id
    start_date = dateutil.parser.parse(row.subsession_start_date)
    start_date = start_date.date()
    start_date = start_date.strftime('%Y%m%d')
    jdata = json.loads(json_str)
    jdata['client_id'] = client_id
    jdata['start_date'] = start_date
    return (
     0, 1, [jdata])


def push_to_dynamo(item_list):
    """
    This connects to DynamoDB and pushes records in `item_list` into
    a table.
    """
    conn = boto3.resource('dynamodb', region_name='us-west-2')
    table = conn.Table('taar_addon_data')
    with table.batch_writer(overwrite_by_pkeys=['client_id']) as (batch):
        for item in item_list:
            batch.put_item(Item=item)


def dynamo_reducer(list_a, list_b):
    if list_a[1] == 0:
        return list_b
    if list_b[1] == 0:
        return list_a
    new_list = [list_a[0] + list_b[0],
     list_a[1] + list_b[1],
     list_a[2] + list_b[2]]
    if new_list[1] > 100:
        push_to_dynamo(new_list[2])
        new_list[0] += new_list[1]
        new_list[1] = 0
        new_list[2] = []
    return tuple(new_list)