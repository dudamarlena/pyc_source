# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/victorng/.virtualenvs/taar/lib/python3.5/site-packages/taar_loader/taar_dynamo.py
# Compiled at: 2018-02-01 13:12:34
# Size of source mod 2**32: 4900 bytes
"""
This module replicates the scala script over at

https://github.com/mozilla/telemetry-batch-view/blob/1c544f65ad2852703883fe31a9fba38c39e75698/src/main/scala/com/mozilla/telemetry/views/HBaseAddonRecommenderView.scala
"""
from pyspark.sql.functions import desc, row_number
from pyspark.sql import Window
from taar_loader.filters import filterDateAndClientID
from taar_loader.filters import list_transformer

def etl(spark, run_date, dataFrameFunc):
    currentDate = run_date
    currentDateString = currentDate.strftime('%Y%m%d')
    print('Processing %s' % currentDateString)
    tmp = dataFrameFunc(currentDateString)
    datasetForDate = tmp.sample(False, 1e-08)
    print('Dataset is sampled!')
    clientShortList = datasetForDate.select('client_id', 'subsession_start_date', row_number().over(Window.partitionBy('client_id').orderBy(desc('subsession_start_date'))).alias('clientid_rank'))
    clientShortList = clientShortList.where('clientid_rank == 1').drop('clientid_rank')
    select_fields = [
     'client_id',
     'subsession_start_date',
     'subsession_length',
     'city',
     'locale',
     'os',
     'places_bookmarks_count',
     'scalar_parent_browser_engagement_tab_open_event_count',
     'scalar_parent_browser_engagement_total_uri_count',
     'scalar_parent_browser_engagement_unique_domains_count',
     'active_addons',
     'disabled_addons_ids']
    dataSubset = datasetForDate.select(*select_fields)
    clientsData = dataSubset.join(clientShortList, [
     'client_id',
     'subsession_start_date'])
    subset = clientsData.select('client_id', 'subsession_start_date')
    jsonDataRDD = clientsData.select('city', 'subsession_start_date', 'subsession_length', 'locale', 'os', 'places_bookmarks_count', 'scalar_parent_browser_engagement_tab_open_event_count', 'scalar_parent_browser_engagement_total_uri_count', 'scalar_parent_browser_engagement_unique_domains_count', 'active_addons', 'disabled_addons_ids').toJSON()
    rdd = subset.rdd.zip(jsonDataRDD)
    filtered_rdd = rdd.filter(filterDateAndClientID)
    merged_filtered_rdd = filtered_rdd.map(list_transformer)
    return merged_filtered_rdd


def main(spark, run_date):
    template = 's3://telemetry-parquet/main_summary/v4/submission_date_s3=%s'

    def load_parquet(dateString):
        return spark.read.parquet(template % dateString)

    rdd = etl(spark, run_date, load_parquet)
    return rdd


def reducer(tuple_a, tuple_b):
    import boto3
    if tuple_a[1] == 0:
        return tuple_b
    if tuple_b[1] == 0:
        return tuple_a
    elem0 = tuple_a[0] + tuple_b[0]
    elem1 = tuple_a[1] + tuple_b[1]
    elem2 = tuple_a[2] + tuple_b[2]
    tuple_data = [
     elem0, elem1, elem2]
    if elem1 >= 3:
        DYNAMO_CONN = boto3.resource('dynamodb', region_name='us-west-2')
        DYNAMO_TABLE = DYNAMO_CONN.Table('taar_addon_data')
        with DYNAMO_TABLE.batch_writer(overwrite_by_pkeys=['client_id']) as (batch):
            for jdata in tuple_data[2]:
                batch.put_item(Item=jdata)

            tuple_data[0] += tuple_data[1]
            tuple_data[1] = 0
        tuple_data = tuple(tuple_data)
    return tuple_data