# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/command-line-interface/biobox_cli/verification/steps/cli.py
# Compiled at: 2017-03-20 04:10:45
# Size of source mod 2**32: 4287 bytes
import os, re, os.path, shutil
from behave import *

def get_stream(context, stream):
    assert stream in ('stderr', 'stdout'), 'Unknown output stream {}'.format(stream)
    return getattr(context.output, stream)


def get_env_path(context, file_):
    return os.path.join(context.env.cwd, file_)


def get_data_file_path(file_):
    dir_ = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dir_, '..', '..', 'verification', 'data', file_)


def assert_not_empty(obj):
    assert len(obj) > 0


def assert_file_exists(file_):
    assert os.path.isfile(file_), 'The file "{}" does not exist.'.format(file_)


def assert_file_not_empty(file_):
    with open(file_, 'r') as (f):
        assert_not_empty(f.read().strip())


def remove_warnings(string_):
    return re.sub('^WARNING:.+\n', '', string_)


def download_file(link, out):
    import wget
    return wget.download(link, out)


def extract_file(file, out):
    import tarfile
    tar = tarfile.open(file)
    tar.extractall(path=out)
    tar.close()


@given('I create the directory "{directory}"')
def step_impl(context, directory):
    os.makedirs(get_env_path(context, directory))


@given('I download and extract the file "{link}" to "{dest}"')
def step_impl(context, link, dest):
    normalized_dest = get_env_path(context, dest)
    extract_file(download_file(link, normalized_dest), normalized_dest)


@given('I create the file "{file_}" with the contents')
def step_impl(context, file_):
    with open(get_env_path(context, file_), 'w') as (f):
        f.write(context.text)


@given('I copy the example data files')
def step_impl(context):
    for row in context.table.rows:
        shutil.copy(get_data_file_path(row['source']), get_env_path(context, row['dest']))


@given('I copy the example data directories')
def step_impl(context):
    for row in context.table.rows:
        shutil.copytree(get_data_file_path(row['source']), get_env_path(context, row['dest']))


@when('I run the command')
def step_impl(context):
    context.output = context.env.run("bash -c '{}'".format(os.path.expandvars(context.text)), expect_error=True, expect_stderr=True)


@then('the {stream} should be empty')
def step_impl(context, stream):
    output = get_stream(context, stream)
    assert output == '', 'The {} should be empty but contains:\n\n{}'.format(stream, output)


@then('excluding warnings the {stream} should be empty')
def step_impl(context, stream):
    output = get_stream(context, stream)
    assert remove_warnings(output) == '', 'The {} should be empty but contains:\n\n{}'.format(stream, output)


@then('the exit code should be {code}')
def step_impl(context, code):
    returned = context.output.returncode
    assert returned == int(code), 'Process should return exit code {} but was {}'.format(code, returned)


@then('the {stream} should contain')
def step_impl(context, stream):
    output = get_stream(context, stream)
    assert context.text in output


@then('the {stream} should equal')
def step_impl(context, stream):
    output = get_stream(context, stream)
    assert context.text == output


@then('excluding warnings the {stream} should equal')
def step_impl(context, stream):
    output = get_stream(context, stream)
    assert context.text == remove_warnings(output)


@then('the {stream} should match /{regexp}/')
def step_impl(context, stream, regexp):
    output = get_stream(context, stream)
    assert re.match(regexp, output) != None, "Regular expression {} not found in:\n'{}'".format(regexp, output)


@then('the directory "{}" should not exist')
def step_impl(context, dir_):
    assert not os.path.isdir(dir_), 'The directory "{}" should not exist.'.format(dir_)


@then('the file "{}" should exist')
def step_impl(context, file_):
    assert_file_exists(get_env_path(context, file_))


@then('the file "{}" should not be empty')
def step_impl(context, file_):
    assert_file_not_empty(get_env_path(context, file_))


@then('the following files should exist and not be empty')
def step_impl(context):
    for row in context.table.rows:
        file_ = get_env_path(context, row['file'])
        assert_file_exists(file_)
        assert_file_not_empty(file_)