# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/comicnamer/config_defaults.py
# Compiled at: 2010-09-01 14:23:04
__doc__ = 'Holds default config values\nModified from http://github.com/dbr/tvnamer\n'
defaults = {'select_first': False, 
   'always_rename': False, 
   'batch': False, 
   'skip_file_on_error': True, 
   'verbose': False, 
   'recursive': False, 
   'valid_extensions': [], 'windows_safe_filenames': False, 
   'normalize_unicode_filenames': False, 
   'replace_invalid_characters_with': '_', 
   'input_filename_replacements': [], 'output_filename_replacements': [], 'move_files_fullpath_replacements': [], 'move_files_enable': False, 
   'move_files_confirmation': True, 
   'move_files_destination': '.', 
   'filename_patterns': [
                       '^\\[.+?\\][ ]? # group name\n        (?P<seriesname>.*?)[ ]?[-_][ ]?          # show name, padding, spaces?\n        (?P<issuenumberstart>\\d+)              # first issue number\n        ([-_]\\d+)*                               # optional repeating issues\n        [-_](?P<issuenumberend>\\d+)            # last issue number\n        [^\\/]*$',
                       '^\\[.+?\\][ ]? # group name\n        (?P<seriesname>.*) # show name\n        [ ]?[-_][ ]?(?P<issuenumber>\\d+)\n        [^\\/]*$',
                       '\n        ^((?P<seriesname>.+?)[ \\._\\-])?          # show name\n        [Ss](?P<seasonnumber>[0-9]+)             # s01\n        [\\.\\- ]?                                 # separator\n        [Ee](?P<issuenumberstart>[0-9]+)       # first e23\n        ([\\.\\- ]+                                # separator\n        [Ss](?P=seasonnumber)                    # s01\n        [\\.\\- ]?                                 # separator\n        [Ee][0-9]+)*                             # e24 etc (middle groups)\n        ([\\.\\- ]+                                # separator\n        [Ss](?P=seasonnumber)                    # last s01\n        [\\.\\- ]?                                 # separator\n        [Ee](?P<issuenumberend>[0-9]+))        # final issue number\n        [^\\/]*$',
                       '\n        ^((?P<seriesname>.+?)[ \\._\\-])?          # show name\n        [Ss](?P<seasonnumber>[0-9]+)             # s01\n        [\\.\\- ]?                                 # separator\n        [Ee](?P<issuenumberstart>[0-9]+)       # first e23\n        ([\\.\\- ]?                                # separator\n        [Ee][0-9]+)*                             # e24e25 etc\n        [\\.\\- ]?[Ee](?P<issuenumberend>[0-9]+) # final issue num\n        [^\\/]*$',
                       '\n        ^((?P<seriesname>.+?)[ \\._\\-])?          # show name\n        (?P<seasonnumber>[0-9]+)                 # first season number (1)\n        [xX](?P<issuenumberstart>[0-9]+)       # first issue (x23)\n        ([ \\._\\-]+                               # separator\n        (?P=seasonnumber)                        # more season numbers (1)\n        [xX][0-9]+)*                             # more issue numbers (x24)\n        ([ \\._\\-]+                               # separator\n        (?P=seasonnumber)                        # last season number (1)\n        [xX](?P<issuenumberend>[0-9]+))        # last issue number (x25)\n        [^\\/]*$',
                       '\n        ^((?P<seriesname>.+?)[ \\._\\-])?          # show name\n        (?P<seasonnumber>[0-9]+)                 # 1\n        [xX](?P<issuenumberstart>[0-9]+)       # first x23\n        ([xX][0-9]+)*                            # x24x25 etc\n        [xX](?P<issuenumberend>[0-9]+)         # final issue num\n        [^\\/]*$',
                       '\n        ^((?P<seriesname>.+?)[ \\._\\-])?          # show name\n        [Ss](?P<seasonnumber>[0-9]+)             # s01\n        [\\.\\- ]?                                 # separator\n        [Ee](?P<issuenumberstart>[0-9]+)       # first e23\n        (                                        # -24 etc\n             [\\-]\n             [Ee]?[0-9]+\n        )*\n             [\\-]                                # separator\n             (?P<issuenumberend>[0-9]+)        # final issue num\n        [\\.\\- ]                                  # must have a separator (prevents s01e01-720p from being 720 issues)\n        [^\\/]*$',
                       '\n        ^((?P<seriesname>.+?)[ \\._\\-])?          # show name\n        (?P<seasonnumber>[0-9]+)                 # 1\n        [xX](?P<issuenumberstart>[0-9]+)       # first x23\n        (                                        # -24 etc\n             [\\-][0-9]+\n        )*\n             [\\-]                                # separator\n             (?P<issuenumberend>[0-9]+)        # final issue num\n        ([\\.\\- ].*                               # must have a separator (prevents 1x01-720p from being 720 issues)\n        |\n        $)',
                       '^(?P<seriesname>.+?)[ \\._\\-]          # show name and padding\n        \\[                                       # [\n            ?(?P<seasonnumber>[0-9]+)            # season\n        [xX]                                     # x\n            (?P<issuenumberstart>[0-9]+)       # issue\n            (- [0-9]+)*\n        -                                        # -\n            (?P<issuenumberend>[0-9]+)         # issue\n        \\]                                       # \\]\n        [^\\/]*$',
                       '^(?P<seriesname>.+?)[ \\._\\-]\n        [Ss](?P<seasonnumber>[0-9]{2})\n        [\\.\\- ]?\n        (?P<issuenumber>[0-9]{2})\n        [^0-9]*$',
                       '^((?P<seriesname>.+?)[ \\._\\-])?       # show name and padding\n        \\[?                                      # [ optional\n        (?P<seasonnumber>[0-9]+)                 # season\n        [xX]                                     # x\n        (?P<issuenumber>[0-9]+)                # issue\n        \\]?                                      # ] optional\n        [^\\/]*$',
                       '^((?P<seriesname>.+?)[ \\._\\-])?\n        [Ss](?P<seasonnumber>[0-9]+)[\\.\\- ]?\n        [Ee]?(?P<issuenumber>[0-9]+)\n        [^\\/]*$',
                       '\n        ^((?P<seriesname>.+?)[ \\._\\-])?         # show name\n        (?P<year>\\d{4})                          # year\n        [ \\._\\-]                                 # separator\n        (?P<month>\\d{2})                         # month\n        [ \\._\\-]                                 # separator\n        (?P<day>\\d{2})                           # day\n        [^\\/]*$',
                       '^(?P<seriesname>.+?)[ ]?[ \\._\\-][ ]?\n        [Ss](?P<seasonnumber>[0-9]+)[\\.\\- ]?\n        [Ee]?[ ]?(?P<issuenumber>[0-9]+)\n        [^\\/]*$',
                       '\n        (?P<seriesname>.+)                       # Seriesname\n        [ ]-[ ]                                  # -\n        [Ee]pisode[ ]\\d+                         # issue 1234 (ignored)\n        [ ]\n        \\[                                       # [\n        [sS][ ]?(?P<seasonnumber>\\d+)            # s 12\n        ([ ]|[ ]-[ ]|-)                          # space, or -\n        ([eE]|[eE]p)[ ]?(?P<issuenumber>\\d+)   # e or ep 12\n        \\]                                       # ]\n        .*$                                      # rest of file\n        ',
                       '^(?P<seriesname>.+)[ \\._\\-]\n        (?P<seasonnumber>[0-9]{1})\n        (?P<issuenumber>[0-9]{2})\n        [\\._ -][^\\/]*$',
                       '^(?P<seriesname>.+)[ \\._\\-]\n        (?P<seasonnumber>[0-9]{2})\n        (?P<issuenumber>[0-9]{2,3})\n        [\\._ -][^\\/]*$',
                       '^(?P<seriesname>.+?)                  # Series name\n        [ \\._\\-]                                 # Padding\n        [Ee](?P<issuenumber>[0-9]+)            # E123\n        [\\._ -][^\\/]*$                          # More padding, then anything\n        '], 
   'filename_with_issue': '%(seriesname)s - [%(seasonno)02dx%(issue)s] - %(issuename)s%(ext)s', 
   'filename_without_issue': '%(seriesname)s - [%(seasonno)02dx%(issue)s]%(ext)s', 
   'filename_with_issue_no_season': '%(seriesname)s - [%(issue)s] - %(issuename)s%(ext)s', 
   'filename_without_issue_no_season': '%(seriesname)s - [%(issue)s]%(ext)s', 
   'multiiss_join_name_with': ', ', 
   'issue_single': '%02d', 
   'issue_separator': '-'}