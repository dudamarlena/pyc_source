# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidj411/Desktop/venvs/tp/lib/python3.7/site-packages/thoughtpad/tp.py
# Compiled at: 2019-03-07 22:24:46
# Size of source mod 2**32: 4436 bytes
"""
    tp is short for __Thought __Pad. 
    it writes ideas to a quick thoughts file . 
    it will also help you find them.
"""
import sys, os, datetime, codecs
from subprocess import Popen, PIPE
import logging
if __name__ == '__main__':
    logging.basicConfig(level=(logging.DEBUG))
    qt_file_basename = 'chronicles.{}.txt'.format(os.environ['USER'])
    logger = logging.getLogger()
    logger.debug('args: %s' % sys.argv)
    DEBUG = 1
    try:
        folder = os.environ['USERPROFILE']
    except KeyError:
        folder = os.environ['HOME']

    editor = 'vim'
    my_file = os.path.join(folder, qt_file_basename)
    if DEBUG:
        logger.debug(my_file)
    logger.debug('len(sys.argv):%s' % len(sys.argv))
    if DEBUG:
        for i in sys.argv:
            print('arg:%s' % i)

    directive = ''
    long_string = ' '.join(sys.argv[1:])
    if '"' in long_string:
        logger.debug('quotes inside: %s', ' '.join(sys.argv))
    accepted_commands = ('x', 'v', 'f', 'h', 'e')
    if len(sys.argv) == 1:
        directive = 'v'
    words = ''
    if len(sys.argv) > 1:
        if sys.argv[1] in accepted_commands:
            directive = sys.argv[1]
            if len(sys.argv) > 2:
                words = ' '.join(sys.argv[2:])
else:
    directive = 'a'
    words = ' '.join(sys.argv[1:])
if ':' in words:
    subject, rest = words.split(':', 1)
else:
    subject = 'quick generic thought'
    rest = words
logger.debug('directive:%s' % directive)
if directive in ('v', 'x', 'f'):
    with codecs.open(my_file, encoding='utf-8', errors='ignore') as (fh):
        for x, line in enumerate(fh):
            try:
                line = line.strip()
                if directive == 'v':
                    print(line)
                else:
                    if directive == 'f':
                        if len(sys.argv) == 3:
                            if words.lower() in line.lower():
                                print(str(x) + ' ' + line)
                        else:
                            for i in line.split():
                                if i.lower() in words.lower():
                                    print('found:%s' % i)
                                    print(str(x) + ' ' + line)
                                    break

                    else:
                        if directive == 'x':
                            if words.lower() in line.lower():
                                logger.debug(str(x) + ' ' + line)
            except:
                logger.error('\n\nline # %s', x, exc_info=True)
                input('waiting...')

else:
    if directive == 'h':
        logger.debug('options are %0 [v or e or f or x or a (implied if not specified)]')
        logger.debug('which amounts to View, Edit, Filter (look for word(s)), and eXact (just find it )')
    else:
        if directive == 'a':
            dt = datetime.date.today().strftime('%Y-%m-%d')
            open(my_file, 'a').write(dt + ' ' + words + '\n')
        else:
            if directive == 'e':
                args = [
                 editor, my_file]
                logger.debug(args)
                out, err = Popen(args).communicate()
                logger.debug('out:%s' % out)
                if err:
                    logger.debug('err:%s' % err)