# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/microcsound/main.py
# Compiled at: 2017-11-27 14:11:10
# Size of source mod 2**32: 8820 bytes
from readline import *
from sys import stdin, stdout, argv
from os import system
import re, argparse
from microcsound import constants
from microcsound.parser import parser, PARSER_PATTERN
from microcsound.state import state_obj
__all__ = [
 'process_buffer', 'live_loop_in', 'main']

def process_buffer(inbuffer, rt_mode=False):
    """ split the whole string buffer into individual voice lines
    and feed each line to the event parser """
    lines = inbuffer.splitlines()
    voiceline = 1
    current_string = '%i:' % voiceline
    while re.search(current_string, inbuffer):
        inst_line = []
        for line_number, line in enumerate(lines, start=1):
            text = line.rstrip()
            if re.match(current_string, text):
                text1 = re.sub('^[0-9]{1,2}[:]', '', text)
                text2 = text1.replace('|', '')
                text3 = re.sub('(.*)[#]+.*', '\\1', text2)
                inst_line.append(text3)
                errors = PARSER_PATTERN.split(''.join(inst_line))
                unspaced_errors = ''.join(errors).replace(' ', '')
                if unspaced_errors != '':
                    print('there were errors at line number %i which reads:' % line_number)
                    print(line)
                    print('The errors are: %s' % unspaced_errors)
                    print('the preprocessed line is:')
                    print(inst_line)
                    if not rt_mode:
                        exit()

        parser(''.join(inst_line))
        voiceline += 1
        current_string = '%i:' % voiceline

    return (
     state_obj.tempostring, state_obj.outstring)


def live_loop_in(test_fp=None):
    """ a function which handles interactive input. """
    if test_fp:
        try:
            inbuff = 'i200 0 -1\n'
            while True:
                phrase = test_fp.readline()
                if phrase.strip() == 'done':
                    test_fp.close()
                    return inbuff
                inbuff += phrase + '\n'

        except (KeyboardInterrupt, EOFError):
            pass

    try:
        pinbuff = 'i200 0 -1\n'
        while True:
            try:
                phrase = raw_input('microcsound--> ')
            except:
                phrase = input('microcsound--> ')

            if phrase.strip() == 'done':
                return pinbuff
            pinbuff += phrase + '\n'

    except (KeyboardInterrupt, EOFError):
        print('Bye!')
        exit()


def main():
    """ The place where the magic begins """
    argparser = argparse.ArgumentParser(epilog='This is microcsound v.20171127')
    argparser.usage = 'microcsound [-h] [--orc orc_file] [-v] \n    [-i | \n          [[-o output_wav_file | -s, --score-only | -r, --realtime]\n           [-t, --stdin | input_mc_filename ]\n          ]  \n    ] '
    argparser.add_argument('--orc', dest='orc_file', default=(constants.DEFAULT_ORC_FILE),
      help='specify an orchestra file for csound to use,  which is not the default (microcsound.orc)')
    argparser.add_argument('-v', '--debug', action='store_true', dest='debug_mode',
      help='turn on debug mode')
    argparser.add_argument('-i', '--interactive', action='store_true', dest='interactive',
      help='use an interactive prompt, render audio in realtime as well, does not work when any of -o, -s, or -r are specified')
    argparser.add_argument('-o', '--output', dest='outwav', help='optional wave file output name')
    argparser.add_argument('-s', '--score-only', action='store_true', dest='score_only',
      help='only generate a score to stdout,  do not post-process it with csound')
    argparser.add_argument('-r', '--realtime', action='store_true', dest='realtime',
      help='render audio in realtime')
    argparser.add_argument('-t', '--stdin', action='store_true', dest='text_stdin',
      help='read text from stdin')
    argparser.add_argument('filename', nargs='?', help="an input '.mc' filename or filepath")
    args = argparser.parse_args()
    if len(argv) < 2:
        argparser.print_help()
        exit(0)
    else:
        if args.interactive:
            if args.outwav or args.realtime or args.score_only or args.text_stdin or args.filename:
                raise argparser.error('-i must not be used with any other arguments')
            else:
                if args.outwav:
                    if args.score_only or args.realtime:
                        raise argparser.error('-o must not be used -s or -r')
                if args.score_only:
                    if args.outwav or args.realtime:
                        raise argparser.error('-s must not be used -o or -r')
                if args.realtime:
                    if args.outwav or args.score_only:
                        raise argparser.error('-r must not be used -o or -s')
        else:
            if args.outwav or args.score_only or args.realtime:
                if not (args.filename or args.text_stdin):
                    raise argparser.error('You need to specify an input: a filename or stdin (-t)')
            else:
                if args.debug_mode:
                    verbosity_string = ''
                else:
                    verbosity_string = ' -O null '
                if args.interactive or args.realtime:
                    rt_mode = True
                    csound_command = constants.RT_CSOUND_COMMAND_STUB + verbosity_string + ' %s/%s /tmp/microcsound.sco' % (
                     constants.ORC_DIR, args.orc_file)
                else:
                    rt_mode = False
                if args.filename and not args.outwav:
                    out_wav = args.filename.replace('.mc', '.wav')
            out_wav = args.outwav
        csound_command = constants.NORMAL_CSOUND_COMMAND_STUB + verbosity_string + ' -o %s %s/%s /tmp/microcsound.sco' % (
         out_wav, constants.ORC_DIR, args.orc_file)
    if args.interactive:
        rt_mode = True
        while True:
            state_obj.__init__()
            live_input = live_loop_in()
            outbuf = process_buffer(live_input, rt_mode=True)
            temp_sco_file = open('/tmp/microcsound.sco', 'w')
            temp_sco_file.write('%s\n%s' % (outbuf[0], outbuf[1]))
            temp_sco_file.close()
            system(csound_command)

    else:
        if args.filename:
            the_file = open(args.filename)
            outbuf = process_buffer((the_file.read()), rt_mode=rt_mode)
            the_file.close()
        else:
            if args.text_stdin:
                outbuf = process_buffer((stdin.read()), rt_mode=rt_mode)
            if args.score_only:
                stdout.write('%s\n%s' % (outbuf[0], outbuf[1]))
            else:
                temp_sco_file = open('/tmp/microcsound.sco', 'w')
                temp_sco_file.write('%s\n%s' % (outbuf[0], outbuf[1]))
                temp_sco_file.close()
                system(csound_command)


if __name__ == '__main__':
    main()