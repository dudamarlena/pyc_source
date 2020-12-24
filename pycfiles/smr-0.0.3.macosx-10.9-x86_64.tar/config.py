# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/smr/config.py
# Compiled at: 2014-09-22 12:38:47
from __future__ import absolute_import, division, print_function, unicode_literals
import argparse, boto, datetime, logging, os, sys
from .version import __version__
LOG_LEVELS = {b'critical': logging.CRITICAL, 
   b'error': logging.ERROR, 
   b'warning': logging.WARNING, 
   b'info': logging.INFO, 
   b'debug': logging.DEBUG}

class DefaultConfig(object):

    def __init__(self):
        self.paramiko_log_level = b'warning'
        self.workers = 8
        self.output_job_progress = True
        self.aws_access_key = None
        self.aws_secret_key = None
        self.aws_ec2_region = b'us-east-1'
        self.aws_ec2_ami = b'ami-30837058'
        self.aws_ec2_instance_type = b'm3.large'
        self.aws_ec2_security_group = [b'default']
        self.aws_ec2_ssh_username = b'ubuntu'
        self.aws_ec2_workers = 1
        self.aws_ec2_remote_config_path = b'/tmp/smr_config.py'
        self.aws_ec2_initialization_commands = [
         b'sudo apt-get update',
         b'sudo apt-get -q -y install python-pip python-dev git',
         b'sudo pip install git+git://github.com/idyedov/smr.git']
        self.aws_iam_profile = None
        self.cpu_usage_interval = 0.1
        self.screen_refresh_interval = 1.0
        self.date_range = None
        self.start_date = None
        self.end_date = None
        return


def get_default_config():
    return DefaultConfig()


def get_config_module(config_name):
    if not os.path.isfile(config_name):
        sys.stderr.write((b'job definition does not exist: {}\n').format(config_name))
        sys.exit(1)
    if config_name.endswith(b'.py'):
        config_name = config_name[:-3]
    else:
        if config_name.endswith(b'.pyc'):
            config_name = config_name[:-4]
        directory, config_module = os.path.split(config_name)
        if directory not in sys.path:
            sys.path.insert(0, directory)
        try:
            config = __import__(config_module)
        except ImportError:
            sys.stderr.write((b'Could not import job definition: {}\n').format(config_module))
            sys.exit(1)

    if not hasattr(config, b'MAP_FUNC'):
        setattr(config, b'MAP_FUNC', None)
    if not hasattr(config, b'REDUCE_FUNC'):
        setattr(config, b'REDUCE_FUNC', None)
    if not hasattr(config, b'OUTPUT_RESULTS_FUNC'):

        def default_output_results_func():
            print(b'done')

        setattr(config, b'OUTPUT_RESULTS_FUNC', default_output_results_func)
    return config


def mkdate(datestring):
    return datetime.datetime.strptime(datestring, b'%Y-%m-%d').date()


def get_config(args=None):
    default_config = DefaultConfig()
    parser = argparse.ArgumentParser()
    parser.add_argument(b'config', help=b'config.py')
    parser.add_argument(b'--paramiko-log-level', help=b'level of logging to be used for paramiko ssh connections (for smr-ec2 only)', choices=LOG_LEVELS.keys(), default=default_config.paramiko_log_level)
    parser.add_argument(b'-w', b'--workers', type=int, help=b'number of worker processes to use', default=default_config.workers)
    parser.add_argument(b'--output-filename', help=b'filename where results for this job will be stored')
    parser.add_argument(b'--output-job-progress', help=b'Output job progress to screen', dest=b'output_job_progress', action=b'store_true', default=default_config.output_job_progress)
    parser.add_argument(b'--no-output-job-progress', help=b'Do not output job progress to screen', dest=b'output_job_progress', action=b'store_false')
    parser.add_argument(b'--aws-access-key', help=b'AWS access key used for S3/EC2 access')
    parser.add_argument(b'--aws-secret-key', help=b'AWS secret key used for S3/EC2 access')
    parser.add_argument(b'--aws-iam-profile', help=b'AWS IAM profile to use when launching EC2 instances')
    parser.add_argument(b'--aws-ec2-region', help=b'region to use when running smr-ec2 workers', default=default_config.aws_ec2_region)
    parser.add_argument(b'--aws-ec2-ami', help=b'AMI to use when running smr-ec2 workers', default=default_config.aws_ec2_ami)
    parser.add_argument(b'--aws-ec2-instance-type', help=b'instance type to use for EC2 instances', default=default_config.aws_ec2_instance_type)
    parser.add_argument(b'--aws-ec2-security-group', help=b'security group to use for accessing EC2 workers (needs port 22 open)', nargs=b'*', default=default_config.aws_ec2_security_group)
    parser.add_argument(b'--aws-ec2-ssh-username', help=b'username to use when logging into EC2 workers over SSH', default=default_config.aws_ec2_ssh_username)
    parser.add_argument(b'--aws-ec2-workers', help=b'number of EC2 instances to use for this job', type=int, default=default_config.aws_ec2_workers)
    parser.add_argument(b'--aws-ec2-remote-config-path', help=b'where to store smr config on EC2 instances', default=default_config.aws_ec2_remote_config_path)
    parser.add_argument(b'--aws-ec2-initialization-commands', help=b'initialization commands to use for EC2 instances', nargs=b'+', default=default_config.aws_ec2_initialization_commands)
    parser.add_argument(b'--cpu-usage-interval', type=float, help=b'interval used for measuring CPU usage in seconds', default=default_config.cpu_usage_interval)
    parser.add_argument(b'--screen-refresh-interval', type=float, help=b"how often to refresh job progress that's displayed on screen in seconds", default=default_config.screen_refresh_interval)
    parser.add_argument(b'--start-date', type=mkdate, help=b'start date (YYYY-mm-dd) for this job, only used if using {year}/{month}/{day} macros in INPUT_DATA')
    parser.add_argument(b'--end-date', type=mkdate, help=b'end date (YYYY-mm-dd) for this job, only used if using {year}/{month}/{day} macros in INPUT_DATA', default=datetime.datetime.utcnow().date())
    parser.add_argument(b'--date-range', type=int, help=b'number of days back to process, overrides start date if used')
    parser.add_argument(b'-v', b'--version', action=b'version', version=(b'SMR {}').format(__version__))
    result = parser.parse_args(args)
    return result


def configure_job(args):
    config = get_config_module(args.config)
    for arg in ('MAP_FUNC', 'REDUCE_FUNC', 'OUTPUT_RESULTS_FUNC', 'INPUT_DATA'):
        setattr(args, arg, getattr(config, arg))

    pip_requirements = getattr(config, b'PIP_REQUIREMENTS', None)
    if pip_requirements:
        for package in pip_requirements:
            args.aws_ec2_initialization_commands.append((b'sudo pip install {}').format(package))

    if not args.aws_iam_profile and (not args.aws_access_key or not args.aws_secret_key):
        metadata = boto.utils.get_instance_metadata(timeout=1.0, num_retries=1, data=b'meta-data/iam/security-credentials/')
        if len(metadata) > 0:
            args.aws_iam_profile = metadata.keys()[0]
    paramiko_level_str = args.paramiko_log_level.lower()
    paramiko_level = LOG_LEVELS.get(paramiko_level_str, logging.WARNING)
    logging.getLogger(b'paramiko').setLevel(paramiko_level)
    logging.getLogger(b'paramiko.transport').addHandler(logging.NullHandler())
    return