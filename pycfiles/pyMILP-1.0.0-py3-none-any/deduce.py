# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymills/ai/deduce.py
# Compiled at: 2013-07-27 09:03:17
import sys, copy
from string import *

class sentence():
    adjectives = [
     'A', 'AN', 'THE', 'ALL', 'EVERY', 'NONE', 'MY', 'YOUR']
    negatives = ['NO', 'NONE', 'NOT', 'CANNOT', 'CANT', 'WONT',
     'DOESNT', 'DONT', 'ISNT', 'ARENT', 'AINT']
    verbs = ['IS', 'ARE', 'AM', 'BE', 'WAS', 'WERE', 'BE']
    helping_verbs = ['DO', 'DOES', 'CAN', 'WILL', 'HAS', 'HAVE']
    contractions = {'DONT': ['DO', 'NOT'], 'DOESNT': [
                'DOES', 'NOT'], 
       'ISNT': [
              'IS', 'NOT'], 
       'ARENT': [
               'ARE', 'NOT'], 
       'WONT': [
              'WILL', 'NOT'], 
       'CANT': [
              'CAN', 'NOT'], 
       'CANNOT': [
                'CAN', 'NOT'], 
       'WASNT': [
               'WAS', 'NOT'], 
       'WERENT': [
                'WERE', 'NOT'], 
       'IM': [
            'I', 'AM'], 
       'ILL': [
             'I', 'WILL'], 
       'YOURE': [
               'YOU', 'ARE'], 
       'YOULL': [
               'YOU', 'WILL']}

    def __init__(self, string):
        string = string.strip()
        string = string.upper()
        string = string.translate(maketrans('', ''), ".?!,'\n\r\t")
        self.words = []
        for word in string.split():
            if word in self.contractions:
                self.words += self.contractions[word]
            else:
                self.words.append(word)

        self.index = 0
        if self.is_question():
            self.question = 1
        else:
            self.question = 0
        self.negative = 0
        self.helping_verb = ''
        self.verb = ''

    def next_word(self):
        if self.index >= len(self.words):
            return
        else:
            self.index += 1
            return self.words[(self.index - 1)]
            return

    def prev_word(self):
        if self.index > 0:
            self.index -= 1

    def rewind_words(self):
        self.index = 0

    def next_phrase(self):
        phrase = {'negative': 0, 'type': 'unknown', 'error': None, 'adj': '', 
           'helping_verb': '', 'primary': ''}
        word = self.next_word()
        state = 0
        while 1:
            if word and word in self.negatives:
                self.negative = 1
                phrase['negative'] += 1
            elif state == 0:
                if word == None:
                    phrase['type'] = 'eol'
                    state = 99
                elif word in self.adjectives:
                    phrase['adj'] = word
                    phrase['type'] = 'noun phrase'
                    state = 1
                elif word in self.helping_verbs:
                    if self.question == 0:
                        phrase['helping_verb'] = word
                        phrase['type'] = 'verb phrase'
                        state = 1
                    else:
                        phrase['helping_verb'] = word
                        phrase['type'] = 'helping verb'
                        state = 99
                elif word in self.verbs:
                    phrase['primary'] = word
                    phrase['type'] = 'verb'
                    state = 99
                else:
                    phrase['primary'] = word
                    state = 99
            elif state == 1:
                if word == None:
                    phrase['error'] = 'Unexpected end of sentence'
                if word in self.adjectives or word in self.helping_verbs:
                    phrase['error'] = 'Unexpected word "' + word + '"'
                else:
                    phrase['primary'] = word
                state = 99
            else:
                if state == 99:
                    if word != None:
                        self.prev_word()
                    return phrase
                print '*** Fatal internal error in next_phrase method'
            word = self.next_word()

        return

    def is_question(self):
        if self.words[0] in self.verbs or self.words[0] in self.helping_verbs:
            return 1
        return 0


