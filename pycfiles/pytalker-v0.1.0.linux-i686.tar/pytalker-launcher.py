# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pytalker/pytalker-launcher.py
# Compiled at: 2014-12-23 03:07:22
import sys, argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="pytalker - pytalker is a python module designed to wrap the TTS capabilities of the Google's TTS service. It easily implements a wrapper for the Google TTS service.", prog='pytalker-launcher.py', epilog='Note that the gst library should be installed on your system. In Debian-like OS, try: sudo apt-get install python-gst0.10')
    groupProcessing = parser.add_argument_group('Processing arguments', 'Configuring the processing parameters.')
    groupProcessing.add_argument('-l', '--languages', metavar='<language>', nargs='+', required=True, action='store', help='list of languages to be used. E. g.: en, es, fr, etc.')
    groupProcessing.add_argument('-o', '--output_folder', metavar='<path_to_output_folder>', action='store', help='path to the output folder where the results will be stored.', required=False, default='./')
    groupProcessing.add_argument('-t', '--text', metavar='<text>', action='store', nargs='+', help='text to be played between commas.', required=True)
    groupAction = parser.add_mutually_exclusive_group(required=True)
    groupAction.add_argument('-d', '--download', default=False, action='store_true', help='Downloading and playing the sound.')
    groupAction.add_argument('-s', '--say', default=False, action='store_true', help='Playing the input text.')
    groupAbout = parser.add_argument_group('About arguments', 'Showing additional information about this program.')
    groupAbout.add_argument('--version', action='version', version='%(prog)s 0.1.0', help='shows the version of the program and exists.')
    args = parser.parse_args()
    from tts import Pytalker
    for lang in args.languages:
        for text in args.text:
            if args.download:
                fName = os.path.join(args.output_folder, lang + '_' + text + '.mp3')
                Pytalker().download(text, lang=lang, filename=fName)
                Pytalker().play(fName)
            elif args.say:
                Pytalker().say(text, lang=lang)