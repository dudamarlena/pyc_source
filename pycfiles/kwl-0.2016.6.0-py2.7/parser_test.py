# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/kwl2text/parser_test.py
# Compiled at: 2016-05-08 19:08:47
import kwl2text, semantics as s, unittest

class KWLTest(unittest.TestCase):

    def setUp(self):
        self.psr = kwl2text.kwl2textParser()
        self.sem = s.Semantics()
        self.maxDiff = None
        self.adj = 'adj:red'
        self.nom = 'nom:food'
        return

    def testToken(self):
        alpha = 'abc'
        number = '12'
        sem_alpha = {'t': 'alpha', 'v': 'abc'}
        sem_number = {'t': 'number', 'v': '12'}
        self.assertEquals(number, self.psr.parse(number, rule_name='token', parseinfo=True))
        self.assertEquals('abc', self.psr.parse(alpha, rule_name='token', parseinfo=True))
        self.assertEquals(number, self.psr.parse(number, rule_name='token', parseinfo=True))
        self.assertEquals('abc', self.psr.parse(alpha, rule_name='token', parseinfo=True))
        self.assertEquals(sem_number, self.psr.parse(number, rule_name='token', semantics=self.sem, parseinfo=True))
        self.assertEquals(sem_alpha, self.psr.parse(alpha, rule_name='token', semantics=self.sem, parseinfo=True))

    def testWord(self):
        noun = 'nom:dog'
        verb = 'act:love'
        pronoun = 'pro:we'
        semantic_noun = {'t': 'nom', 'v': {'t': 'alpha', 'v': 'dog'}}
        semantic_verb = {'t': 'act', 'v': {'t': 'alpha', 'v': 'love'}}
        semantic_pronoun = {'t': 'pro', 'v': {'t': 'alpha', 'v': 'we'}}
        self.assertEquals(semantic_noun, self.psr.parse(noun, rule_name='expression', semantics=self.sem, parseinfo=True))
        self.assertEquals(semantic_verb, self.psr.parse(verb, rule_name='expression', semantics=self.sem, parseinfo=True))
        self.assertEquals(semantic_pronoun, self.psr.parse(pronoun, rule_name='expression', semantics=self.sem, parseinfo=True))

    def testFormatting(self):
        defn = 'defn(%s)' % self.adj
        sample = 'sample(%s)' % self.nom
        quote = 'quote(raw(1 2 3))'
        semantic_defn = {'t': 'defn', 'v': {'t': 'adj', 'v': {'t': 'alpha', 'v': 'red'}}}
        semantic_sample = {'t': 'sample', 'v': {'t': 'nom', 'v': {'t': 'alpha', 'v': 'food'}}}
        semantic_quote = {'t': 'quote', 'v': {'t': 'raw', 'v': '1 2 3'}}
        self.assertEquals(semantic_defn, self.psr.parse(defn, rule_name='sentence', semantics=self.sem, parseinfo=True))
        self.assertEquals(semantic_sample, self.psr.parse(sample, rule_name='sentence', semantics=self.sem, parseinfo=True))
        self.assertEquals(semantic_quote, self.psr.parse(quote, rule_name='sentence', semantics=self.sem, parseinfo=True))

    def testPhrase(self):
        adj = self.adj
        nom = self.nom
        pre = 'pre:for'
        act = 'act:love'
        adj_nom = 'adj:good_nom:dog;'
        pos_nom = 'pos:his_nom:country'
        det_adj_nom = 'det:the(adj:good_nom:dog)'
        conjugation = 'ydy(tu(act:walk))'
        semantic_adj = {'t': 'adj', 'v': {'t': 'alpha', 'v': 'red'}}
        semantic_nom = {'t': 'nom', 'v': {'t': 'alpha', 'v': 'food'}}
        semantic_pre = {'t': 'pre', 'v': {'t': 'alpha', 'v': 'for'}}
        semantic_act = {'t': 'act', 'v': {'t': 'alpha', 'v': 'love'}}
        semantic_adj_nom = {'t': 'adj_nom', 'v': [{'t': 'adj', 'v': {'t': 'alpha', 'v': 'good'}}, {'t': 'nom', 'v': {'t': 'alpha', 'v': 'dog'}}]}
        semantic_pos_nom = {'t': 'pos_nom', 'v': [{'t': 'pos', 'v': {'t': 'alpha', 'v': 'his'}}, {'t': 'nom', 'v': {'t': 'alpha', 'v': 'country'}}]}
        semantic_det_adj_nom = {'t': 'det_adj_nom', 'v': [{'t': 'det', 'v': {'t': 'alpha', 'v': 'the'}}, {'t': 'adj_nom', 'v': [{'t': 'adj', 'v': {'t': 'alpha', 'v': 'good'}}, {'t': 'nom', 'v': {'t': 'alpha', 'v': 'dog'}}]}]}
        semantic_conjugation = {'t': 'ydy', 'v': {'t': 'tu', 'v': {'t': 'act', 'v': {'t': 'alpha', 'v': 'walk'}}}}
        self.assertEquals(semantic_adj, self.psr.parse(adj, rule_name='expression', semantics=self.sem, parseinfo=True))
        self.assertEquals(semantic_nom, self.psr.parse(nom, rule_name='expression', semantics=self.sem, parseinfo=True))
        self.assertEquals(semantic_pre, self.psr.parse(pre, rule_name='expression', semantics=self.sem, parseinfo=True))
        self.assertEquals(semantic_act, self.psr.parse(act, rule_name='expression', semantics=self.sem, parseinfo=True))
        self.assertEquals(semantic_adj_nom, self.psr.parse(adj_nom, 'expression'))
        self.assertEquals(semantic_pos_nom, self.psr.parse(pos_nom, 'expression'))
        self.assertEquals(semantic_det_adj_nom, self.psr.parse(det_adj_nom, 'expression'))
        self.assertEquals(semantic_conjugation, self.psr.parse(conjugation, 'expression'))

    def testExpression(self):
        subject_verb = 'pro:I act:love'
        verb_object = 'act:love nom:food'
        subject_verb_object = 'pro:I act:love nom:food'
        semantic_s_v = {'t': 's_v', 'v': [{'t': 'subject', 'v': {'t': 'pro', 'v': {'t': 'alpha', 'v': 'I'}}}, {'t': 'verb', 'v': {'t': 'act', 'v': {'t': 'alpha', 'v': 'love'}}}]}
        semantic_v_o = {'t': 'v_o', 'v': [{'t': 'verb', 'v': {'t': 'act', 'v': {'t': 'alpha', 'v': 'love'}}}, {'t': 'object', 'v': {'t': 'nom', 'v': {'t': 'alpha', 'v': 'food'}}}]}
        semantic_s_v_o = {'t': 's_v_o', 'v': [{'t': 'subject', 'v': {'t': 'pro', 'v': {'t': 'alpha', 'v': 'I'}}}, {'t': 'verb', 'v': {'t': 'act', 'v': {'t': 'alpha', 'v': 'love'}}}, {'t': 'object', 'v': {'t': 'nom', 'v': {'t': 'alpha', 'v': 'food'}}}]}
        self.assertEquals(semantic_s_v, self.psr.parse(subject_verb, rule_name='expression', semantics=self.sem, parseinfo=True))
        self.assertEquals(semantic_v_o, self.psr.parse(verb_object, rule_name='expression', semantics=self.sem, parseinfo=True))
        self.assertEquals(semantic_s_v_o, self.psr.parse(subject_verb_object, rule_name='expression', semantics=self.sem, parseinfo=True))

    def testSentence(self):
        statement = 'pro:I act:love nom:food.'
        question = 'pro:I act:love nom:food?'
        command = 'pro:I act:love nom:food!'
        semantic_statement = {'t': 'statement', 'v': {'t': 's_v_o', 'v': [{'t': 'subject', 'v': {'t': 'pro', 'v': {'t': 'alpha', 'v': 'I'}}}, {'t': 'verb', 'v': {'t': 'act', 'v': {'t': 'alpha', 'v': 'love'}}}, {'t': 'object', 'v': {'t': 'nom', 'v': {'t': 'alpha', 'v': 'food'}}}]}}
        semantic_question = {'t': 'question', 'v': {'t': 's_v_o', 'v': [{'t': 'subject', 'v': {'t': 'pro', 'v': {'t': 'alpha', 'v': 'I'}}}, {'t': 'verb', 'v': {'t': 'act', 'v': {'t': 'alpha', 'v': 'love'}}}, {'t': 'object', 'v': {'t': 'nom', 'v': {'t': 'alpha', 'v': 'food'}}}]}}
        semantic_command = {'t': 'command', 'v': {'t': 's_v_o', 'v': [{'t': 'subject', 'v': {'t': 'pro', 'v': {'t': 'alpha', 'v': 'I'}}}, {'t': 'verb', 'v': {'t': 'act', 'v': {'t': 'alpha', 'v': 'love'}}}, {'t': 'object', 'v': {'t': 'nom', 'v': {'t': 'alpha', 'v': 'food'}}}]}}
        self.assertEquals(semantic_statement, {'t': 'statement', 'v': self.psr.parse(statement.replace('.', ''), rule_name='sentence', semantics=self.sem, parseinfo=True)})
        self.assertEquals(semantic_statement, self.psr.parse(statement, rule_name='sentence', semantics=self.sem, parseinfo=True))
        self.assertEquals(semantic_question, self.psr.parse(question, rule_name='sentence', semantics=self.sem, parseinfo=True))
        self.assertEquals(semantic_command, self.psr.parse(command, rule_name='sentence', semantics=self.sem, parseinfo=True))

    def testKWL2Text(self):
        story = open('test.kwl', 'r').read()
        t = self.psr.parse(story, rule_name='kwl2text', semantics=self.sem, parseinfo=True)
        self.assertEquals(len(story.split(';')), 1 + len(t['v']))

    def testDate(self):
        self.assertEquals({'t': 'date', 'v': '2015-11-11'}, self.psr.parse('date(2015-11-11)', rule_name='raw', semantics=self.sem, parseinfo=True))

    def testRaw(self):
        self.assertEquals('raw(dog)', self.psr.parse('raw(dog)', rule_name='raw', parseinfo=True))
        self.assertEquals('raw(Obuor)', self.psr.parse('raw(Obuor)', rule_name='raw', parseinfo=True))
        self.assertEquals('raw(13:4)', self.psr.parse('raw(13:4)', rule_name='raw', parseinfo=True))
        self.assertEquals({'t': 'raw', 'v': '13:4'}, self.psr.parse('raw(13:4)', rule_name='raw', semantics=self.sem, parseinfo=True))
        self.assertEquals({'t': 'raw', 'v': '13:4'}, self.psr.parse('raw(13:4)', rule_name='expression', semantics=self.sem, parseinfo=True))
        self.assertEquals({'t': 'nom_raw', 'v': [{'t': 'nom', 'v': {'t': 'alpha', 'v': 'dog'}}, {'t': 'raw', 'v': '13:4'}]}, self.psr.parse('nom:dog_raw(13:4)', rule_name='expression', semantics=self.sem, parseinfo=True))

    def testForcedGrouping(self):
        kwl_text = 'nom:wealth'
        p1 = self.psr.parse(kwl_text, rule_name='expression', semantics=self.sem)
        kwl_text2 = '{ nom:wealth }'
        p2 = self.psr.parse(kwl_text2, rule_name='expression', semantics=self.sem)
        self.assertEquals(p1, p2)
        kwl_text = 'nom:wealth and nom:happiness'
        p1 = self.psr.parse(kwl_text, rule_name='expression', semantics=self.sem)
        kwl_text2 = '{nom:wealth and nom:happiness}'
        p2 = self.psr.parse(kwl_text2, rule_name='expression', semantics=self.sem)
        self.assertEquals(p1, p2)
        kwl_text = 'pro:it tdy(il(act:bring)) nom:wealth'
        p1 = self.psr.parse(kwl_text, rule_name='expression', semantics=self.sem)
        kwl_text2 = '{pro:it} tdy(il(act:bring)) nom:wealth'
        p2 = self.psr.parse(kwl_text2, rule_name='expression', semantics=self.sem)
        self.assertEquals(p1, p2)
        kwl_text3 = 'pro:it {tdy(il(act:bring))} nom:wealth'
        p3 = self.psr.parse(kwl_text3, rule_name='expression', semantics=self.sem)
        self.assertEquals(p1, p3)
        kwl_text4 = 'pro:it tdy(il(act:bring)) {nom:wealth}'
        p4 = self.psr.parse(kwl_text4, rule_name='expression', semantics=self.sem)
        self.assertEquals(p1, p4)
        kwl_text5 = '{pro:it} {tdy(il(act:bring))} {nom:wealth}'
        p5 = self.psr.parse(kwl_text5, rule_name='expression', semantics=self.sem)
        self.assertEquals(p1, p5)
        kwl_text6 = 'pro:you tdy(il(act:bring)) {nom:wealth and nom:happiness}'
        p6 = self.psr.parse(kwl_text6, rule_name='expression', semantics=self.sem)
        kwl_text7 = 'pro:you {tdy(il(act:go)) and tdy(il(act:bring))} {nom:wealth and nom:happiness}'
        p7 = self.psr.parse(kwl_text7, rule_name='expression', semantics=self.sem)
        kwl_text8 = '{pro:you and pro:I} {tdy(nous(act:go)) and tdy(nous(act:bring))} {nom:wealth and nom:happiness}'
        p8 = self.psr.parse(kwl_text8, rule_name='expression', semantics=self.sem)
        kwl_text9 = 'pro:you tdy(il(act:bring)) {nom:wealth and nom:happiness}'
        p9 = self.psr.parse(kwl_text9, rule_name='expression', semantics=self.sem)
        self.assertEquals({'t': 's_v_o', 'v': [{'t': 'subject', 'v': {'t': 'pro', 'v': {'t': 'alpha', 'v': 'you'}}}, {'t': 'verb', 'v': {'t': 'tdy', 'v': {'t': 'il', 'v': {'t': 'act', 'v': {'t': 'alpha', 'v': 'bring'}}}}}, {'t': 'object', 'v': {'t': 'and', 'v': [{'t': 'nom', 'v': {'t': 'alpha', 'v': 'wealth'}}, {'t': 'nom', 'v': {'t': 'alpha', 'v': 'happiness'}}]}}]}, p6)

    def testJoins(self):
        and_nouns = 'nom:eagle and nom:bird;'
        ast_and_nouns = [{'v': 'eagle', 't': 'nom'}, 'and', {'v': 'bird', 't': 'nom'}]
        sem_and_nouns = {'t': 'and', 'v': [{'t': 'nom', 'v': {'t': 'alpha', 'v': 'eagle'}}, {'t': 'nom', 'v': {'t': 'alpha', 'v': 'bird'}}]}
        or_nouns = 'nom:eagle or nom:bird;'
        ast_or_nouns = [{'v': 'eagle', 't': 'nom'}, 'or', {'v': 'bird', 't': 'nom'}]
        sem_or_nouns = {'t': 'or', 'v': [{'t': 'nom', 'v': {'t': 'alpha', 'v': 'eagle'}}, {'t': 'nom', 'v': {'t': 'alpha', 'v': 'bird'}}]}
        ifthen_nouns = 'if nom:eagle then nom:bird'
        ast_ifthen_nouns = [{'v': 'eagle', 't': 'nom'}, 'then', {'v': 'bird', 't': 'nom'}]
        self.assertEquals(ast_and_nouns, self.psr.parse(and_nouns, 'conjunction'))
        self.assertEquals(ast_or_nouns, self.psr.parse(or_nouns, 'conjunction'))
        self.assertEquals(ast_ifthen_nouns, self.psr.parse(ifthen_nouns, 'conjunction'))
        sen = ' pos:his_nom:birthday tdy(elle(act:be)) date(1982-01-30)'
        sen = 'pro:it tdy(i(act:use)) plural(adj:neural_nom:net), {inf(act:think)} like(det:a_nom:human)'
        sen = '{inf(tu(act:think))} like(det:a_nom:human)'
        sen = 'title({inf(tu(act:think))} like(det:a_nom:human))'
        sen = 'quote(raw(1 2 3))'
        sen = 'title(pro:you) act:have adj:three_plural(nom:part): nom:body and nom:mind and nom:spirit'
        self.assertEquals(sem_and_nouns, self.psr.parse(and_nouns, rule_name='conjunction', semantics=self.sem))
        self.assertEquals(sem_or_nouns, self.psr.parse(or_nouns, rule_name='conjunction', semantics=self.sem))


if __name__ == '__main__':
    unittest.main()