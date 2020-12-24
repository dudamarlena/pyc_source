# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/messenger/slack/methods/files/upload.py
# Compiled at: 2020-01-06 01:07:42
# Size of source mod 2**32: 822 bytes
import os
from foxylib.tools.file.file_tool import FileTool
from foxylib.tools.messenger.slack.slack_tool import SlackFiletype

class FilesUploadMethod:

    @classmethod
    def invoke(cls, web_client, channel, filepath):
        mimetype = FileTool.filepath2mimetype(filepath)
        filetype = SlackFiletype.mimetype2filetype(mimetype)
        j_files_upload_in = {'channels':channel, 
         'file':filepath, 
         'filename':os.path.basename(filepath), 
         'filetype':filetype}
        response = (web_client.files_upload)(**j_files_upload_in)
        return response

    @classmethod
    def j_response2j_file(cls, j_response):
        return j_response.get('file')