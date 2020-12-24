# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/lib/eliza.py
# Compiled at: 2011-04-22 06:35:42
""" a simple eliza ki implementation with regular expressions """
import random, re

class eliza:
    reflections = {}
    patterns = {}

    def setReflections(self, refl):
        self.reflections = refl

    def setPatterns(self, pat):
        self.patterns = {}
        for key in pat.keys():
            self.patterns[re.compile(key, re.I)] = pat[key]

    def reply(self, input):
        for regex in self.patterns.keys():
            match = regex.match(input)
            if match:
                answer = random.choice(self.patterns[regex])
                if '%s' in answer:
                    answer = answer % match.groups()
                if answer[(-2)] in '.?!':
                    for refl in self.reflections.keys():
                        answer = answer.replace(refl, self.reflections[refl])

                    answer = answer[:-1]
                return answer