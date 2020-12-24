# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_paas_oracle/extension.py
# Compiled at: 2016-12-16 07:39:01
from nodeconductor.core import NodeConductorExtension

class OracleExtension(NodeConductorExtension):

    class Settings:
        ORACLE_TICKET_TEMPLATES = {'provision': {'summary': 'Request for a new Oracle instance', 
                         'details': '\n                    Oracle DB purchase details\n\n                    Customer name: {customer.name}\n                    Project name: {project.project_group.name}\n                    Environment name: {project.name}\n                    Customer UUID: {customer.uuid.hex}\n                    Project UUID: {project.project_group.uuid.hex}\n                    Environment UUID: {project.uuid.hex}\n                    OpenStack tenant id: {deployment.tenant.backend_id}\n\n                    Hardware Configuration:\n                    Name: {deployment.name}\n                    Flavor: {deployment.flavor_info}\n                    SSH key: {ssh_key.name}\n                    SSH key UUID: {ssh_key.uuid.hex}\n\n                    Oracle DB Configuration:\n                    Name: {deployment.db_name}\n                    Size: {deployment.db_size} GB / {deployment.db_arch_size} GB\n                    Version: {deployment.db_version_type}\n                    Database type: {deployment.db_template}\n                    Character set: {deployment.db_charset}\n                    Additional data: {deployment.user_data}\n                '}, 
           'undeploy': {'summary': 'Request for removing Oracle DB PaaS instance', 
                        'details': '\n                    Customer name: {customer.name}\n                    Project name: {project.project_group.name}\n                    Environment name: {project.name}\n                    Customer UUID: {customer.uuid.hex}\n                    Project UUID: {project.project_group.uuid.hex}\n                    Environment UUID: {project.uuid.hex}\n\n                    Oracle DB details:\n                    Name: {deployment.name}\n                    UUID: {deployment.uuid.hex}\n                '}, 
           'resize': {'summary': 'Request for resizing Oracle DB PaaS instance', 
                      'details': '\n                    Customer name: {customer.name}\n                    Project name: {project.project_group.name}\n                    Environment name: {project.name}\n                    Customer UUID: {customer.uuid.hex}\n                    Project UUID: {project.project_group.uuid.hex}\n                    Environment UUID: {project.uuid.hex}\n\n                    Oracle DB details:\n                    Name: {deployment.name}\n                    UUID: {deployment.uuid.hex}\n\n                    Hardware Configuration:\n                    Flavor: {deployment.flavor_info}\n                '}, 
           'support': {'summary': 'Custom support request', 
                       'details': '\n                    Customer name: {customer.name}\n                    Project name: {project.project_group.name}\n                    Environment name: {project.name}\n                    Customer UUID: {customer.uuid.hex}\n                    Project UUID: {project.project_group.uuid.hex}\n                    Environment UUID: {project.uuid.hex}\n\n                    Oracle DB details:\n                    Name: {deployment.name}\n                    UUID: {deployment.uuid.hex}\n\n                    {message}\n                '}}

    @staticmethod
    def django_app():
        return 'nodeconductor_paas_oracle'

    @staticmethod
    def rest_urls():
        from .urls import register_in
        return register_in