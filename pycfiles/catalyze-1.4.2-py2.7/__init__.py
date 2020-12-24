# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/catalyze/__init__.py
# Compiled at: 2015-08-04 23:59:02
from __future__ import absolute_import
cli = None

def init_cli():
    global cli
    import click
    from . import config, output

    @click.group('catalyze')
    @click.option('--baas-host', help='Alternate BaaS API URL')
    @click.option('--paas-host', help='Alternate PaaS API URL')
    @click.option('--username', help='Catalyze Username')
    @click.option('--password', help='Catalyze Password')
    @click.option('--skip-validation', is_flag=True, help='Skip certificate validation')
    @click.version_option(version=config.version)
    def inner_cli(baas_host, paas_host, username, password, skip_validation):
        if baas_host is not None:
            config.baas_host = baas_host
            output.write('Overriding BaaS URL: ' + config.baas_host)
        if paas_host is not None:
            config.paas_host = paas_host
            output.write('Overriding PaaS URL: ' + config.paas_host)
        config.username = username
        config.password = password
        if skip_validation:
            config.behavior['skip_cert_validation'] = False
            output.write('Skipping cert validation, I hope this was intentional')
        return

    cli = inner_cli
    from catalyze.commands import associate, backup, console, dashboard, db, environments, metrics, rake, redeploy, status, support_ids, users, variables, worker


def run():
    import catalyze.__main__