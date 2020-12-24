# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/bayesdb/settings.py
# Compiled at: 2015-02-12 15:25:14
import os

class path:
    user_home_dir = os.environ['HOME']
    if 'WORKSPACE' in os.environ:
        user_home_dir = os.environ['WORKSPACE']
    remote_code_dir = os.path.join('/home/sgeadmin', 'tabular_predDB')
    this_dir = os.path.dirname(os.path.abspath(__file__))
    this_repo_dir = os.path.abspath(os.path.join(this_dir, '..'))
    install_script_dir = os.path.join(this_repo_dir, 'install_scripts')
    web_resources_dir = os.path.join(this_repo_dir, 'www')
    web_resources_data_dir = os.path.join(web_resources_dir, 'data')
    install_ubuntu_script = os.path.join(install_script_dir, 'install_ubuntu_packages.sh')
    install_boost_script = os.path.join(install_script_dir, 'install_boost.sh')
    virtualenv_setup_script = os.path.join(install_script_dir, 'virtualenv_setup.sh')
    run_server_script = os.path.join(this_repo_dir, 'run_server.sh')
    run_webserver_script = os.path.join(this_repo_dir, 'run_simplehttpserver.sh')
    try:
        os.makedirs(web_resources_dir)
        os.makedirs(web_resources_data_dir)
    except Exception as e:
        pass


class Hadoop:
    DEFAULT_CLUSTER = 'xdata_highmem'
    DEBUG = False
    xdata_hadoop_jar_420 = '/usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.2.0.jar'
    xdata_hadoop_jar_412 = '/usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.1.2.jar'
    default_xdata_hadoop_jar = xdata_hadoop_jar_420 if os.path.exists(xdata_hadoop_jar_420) else xdata_hadoop_jar_412
    default_xdata_compute_hdfs_uri = 'hdfs://10.1.92.51:8020/'
    default_xdata_compute_jobtracker_uri = '10.1.92.53:8021'
    default_xdata_highmem_hdfs_uri = 'hdfs://10.1.93.51:8020/'
    default_xdata_highmem_jobtracker_uri = '10.1.93.53:8021'
    default_starcluster_hadoop_jar = '/usr/lib/hadoop-0.20/contrib/streaming/hadoop-streaming-0.20.2-cdh3u2.jar'
    default_starcluster_hdfs_uri = None
    default_starcluster_jobtracker_uri = None
    default_localhost_hadoop_jar = default_xdata_hadoop_jar
    default_localhost_hdfs_uri = None
    default_localhost_jobtracker_uri = None
    if DEFAULT_CLUSTER == 'starcluster':
        default_hadoop_jar = default_starcluster_hadoop_jar
        default_hdfs_uri = default_starcluster_hdfs_uri
        default_jobtracker_uri = default_starcluster_jobtracker_uri
    elif DEFAULT_CLUSTER == 'localhost':
        default_hadoop_jar = default_localhost_hadoop_jar
        default_hdfs_uri = default_localhost_hdfs_uri
        default_jobtracker_uri = default_localhost_jobtracker_uri
    else:
        default_hadoop_jar = default_xdata_hadoop_jar
        if DEFAULT_CLUSTER == 'xdata_compute':
            default_hdfs_uri = default_xdata_compute_hdfs_uri
            default_jobtracker_uri = default_xdata_compute_jobtracker_uri
        else:
            default_hdfs_uri = default_xdata_highmem_hdfs_uri
            default_jobtracker_uri = default_xdata_highmem_jobtracker_uri
    default_hadoop_binary = 'hadoop'
    default_engine_binary = '/user/bigdata/SSCI/hadoop_line_processor.jar'
    default_hdfs_dir = '/user/bigdata/SSCI/'
    default_output_path = 'myOutputDir'
    default_input_filename = 'hadoop_input'
    default_table_data_filename = 'table_data.pkl.gz'
    default_command_dict_filename = 'command_dict.pkl.gz'
    default_table_filename = os.path.join(path.web_resources_data_dir, 'dha.csv')
    default_analyze_args_dict_filename = 'analyze_args_dict.pkl.gz'
    default_initialize_args_dict = dict(command='initialize', initialization='from_the_prior')
    default_analyze_args_dict = dict(command='analyze', kernel_list=(), n_steps=1, c=(), r=(), max_time=-1)


class s3:
    bucket_str = 'mitpcp-tabular-predDB'
    bucket_dir = ''
    ec2_credentials_file = os.path.expanduser('~/.boto')


class gdocs:
    auth_file = os.path.expanduser('~/mh_gdocs_auth')
    gdocs_folder_default = 'MH'


class git:
    repo_prefix = 'git@github.com:'
    repo_suffix = 'mit-probabilistic-computing-project/tabular-predDB.git'
    repo = repo_prefix + repo_suffix
    branch = 'master'