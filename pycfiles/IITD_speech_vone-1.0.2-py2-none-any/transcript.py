# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ravijayanth/Desktop/project/library/Transcript/transcript.py
# Compiled at: 2019-11-10 06:55:03
"""
First we need to have all the audio in Google storage. 
This code shows how to send all of the wav files to a bucket. 
"""
from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials
import json, glob, re, os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

def upload(bucket_name, bucket_folder, key_json, folder):
    with open(key_json) as (credentials_dict):
        credentials_dict = json.load(credentials_dict)
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict)
    client = storage.Client(credentials=credentials, project=bucket_name)
    files = glob.glob(folder + '/*.wav')
    bucket = client.get_bucket(bucket_name)
    for f in sorted(files):
        f_new = f.split('/')
        f_new = f_new[(len(f_new) - 1)]
        blob = bucket.blob(bucket_folder + '/' + f_new)
        try:
            blob.upload_from_filename(f)
        except:
            print 'already there'


def getTranscriptFromgcsuri(gcs_uri, outputfile, key_json):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_json
    client = speech.SpeechClient()
    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16, language_code='hi-IN')
    operation = client.long_running_recognize(config, audio)
    print 'Waiting for operation to complete...'
    response = operation.result(timeout=2000)
    file1 = open(outputfile, 'w')
    for result in response.results:
        x = result.alternatives[0].transcript
        file1.write(x.encode('utf-8'))
        file1.write(' ')

    file1.close()


def get_transcript(bucket_name, bucket_folder, key_json, folder):
    filenames = glob.glob(folder + '/*.wav')
    if not os.path.exists(folder + '_transcripts'):
        os.mkdir(folder + '_transcripts')
    for fname in filenames:
        fname_new = fname.split('/')
        fname_new = fname_new[(len(fname_new) - 1)]
        gcs_uri = 'gs://' + bucket_name + '/' + bucket_folder + '/' + fname_new
        transcript_filename = folder + '_transcripts/' + fname_new.split('.')[0] + '.txt'
        print transcript_filename
        if not os.path.exists(transcript_filename):
            getTranscriptFromgcsuri(gcs_uri, transcript_filename, key_json)