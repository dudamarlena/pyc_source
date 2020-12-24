# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryosukekita/Desktop/PROJECTS/DSVISUALIZER/aefiles/scripts/talk_with_google.py
# Compiled at: 2017-10-27 18:08:28
"""
DESCRIPTION: Functions to talk with google app engine from local.

NOTES:
    - Make sure the os environment flag is not operating. 
"""
import os

def gsutil_cp_rsync_file_to_cloud_storage(filePathIn, filePathOut, singleFile=False):
    """
    DESCRIPTION: 
        - Creates a directory for the files in the app default bucket. 
        - Can copy an entire directory at a time. 
        - rsyncs if singleFile=False
        - copies if singleFile=True
    
    USES:
        - During the initial setup of the webapp - copying the figures from local directories to cloud storage.
    
    NOTES:
        - Use a multithreaded approach.
        - Files will be copied with rsync
        - To overwrite - one must include -d as an option?
        - #Instead of copying directories at a time, it might be better if we just copy the files that we are interested in. 
    """
    if singleFile:
        cmd = [
         'gsutil', 'cp', filePathIn, filePathOut]
    else:
        cmd = [
         'gsutil', '-m', 'rsync', '-r', filePathIn, filePathOut]
    print cmd
    os.system((' ').join(cmd))