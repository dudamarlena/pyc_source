# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x0ox/Dropbox/ActiveDev/yac/yac/lib/state.py
# Compiled at: 2017-11-16 20:28:41
import re, boto3, os, json, jmespath, sys, argparse, botocore
from subprocess import call
from yac.lib.variables import get_variable, set_variable
from yac.lib.file import get_file_contents, dump_dictionary
from yac.lib.cache import get_cache_value, set_cache_value_dt, delete_cache_value
from yac.lib.inputs import string_validation
STATE_CACHE_KEY_PREFIX = 'yac/lib/state'

def load_state_s3(s3_bucket, s3_path, service_alias):
    state = {}
    s3 = boto3.resource('s3')
    state_filename = get_state_filename(service_alias)
    state_file_local_path_full = get_state_local_path(s3_path, service_alias)
    s3_file_path = '%s/%s' % (s3_path, state_filename)
    if state_exists(s3_bucket, s3_file_path):
        s3.meta.client.download_file(s3_bucket, s3_file_path, state_file_local_path_full)
        file_contents = get_file_contents(state_file_local_path_full)
        state = json.loads(file_contents)
    else:
        print "stack state doesn't exist at %s:%s..." % (s3_bucket, s3_path)
    return state


def load_state(s3_path, service_alias):
    state = {}
    state_filename = get_state_filename(service_alias)
    s3_full_path = get_s3_full_path(s3_path, service_alias)
    s3_bucket = find_bucket_with_state_in_cache(s3_full_path, service_alias)
    if not s3_bucket:
        s3_bucket = find_bucket_with_state_by_name(s3_full_path, service_alias)
        if not s3_bucket:
            s3_bucket = prompt_for_bucket(service_alias)
        else:
            msg = 'Loading service state from ' + 's3://%s/%s/%s.\n' % (s3_bucket, s3_path, state_filename) + "(hint: to use a different bucket either move or rename the state file and re-run 'yac stack ...')"
            print msg
    else:
        msg = 'Loading service state from ' + 's3://%s/%s/%s.\n' % (s3_bucket, s3_path, state_filename) + "(hint: to use a different bucket either move or rename the state file and re-run 'yac stack ...')"
        print msg
    state_file_local_path_full = get_state_local_path(s3_full_path, service_alias)
    s3_file_path = '%s/%s' % (s3_full_path, state_filename)
    if state_exists(s3_bucket, s3_file_path):
        s3 = boto3.resource('s3')
        s3.meta.client.download_file(s3_bucket, s3_file_path, state_file_local_path_full)
        file_contents = get_file_contents(state_file_local_path_full)
        state = json.loads(file_contents)
    else:
        print "stack state doesn't exist at %s ..." % s3_file_path
    return (
     state, s3_bucket)


def get_s3_full_path(s3_path, service_alias):
    s3_full_path = '%s/%s' % (service_alias, s3_path)
    return s3_full_path


def state_exists(s3_bucket, s3_path):
    object_exists = False
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(s3_bucket)
    objs = list(bucket.objects.filter(Prefix=s3_path))
    if len(objs) > 0 and objs[0].key == s3_path:
        object_exists = True
    return object_exists


def save_state(s3_path, service_alias, state, s3_bucket=''):
    state_filename = get_state_filename(service_alias)
    if not s3_bucket:
        s3_bucket = find_bucket_in_cache(service_alias)
        if not s3_bucket:
            s3_bucket = find_bucket_by_name(service_alias)
            if not s3_bucket:
                s3_bucket = prompt_for_bucket(service_alias)
            else:
                msg = 'Saving service state to s3://%s/%s/%s.\n' % (s3_bucket, s3_path, state_filename)
                print msg
        else:
            msg = 'Saving service state to s3://%s/%s/%s.\n' % (s3_bucket, s3_path, state_filename)
            print msg
    s3_path = get_s3_full_path(s3_path, service_alias)
    state_file_local_path_full = get_state_local_path(s3_path, service_alias)
    state_str = json.dumps(state, indent=2)
    state_file_local_path = os.path.basename(state_file_local_path_full)
    if not os.path.exists(state_file_local_path):
        os.makedirs(state_file_local_path)
    with open(state_file_local_path_full, 'w') as (file_arg_fp):
        file_arg_fp.write(state_str)
    state_filename = get_state_filename(service_alias)
    s3_file_path = '%s/%s' % (s3_path, state_filename)
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(state_file_local_path_full, s3_bucket, s3_file_path)
    return s3_bucket


def save_state_s3(s3_bucket, s3_path, service_alias, state):
    s3 = boto3.resource('s3')
    state_file_local_path_full = get_state_local_path(s3_path, service_alias)
    state_str = json.dumps(state, indent=2)
    state_file_local_path = os.path.basename(state_file_local_path_full)
    if not os.path.exists(state_file_local_path):
        os.makedirs(state_file_local_path)
    with open(state_file_local_path_full, 'w') as (file_arg_fp):
        file_arg_fp.write(state_str)
    state_filename = get_state_filename(service_alias)
    s3_file_path = '%s/%s' % (s3_path, state_filename)
    s3.meta.client.upload_file(state_file_local_path_full, s3_bucket, s3_file_path)


def get_state_filename(service_alias):
    state_filename = '%s-state.json' % service_alias
    return state_filename


def get_state_local_path(s3_full_path, service_alias):
    home = os.path.expanduser('~')
    state_file_local_path = os.path.join(home, '.yac', s3_full_path)
    state_filename = get_state_filename(service_alias)
    state_file_local_path_full = os.path.join(state_file_local_path, state_filename)
    if not os.path.exists(state_file_local_path):
        os.makedirs(state_file_local_path)
    return state_file_local_path_full