class fact():
    subj_adj = ''
    subj = ''
    helping_verb = ''
    verb = ''
    orig_verb = ''
    obj_adj = ''
    obj = ''
    question = 0
    negative = 0
    seen = 0
    to_be = [
     'IS', 'ARE', 'AM', 'BE', 'WAS', 'WERE']

    def __init__(self, statement):
        if statement != '':
            self.translate(statement)

    def __str__(self):
        out = []
        if self.negative == 1:
            if self.helping_verb:
                verb_ph = self.helping_verb + ' NOT ' + self.verb
            else:
                verb_ph = self.orig_verb + ' NOT'
        else:
            verb_ph = join([self.helping_verb, self.orig_verb], ' ').strip()
        for word in [self.subj_adj,
         self.subj,
         verb_ph,
         self.obj_adj,
         self.obj]:
            if word != '' and word[0] != '.':
                out.append(word)

        return join(out, ' ')

    def translate(self, statement):
        sent = sentence(statement)
        state = 0
        self.question = sent.is_question()
        self.error = ''
        phrase = sent.next_phrase()
        while phrase['error'] == None and phrase['type'] != 'eol':
            self.negative += phrase['negative']
            if state == 0:
                if phrase['type'] == 'unknown' or phrase['type'] == 'noun phrase':
                    self.subj_adj = phrase['adj']
                    self.subj = phrase['primary']
                    state = 1
                elif phrase['type'] == 'verb':
                    self.orig_verb = phrase['primary']
                    if phrase['primary'] in self.to_be:
                        self.verb = 'IS'
                    else:
                        self.verb = phrase['primary']
                    state = 3
                elif phrase['type'] == 'helping verb':
                    self.helping_verb = phrase['helping_verb']
                    state = 5
                else:
                    self.error = "I DON'T UNDERSTAND"
                    state = 99
            elif state == 1:
                self.orig_verb = phrase['primary']
                if phrase['type'] == 'verb':
                    if phrase['primary'] in self.to_be:
                        self.verb = 'IS'
                    else:
                        self.verb = phrase['primary']
                    state = 2
                elif phrase['type'] == 'verb phrase':
                    if phrase['primary'] in self.to_be:
                        self.helping_verb = phrase['helping_verb']
                        self.verb = 'IS'
                    else:
                        self.helping_verb = phrase['helping_verb']
                        self.verb = phrase['primary']
                    state = 2
                elif phrase['type'] == 'unknown':
                    self.verb = phrase['primary']
                    state = 2
                else:
                    self.error = "I DON'T UNDERSTAND"
                    state = 99
            elif state == 2:
                if phrase['type'] == 'unknown':
                    self.obj = phrase['primary']
                    state = 99
                elif phrase['type'] == 'noun phrase':
                    self.obj_adj = phrase['adj']
                    self.obj = phrase['primary']
                    state = 99
                else:
                    self.error = "I DON'T UNDERSTAND"
                    state = 99
            elif state == 3:
                if phrase['type'] == 'unknown':
                    self.subj = phrase['primary']
                    state = 4
                elif phrase['type'] == 'noun phrase':
                    self.subj_adj = phrase['adj']
                    self.subj = phrase['primary']
                    state = 4
                else:
                    self.error = "I DON'T UNDERSTAND"
                    state = 99
            elif state == 4:
                if phrase['type'] == 'unknown':
                    self.obj = phrase['primary']
                    state = 99
                elif phrase['type'] == 'noun phrase':
                    self.obj_adj = phrase['adj']
                    self.obj = phrase['primary']
                    state = 99
                else:
                    self.error = "I DON'T UNDERSTAND"
                    state = 99
            elif state == 5:
                if phrase['type'] == 'unknown':
                    self.subj = phrase['primary']
                    state = 6
                elif phrase['type'] == 'noun phrase':
                    self.subj_adj = phrase['adj']
                    self.subj = phrase['primary']
                    state = 6
                else:
                    self.error = "I DON'T UNDERSTAND"
                    state = 99
            elif state == 6:
                if phrase['type'] == 'unknown':
                    self.orig_verb = phrase['primary']
                    if phrase['primary'] in self.to_be:
                        self.verb = 'IS'
                    else:
                        self.verb = phrase['primary']
                    state = 7
                else:
                    self.error = "I DON'T UNDERSTAND"
                    state = 99
            elif state == 7:
                if phrase['type'] == 'eol':
                    state = 99
                elif phrase['type'] == 'unknown':
                    self.obj = phrase['primary']
                    state = 99
                elif phrase['type'] == 'noun phrase':
                    self.obj_adj = phrase['adj']
                    self.obj = phrase['primary']
                    state = 99
                else:
                    self.error = "I DON'T UNDERSTAND"
                    state = 99
            elif state == 99:
                self.error = 'THE SENTENCE IS TOO LONG'
            phrase = sent.next_phrase()

        if self.error == '':
            if self.negative > 1:
                self.error = "DON'T GIVE ME NO DOUBLE NEGATIVES"
        return

    def swap_person(self):
        newfact = copy.copy(self)
        if self.subj_adj == 'MY':
            newfact.subj_adj = 'YOUR'
        if self.subj_adj == 'YOUR':
            newfact.subj_adj = 'MY'
        if self.subj == 'I':
            if self.orig_verb == 'AM':
                newfact.subj = 'YOU'
                newfact.orig_verb = 'ARE'
            elif self.orig_verb == 'WAS':
                newfact.subj = 'YOU'
                newfact.orig_verb = 'WERE'
            else:
                newfact.subj = 'YOU'
        if self.subj == 'YOU':
            if self.orig_verb == 'ARE':
                newfact.subj = 'I'
                newfact.orig_verb = 'AM'
            elif self.orig_verb == 'WERE':
                newfact.subj = 'I'
                newfact.orig_verb = 'WAS'
            else:
                newfact.subj = 'I'
        if self.obj_adj == 'MY':
            newfact.obj_adj = 'YOUR'
        if self.obj_adj == 'YOUR':
            newfact.obj_adj = 'MY'
        if self.obj == 'ME':
            newfact.obj = 'YOU'
        if self.obj == 'MYSELF':
            newfact.obj = 'YOURSELF'
        if self.obj == 'YOU':
            newfact.obj = 'ME'
        if self.obj == 'YOURSELF':
            newfact.obj = 'MYSELF'
        return newfact


