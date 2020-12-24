# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cloudmitigator_semantic/git.py
# Compiled at: 2020-03-26 22:21:52
# Size of source mod 2**32: 3672 bytes
"""Object handling interactions between the command line and git."""
import os, re, yaml, cloudmitigator_semantic.utilities, cloudmitigator_semantic.version

class GitActions:
    __doc__ = 'Object holding all git actions.'

    def __init__(self):
        """Call object methods to instantiate shared features."""
        self.git_commit_message = self.get_most_recent_commit_message()
        self.bump_type = self.scan_git_for_trigger_words()
        self.version = self.get_current_git_version_from_tag()
        self.check_if_bump_version()

    @staticmethod
    def get_current_git_version_from_tag():
        """
        Get list of all current git tags, and return the most recent one.

        :return: Version object initialized with current tag.
        """
        git_tag_list = cloudmitigator_semantic.utilities.run_bash_command_split_lines_return_error('git tag -l --sort=-v:refname')
        regex = '^v(?P<major>0|[1-9]\\d*)\\.(?P<minor>0|[1-9]\\d*)\\.(?P<patch>0|[1-9]\\d*)(?:-(?P<prerelease>(?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\\.(?:0|[1-9]\\d*|\\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\\.[0-9a-zA-Z-]+)*))?$'
        most_recent_tag = 'v0.0.0'
        for tag in git_tag_list:
            if re.search(regex, tag):
                most_recent_tag = tag
                break
            return cloudmitigator_semantic.version.Version(most_recent_tag)

    @staticmethod
    def get_most_recent_commit_message():
        """Extract git commit message from git log commands."""
        git_recent_commit = cloudmitigator_semantic.utilities.run_bash_command_return_error('git log -1')
        return git_recent_commit.lower()

    def scan_git_for_trigger_words(self):
        """Check if trigger word in commit message."""
        if os.path.exists(f"{os.getcwd()}/semantic.yml"):
            with open(f"{os.getcwd()}/semantic.yml") as (trigger_file):
                trigger_dict = yaml.safe_load(trigger_file)
        else:
            trigger_dict = {'major':[
              'major:', 'breaking:'], 
             'minor':[
              'minor:'], 
             'patch':[
              'patch:'], 
             'prerelease':[],  'metadata':[]}
        message = self.git_commit_message
        for key in trigger_dict:
            for trigger_word in trigger_dict[key]:
                if trigger_word in message:
                    return key

    def check_if_bump_version(self):
        """Check if version bump trigger word detected."""
        git_version = self.version
        bump_type = self.bump_type
        if bump_type is not None:
            if bump_type == 'major':
                git_version.bump_major()
            else:
                if bump_type == 'minor':
                    git_version.bump_minor()
                else:
                    if bump_type == 'patch':
                        git_version.bump_patch()

    def tag_current_repo(self):
        """Tag git repo with updated version."""
        if self.version.version_changed:
            cloudmitigator_semantic.utilities.run_bash_command_return_error(f"git tag {self.version.version}")

    def get_commits_between_tags(self):
        """Create release body for Github Actions"""
        release_body = cloudmitigator_semantic.utilities.run_bash_command_return_error(f"git log {self.version.original_version}..HEAD --pretty=format:%s</br>")
        return release_body