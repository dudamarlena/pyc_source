# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/example_dags/example_gcp_sql_query.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 11463 bytes
__doc__ = '\nExample Airflow DAG that performs query in a Cloud SQL instance.\n\nThis DAG relies on the following OS environment variables\n\n* GCP_PROJECT_ID - Google Cloud Platform project for the Cloud SQL instance\n* GCP_REGION - Google Cloud region where the database is created\n*\n* GCSQL_POSTGRES_INSTANCE_NAME - Name of the postgres Cloud SQL instance\n* GCSQL_POSTGRES_USER - Name of the postgres database user\n* GCSQL_POSTGRES_PASSWORD - Password of the postgres database user\n* GCSQL_POSTGRES_PUBLIC_IP - Public IP of the Postgres database\n* GCSQL_POSTGRES_PUBLIC_PORT - Port of the postgres database\n*\n* GCSQL_MYSQL_INSTANCE_NAME - Name of the postgres Cloud SQL instance\n* GCSQL_MYSQL_USER - Name of the mysql database user\n* GCSQL_MYSQL_PASSWORD - Password of the mysql database user\n* GCSQL_MYSQL_PUBLIC_IP - Public IP of the mysql database\n* GCSQL_MYSQL_PUBLIC_PORT - Port of the mysql database\n'
import os, subprocess
from os.path import expanduser
from six.moves.urllib.parse import quote_plus
import airflow
from airflow import models
from airflow.contrib.operators.gcp_sql_operator import CloudSqlQueryOperator
GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID', 'example-project')
GCP_REGION = os.environ.get('GCP_REGION', 'europe-west-1b')
GCSQL_POSTGRES_INSTANCE_NAME_QUERY = os.environ.get('GCSQL_POSTGRES_INSTANCE_NAME_QUERY', 'testpostgres')
GCSQL_POSTGRES_DATABASE_NAME = os.environ.get('GCSQL_POSTGRES_DATABASE_NAME', 'postgresdb')
GCSQL_POSTGRES_USER = os.environ.get('GCSQL_POSTGRES_USER', 'postgres_user')
GCSQL_POSTGRES_PASSWORD = os.environ.get('GCSQL_POSTGRES_PASSWORD', 'password')
GCSQL_POSTGRES_PUBLIC_IP = os.environ.get('GCSQL_POSTGRES_PUBLIC_IP', '0.0.0.0')
GCSQL_POSTGRES_PUBLIC_PORT = os.environ.get('GCSQL_POSTGRES_PUBLIC_PORT', 5432)
GCSQL_POSTGRES_CLIENT_CERT_FILE = os.environ.get('GCSQL_POSTGRES_CLIENT_CERT_FILE', '.key/postgres-client-cert.pem')
GCSQL_POSTGRES_CLIENT_KEY_FILE = os.environ.get('GCSQL_POSTGRES_CLIENT_KEY_FILE', '.key/postgres-client-key.pem')
GCSQL_POSTGRES_SERVER_CA_FILE = os.environ.get('GCSQL_POSTGRES_SERVER_CA_FILE', '.key/postgres-server-ca.pem')
GCSQL_MYSQL_INSTANCE_NAME_QUERY = os.environ.get('GCSQL_MYSQL_INSTANCE_NAME_QUERY', 'testmysql')
GCSQL_MYSQL_DATABASE_NAME = os.environ.get('GCSQL_MYSQL_DATABASE_NAME', 'mysqldb')
GCSQL_MYSQL_USER = os.environ.get('GCSQL_MYSQL_USER', 'mysql_user')
GCSQL_MYSQL_PASSWORD = os.environ.get('GCSQL_MYSQL_PASSWORD', 'password')
GCSQL_MYSQL_PUBLIC_IP = os.environ.get('GCSQL_MYSQL_PUBLIC_IP', '0.0.0.0')
GCSQL_MYSQL_PUBLIC_PORT = os.environ.get('GCSQL_MYSQL_PUBLIC_PORT', 3306)
GCSQL_MYSQL_CLIENT_CERT_FILE = os.environ.get('GCSQL_MYSQL_CLIENT_CERT_FILE', '.key/mysql-client-cert.pem')
GCSQL_MYSQL_CLIENT_KEY_FILE = os.environ.get('GCSQL_MYSQL_CLIENT_KEY_FILE', '.key/mysql-client-key.pem')
GCSQL_MYSQL_SERVER_CA_FILE = os.environ.get('GCSQL_MYSQL_SERVER_CA_FILE', '.key/mysql-server-ca.pem')
SQL = [
 'CREATE TABLE IF NOT EXISTS TABLE_TEST (I INTEGER)',
 'CREATE TABLE IF NOT EXISTS TABLE_TEST (I INTEGER)',
 'INSERT INTO TABLE_TEST VALUES (0)',
 'CREATE TABLE IF NOT EXISTS TABLE_TEST2 (I INTEGER)',
 'DROP TABLE TABLE_TEST',
 'DROP TABLE TABLE_TEST2']
