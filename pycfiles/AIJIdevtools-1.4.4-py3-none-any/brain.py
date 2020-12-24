# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aiio/brain.py
# Compiled at: 2016-09-29 17:00:13
import random
from model import *
from think import learn, phrase, meaning, question, identify, tag, nextNoun, retorts
from util import randphrase
from hear import listen
from speak import say

class Brain(object):

    def __init__(self, name, ear=False, retorts=True):
        self.name = name
        self.identity = identify(name)
        self.examiner = None
        say('who are you?')
        self.retorts = retorts
        if ear:
            self.ear = listen(self)
        return

    def __call__(self, sentence):
        tagged = tag(sentence)
        if tagged[0][1] == 'WP':
            return say(self.answer(sentence))
        if sentence.startswith('tell me'):
            subject = sentence.split(' about ')[1]
            if 'you' in subject:
                person = self.identity
            else:
                if subject == 'me':
                    person = self.examiner
                else:
                    person = identify(subject)
                content = person.content()
                if content == person.name:
                    content = learn(subject, True).meaning()
                if content:
                    return say(content)
            return say(randphrase('exhausted'))
        else:
            self.ingest(sentence)
            if self.retorts:
                return say(self.retort(sentence))

    def ingest(self, sentence):
        tagged = tag(sentence)
        if len(tagged) > 1:
            if tagged[0][0] == 'i' and tagged[1][0] == 'am':
                desc = sentence[5:]
                if not self.examiner:
                    self.examiner = identify(nextNoun(tagged[2:]))
                elif not self.examiner.summary:
                    self.examiner.summary = desc
                else:
                    self.examiner.description = '%s %s' % (self.examiner.description, desc)
                self.examiner.qualifiers.append(phrase(desc).key)
                self.examiner.put()
                q = question('who am i?')
                q.answers.append(self.examiner.key)
                q.put()
                say('hello %s' % (self.examiner.name,))
                if self.examiner.qualifiers:
                    qual = random.choice(self.examiner.qualifiers).get().content()
                    qper = []
                    for qword, qpos in tag(qual):
                        if qpos == 'PRP':
                            qword = 'you'
                        elif qpos == 'PRP$':
                            qword = 'your'
                        qper.append(qword)

                    say((' ').join(qper))
            elif 'because' in sentence:
                event, reason = sentence.split(' because ')
                Reason(person=self.examiner and self.examiner.key, name=event, reason=phrase(reason)).put()
                say('ok, so %s because %s?' % (event, reason))
            elif tagged[0][1].startswith('NN'):
                if tagged[1][0] in ('is', 'are'):
                    meaning(tagged[0][0], (' ').join([ w for w, p in tagged[2:] ]))
                    say(randphrase('noted'))

    def clarify(self, sentence):
        return randphrase('what')

    def answer(self, sentence):
        q = question(sentence)
        if not q.answers:
            tagged = tag(sentence)
            if tagged[0][0] == 'who':
                if tagged[1][0] in ('is', 'are'):
                    if tagged[2][0] == 'you':
                        q.answers.append(self.identity.key)
                    else:
                        q.answers.append(identify(nextNoun(tagged[2:])).key)
                else:
                    if tagged[1][0] == 'am':
                        return "i don't know. who are you?"
                    else:
                        return randphrase('what')

            elif tagged[0][0] == 'what':
                if tagged[1][0] in ('is', 'are'):
                    obj = learn(nextNoun(tagged[2:]), True)
                    meanings = obj.meanings()
                    if not meanings:
                        return '%s. what does %s mean to you?' % (randphrase('unsure'), obj.word)
                    q.answers.append(meanings[0].key)
                else:
                    return randphrase('what')
            else:
                if tagged[0][0] == 'why':
                    return 'nevermind the whys and wherefores!'
                else:
                    return randphrase('what')

            q.put()
        return random.choice(q.answers).get().content()

    def retort(self, sentence):
        retz = retorts.keys()
        random.shuffle(retz)
        for r in retz:
            v = retorts[r](sentence)
            if v:
                v = v.replace(self.identity.name, 'i')
                return self.examiner and v.replace(self.examiner.name, 'you') or v