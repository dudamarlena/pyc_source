# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x0ox/Dropbox/ActiveDev/yac/yac/lib/container/config.py
# Compiled at: 2017-11-16 20:28:41
import os, json, jmespath

def env_ec2_to_api(taskdef_envs):
    env_map = {}
    for env in taskdef_envs:
        env_map[env['Name']] = env['Value']

    return env_map


def get_volumes_map(taskdef_volumes, taskdef_mountPoints):
    volume_map = {}
    volume_bindings = []
    for volume in taskdef_volumes:
        cp_search_str = "[?SourceVolume=='%s'].ContainerPath" % volume['Name']
        ro_search_str = "[?SourceVolume=='%s'].ReadOnly" % volume['Name']
        bind_path = jmespath.search(cp_search_str, taskdef_mountPoints)
        read_only = jmespath.search(ro_search_str, taskdef_mountPoints)
        if len(bind_path) == 1 and len(read_only) == 1:
            volume_bindings.append(volume['Host']['SourcePath'])
            volume_map[volume['Host']['SourcePath']] = {'bind': jmespath.search(cp_search_str, taskdef_mountPoints)[0], 
               'ro': jmespath.search(ro_search_str, taskdef_mountPoints)[0]}

    return (
     volume_map, volume_bindings)


def get_port_bindings(taskdef_port_mappings):
    port_binding = {}
    for port_mapping in taskdef_port_mappings:
        port_binding[str(port_mapping['ContainerPort'])] = str(port_mapping['HostPort'])

    return port_binding


def get_aliases(taskdef_configs):
    return jmespath.search('ContainerDefinitions[*].name', taskdef_configs)


def find_image_tag(name_tag, stack_template):
    image_tag = ''
    container_defs = get_container_defs(stack_template)
    image_tags = jmespath.search("[?Name=='%s'].Image" % name_tag, container_defs)
    if len(image_tags) == 1:
        image_tag = image_tags[0]
    return image_tag


def get_container_envs(name_tag, stack_template):
    env_variables = []
    container_defs = get_container_defs(stack_template)
    ecs_env = jmespath.search("[?Name=='%s'].Environment" % name_tag, container_defs)
    if len(ecs_env) == 1:
        env_variables = env_ec2_to_api(ecs_env[0])
    return env_variables


def get_container_names(stack_template):
    container_names = []
    container_defs = get_container_defs(stack_template)
    container_names = jmespath.search('[*].Name', container_defs)
    return container_names


def get_container_volumes(name_tag, stack_template):
    app_taskdefs = get_task_defs(name_tag, stack_template)
    all_volumes = jmespath.search('Properties.Volumes', app_taskdefs)
    mount_points = jmespath.search("Properties.ContainerDefinitions[?Name=='%s'].MountPoints" % name_tag, app_taskdefs)[0]
    volumes_map, volumes_bindings = get_volumes_map(all_volumes, mount_points)
    return (
     volumes_map, volumes_bindings)


def get_container_ports(name_tag, stack_template):
    port_bindings = []
    container_defs = get_container_defs(stack_template)
    port_mappings = jmespath.search("[?Name=='%s'].PortMappings" % name_tag, container_defs)[0]
    port_bindings = get_port_bindings(port_mappings)
    return port_bindings


def get_task_defs(name_tag, stack_template):
    task_defs = {}
    if 'Resources' in stack_template:
        resources = stack_template['Resources']
        resource_keys = resources.keys()
        for resource_key in resource_keys:
            if resources[resource_key]['Type'] == 'AWS::ECS::TaskDefinition':
                container_defs = resources[resource_key]['Properties']['ContainerDefinitions']
                image_tags = jmespath.search("[?Name=='%s'].Image" % name_tag, container_defs)
                if len(image_tags) == 1:
                    task_defs = resources[resource_key]

    return task_defs


def get_container_defs(stack_template):
    container_defs = []
    if 'Resources' in stack_template:
        resources = stack_template['Resources']
        resource_keys = resources.keys()
        for resource_key in resource_keys:
            if resources[resource_key]['Type'] == 'AWS::ECS::TaskDefinition':
                container_defs = container_defs + resources[resource_key]['Properties']['ContainerDefinitions']

    return container_defs