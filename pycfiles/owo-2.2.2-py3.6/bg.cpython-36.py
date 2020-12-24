# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/owo/bg.py
# Compiled at: 2017-05-02 07:34:37
# Size of source mod 2**32: 4358 bytes
"""
owo.py background process
main use intended for mobile devices
usage: `$ owo-bg -p path -k API_KEY`
"""
from __future__ import print_function
import argparse, owo, os, sys, time, shlex, subprocess

def print_v(text):
    if args.verbose:
        print(text)


parser = argparse.ArgumentParser()
parser.add_argument('-k', '--key', help='API Key', required=True)
parser.add_argument('-p', '--path', help='Path to check file updates', default='/sdcard/pictures/screenshots/')
parser.add_argument('-u', '--url', help='Base vanity url to use', default='https://owo.whats-th.is/')
parser.add_argument('-v', '--verbose', help='Increase output verbosity', action='store_true')
parser.add_argument('-tts', help=' Confirm message over tts | Mobile only', action='store_true')
args = parser.parse_args()
sent_files = os.listdir(args.path)

def main():
    if not args.path.endswith('/'):
        args.path += '/'
    print('Starting background process...')
    while True:
        time.sleep(2)
        new_files = [f for f in os.listdir(args.path) if f not in sent_files if os.path.isfile(args.path + f)]
        if new_files == []:
            pass
        else:
            for file in new_files:
                print_v('Found file: {}'.format(file))
                try:
                    urls = list(owo.upload_files((args.key), (args.path + file), verbose=True).values())[0]
                    url = urls.get(args.url)
                    if url is None:
                        print('Vanity url base {} was not found, using default'.format(args.url))
                        url = urls['https://owo.whats-th.is/']
                except ValueError as e:
                    print('Upload failed:\n{}'.format(e.args[0]))
                    try:
                        if args.tts:
                            os.system('termux-tts-speak "Upload failed"')
                        else:
                            os.system('termux-toast "Upload failed"')
                    except:
                        pass

                except OverflowError:
                    print('File too big: {}'.format(file))
                    try:
                        if args.tts:
                            os.system('termux-tts-speak "Upload too big"')
                        else:
                            os.system('termux-toast "Upload too big"')
                    except:
                        pass

                    sent_files.append(file)
                else:
                    print_v('Upload successful.')
                    sent_files.append(file)
                if sys.executable == '/data/data/com.termux/files/usr/bin/python':
                    try:
                        subprocess.run(shlex.split('termux-notification --title "File uploaded" --content "{0}" --button1 "Copy link" --button1-action "termux-clipboard-set {0}" --button2 "Share" --button2-action "termux-open "{0}"" '.format(url)))
                        if args.tts:
                            os.system('termux-tts-speak "Upload success"')
                        else:
                            os.system('termux-toast "Upload success"')
                        print_v('Sent notification')
                    except FileNotFoundError:
                        print('File uploaded: {}, URL: {}'.format(file, url))

                else:
                    print('File uploaded: {}, URL: {}'.format(file, url))


if __name__ == '__main__':
    main()