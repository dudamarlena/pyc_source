# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/crcli/scripts/dump.py
# Compiled at: 2016-02-19 20:37:08
import click, json, boto3, gzip, xmltodict
client = boto3.client('dynamodb')

@click.command(short_help='Download a database into a gzipped file')
@click.argument('table', default='-', required=True)
@click.argument('filepath', default='dump.gz', required=False)
@click.option('--xml', default=False, help='download as xml')
@click.pass_context
def dump(ctx, table, filepath):
    """This command dumps the contents of a dynamodb table into a gzipped file.

    To get the dump of the game-test table, do:

        $ cr dump 'game-test' ./path/to/dump.gz

    To get the dump of the pad-test table in xml, do:

        $ cr dump 'pad-test' ./path/to/dump.gz --xml
    """
    items = []
    response = client.scan(TableName=table)
    items += response.get('Items')
    while response.has_key('LastEvaluatedKey'):
        response = client.scan(TableName=table, ExclusiveStartKey=response.get('LastEvaluatedKey'))
        items += response.get('Items')

    itemstring = xmltodict.unparse(items)
    with gzip.open(filepath, 'wb') as (f_out):
        f_out.write(itemstring)
        f_out.close()