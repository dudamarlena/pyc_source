# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/google/youtube/sample/youtube_videos_list.py
# Compiled at: 2020-01-08 12:53:55
# Size of source mod 2**32: 1513 bytes
import os, google_auth_oauthlib.flow, googleapiclient.discovery, googleapiclient.errors
scopes = [
 'https://www.googleapis.com/auth/youtube.readonly']

def main():
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    api_service_name = 'youtube'
    api_version = 'v3'
    client_secrets_file = 'YOUR_CLIENT_SECRET_FILE.json'
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(api_service_name,
      api_version, credentials=credentials)
    request = youtube.videos().list(part='id',
      id='EJX18Ft3-lw')
    response = request.execute()
    print(response)


if __name__ == '__main__':
    main()