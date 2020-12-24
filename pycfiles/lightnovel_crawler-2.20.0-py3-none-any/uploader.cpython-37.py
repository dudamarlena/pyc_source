# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\utils\uploader.py
# Compiled at: 2019-10-17 11:50:46
# Size of source mod 2**32: 1623 bytes
"""Uploader for google drive"""
import os, logging
logger = logging.getLogger('UPLOADER')
try:
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive
except Exception:
    logger.error('`pydrive` was not setup properly')

def upload(file_path):
    try:
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile('mycreds.txt')
        if gauth.credentials is None:
            gauth.LocalWebserverAuth()
        else:
            if gauth.access_token_expired:
                gauth.Refresh()
            else:
                gauth.Authorize()
        gauth.SaveCredentialsFile('mycreds.txt')
        drive = GoogleDrive(gauth)
        folder_id = '118iN1jzavVV-9flrLPZo7DOi0cuxrQ5F'
        filename_w_ext = os.path.basename(file_path)
        filename, file_extension = os.path.splitext(filename_w_ext)
        f = drive.CreateFile({'parents': [{'kind':'drive#fileLink',  'id':folder_id}]})
        f['title'] = filename_w_ext
        f.SetContentFile(file_path)
        f.Upload()
        logger.info(f['id'])
        return f['id']
    except Exception:
        logger.exception('Failed to upload %s', file_path)