# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/forgetmenot/__init__.py
# Compiled at: 2010-03-29 08:19:26
from optparse import OptionParser
from forgetmenot.quiz import load_quiz

def get_options():
    parser = OptionParser(usage='%prog [OPTIONS] QUIZ', version='%prog $Rev: 683 $')
    parser.add_option('-r', '--reverse', action='store_true', dest='reverse', help='Reverse the deck.')
    parser.add_option('-t', '--text-mode', action='store_true', dest='text', help='Force text mode.')
    parser.add_option('-s', '--strict', action='store_true', dest='strict', help='Enable strict mode (require all possible definitions to be entered). Implies --text.')
    parser.add_option('--font-size', type='int', default=24, dest='font_size', help='Font size to display quiz in.')
    (options, args) = parser.parse_args()
    if options.strict:
        options.text = True
    if len(args) != 1:
        parser.error('Required argument QUIZ missing.')
    return (options, args)


def main():
    (options, args) = get_options()
    quiz = load_quiz(args[0], options.reverse)
    if options.text:
        import forgetmenot.text
        run_quiz = forgetmenot.text.run_quiz
        args = [options.strict]
    else:
        import forgetmenot.gui
        run_quiz = forgetmenot.gui.run_quiz
        args = [options.font_size]
    try:
        run_quiz(quiz, *args)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()