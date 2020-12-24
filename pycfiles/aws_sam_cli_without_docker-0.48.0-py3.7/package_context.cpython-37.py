# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/commands/package/package_context.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 3936 bytes
"""
Logic for uploading to s3 based on supplied template file and s3 bucket
"""
import json, logging, os, boto3, click
from botocore.config import Config
from samcli.commands.package.exceptions import PackageFailedError
from samcli.lib.package.artifact_exporter import Template
from samcli.lib.package.s3_uploader import S3Uploader
from samcli.lib.utils.botoconfig import get_boto_config_with_user_agent
from samcli.yamlhelper import yaml_dump
LOG = logging.getLogger(__name__)

class PackageContext:
    MSG_PACKAGED_TEMPLATE_WRITTEN = '\nSuccessfully packaged artifacts and wrote output template to file {output_file_name}.\nExecute the following command to deploy the packaged template\nsam deploy --template-file {output_file_path} --stack-name <YOUR STACK NAME>\n'

    def __init__(self, template_file, s3_bucket, s3_prefix, kms_key_id, output_template_file, use_json, force_upload, metadata, region, profile, on_deploy=False):
        self.template_file = template_file
        self.s3_bucket = s3_bucket
        self.s3_prefix = s3_prefix
        self.kms_key_id = kms_key_id
        self.output_template_file = output_template_file
        self.use_json = use_json
        self.force_upload = force_upload
        self.metadata = metadata
        self.region = region
        self.profile = profile
        self.on_deploy = on_deploy
        self.s3_uploader = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def run(self):
        s3_client = boto3.client('s3',
          config=get_boto_config_with_user_agent(signature_version='s3v4',
          region_name=(self.region if self.region else None)))
        self.s3_uploader = S3Uploader(s3_client, self.s3_bucket, self.s3_prefix, self.kms_key_id, self.force_upload)
        self.s3_uploader.artifact_metadata = self.metadata
        try:
            exported_str = self._export(self.template_file, self.use_json)
            self.write_output(self.output_template_file, exported_str)
            if self.output_template_file:
                if not self.on_deploy:
                    msg = self.MSG_PACKAGED_TEMPLATE_WRITTEN.format(output_file_name=(self.output_template_file),
                      output_file_path=(os.path.abspath(self.output_template_file)))
                    click.echo(msg)
        except OSError as ex:
            try:
                raise PackageFailedError(template_file=(self.template_file), ex=(str(ex)))
            finally:
                ex = None
                del ex

    def _export(self, template_path, use_json):
        template = Template(template_path, os.getcwd(), self.s3_uploader)
        exported_template = template.export()
        if use_json:
            exported_str = json.dumps(exported_template, indent=4, ensure_ascii=False)
        else:
            exported_str = yaml_dump(exported_template)
        return exported_str

    def write_output(self, output_file_name, data):
        if output_file_name is None:
            click.echo(data)
            return
        with open(output_file_name, 'w') as (fp):
            fp.write(data)