# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_twitter_dag.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 7310 bytes
import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.hive_operator import HiveOperator
from datetime import date, timedelta

def fetchtweets():
    pass


def cleantweets():
    pass


def analyzetweets():
    pass


def transfertodb():
    pass


default_args = {'owner':'Ekhtiar', 
 'depends_on_past':False, 
 'start_date':airflow.utils.dates.days_ago(5), 
 'email':[
  'airflow@example.com'], 
 'email_on_failure':False, 
 'email_on_retry':False, 
 'retries':1, 
 'retry_delay':timedelta(minutes=5)}
dag = DAG('example_twitter_dag',
  default_args=default_args, schedule_interval='@daily')
fetch_tweets = PythonOperator(task_id='fetch_tweets',
  python_callable=fetchtweets,
  dag=dag)
clean_tweets = PythonOperator(task_id='clean_tweets',
  python_callable=cleantweets,
  dag=dag)
clean_tweets.set_upstream(fetch_tweets)
analyze_tweets = PythonOperator(task_id='analyze_tweets',
  python_callable=analyzetweets,
  dag=dag)
analyze_tweets.set_upstream(clean_tweets)
hive_to_mysql = PythonOperator(task_id='hive_to_mysql',
  python_callable=transfertodb,
  dag=dag)
from_channels = [
 'fromTwitter_A', 'fromTwitter_B', 'fromTwitter_C', 'fromTwitter_D']
to_channels = ['toTwitter_A', 'toTwitter_B', 'toTwitter_C', 'toTwitter_D']
yesterday = date.today() - timedelta(days=1)
dt = yesterday.strftime('%Y-%m-%d')
local_dir = '/tmp/'
hdfs_dir = ' /tmp/'
for channel in to_channels:
    file_name = 'to_' + channel + '_' + yesterday.strftime('%Y-%m-%d') + '.csv'
    load_to_hdfs = BashOperator(task_id=('put_' + channel + '_to_hdfs'),
      bash_command=('HADOOP_USER_NAME=hdfs hadoop fs -put -f ' + local_dir + file_name + hdfs_dir + channel + '/'),
      dag=dag)
    load_to_hdfs.set_upstream(analyze_tweets)
    load_to_hive = HiveOperator(task_id=('load_' + channel + '_to_hive'),
      hql=("LOAD DATA INPATH '" + hdfs_dir + channel + '/' + file_name + "' INTO TABLE " + channel + " PARTITION(dt='" + dt + "')"),
      dag=dag)
    load_to_hive.set_upstream(load_to_hdfs)
    load_to_hive.set_downstream(hive_to_mysql)

for channel in from_channels:
    file_name = 'from_' + channel + '_' + yesterday.strftime('%Y-%m-%d') + '.csv'
    load_to_hdfs = BashOperator(task_id=('put_' + channel + '_to_hdfs'),
      bash_command=('HADOOP_USER_NAME=hdfs hadoop fs -put -f ' + local_dir + file_name + hdfs_dir + channel + '/'),
      dag=dag)
    load_to_hdfs.set_upstream(analyze_tweets)
    load_to_hive = HiveOperator(task_id=('load_' + channel + '_to_hive'),
      hql=("LOAD DATA INPATH '" + hdfs_dir + channel + '/' + file_name + "' INTO TABLE " + channel + " PARTITION(dt='" + dt + "')"),
      dag=dag)
    load_to_hive.set_upstream(load_to_hdfs)
    load_to_hive.set_downstream(hive_to_mysql)