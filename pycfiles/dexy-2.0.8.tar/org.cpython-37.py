# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/filters/org.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 1312 bytes
from dexy.filters.process import SubprocessFilter
import dexy.exceptions

class OrgModeFilter(SubprocessFilter):
    __doc__ = '\n    Convert .org files to other formats.\n    '
    aliases = ['org']
    _settings = {'executable':'emacs', 
     'output':True, 
     'input-extensions':[
      '.org', '.txt'], 
     'output-extensions':[
      '.txt', '.html', '.tex', '.pdf', '.odt'], 
     'command-string':'%(prog)s --batch %(args)s --eval "(progn \\\n(find-file \\"%(script_file)s\\") \\\n(%(export_command)s 1) \\\n(kill-buffer) \\\n)"\n'}

    def command_string_args(self):
        if self.ext == '.txt':
            export_command = 'org-export-as-ascii'
        else:
            if self.ext == '.html':
                export_command = 'org-export-as-html'
            else:
                if self.ext == '.tex':
                    export_command = 'org-export-as-latex'
                else:
                    if self.ext == '.pdf':
                        export_command = 'org-export-as-pdf'
                    else:
                        if self.ext == '.odt':
                            export_command = 'org-export-as-odt'
                        else:
                            msg = 'unsupported extension %s'
                            msgargs = self.ext
                            raise dexy.exceptions.InternalDexyProblem(msg % msgargs)
        args = self.default_command_string_args()
        args['export_command'] = export_command
        return args