class brain():
    to_be = [
     'IS', 'ARE', 'BE', 'WAS', 'WERE']

    def __init__(self):
        self.brain = {}
        self.brain_verb = {}
        self.brain_obj = {}

    def __str__(self):
        out = ''
        for s in self.brain.keys():
            for v in self.brain[s].keys():
                for o in self.brain[s][v].keys():
                    if s != o or v != 'IS':
                        out = out + self.brain[s][v][o].__str__() + '\n'

        return out

    def learn(self, newfact):
        if type(newfact) == type(''):
            newfact = fact(newfact)
        if newfact.error != '':
            return [newfact.error, []]
        else:
            if newfact.subj == newfact.obj and newfact.negative == 1:
                return ["I'M NOT BUYING IT", []]
            stat, str, reason = self.query(newfact)
            if stat == 0:
                return ["THAT CAN'T BE RIGHT", reason]
            if stat == 1:
                return ['YEAH, I KNOW', reason]
            if not self.brain.has_key(newfact.subj):
                self.brain[newfact.subj] = {}
            if not self.brain[newfact.subj].has_key(newfact.verb):
                self.brain[newfact.subj][newfact.verb] = {}
            if newfact.obj == '':
                newfact.obj = '.fact'
            if self.brain[newfact.subj][newfact.verb].has_key(newfact.obj):
                oldfact = self.brain[newfact.subj][newfact.verb][newfact.obj]
                if newfact.negative == oldfact.negative:
                    return ['YEAH I KNOW', [oldfact]]
                return [
                 "THAT CAN'T BE RIGHT (" + oldfact.__str__() + ')', [oldfact]]
            else:
                self.brain[newfact.subj][newfact.verb][newfact.obj] = newfact
            if not self.brain_verb.has_key(newfact.verb):
                self.brain_verb[newfact.verb] = 1
            if newfact.obj != '' and not self.brain_obj.has_key(newfact.obj):
                self.brain_obj[newfact.obj] = 1
            if newfact.subj == newfact.obj:
                return ['WELL, OK', []]
            return [
             'OK', []]

    def describe_subj(self, subject):
        subject = upper(subject)
        dfact = fact('')
        symmetry = fact(subject + ' is ' + subject)
        desc = [symmetry]
        if not self.brain.has_key(subject):
            return desc
        for verb in self.brain[subject]:
            for object in self.brain[subject][verb]:
                dfact = copy.deepcopy(self.brain[subject][verb][object])
                if dfact.seen == 0:
                    desc.append(dfact)
                    if dfact.verb not in self.to_be:
                        if dfact.obj != '.fact' and not dfact.negative:
                            dfact.obj = ''
                            dfact.obj_adj = ''
                            desc.append(dfact)
                    elif not dfact.negative:
                        if object == '.fact':
                            newsubj = dfact.verb
                        else:
                            newsubj = dfact.obj
                        self.brain[subject][verb][object].seen = 1
                        desc2 = self.describe_subj(newsubj)
                        self.brain[subject][verb][object].seen = 0
                        for index in xrange(0, len(desc2)):
                            desc2[index].subj_adj = dfact.subj_adj
                            desc2[index].subj = dfact.subj

                        desc += desc2
                        del desc2

        return desc

    def query(self, question):
        if type(question) == type(''):
            question = fact(question)
        if not self.brain.has_key(question.subj) and not self.brain_obj.has_key(question.subj):
            return [
             -1, 'WHAT\'S THIS "' + question.subj + '" THING?', []]
        if question.obj != '' and not self.brain.has_key(question.obj) and not self.brain_obj.has_key(question.obj):
            return [
             -1, 'WHAT\'S THIS "' + question.obj + '" THING?', []]
        if question.verb != 'IS':
            if not self.brain_verb.has_key(question.verb):
                return [-1, "I DON'T KNOW WHAT IT MEANS TO " + question.verb, []]
        if question.subj == question.obj and question.verb == 'IS':
            if question.negative == 0:
                return [1, 'DUH, YES', [question]]
            else:
                return [
                 0, 'UGH, NO', [question]]

        ans, reason = self.query_i(question)
        if ans == 0:
            question.negative = 1 - question.negative
            return [
             0, 'NO, ' + question.swap_person().__str__(), reason]
        if ans == 1:
            return [1, 'YES, ' + question.swap_person().__str__(), reason]
        if question.obj != '' and question.verb == 'IS':
            subject_attr = self.describe_subj(question.subj)
            object_attr = self.describe_subj(question.obj)
            for f in subject_attr:
                f2 = copy.copy(f)
                f2.subj = question.obj
                f2.subj_adj = question.obj_adj
                ans, reason = self.query_i(f2)
                if ans == 0:
                    ans, reason0 = self.query_i(f)
                    reason = reason0 + reason
                    if question.negative == 0:
                        question.negative = 1 - question.negative
                        return [
                         0, 'NO, ' + question.swap_person().__str__(), reason]
                    return [
                     1, 'YES, ' + question.swap_person().__str__(), reason]

            for f in object_attr:
                f2 = copy.copy(f)
                f2.subj = question.subj
                f2.subj_adj = question.subj_adj
                ans, reason = self.query_i(f2)
                if ans == 0:
                    ans, reason0 = self.query_i(f)
                    reason = reason0 + reason
                    if question.negative == 0:
                        question.negative = 1 - question.negative
                        return [
                         0, 'NO, ' + question.swap_person().__str__(), reason]
                    return [
                     1, 'YES, ' + question.swap_person().__str__(), reason]

        return [
         -1, "I DON'T KNOW", []]

    def query_i(self, q):
        if not self.brain.has_key(q.subj):
            return [-1, []]
        if q.verb == 'IS':
            if q.subj == q.obj:
                return [
                 1, [q]]
            if self.brain[q.subj].has_key(q.verb):
                if self.brain[q.subj][q.verb].has_key(q.obj):
                    ans = self.brain[q.subj][q.verb][q.obj].negative
                    if q.negative == 0:
                        ans = 1 - ans
                    return [
                     ans, [self.brain[q.subj][q.verb][q.obj]]]
                for obj in self.brain[q.subj][q.verb]:
                    if self.brain[q.subj][q.verb][obj].negative == 0:
                        if self.brain[q.subj]['IS'][obj].seen == 0:
                            q2 = copy.copy(q)
                            q2.subj_adj = self.brain[q.subj][q.verb][obj].obj_adj
                            q2.subj = obj
                            self.brain[q.subj][q.verb][obj].seen = 1
                            ans, reason = self.query_i(q2)
                            self.brain[q.subj][q.verb][obj].seen = 0
                            if ans == 0 or ans == 1:
                                reason = [
                                 self.brain[q.subj][q.verb][obj]] + reason
                                return [
                                 ans, reason]

            return [
             -1, []]
        if q.obj == '' or q.obj == '.fact':
            if self.brain[q.subj].has_key(q.verb):
                if self.brain[q.subj][q.verb].has_key('.fact'):
                    ans = self.brain[q.subj][q.verb]['.fact'].negative
                    if q.negative == 0:
                        ans = 1 - ans
                    return [ans, [self.brain[q.subj][q.verb]['.fact']]]
                for obj in self.brain[q.subj][q.verb]:
                    if self.brain[q.subj][q.verb][obj].negative == 0:
                        return [1, [self.brain[q.subj][q.verb][obj]]]

                return [
                 -1, []]
            else:
                if self.brain[q.subj].has_key('IS'):
                    for obj in self.brain[q.subj]['IS']:
                        if self.brain[q.subj]['IS'][obj].seen == 0 and self.brain[q.subj]['IS'][obj].negative == 0:
                            q2 = copy.copy(q)
                            q2.subj = obj
                            q2.subj_adj = self.brain[q.subj]['IS'][obj].obj_adj
                            self.brain[q.subj]['IS'][obj].seen = 1
                            ans, reason = self.query_i(q2)
                            self.brain[q.subj]['IS'][obj].seen = 0
                            if ans == 0 or ans == 1:
                                reason = [
                                 self.brain[q.subj]['IS'][obj]] + reason
                                return [
                                 ans, reason]

                return [
                 -1, []]

        else:
            if self.brain[q.subj].has_key(q.verb):
                if self.brain[q.subj][q.verb].has_key(q.obj):
                    ans = self.brain[q.subj][q.verb][q.obj].negative
                    if q.negative == 0:
                        ans = 1 - ans
                    return [ans, [self.brain[q.subj][q.verb][q.obj]]]
            if self.brain[q.subj].has_key('IS'):
                for obj in self.brain[q.subj]['IS']:
                    if self.brain[q.subj]['IS'][obj].seen == 0 and self.brain[q.subj]['IS'][obj].negative == 0:
                        q2 = copy.copy(q)
                        q2.subj_adj = self.brain[q.subj]['IS'][obj].obj_adj
                        q2.subj = obj
                        self.brain[q.subj]['IS'][obj].seen = 1
                        ans, reason = self.query_i(q2)
                        self.brain[q.subj]['IS'][obj].seen = 0
                        if ans == 0 or ans == 1:
                            reason = [
                             self.brain[q.subj]['IS'][obj]] + reason
                            return [
                             ans, reason]

            if self.brain.has_key(q.obj):
                if self.brain[q.obj].has_key('IS'):
                    for obj in self.brain[q.obj]['IS']:
                        if self.brain[q.obj]['IS'][obj].negative == 0:
                            q2 = copy.copy(q)
                            q2.obj_adj = self.brain[q.obj]['IS'][obj].obj_adj
                            q2.obj = obj
                            self.brain[q.obj]['IS'][obj].seen = 1
                            ans, reason = self.query_i(q2)
                            self.brain[q.obj]['IS'][obj].seen = 0
                            if ans == 1:
                                reason = [
                                 self.brain[q.obj]['IS'][obj]] + reason
                                return [
                                 ans, reason]

            return [
             -1, []]


