# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/forgetmenot/text.py
# Compiled at: 2010-03-29 07:24:08
import string, sys

def encode(s):
    try:
        return s.encode(sys.stdout.encoding)
    except UnicodeEncodeError:
        sys.stderr.write("error: couldn't encode %r to the terminal encoding\n" % s)
        return repr(s)


def decode(s):
    return s.decode(sys.stdin.encoding)


def ask(question, strict):
    prompt = '%s = ' % encode(question.prompt)
    response = raw_input(prompt)
    response = decode(response.strip().lower())
    answer_set = set(map(string.lower, question.answers))
    if strict:
        response_set = set(map(string.lower, parse_alternates(response)))
        return response_set == answer_set
    return response.lower() in answer_set


def run_quiz(quiz, strict=False):
    correct = None
    try:
        while True:
            question = quiz.send(correct)
            correct = ask(question, strict)
            if correct:
                print 'correct'
            else:
                answers = ('; ').join(question.answers)
                print 'incorrect: %s' % encode(answers)

    except (EOFError, StopIteration):
        pass

    return