default_args = {'start_date': airflow.utils.dates.days_ago(1)}
HOME_DIR = expanduser('~')

def get_absolute_path(path):
    if path.startswith('/'):
        return path
    else:
        return os.path.join(HOME_DIR, path)


postgres_kwargs = dict(user=(quote_plus(GCSQL_POSTGRES_USER)),
  password=(quote_plus(GCSQL_POSTGRES_PASSWORD)),
  public_port=GCSQL_POSTGRES_PUBLIC_PORT,
  public_ip=(quote_plus(GCSQL_POSTGRES_PUBLIC_IP)),
  project_id=(quote_plus(GCP_PROJECT_ID)),
  location=(quote_plus(GCP_REGION)),
  instance=(quote_plus(GCSQL_POSTGRES_INSTANCE_NAME_QUERY)),
  database=(quote_plus(GCSQL_POSTGRES_DATABASE_NAME)),
  client_cert_file=(quote_plus(get_absolute_path(GCSQL_POSTGRES_CLIENT_CERT_FILE))),
  client_key_file=(quote_plus(get_absolute_path(GCSQL_POSTGRES_CLIENT_KEY_FILE))),
  server_ca_file=(quote_plus(get_absolute_path(GCSQL_POSTGRES_SERVER_CA_FILE))))
os.environ['AIRFLOW_CONN_PROXY_POSTGRES_TCP'] = ('gcpcloudsql://{user}:{password}@{public_ip}:{public_port}/{database}?database_type=postgres&project_id={project_id}&location={location}&instance={instance}&use_proxy=True&sql_proxy_use_tcp=True'.format)(**postgres_kwargs)
os.environ['AIRFLOW_CONN_PROXY_POSTGRES_SOCKET'] = ('gcpcloudsql://{user}:{password}@{public_ip}:{public_port}/{database}?database_type=postgres&project_id={project_id}&location={location}&instance={instance}&use_proxy=True&sql_proxy_version=v1.13&sql_proxy_use_tcp=False'.format)(**postgres_kwargs)
os.environ['AIRFLOW_CONN_PUBLIC_POSTGRES_TCP'] = ('gcpcloudsql://{user}:{password}@{public_ip}:{public_port}/{database}?database_type=postgres&project_id={project_id}&location={location}&instance={instance}&use_proxy=False&use_ssl=False'.format)(**postgres_kwargs)
os.environ['AIRFLOW_CONN_PUBLIC_POSTGRES_TCP_SSL'] = ('gcpcloudsql://{user}:{password}@{public_ip}:{public_port}/{database}?database_type=postgres&project_id={project_id}&location={location}&instance={instance}&use_proxy=False&use_ssl=True&sslcert={client_cert_file}&sslkey={client_key_file}&sslrootcert={server_ca_file}'.format)(**postgres_kwargs)
mysql_kwargs = dict(user=(quote_plus(GCSQL_MYSQL_USER)),
  password=(quote_plus(GCSQL_MYSQL_PASSWORD)),
  public_port=GCSQL_MYSQL_PUBLIC_PORT,
  public_ip=(quote_plus(GCSQL_MYSQL_PUBLIC_IP)),
  project_id=(quote_plus(GCP_PROJECT_ID)),
  location=(quote_plus(GCP_REGION)),
  instance=(quote_plus(GCSQL_MYSQL_INSTANCE_NAME_QUERY)),
  database=(quote_plus(GCSQL_MYSQL_DATABASE_NAME)),
  client_cert_file=(quote_plus(get_absolute_path(GCSQL_MYSQL_CLIENT_CERT_FILE))),
  client_key_file=(quote_plus(get_absolute_path(GCSQL_MYSQL_CLIENT_KEY_FILE))),
  server_ca_file=(quote_plus(get_absolute_path(GCSQL_MYSQL_SERVER_CA_FILE))))