def get_state_s3_bucket(service_alias):
    s3_bucket = ''
    if bucket_exists(service_alias):
        s3_bucket = service_alias
    return s3_bucket


def get_state_s3_bucket_old(service_alias):
    s3_bucket = ''
    if bucket_exists(service_alias):
        s3_bucket = service_alias
    return s3_bucket


def find_bucket_in_cache(service_alias):
    state_cache_key = get_state_cache_key(service_alias)
    s3_bucket = get_cache_value(state_cache_key, '')
    return s3_bucket


def get_state_cache_key(service_alias):
    return '%s/%s' % (STATE_CACHE_KEY_PREFIX, service_alias)


def find_bucket_with_state_in_cache(this_s3_path, service_alias):
    s3_bucket = ''
    s3_bucket_candidate = find_bucket_in_cache(service_alias)
    if s3_bucket_candidate:
        if state_file_exists(s3_bucket_candidate, service_alias, this_s3_path):
            print 'state file exists ...'
            s3_bucket = s3_bucket_candidate
    return s3_bucket


def find_bucket_by_name(search_str):
    s3_bucket = ''
    s3 = boto3.client('s3')
    buckets = s3.list_buckets()
    for bucket in buckets['Buckets']:
        if search_str in bucket['Name']:
            s3_bucket = bucket['Name']

    return s3_bucket


def find_bucket_with_state_by_name(this_s3_path, service_alias):
    s3_bucket = ''
    s3_bucket_candidate = find_bucket_by_name(service_alias)
    if s3_bucket_candidate:
        if state_file_exists(s3_bucket_candidate, service_alias, this_s3_path):
            s3_bucket = s3_bucket_candidate
    return s3_bucket


def prompt_for_bucket(service_alias):
    s3_bucket = ''
    while True:
        print 'The service needs an S3 bucket that can be used to save its state. Available buckets include:'
        print str(get_buckets_names()) + '\n'
        msg = 'Please enter the name a bucket >> '
        s3_bucket = raw_input(msg)
        if bucket_exists(s3_bucket):
            set_state_cache(service_alias, s3_bucket)
            break
        else:
            print "bucket doesn't exist ... try again"

    return s3_bucket


def set_state_cache(service_alias, s3_bucket):
    state_cache_key = get_state_cache_key(service_alias)
    set_cache_value_dt(state_cache_key, s3_bucket)


def clear_state_cache(service_alias):
    state_cache_key = get_state_cache_key(service_alias)
    delete_cache_value(state_cache_key)


def get_state_s3_bucket_cached_old(service_alias):
    s3_bucket = ''
    STATE_CACHE_KEY = 'yac/lib/state/%s' % service_alias
    while True:
        jira_state_s3 = get_cache_value(STATE_CACHE_KEY, {})
        if 'state-bucket' not in jira_state_s3:
            msg = 'Please enter the name of the S3 buckets that this app uses to persist its state >> '
            s3_bucket = raw_input(msg)
            if bucket_exists(s3_bucket):
                jira_state_s3['state-bucket'] = s3_bucket
                set_cache_value_dt(STATE_CACHE_KEY, jira_state_s3)
                break
            else:
                print "bucket doesn't exist ... try again"
        else:
            msg = ("Loading service state from the '%s' S3 buckets ('enter' to continue, 'n' to specify " + 'a different bucket)  >> ') % jira_state_s3['state-bucket']
            re_load = raw_input(msg)
            if not re_load:
                s3_bucket = jira_state_s3['state-bucket']
                break
            else:
                delete_cache_value(STATE_CACHE_KEY)

    return s3_bucket


def create_state_s3_bucket(service_alias):
    s3 = boto3.resource('s3')
    response = client.create_bucket(ACL='private', Bucket=service_alias)
    response = client.put_bucket_versioning(Bucket=service_alias, VersioningConfiguration={'MFADelete': 'Disabled', 
       'Status': 'Enabled'})


def state_file_exists(s3_bucket, service_alias, s3_path):
    state_file_exists = False
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(s3_bucket)
    state_filename = get_state_filename(service_alias)
    s3_file_path = '%s/%s' % (s3_path, state_filename)
    try:
        objs = list(bucket.objects.filter(Prefix=s3_file_path))
        if objs:
            state_file_exists = True
    except botocore.exceptions.ClientError as e:
        state_file_exists = False

    return state_file_exists


def bucket_exists(s3_bucket):
    bucket_exists = True
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(s3_bucket)
    try:
        objs = list(bucket.objects.filter(Prefix='/'))
        bucket_exists = True
    except botocore.exceptions.ClientError as e:
        bucket_exists = False

    return bucket_exists


def edit_state(s3_path, service_alias, state_params):
    s3_full_path = get_s3_full_path(s3_path, service_alias)
    tmp_file_name = '%s-state.json' % service_alias
    state_file_local_path_full = dump_dictionary(state_params, service_alias, tmp_file_name)
    EDITOR = os.environ.get('EDITOR', 'nano')
    call([EDITOR, state_file_local_path_full])
    file_contents = get_file_contents(state_file_local_path_full)
    if file_contents:
        new_state_params = json.loads(file_contents)
        state_params.clear()
        state_params.update(new_state_params)


def state_change_prompter(msg):
    validation_failed = True
    change = False
    options = [
     'y', 'n', '']
    while validation_failed:
        input = raw_input(msg)
        validation_failed = string_validation(input, options, False)

    if input and input == 'y':
        change = True
    return change


def get_buckets_names():
    bucket_names = []
    s3 = boto3.client('s3')
    buckets = s3.list_buckets()
    for bucket in buckets['Buckets']:
        bucket_names = bucket_names + [bucket['Name']]

    return bucket_names