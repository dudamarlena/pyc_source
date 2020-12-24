# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.7/site-packages/cfndeployer.py
# Compiled at: 2019-04-18 12:20:33
# Size of source mod 2**32: 220 bytes
import click
from cfn import CfnDeploy

@click.command()
def main():
    with open('.cfndeployrc') as (f):
        config = f.read()
        cfn_deploy = CfnDeploy()
        cfn_deploy.deploy_stacks()


if __name__ == '__main__':
    main()