def ui():
    reason = []
    b = brain()
    while 1:
        sys.stdout.write('\n> ')
        quote = sys.stdin.readline()
        quote = quote.strip()
        cmd = quote.split()
        if len(cmd) > 0:
            cmd[0] = cmd[0].upper()
        if quote == '':
            print 'I BEG YOUR PARDON?'
        elif cmd[0] == 'HELP':
            print 'LOAD <filename> - Load a session from a file'
            print 'SAVE <filename> - Save your current session to a file'
            print "FORGET - Clear Deduce's memory"
            print 'WHY - Have Deduce explain its answer to a question'
            print "DIVULGE - Dump Deduce's memory to the screen"
            print 'HELP - Display this help text'
            print 'ABOUT - Display information about Deduce'
            print 'QUIT - Exit the program'
        elif cmd[0] == 'SAVE':
            if len(cmd) != 2:
                print '** Usage: SAVE <filename>'
            else:
                try:
                    f = file(cmd[1], 'w')
                    f.write(b.__str__())
                    f.close()
                    print 'SESSION SAVED'
                except IOError as err:
                    print '** Error saving:', err

        elif cmd[0] == 'LOAD':
            if len(cmd) != 2:
                print '** Usage: LOAD <filename>'
            else:
                try:
                    f = file(cmd[1], 'rU')
                    count = 0
                    for line in iter(f):
                        count += 1
                        line = line.strip()
                        if len(line) > 0:
                            msg, reason = b.learn(line)
                            print count.__str__() + ':', line, ' (' + msg + ')'
                        if count >= 10000:
                            print 'Too many input lines, bailing out'
                            break

                    f.close()
                    print 'SESSION LOADED'
                except IOError as err:
                    print '** Error loading:', err

        elif cmd[0] == 'DIVULGE':
            print b
        elif cmd[0] == 'FORGET':
            print 'FORGOTTEN'
            b = brain()
            reason = []
        elif cmd[0] == 'WHY':
            if len(reason) == 0:
                print '*SHRUG*'
            elif len(reason) == 1:
                if reason[0].subj == reason[0].obj:
                    if reason[0].negative == 0:
                        print 'WHAT ELSE WOULD', reason[0].subj_adj, reason[0].subj, 'BE?'
                    else:
                        print reason[0].subj, reason[0].orig_verb, reason[0].obj + ', THROUGH AND THROUGH'
                else:
                    print 'YOU SAID EARLIER THAT', reason[0].swap_person()
            else:
                print 'BECAUSE:'
                for r in reason:
                    print ' ', r.swap_person()

        elif cmd[0] == 'ABOUT':
            print 'Deduce 1.3.0, Copyright (C) 1995-2004  James Williams'
            print 'This program is licensed under the GNU General Public'
            print 'Licence (GPL) and may be distributed freely.  This'
            print 'program comes with ABSOLUTELY NO WARRANTY.  For details,'
            print 'please refer to the file COPYING, which should have'
            print 'been included with this program.'
        else:
            if cmd[0] == 'QUIT' or cmd[0] == 'EXIT' or cmd[0] == 'BYE' or cmd[0] == 'STOP':
                print 'GOODBYE'
                return
            if len(cmd) == 1:
                print '** Unknown command'
            else:
                f = fact(quote)
                if f.question == 0:
                    msg, reason = b.learn(quote)
                    print msg
                else:
                    ans, ans_str, reason = b.query(quote)
                    print ans_str


if __name__ == '__main__':
    print "HI, I'M DEDUCE.  FILL MY HEAD WITH TRIVIA, THEN QUIZ ME ON IT."
    print "I'M A GOOD LISTENER.  REALLY I AM."
    ui()