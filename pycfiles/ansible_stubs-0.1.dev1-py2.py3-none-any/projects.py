# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/ansible/module_utils/selvpc_utils/projects.py
# Compiled at: 2018-02-16 17:30:07
from ansible.module_utils.selvpc_utils import common, wrappers

@wrappers.create_object('project')
def create_project(module, client, project_name):
    result = client.projects.create(project_name)
    changed, msg = True, ("Project '{}' has been created").format(project_name)
    return (
     result, changed, msg)


@wrappers.get_object('project')
@common.check_project_id
def get_project(module, client, project_id, project_name, show_list=False):
    if not show_list:
        return client.projects.show(project_id)
    return client.projects.list()


@wrappers.update_object
@common.check_project_id
def update_project(module, client, project_id, project_name, new_project_name):
    changed, msg = False, 'Nothing to change'
    if not common.get_project_by_name(client, new_project_name):
        client.projects.update(project_id, new_project_name)
        changed, msg = True, 'Project updated'
    else:
        msg = 'Project with such name already exists'
    return (changed, msg)


@wrappers.delete_object
@common.check_project_id
def delete_project(module, client, project_id, project_name):
    client.projects.delete(project_id)