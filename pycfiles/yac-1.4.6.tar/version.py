# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x0ox/Dropbox/ActiveDev/yac/yac/lib/version.py
# Compiled at: 2017-11-16 20:28:41
import requests, jmespath

def get_latest_version(app, container_org, registry_url='https://registry.hub.docker.com'):
    endpoint_uri = '/v2/repositories/%s/%s/tags' % (container_org, app)
    endpoint_response = requests.get(registry_url + endpoint_uri)
    versions = jmespath.search('results[*].name', endpoint_response.json())
    latest_version = 'not found!'
    if versions:
        versions = [ str(i) for i in versions ]
        latest_version = ''
        if versions and len(versions) >= 1:
            if 'latest' in versions:
                latest_version = 'latest'
            else:
                versions.sort()
                latest_version = versions[(-1)]
    return str(latest_version)


def get_app_version(app_alias, my_service_descriptor):
    app_version = ''
    search_str = "task-definition.containerDefinitions[?name=='%s'].image" % app_alias
    images_found = jmespath.search(search_str, my_service_descriptor)
    if images_found and len(images_found) == 1:
        app_version = str(images_found[0]).split(':')[(-1)]
    return app_version


def return_latest(version1, version2):
    v1, v2 = version1.split('.'), version2.split('.')
    if len(v1) > len(v2):
        v2 += [ '0' for _ in xrange(len(v1) - len(v2)) ]
    else:
        if len(v1) < len(v2):
            v1 += [ '0' for _ in xrange(len(v2) - len(v1)) ]
        latest = ''
        i = 0
        while i < len(v1):
            if v1[i].isdigit() and v2[i].isdigit() and int(v1[i]) > int(v2[i]):
                latest = version1
                break
            elif v1[i].isdigit() and v2[i].isdigit() and int(v1[i]) < int(v2[i]):
                latest = version2
                break
            else:
                i += 1

    return latest


def is_same(version1, version2):
    v1, v2 = version1.split('.'), version2.split('.')
    if len(v1) > len(v2):
        v2 += [ '0' for _ in xrange(len(v1) - len(v2)) ]
    else:
        if len(v1) < len(v2):
            v1 += [ '0' for _ in xrange(len(v2) - len(v1)) ]
        same = True
        i = 0
        while i < len(v1):
            if v1[i].isdigit() and v2[i].isdigit() and int(v1[i]) == int(v2[i]):
                same = same and True
            else:
                same = same and False
            i += 1

    return same


def is_first_arg_latest(version1, version2):
    version = return_latest(version1, version2)
    if version == version1:
        return True
    else:
        if version == version2:
            return False
        return False


def is_a_version(version):
    v1 = version.split('.')
    is_version = True
    i = 0
    while i < len(v1):
        if not v1[i].isdigit():
            is_version = False
            break
        else:
            i += 1

    return is_version