# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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