# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cloudmitigator_semantic/git.py
# Compiled at: 2020-03-26 22:21:52
# Size of source mod 2**32: 3672 bytes
__doc__ = 'Object handling interactions between the command line and git.'
import os, re, yaml, cloudmitigator_semantic.utilities, cloudmitigator_semantic.version

class GitActions:
    """GitActions"""

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

    def scan_git_for_trigger_words--- This code section failed: ---

 L.  56         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_METHOD              exists
                6  LOAD_GLOBAL              os
                8  LOAD_METHOD              getcwd
               10  CALL_METHOD_0         0  ''
               12  FORMAT_VALUE          0  ''
               14  LOAD_STR                 '/semantic.yml'
               16  BUILD_STRING_2        2 
               18  CALL_METHOD_1         1  ''
               20  POP_JUMP_IF_FALSE    64  'to 64'

 L.  57        22  LOAD_GLOBAL              open
               24  LOAD_GLOBAL              os
               26  LOAD_METHOD              getcwd
               28  CALL_METHOD_0         0  ''
               30  FORMAT_VALUE          0  ''
               32  LOAD_STR                 '/semantic.yml'
               34  BUILD_STRING_2        2 
               36  CALL_FUNCTION_1       1  ''
               38  SETUP_WITH           56  'to 56'
               40  STORE_FAST               'trigger_file'

 L.  58        42  LOAD_GLOBAL              yaml
               44  LOAD_METHOD              safe_load
               46  LOAD_FAST                'trigger_file'
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'trigger_dict'
               52  POP_BLOCK        
               54  BEGIN_FINALLY    
             56_0  COME_FROM_WITH       38  '38'
               56  WITH_CLEANUP_START
               58  WITH_CLEANUP_FINISH
               60  END_FINALLY      
               62  JUMP_FORWARD         88  'to 88'
             64_0  COME_FROM            20  '20'

 L.  61        64  LOAD_STR                 'major:'
               66  LOAD_STR                 'breaking:'
               68  BUILD_LIST_2          2 

 L.  62        70  LOAD_STR                 'minor:'
               72  BUILD_LIST_1          1 

 L.  63        74  LOAD_STR                 'patch:'
               76  BUILD_LIST_1          1 

 L.  64        78  BUILD_LIST_0          0 

 L.  65        80  BUILD_LIST_0          0 

 L.  60        82  LOAD_CONST               ('major', 'minor', 'patch', 'prerelease', 'metadata')
               84  BUILD_CONST_KEY_MAP_5     5 
               86  STORE_FAST               'trigger_dict'
             88_0  COME_FROM            62  '62'

 L.  67        88  LOAD_FAST                'self'
               90  LOAD_ATTR                git_commit_message
               92  STORE_FAST               'message'

 L.  68        94  LOAD_FAST                'trigger_dict'
               96  GET_ITER         
               98  FOR_ITER            138  'to 138'
              100  STORE_FAST               'key'

 L.  69       102  LOAD_FAST                'trigger_dict'
              104  LOAD_FAST                'key'
              106  BINARY_SUBSCR    
              108  GET_ITER         
            110_0  COME_FROM           120  '120'
              110  FOR_ITER            136  'to 136'
              112  STORE_FAST               'trigger_word'

 L.  70       114  LOAD_FAST                'trigger_word'
              116  LOAD_FAST                'message'
              118  COMPARE_OP               in
              120  POP_JUMP_IF_FALSE   110  'to 110'

 L.  71       122  LOAD_FAST                'key'
              124  ROT_TWO          
              126  POP_TOP          
              128  ROT_TWO          
              130  POP_TOP          
              132  RETURN_VALUE     
              134  JUMP_BACK           110  'to 110'
              136  JUMP_BACK            98  'to 98'

Parse error at or near `BEGIN_FINALLY' instruction at offset 54

    def check_if_bump_version(self):
        """Check if version bump trigger word detected."""
        git_version = self.version
        bump_type = self.bump_type
        if bump_type is not None:
            if bump_type == 'major':
                git_version.bump_major()
            elif bump_type == 'minor':
                git_version.bump_minor()
            elif bump_type == 'patch':
                git_version.bump_patch()

    def tag_current_repo(self):
        """Tag git repo with updated version."""
        if self.version.version_changed:
            cloudmitigator_semantic.utilities.run_bash_command_return_error(f"git tag {self.version.version}")

    def get_commits_between_tags(self):
        """Create release body for Github Actions"""
        release_body = cloudmitigator_semantic.utilities.run_bash_command_return_error(f"git log {self.version.original_version}..HEAD --pretty=format:%s</br>")
        return release_body