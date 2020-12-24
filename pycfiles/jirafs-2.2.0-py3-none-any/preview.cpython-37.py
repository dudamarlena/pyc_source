# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acoddington/Documents/Projects/jirafs/jirafs/commands/preview.py
# Compiled at: 2020-01-09 12:39:47
# Size of source mod 2**32: 2992 bytes
import json, os, tempfile, webbrowser
from jirafs.plugin import CommandPlugin

class Command(CommandPlugin):
    __doc__ = ' Preview your Jira wiki markup '
    MIN_VERSION = '2.0.0'
    MAX_VERSION = '3.0.0'

    def add_arguments(self, parser):
        parser.add_argument('--output',
          '-o',
          help='Instead of opening a preview in your browser, write HTML output to the specified path.')
        parser.add_argument('field_name')

    def handle(self, args, folder, **kwargs):
        return self.cmd(folder, (args.field_name), output=(args.output))

    def get_comments(self, folder):
        lines = []
        for comment in folder.issue.fields.comment.comments:
            lines.append('h3. At %s, %s wrote:\n' % (
             comment.created,
             comment.author))
            lines.append(comment.body.replace('\r\n', '\n'))

        return '\n'.join(lines)

    def main(self, folder, field_name, output=None, **kwargs):
        special_fields = {'new_comment':folder.get_new_comment, 
         'comments':lambda : self.get_comments(folder)}
        if field_name in special_fields:
            data = special_fields[field_name]()
        else:
            data = folder.get_field_value_by_dotpath(field_name)
        url = folder.jira._get_url('../1.0/render')
        response = folder.jira._session.post(url,
          headers={'Accept': 'text/html, */*; q=0.01'},
          data=(json.dumps({'issueKey':folder.ticket_number, 
         'rendererType':'atlassian-wiki-renderer', 
         'unrenderedMarkup':data})))
        if output:
            with open(os.path.expanduser(output), 'w') as (outf):
                outf.write(response.text)
        else:
            with tempfile.NamedTemporaryFile('w', suffix='.html') as (outf):
                outf.write('\n                    <html>\n                        <style type="text/css">\n                            body {\n                                font-family: sans-serif;\n                            }\n                            table {\n                                border-collapse: collapse;\n                            }\n                            table, th, td {\n                                border: 1px solid black;\n                            }\n                        </style>\n                        <body>\n                ')
                outf.write(response.text)
                outf.write('\n                        </body>\n                    </html>\n                ')
                outf.flush()
                webbrowser.open(outf.name)
                input('Press <Enter> to continue')