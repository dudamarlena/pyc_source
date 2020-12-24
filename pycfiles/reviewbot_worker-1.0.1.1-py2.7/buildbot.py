# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/reviewbot/tools/buildbot.py
# Compiled at: 2018-07-31 04:26:56
from __future__ import unicode_literals
from reviewbot.tools import Tool
from reviewbot.utils.process import execute

class BuildBotTool(Tool):
    """Review Bot tool to do a build using `buildbot try`."""
    name = b'BuildBot try'
    version = b'1.0'
    description = b'Runs the buildbot try command and posts the result of the build.'
    options = [
     {b'name': b'address', 
        b'field_type': b'django.forms.CharField', 
        b'default': None, 
        b'field_options': {b'label': b'Buildmaster Address', 
                           b'help_text': b'The address of the buildmaster. Used by both PB and SSH.', 
                           b'required': True}},
     {b'name': b'connect_method', 
        b'field_type': b'django.forms.ChoiceField', 
        b'field_options': {b'label': b'Connect Method', 
                           b'help_text': b'Connection method used by buildbot to contact the try server.', 
                           b'required': True, 
                           b'choices': (
                                      ('PB', 'PB authentication'),
                                      ('SSH', 'SSH authentication'))}},
     {b'name': b'port', 
        b'field_type': b'django.forms.CharField', 
        b'default': None, 
        b'field_options': {b'label': b'Port', 
                           b'help_text': b'Port used to communicate with buildbot. Not the the ssh connection port.', 
                           b'required': False}},
     {b'name': b'username', 
        b'field_type': b'django.forms.CharField', 
        b'default': None, 
        b'field_options': {b'label': b'Username', 
                           b'help_text': b'Username, used by both PB and SSH authentication.', 
                           b'required': True}},
     {b'name': b'password', 
        b'field_type': b'django.forms.CharField', 
        b'default': None, 
        b'field_options': {b'label': b'PB Password', 
                           b'help_text': b'PB Password: Stored as plaintext in database. Use with extreme caution.', 
                           b'required': False}},
     {b'name': b'jobdir', 
        b'field_type': b'django.forms.CharField', 
        b'default': None, 
        b'field_options': {b'label': b'Job directory', 
                           b'help_text': b'SSH Job dir: Directory chosen in buildbot config to be writeable by all allowed users.', 
                           b'required': False}},
     {b'name': b'pblistener', 
        b'field_type': b'django.forms.CharField', 
        b'default': None, 
        b'field_options': {b'label': b'PB listener port', 
                           b'help_text': b'Required when using SSH. Indicate port used to check build status.', 
                           b'required': False}},
     {b'name': b'buildbotbin', 
        b'field_type': b'django.forms.CharField', 
        b'default': None, 
        b'field_options': {b'label': b'buildbot binary location', 
                           b'help_text': b"SSH buildbot binary location: path to buildbot if not in user's path. For use with virtualenv.", 
                           b'required': False}},
     {b'name': b'use_branch', 
        b'field_type': b'django.forms.BooleanField', 
        b'default': False, 
        b'field_options': {b'label': b'Use Branch Field', 
                           b'help_text': b'Tell BuildBot to use the contents of the branch field in the review request. WARNING: this field is free-form and may not contain a valid branch name.', 
                           b'required': False}},
     {b'name': b'default_branch', 
        b'field_type': b'django.forms.CharField', 
        b'field_options': {b'label': b'Default Branch', 
                           b'help_text': b'Default branch to build off of. Uses master by default.', 
                           b'required': False}},
     {b'name': b'builder', 
        b'field_type': b'django.forms.CharField', 
        b'field_options': {b'label': b'Builder', 
                           b'help_text': b'Comma-separated list of builders to use. Required when using SSH.', 
                           b'required': False}}]

    def execute(self, review, settings={}, repository=None, base_commit_id=None):
        """Perform a review using the tool.

        Args:
            review (reviewbot.processing.review.Review):
                The review object.

            settings (dict):
                Tool-specific settings.

            repository (reviewbot.repositories.Repository):
                The repository.

            base_commit_id (unicode):
                The ID of the commit that the patch should be applied to.
        """
        cmd = [
         b'buildbot',
         b'try',
         b'--wait',
         b'--quiet',
         b'--diff=%s' % review.get_patch_file_path(),
         b'--patchlevel=1',
         b'--username=%s' % settings[b'username'],
         b'--master=%s:%s' % (settings[b'address'],
          settings[b'port'])]
        branch = review.api_root.get_review_request(review_request_id=review.request_id).branch
        if branch != b'' and settings[b'use_branch']:
            cmd.append(b'--branch=%s' % branch)
        elif b'default_branch' in settings:
            cmd.append(b'--branch=%s' % settings[b'default_branch'])
        if settings[b'connect_method'] == b'PB':
            cmd.extend([
             b'--connect=pb',
             b'--passwd=%s' % settings[b'password']])
        else:
            cmd.extend([
             b'--connect=ssh',
             b'--jobdir=%s' % settings[b'jobdir'],
             b'--host=%s' % settings[b'address']])
            for builder in settings[b'builders'].split(b','):
                cmd.append(b'--builder=%s' % builder.strip())

        if settings[b'buildbotbin'] != b'':
            cmd.append(b'--buildbotbin=%s' % settings[b'buildbotbin'])
        review.body_top = execute(cmd, ignore_errors=True)