# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jim/workspace/python_module_helm_values/reckoner_values/reckoner_file_updater.py
# Compiled at: 2019-07-17 08:32:22
# Size of source mod 2**32: 2015 bytes
from .yaml_utils import ordered_load
from .yaml_utils import data_to_yaml
from .git_values import GitValues
import yaml, click, os

class ReckonerFileUpdater:

    def __init__(self, source, dest, region, extra_files=None, extra_values=None, bucket='git', download_path='/tmp/downloaded_values'):
        self.source = source
        self.dest = dest
        self.extra_files = extra_files
        self.extra_values = extra_values
        self.bucket = bucket
        self.region = region
        self.data = None
        self.download_path = download_path

    def load_yaml(self):
        with open(self.source, 'r') as (stream):
            try:
                self.data = ordered_load(stream, yaml.FullLoader)
            except yaml.YAMLError as exc:
                try:
                    print(exc)
                    quit()
                finally:
                    exc = None
                    del exc

        return self.data

    def save_dest(self):
        yaml_string = data_to_yaml(self.data)
        f = open(self.dest, 'w')
        f.write(yaml_string)
        f.close()
        return yaml_string

    def add_files(self):
        namespace = self.data['namespace']
        for chart_index in self.data['charts']:
            chart = self.data['charts'][chart_index]
            click.echo(click.style(('Parsing chart {}'.format(chart_index)), fg='black', bg='green'))
            app_name = chart_index.replace('{}-'.format(namespace), '')
            chart_name = chart['chart']
            gv = GitValues(namespace, chart_name, app_name, region=(self.region), extra_files=['_system'], download_path=(self.download_path))
            path_prefix = os.path.join(self.download_path, '')
            files = [path_prefix + s for s in gv.get_existing_files()]
            chart['files'] = files
            click.echo(click.style(('Found {} files'.format(len(chart['files']))), fg='green'))
            for file in chart['files']:
                click.echo(click.style(('- {}'.format(file)), fg='green'))

    def update(self):
        self.load_yaml()
        self.add_files()
        self.save_dest()