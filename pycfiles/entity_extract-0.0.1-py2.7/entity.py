# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/entity/entity.py
# Compiled at: 2017-10-31 05:08:55
import difflib, re, csv
from string import uppercase
from nltk import RegexpParser
from nltk.stem import WordNetLemmatizer
from stanford_pos_tagger.stanfordapi import StanfordAPI
from unidecode import unidecode
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class Extractor:
    """Used to extract entities based on POS tagging"""

    def __init__(self):
        self.pos_tag_obj = StanfordAPI()

    @staticmethod
    def tokenize_words(sentence, preserve_case=True):
        """Word separation in a sentence"""
        words = []
        for word in re.split('^[-,.()!:+?\\"\\\'*]+|[-,.()!:+?\\"\\\'*]*\\s+[-,.()!:+?\\"\\\'*]*|[-,.()!:+?\\"\\\'*]+$', sentence):
            if word != '':
                words.append(word)

        if not preserve_case:
            words = list(map(lambda x: x.lower(), words))
        return words

    @staticmethod
    def sentence_phrases_separation(text):
        """Used for part of sentence extraction based on punctuation delimiters.
        An additional space is added in between period and capital letter"""
        sentence_phrases = [ sent for sent in re.split('[.,!:;?*()\\n]+\\s+|\\s+[.,!:;?*()\\n]+|(->)', re.sub('(\\.)([A-Z])', '\\1 \\2', text)) if sent != ''
                           ]
        return sentence_phrases

    @staticmethod
    def word_combination(pos_tagged_sentence, tag_set='ptb'):
        """Chunking of a part of speech tagged sentence based on specific grammar"""
        if tag_set == 'ptb':
            grammar = '\n            EN: {<JJ.*>*<NN.*>+}\n            '
        elif tag_set == 'universal':
            grammar = '\n            EN: {<ADJ>*<NOUN>+}\n            '
        else:
            raise SyntaxError
        cp = RegexpParser(grammar)
        result = cp.parse(pos_tagged_sentence)
        return result

    @staticmethod
    def calculate_symbol_ratio(word):
        """Calculating the symbol ratio of an element"""
        symbol_ratio = float(len(re.findall('[^A-Za-z\\s]', word))) / len(word)
        return symbol_ratio

    @staticmethod
    def entity_generation(pos_tagged_tree):
        """Used for the entity generation using the chunked entity tree
        :type pos_tagged_tree: Tree
        """
        sent_entities = []
        unimp_tokens = [
         'thank', 'thanks', 'anyone', 'everyone', 'anyhelp', 'hi', 'please', 'help', 'welcome']
        abbrv = ['e.g', 'i.e', 'um', 'etc']
        whole_entity = []
        neglect = False
        for result_tree in pos_tagged_tree:
            if type(result_tree) is not tuple:
                entity = []
                for subtree in result_tree:
                    if subtree[0].lower() in unimp_tokens:
                        neglect = True
                    elif subtree[0].lower() not in abbrv and len(subtree[0]) > 1:
                        entity.append(subtree[0])

                if entity and not neglect:
                    concat_word = (' ').join([ word for word in entity if word ])
                    whole_entity.append(concat_word)

        for en in whole_entity:
            sent_entities.append(en)

        for element in sent_entities:
            if element:
                symbol_ratio = Extractor.calculate_symbol_ratio(element)
                if symbol_ratio <= 0.5:
                    yield lemmatizer(element)
                else:
                    print str(element) + ' entity rejected due to symbol ratio :' + str(symbol_ratio)

    def extract_entities(self, text):
        """Used to extract entities based on part of speech tagging
        :type text: str
        """
        text = unidecode(text.decode('utf-8')).decode('ascii', 'ignore')
        input_sentences = self.sentence_phrases_separation(text)
        entities = []
        for sentence in input_sentences:
            if sentence:
                tokens = self.tokenize_words(sentence)
                pos_tagged_sentence = self.pos_tag_obj.pos_tag((' ').join(tokens))
                result = self.word_combination(pos_tagged_sentence)
                entities += [ en for en in list(self.entity_generation(result)) ]

        return iter(entities)


def extract_entities_corpora(pos_tagged_text):
    """Entity generation of a pos tagged text in a particular corpora
    :type pos_tagged_text: Generator
    """
    for sentence in pos_tagged_text:
        result = Extractor.word_combination(sentence, tag_set='universal')
        yield Extractor.entity_generation(result)


def lemmatizer(entity):
    """Used to lemmatize the entities"""
    if re.search('([A-Z]s)$', entity):
        return entity[:-1]
    words = Extractor.tokenize_words(entity)
    last_word = words.pop()
    lem_word = WordNetLemmatizer().lemmatize(last_word.lower())
    if len(lem_word) > 1:
        out = ''
        for i, e in enumerate(lem_word):
            out += str(e).upper() if len(last_word) > i and str(last_word[i]).isupper() else e

        words.append(out)
        return str((' ').join(words))
    if len(words) == 1:
        return entity


def comparator(entity_list1, entity_list2, threshold=0.93):
    """Return the equal entities between two entity lists based on it's similarity up to a certain threshold value"""
    equal_entities = []
    for entity1 in entity_list1:
        for entity2 in entity_list2:
            seq = difflib.SequenceMatcher(a=str(entity1).lower(), b=str(entity2).lower())
            if seq.ratio() > threshold:
                print entity2
                equal_entities.append(entity1)

    return equal_entities


def reducer(entity_list, threshold=0.93, case_sensitive=True):
    """Used to reduce an entity list based on it's similarities up to a certain threshold"""
    for i in range(len(entity_list)):
        for j in range(i + 1, len(entity_list)):
            if case_sensitive:
                seq = difflib.SequenceMatcher(a=str(entity_list[i]).lower(), b=str(entity_list[j]).lower())
            else:
                seq = difflib.SequenceMatcher(a=entity_list[i], b=entity_list[j])
            if seq.ratio() > threshold:
                no_case1 = len(filter(lambda x: x in uppercase, entity_list[i]))
                no_case2 = len(filter(lambda x: x in uppercase, entity_list[j]))
                if no_case1 > no_case2:
                    entity_list[j] = entity_list[i]
                elif no_case2 > no_case1:
                    entity_list[i] = entity_list[j]
                else:
                    len1 = len(entity_list[i])
                    len2 = len(entity_list[j])
                    if len1 > len2:
                        entity_list[j] = entity_list[i]
                    else:
                        entity_list[i] = entity_list[j]

    reduced_set = set()
    for en in entity_list:
        if en not in reduced_set:
            reduced_set.add(en)
            yield en
        else:
            continue


def test():
    text = 'The Send Mediator used by WSO2 ESB comes from the Apache,Axis2,MySQL project. and it makes use of JNDI or LOL \n    or JMS or HELL to connect to various JMS brokers. '
    print list(Extractor().extract_entities(text))


if __name__ == '__main__':
    test()