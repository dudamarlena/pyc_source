# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/forgetmenot/quiz.py
# Compiled at: 2010-03-29 08:15:04
import codecs, collections, itertools, random
Question = collections.namedtuple('Question', 'prompt answers')

def parse_alternates(semi_sep):
    return [ i.strip() for i in semi_sep.split(';') ]


def parse_quiz(filename, reverse):
    questions = {}
    with codecs.open(filename, encoding='utf-8') as (f):
        for line in f:
            (prompts, answers) = map(parse_alternates, line.split('=', 1))
            for p in prompts:
                if not reverse:
                    questions.setdefault(p, []).extend(answers)
                else:
                    for a in answers:
                        questions.setdefault(a, []).append(p)

    return itertools.starmap(lambda p, answers: Question(p, tuple(answers)), questions.iteritems())


def random_element(set_):
    x = random.randint(0, len(set_) - 1)
    it = iter(set_)
    while x > 0:
        it.next()
        x -= 1

    return it.next()


def question_iter(questions):
    remaining = set(questions)
    while True:
        if len(remaining) == 0:
            raise StopIteration
        next = random_element(remaining)
        remove = yield next
        if remove:
            remaining.remove(next)


def load_quiz(filename, reverse):
    questions = parse_quiz(filename, reverse)
    return question_iter(questions)