# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dsupplee/dev/apis-client-generator/src/googleapis/codegen/utilities/maven_utils.py
# Compiled at: 2019-01-24 16:56:47
"""Maven-related utilities for java packages."""
import re

def GetMavenArtifactId(api_name, package_path='', canonical_name='', owner_domain='google.com'):
    """Returns the maven artifact id for a given api.

  Args:
    api_name:  (str) The api name.
    package_path: (str|None) The package path, if any.
    canonical_name: (str|None) The canonical api name, if any.
    owner_domain: (str) The api's owner domain.
  Returns:
    (str) The artifact id.
  """
    if package_path and canonical_name:
        api_name = canonical_name.lower().replace(' ', '')
    parts = []
    if owner_domain == 'google.com':
        parts.extend(['google', 'api', 'services'])
    if package_path:
        parts.extend(re.split('\\.|/', package_path))
    parts.append(api_name)
    return ('-').join(parts)


def GetMavenGroupId(owner_domain):
    """Returns the maven group id for a given owner domain.

  Args:
    owner_domain: (str) The owner domain.
  Returns:
    (str) The group id.
  """
    if owner_domain == 'google.com':
        return 'com.google.apis'
    else:
        return ('.').join(reversed(owner_domain.split('.')))


def GetMavenVersion(api, language_version):
    """Returns the maven version."""
    if api.get('ownerDomain') == 'google.com':
        return '%s-rev%s-%s' % (api['version'],
         api['revision'],
         language_version)
    return '%s-%s-SNAPSHOT' % (api['version'], language_version)


def GetMavenMetadata(api, language_version):
    """Returns a dict of useful maven metadata."""
    owner_domain = api.get('ownerDomain', 'google.com')
    return {'artifact_id': GetMavenArtifactId(api['name'], api.get('packagePath'), api.get('canonicalName'), owner_domain), 
       'group_id': GetMavenGroupId(owner_domain), 
       'version': GetMavenVersion(api, language_version)}