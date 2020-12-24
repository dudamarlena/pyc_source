# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ayoubix/projects/fr_word_segment/fr_word_segment/wordseg.py
# Compiled at: 2019-08-01 07:59:28
# Size of source mod 2**32: 4344 bytes
import math, spacy
nlp = spacy.load('fr_core_news_md')

def average(number1, number2, number3):
    """
        Calculating the average of three given numbers

        Parameters:
        number1|2|3 (float): three given numbers

        Returns:
        number (float): Returning the statistical average of these three numbers
        """
    return (number1 + number2 + number3) / 3.0


def measure_similarity(token_1, token_2, token_3):
    """
        Measuring the semantic similarity between three tokens

        Parameters:
        token_1|2|3 (string): three given tokens

        Returns:
        number (float): Returning the average of cosine similarity after applying sigmoid
        """
    token_1_vector, token_2_vector, token_3_vector = nlp(token_1)[0], nlp(token_2)[0], nlp(token_3)[0]
    avg = 0.0
    if token_1_vector.has_vector:
        if token_2_vector.has_vector:
            if token_3_vector.has_vector:
                similarity_1 = sigmoid(token_1_vector.similarity(token_2_vector))
                similarity_2 = sigmoid(token_2_vector.similarity(token_3_vector))
                similarity_3 = sigmoid(token_1_vector.similarity(token_3_vector))
                similarity_3 = 0
                avg = average(similarity_1, similarity_2, similarity_3)
    return avg


def sigmoid(x):
    """
        Calculating the sigmoid of a given number

        Parameters:
        x (float): a cosine similarity

        Returns:
        sigmoid (float): Transforming a given cosine similarity to a sort of probability between 0 and 1
        """
    return 1 / (1 + math.exp(-x))


def generate_combination(token):
    """
        Generate all possible combination of a three words splitted token

        Parameters:
        token (string): the mispelled word to split

        Returns:
        list_of_combinations (list): a list of all possible combinations that could be extracted from that toekn 
        """
    token_length = len(token)
    list_of_combinations = []
    for i in range(0, token_length - 1):
        token_1 = token[0:i + 1]
        token_2 = token[i + 1:]
        for j in range(0, len(token_2)):
            list_of_combinations.append(token_1 + ' ' + token_2[0:j + 1] + ' ' + token_2[j + 1:])

    return list_of_combinations


def segment_token(token):
    """
        segment a given token into the right set of tokens

        Parameters:
        list_of_combinations (list): the mispelled word to split

        Returns:
        list_of_combinations (list): a list of all possible combinations that could be extracted from that toekn 
        """
    token_vector = nlp(token)[0]
    if token_vector.has_vector:
        return token
    else:
        sim_values = {}
        separated_tokens = ''
        list_of_combinations = generate_combination(token)
        for elm in list_of_combinations:
            text = elm.split(' ')
            token1 = text[0]
            token2 = text[1]
            token3 = text[2]
            if token3 == '':
                token_1_vector = nlp(token1)[0]
                token_2_vector = nlp(token2)[0]
                if token_1_vector.has_vector:
                    if token_2_vector.has_vector:
                        sim = sigmoid(token_1_vector.similarity(token_2_vector))
                        sim_values[sim] = token1 + ' ' + token2
                        separated_tokens = sim_values[max(sim_values)]
            else:
                token_1_vector = nlp(token1)[0]
                token_2_vector = nlp(token2)[0]
                token_3_vector = nlp(token3)[0]
                if token_1_vector.has_vector and token_2_vector.has_vector and token_3_vector.has_vector:
                    sim = measure_similarity(token1, token2, token3)
                    sim_values[sim] = elm
                    separated_tokens = sim_values[max(sim_values)]

        return separated_tokens