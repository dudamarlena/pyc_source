# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jceciliano/Documents/coding/lantern/lantern-cli/.virtualenv/lib/python3.6/site-packages/lantern_cli/cli.py
# Compiled at: 2019-05-22 19:56:04
# Size of source mod 2**32: 1233 bytes
import click
from lantern_cli import settings
from lantern_cli import templates
from lantern_cli import dynamodb

@click.group()
def cli():
    """
    \x08
             * * * * * * * * * * * * * * *
             *                           * 
             *    Lantern Engine CLI     * 
             *                           *
             * * * * * * * * * * * * * * *
        \x08
    This tool is for internal user
    in Lantern.tech.
    \x08
    "Happy Coding!"
    """
    pass


@cli.command()
def createservice():
    """Create a new Serverless (Zappa) based microservice
        Usage:
        
                 lantern-cli createservice [SERVICE_NAME]
    """
    templates.startapp(template=(settings.MICROSERVICE_ZAPPA_TEMPLATE_repo))


@cli.command()
def createservice_docker():
    """Create a new Docker Based MicroService project 

           Check the generated README file (project root) for docker instructions. 

           Usage:
           
                 lantern-cli createservice_docker [SERVICE_NAME]
        """
    templates.startapp(template=(settings.MICROSERVICE_DOCKER_TEMPLATE_repo))


@cli.command()
def dynamodb_delete():
    """Interface for quering, validate and confirm data from dynamodb
           Usage:
           
                 lantern-cli dynamodb_delete
        """
    dynamodb.delete_method()