os.environ['AIRFLOW_CONN_PROXY_MYSQL_TCP'] = ('gcpcloudsql://{user}:{password}@{public_ip}:{public_port}/{database}?database_type=mysql&project_id={project_id}&location={location}&instance={instance}&use_proxy=True&sql_proxy_version=v1.13&sql_proxy_use_tcp=True'.format)(**mysql_kwargs)
try:
    sql_proxy_binary_path = subprocess.check_output([
     'which', 'cloud_sql_proxy']).decode('utf-8').rstrip()
except subprocess.CalledProcessError:
    sql_proxy_binary_path = '/tmp/anyhow_download_cloud_sql_proxy'

os.environ['AIRFLOW_CONN_PROXY_MYSQL_SOCKET'] = ('gcpcloudsql://{user}:{password}@{public_ip}:{public_port}/{database}?database_type=mysql&project_id={project_id}&location={location}&instance={instance}&use_proxy=True&sql_proxy_binary_path={sql_proxy_binary_path}&sql_proxy_use_tcp=False'.format)(sql_proxy_binary_path=quote_plus(sql_proxy_binary_path), **mysql_kwargs)
os.environ['AIRFLOW_CONN_PUBLIC_MYSQL_TCP'] = ('gcpcloudsql://{user}:{password}@{public_ip}:{public_port}/{database}?database_type=mysql&project_id={project_id}&location={location}&instance={instance}&use_proxy=False&use_ssl=False'.format)(**mysql_kwargs)
os.environ['AIRFLOW_CONN_PUBLIC_MYSQL_TCP_SSL'] = ('gcpcloudsql://{user}:{password}@{public_ip}:{public_port}/{database}?database_type=mysql&project_id={project_id}&location={location}&instance={instance}&use_proxy=False&use_ssl=True&sslcert={client_cert_file}&sslkey={client_key_file}&sslrootcert={server_ca_file}'.format)(**mysql_kwargs)
os.environ['AIRFLOW_CONN_PUBLIC_MYSQL_TCP_SSL_NO_PROJECT_ID'] = ('gcpcloudsql://{user}:{password}@{public_ip}:{public_port}/{database}?database_type=mysql&location={location}&instance={instance}&use_proxy=False&use_ssl=True&sslcert={client_cert_file}&sslkey={client_key_file}&sslrootcert={server_ca_file}'.format)(**mysql_kwargs)
connection_names = [
 'proxy_postgres_tcp',
 'proxy_postgres_socket',
 'public_postgres_tcp',
 'public_postgres_tcp_ssl',
 'proxy_mysql_tcp',
 'proxy_mysql_socket',
 'public_mysql_tcp',
 'public_mysql_tcp_ssl',
 'public_mysql_tcp_ssl_no_project_id']
tasks = []
with models.DAG(dag_id='example_gcp_sql_query',
  default_args=default_args,
  schedule_interval=None) as (dag):
    prev_task = None
    for connection_name in connection_names:
        task = CloudSqlQueryOperator(gcp_cloudsql_conn_id=connection_name,
          task_id=('example_gcp_sql_task_' + connection_name),
          sql=SQL)
        tasks.append(task)
        if prev_task:
            prev_task >> task
        prev_task = task