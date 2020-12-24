# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/testing/run.py
# Compiled at: 2018-12-15 13:03:34
# Size of source mod 2**32: 1263 bytes
import asyncio, os
from speech import Amazon, Azure, Sphinx, DeepSpeech, play_audio, settings
speech_service = settings['service']
audio_dir = 'audio_files'
post_play_audio = True

async def solve(service, audio_file):
    answer = None
    service = service.lower()
    if service in ('azure', 'pocketsphinx', 'deepspeech'):
        if service == 'azure':
            speech = Azure()
        else:
            if service == 'pocketsphinx':
                speech = Sphinx()
            else:
                speech = DeepSpeech()
        answer = await speech.get_text(audio_file)
    else:
        speech = Amazon()
        answer = await speech.get_text(audio_file)
    if answer:
        print(f"audio file: {audio_file}")
        print(f"{service}'s best guess: {answer}")
    else:
        print(f"{service}'s failed to decipher: {audio_file}")
    if post_play_audio:
        await play_audio(audio_file)
    print('------------------------------------------------------------------------------------------------------------------------')


async def main():
    for dirs, subdirs, files in os.walk(audio_dir):
        for fname in files:
            ext = os.path.splitext(fname)[(-1)].lower()
            if ext == '.mp3':
                fpath = os.path.join(audio_dir, fname)
                await solve(speech_service, fpath)


asyncio.get_event_loop().run_until_complete(main())