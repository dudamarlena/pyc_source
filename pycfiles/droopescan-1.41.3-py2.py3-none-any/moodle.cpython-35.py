# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/droopescan/dscan/plugins/moodle.py
# Compiled at: 2019-06-14 01:34:00
# Size of source mod 2**32: 2182 bytes
from cement.core import handler, controller
from dscan import common
from dscan.plugins import BasePlugin
import dscan.common.update_api as ua

class Moodle(BasePlugin):
    __doc__ = '\n    Moodle scanning implementation. Thanks to @fede2cr.\n    '
    plugins_base_url = ['%smod/%s/']
    themes_base_url = ['%stheme/%s/']
    forbidden_url = 'cache/'
    regular_file_url = ['lib/javascript-static.js']
    module_common_file = 'version.php'
    update_majors = ['2.7', '2.9', '3.0', '3.1', '3.2', '3.3']
    interesting_urls = [
     ('tags.txt', 'A doc about creating tags.'),
     ('README.txt', 'Static readme file.'),
     ('login/', 'Admin panel')]
    interesting_module_urls = [
     ('README.txt', 'Readme text file'),
     ('upgrade.txt', 'Upgrade text file'),
     ('readme.txt', 'Readme file (lowercase)'),
     ('README.md', 'Readme markdown file'),
     ('version.php', 'Version file')]

    class Meta:
        label = 'moodle'

    @controller.expose(help='Moodle scanner')
    def moodle(self):
        self.plugin_init()

    def update_version_check(self):
        """
        @return: True if new versions of this software have been found.
        """
        return ua.github_tags_newer('moodle/moodle/', self.versions_file, update_majors=self.update_majors)

    def update_version(self):
        """
        @return: updated VersionsFile
        """
        gr, versions_file, new_tags = ua.github_repo_new('moodle/moodle/', 'moodle/moodle', self.versions_file, self.update_majors)
        hashes = {}
        for version in new_tags:
            gr.tag_checkout('v' + version)
            hashes[version] = gr.hashes_get(versions_file)

        versions_file.update(hashes)
        return versions_file

    def update_plugins_check(self):
        pass

    def update_plugins(self):
        """
        This function needs to return two updated lists containing plugins
        and themes. There are APIs on common.update_api which can be used.
        @return: (plugins, themes)
        """
        pass


def load(app=None):
    handler.register(Moodle)