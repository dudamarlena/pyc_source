# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/command/dependencies.py
# Compiled at: 2017-08-24 09:41:45
"""
Manage Moya package dependencies

"""
from __future__ import unicode_literals
from __future__ import print_function
from moya import jsonrpc
from moya import settings
from moya import versioning
from collections import OrderedDict
import io, requests

class DependencyError(Exception):
    pass


def gather_dependencies(rpc, app_name, mount, package, console, no_deps=False, ignore_libs=None):
    ignore_libs = ignore_libs or {}
    visited = set()
    package_stack = [(app_name, mount, package)]
    requirements = OrderedDict()
    dependancy = False
    while package_stack:
        app_name, mount, package = package_stack.pop()
        if package in visited:
            continue
        visited.add(package)
        if package in ignore_libs:
            requirements[package] = (package.rpartition(b'.')[(-1)],
             None,
             {b'name': package, 
                b'version': ignore_libs[package], 
                b'system': True})
            continue
        package_select = rpc.call(b'package.select', package=package)
        if dependancy and package_select[b'version'] is None:
            console.text((b"dependency '{}' has no installation candidate").format(package), fg=b'red')
            continue
        name_version = (b'{} {}').format(package_select[b'name'], package_select[b'version'])
        if dependancy:
            console.text((b'selected {} (dependency)').format(name_version), italic=True)
        else:
            console.text((b'selected {}').format(name_version), italic=True)
        name = package_select[b'name']
        package_select[b'system'] = False
        requirements[name] = (app_name, mount, package_select)
        if no_deps:
            break
        lib_ini_url = package_select[b'download'] + b'/lib.ini'
        lib_settings_response = requests.get(lib_ini_url, verify=False)
        lib_settings = settings.SettingsContainer.read_from_file(io.StringIO(lib_settings_response.text))

        def make_app_name(dep):
            long_name = versioning.VersionSpec(dep).name
            return long_name.split(b'.', 1)[(-1)].replace(b'.', b'')

        if b'requires' in lib_settings:
            for dep in lib_settings.get_list(b'requires', b'install', b''):
                app_name = make_app_name(dep)
                package_stack.append((app_name, None, dep))
                dependancy = True

            for dep in lib_settings.get_list(b'requires', b'mount', b''):
                app_name = make_app_name(dep)
                package_stack.append((app_name, (b'/{}/').format(app_name), dep))

    return requirements


if __name__ == b'__main__':
    from moya.console import Console
    rpc = jsonrpc.JSONRPC(b'https://packages.moyaproject.com/jsonrpc/', ssl_verify=False)
    req = gather_dependencies(rpc, b'moya.logins==0.1.1-beta', Console())
    print(req)