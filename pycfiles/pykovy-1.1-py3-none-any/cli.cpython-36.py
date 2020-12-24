# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/pykovi/cli.py
# Compiled at: 2019-11-19 09:29:28
# Size of source mod 2**32: 1271 bytes
import click, os, re, importlib.util as iu, glue_jobs, awswrangler as aw
glue_jobs.disable_auto_execute()

@click.command('publish_jobs', context_settings={'ignore_unknown_options': True})
@click.option('--aws-access-key-id', type=(click.STRING), envvar='AWS_ACCESS_KEY_ID')
@click.option('--aws-secret-access-key',
  type=(click.STRING), envvar='AWS_SECRET_ACCESS_KEY')
@click.option('--aws-session-token', type=(click.STRING), envvar='AWS_SESSION_TOKEN')
@click.argument('files',
  nargs=(-1),
  type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True))
def publish_jobs(aws_access_key_id, aws_secret_access_key, aws_session_token, files):
    for filename in [f for f in list(files) if f.endswith('.py')]:
        spec = iu.spec_from_file_location(os.path.basename(filename), filename)
        module = iu.module_from_spec(spec)
        spec.loader.exec_module(module)

    for glue_job_item in glue_jobs.declared_jobs:
        session = aw.Session(aws_access_key_id=aws_access_key_id,
          aws_secret_access_key=aws_secret_access_key,
          aws_session_token=aws_session_token)
        glue_job_item.publish_job(session)


if __name__ == '__main__':
    publish_jobs()