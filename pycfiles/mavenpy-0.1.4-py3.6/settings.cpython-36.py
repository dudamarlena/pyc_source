# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mavenpy/settings.py
# Compiled at: 2020-02-06 03:54:37
# Size of source mod 2**32: 3113 bytes
import os, pystache

class MavenSettingsGenerator(object):

    def __init__(self, location=None, repositories=None, mirrors=None):
        self.location = location or MavenSettingsGenerator.user_settings_location()
        self.repositories = repositories or []
        self.mirrors = mirrors or []

    def generate(self):
        profileDict = {}
        for repo in self.repositories:
            profileId, repoId, url, layout, releases, snapshots, plugins = repo
            if profileId not in profileDict:
                profileDict[profileId] = []
            profileDict[profileId].append({'id':repoId, 
             'url':url, 
             'layout':layout, 
             'releases':str(releases).lower(), 
             'snapshots':str(snapshots).lower(), 
             'plugins':plugins})

        profileObjects = []
        for profileId, repos in profileDict.items():
            profileObjects.append({'profileId':profileId,  'repos':repos})

        mirrorObjects = []
        for mirror in self.mirrors:
            mirrorId, url, mirrorOf = mirror
            mirrorObjects.append({'id':mirrorId,  'url':url,  'mirrorOf':mirrorOf})

        settingsTemplate = '<?xml version="1.0" ?>\n  <settings xmlns="http://maven.apache.org/SETTINGS/1.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n  xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">\n    <profiles>\n      {{#profiles}}\n      <profile>\n        <id>{{profileId}}</id>\n        <activation>\n          <activeByDefault>true</activeByDefault>\n        </activation>\n        <repositories>\n          {{#repos}}\n          <repository>\n            <id>{{id}}</id>\n            <url>{{url}}</url>\n            {{#layout}}<layout>{{layout}}</layout>\n            {{/layout}}<releases>\n              <enabled>{{releases}}</enabled>\n            </releases>\n            <snapshots>\n              <enabled>{{snapshots}}</enabled>\n            </snapshots>\n          </repository>\n          {{/repos}}\n        </repositories>\n        <pluginRepositories>\n          {{#repos}}{{#plugins}}<pluginRepository>\n            <id>{{id}}</id>\n            <url>{{url}}</url>\n            {{#layout}}<layout>{{layout}}</layout>\n            {{/layout}}<releases>\n              <enabled>{{releases}}</enabled>\n            </releases>\n            <snapshots>\n              <enabled>{{snapshots}}</enabled>\n            </snapshots>\n          </pluginRepository>{{/plugins}}{{/repos}}\n        </pluginRepositories>\n      </profile>\n      {{/profiles}}\n    </profiles>\n    <mirrors>\n      {{#mirrors}}\n      <mirror>\n        <id>{{id}}</id>\n        <url>{{url}}</url>\n        <mirrorOf>{{mirrorOf}}</mirrorOf>\n      </mirror>\n      {{/mirrors}}\n    </mirrors>\n  </settings>\n  '
        settingsXml = pystache.render(settingsTemplate, {'profiles':profileObjects,  'mirrors':mirrorObjects})
        print('Setting contents of {} to:\n{}'.format(self.location, settingsXml))
        with open(self.location, 'w') as (settingsFile):
            settingsFile.write(settingsXml)

    @staticmethod
    def user_settings_location():
        return os.path.join(os.path.expanduser('~'), '.m2/settings.xml')