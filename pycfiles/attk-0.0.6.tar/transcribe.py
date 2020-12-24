# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: attk/transcribe.py
# Compiled at: 2017-06-03 23:43:08
import sys, getopt, os, array, random, speech_recognition as sr, subprocess
from time import gmtime, strftime

def transcribe(inputfile, outputfile='', to_txt=True):
    wav_source = True
    if inputfile.lower()[-4:] != '.wav':
        wav_source = False
        temp_filename = inputfile.split('/')[(-1)] + '_temp.wav'
        wav_path = '/var/tmp/' + temp_filename
        subprocess.call(['ffmpeg', '-y', '-i', inputfile, wav_path])
    else:
        wav_path = inputfile
    transcript = ''
    r = sr.Recognizer()
    with sr.AudioFile(wav_path) as (source):
        audio = r.record(source)
    try:
        print 'Processing ...'
        transcript = r.recognize_sphinx(audio)
    except sr.UnknownValueError:
        print 'Sphinx error: No speech detected.'
    except sr.RequestError as e:
        print ('Sphinx error; {0}').format(e)

    if wav_source == False:
        os.remove(wav_path)
    if to_txt == True:
        if outputfile == '':
            outputfile = inputfile[:-4] + '.pocketsphinx.txt'
        with open(outputfile, 'w') as (fo):
            fo.write(transcript)
        return transcript
    else:
        return transcript


def main(argv):
    inputfile = ''
    outputfile = ''
    to_txt = True
    try:
        opts, args = getopt.getopt(argv, 'hi:o:t', ['ifile=', 'ofile='])
    except getopt.GetoptError:
        print "FindApplause.py -i <inputfile> -o <outputfile> -p'"
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'FindApplause.py -i <inputfile> -o <outputfile> -p'
            sys.exit()
        elif opt in ('-i', '--ifile'):
            inputfile = arg.strip('"')
        elif opt in ('-o', '--ofile'):
            outputfile = arg
            to_txt = True

    if ('-t' in sys.argv[1:]) | ('--txt' in sys.argv[1:]):
        to_txt = True
    if ('.mp3' in inputfile.lower()) | ('.wav' in inputfile.lower()) | ('.mp4' in inputfile.lower()):
        transcript = transcribe(inputfile, outputfile, to_txt)
        print transcript
    elif os.path.isdir(sys.argv[(-1)]):
        media_dir = sys.argv[(-1)]
        media_paths = [ os.path.join(media_dir, item) for item in os.listdir(media_dir) if item[-4:].lower() in ('.mp3',
                                                                                                                 '.wav',
                                                                                                                 '.mp4') ]
        for pathname in media_paths:
            transcript = transcribe(pathname, outputfile, to_txt)
            print transcript + '\n'
            print transcript + '\n\n'


if __name__ == '__main__':
    main(sys.argv[1:])