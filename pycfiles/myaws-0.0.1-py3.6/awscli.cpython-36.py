# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/myaws/awscli.py
# Compiled at: 2018-05-12 22:14:18
# Size of source mod 2**32: 5529 bytes
import click, boto3, json, Modules

@click.group(help='Subcommand click CLI')
@click.option('-p', '--profile', type=str)
@click.pass_context
def main(ctx, profile):
    ctx.params['session'] = boto3.session.Session(profile_name=(ctx.params.get('profile')))


@main.group(help='EC2 API')
@click.pass_context
def ec2(ctx):
    ctx.params['client'] = ctx.parent.params['session'].client('ec2')


@main.group(help='S3 API')
@click.pass_context
def s3(ctx):
    ctx.params['client'] = ctx.parent.params['session'].resource('s3')


@main.group(help='AutoScaling API')
@click.pass_context
def asg(ctx):
    ctx.params['client'] = ctx.parent.params['session'].client('autoscaling')


@main.group(help='Route53 API')
@click.pass_context
def route53(ctx):
    ctx.params['client'] = ctx.parent.params['session'].client('route53')


@main.group(help='RDS API')
@click.pass_context
def rds(ctx):
    ctx.params['client'] = ctx.parent.params['session'].client('rds')


@ec2.command(help='EC2 DescribeInstances API')
@click.option('--instance-id', type=str, help='specify instance id')
@click.pass_context
def describe_instances(ctx, instance_id):
    Modules.ec2.describe_instances(ctx, instance_id)


@ec2.command(help='EC2 RunInstances API')
@click.option('--instance-id', type=str, help='specify instance id')
@click.pass_context
def start_instances(ctx, instance_id):
    Modules.ec2.start_instances(ctx, instance_id)


@ec2.command(help='EC2 StopInstances API')
@click.option('--instance-id', type=str, help='specify instance id')
@click.pass_context
def stop_instances(ctx, instance_id):
    Modules.ec2.stop_instances(ctx, instance_id)


@ec2.command(help='EC2 TerminateInstances API')
@click.option('--instance-id', type=str, help='specify instance id')
@click.pass_context
def terminate_instances(ctx, instance_id):
    Modules.ec2.ter_instances(ctx, instance_id)


@ec2.command(help='Amazon Linux Image List API')
@click.pass_context
def describe_ami(ctx):
    Modules.ec2.describe_ami(ctx)


@ec2.command(help='Amazon Linux Image Create API')
@click.option('--instance-id', type=str, help='input instanceid')
@click.option('--aminame', type=str, help='input aminame')
@click.pass_context
def create_ami(ctx, instance_id, aminame):
    Modules.ec2.create_ami(ctx, instance_id, aminame)


@ec2.command(help='Amazon Linux Image Delete API')
@click.option('--imageid', type=str, help='input imageid')
@click.pass_context
def delete_ami(ctx, imageid):
    Modules.ec2.delete_ami(ctx, imageid)


@rds.command(help='RDS RunInstances describe API')
@click.pass_context
def describe_instances(ctx):
    Modules.rds.describe_instances(ctx)


@rds.command(help='RDS RunInstances start API')
@click.option('--name', type=str, help='specify instance id')
@click.pass_context
def start_instances(ctx, name):
    Modules.rds.start_instances(ctx, name)


@rds.command(help='RDS RunInstances stop API')
@click.option('--name', type=str, help='specify instance id')
@click.pass_context
def stop_instances(ctx, name):
    Modules.rds.stop_instances(ctx, name)


@asg.command(help='AutoScaling Describe API')
@click.pass_context
def describe_asg(ctx):
    Modules.autoscaling.describe_asg(ctx)


@asg.command(help='AutoScaling Update Max API')
@click.option('--asgname', type=str, help='update asgname')
@click.option('--max', type=int, help='update max')
@click.pass_context
def update_max(ctx, asgname, max):
    Modules.autoscaling.update_max(ctx, asgname, max)


@asg.command(help='AutoScaling Update Min API')
@click.option('--asgname', type=str, help='update asgname')
@click.option('--min', type=int, help='update min')
@click.pass_context
def update_min(ctx, asgname, min):
    Modules.autoscaling.update_min(ctx, asgname, min)


@asg.command(help='AutoScaling Update Desire API')
@click.option('--asgname', type=str, help='update asgname')
@click.option('--desire', type=int, help='update desire')
@click.pass_context
def update_desire(ctx, asgname, desire):
    Modules.autoscaling.update_desire(ctx, asgname, desire)


@route53.command(help='Route53 API')
@click.pass_context
def describe_zones(ctx):
    Modules.route53.describe_zones(ctx)


@route53.command(help='Route53 List recoard')
@click.option('--zone-id', type=str, help='update asgname')
@click.pass_context
def describe_records(ctx, zone_id):
    Modules.route53.describe_records(ctx, zone_id)


@s3.command(help='S3 List API')
@click.pass_context
def list_buckets(ctx):
    Modules.s3.list_buckets(ctx)


if __name__ == '__main__':
    main()