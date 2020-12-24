# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/plecos/validate_cli.py
# Compiled at: 2019-11-07 16:34:06
# Size of source mod 2**32: 1603 bytes
__doc__ = 'Ocean Protocol wrapper around json schema'
from pathlib import Path
import click

@click.command()
@click.argument('schema_file', type=click.Path(exists=True))
@click.argument('json_file', type=click.Path(exists=True))
def validate(schema_file, json_file):
    """This script validates a json file according a schema file.
    Wraps the jsonschema project, see https://pypi.org/project/jsonschema/.

    Arguments:

        SCHEMA_FILE_NAME: the name of the schema file, found in ./schemas

        JSON_FILE: the relative (to current directory) path of the json file to validate against
    """
    click.echo('schema_file_name: {}'.format(schema_file))
    click.echo('json_file {}'.format(json_file))
    print(type(schema_file))
    json_file_path = Path.cwd() / json_file
    if not json_file_path.exists():
        raise AssertionError('Json file path {} does not exist'.format(json_file_path))
    else:
        schema_file_path = Path.cwd() / schema_file
        assert schema_file_path.exists()
    validator = Draft4Validator(valid_schema)


if __name__ == '__main__':
    validate()