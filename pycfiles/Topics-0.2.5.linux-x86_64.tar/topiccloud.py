# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/Topics/visualization/topiccloud.py
# Compiled at: 2013-03-05 08:45:27
import numpy as np
from Topics.visualization.wordcloud import make_wordcloud

class GenCloud(object):

    def __init__(self, vocab, topics):
        """
        Generates topic cloud image for the LDA topic model
        :param vocab: vocabulary list used to estimate topics
        :param topics: variational parameter numpy matrix, in which each line is a topic, with the coefficients
            for each word in the vocabulary.
        """
        self.vocab = np.array(vocab)
        self.topics = topics

    def gen_image(self, topic, fname='topic', width=600, height=400):
        """
        Generates and shows the image for the topic specified
        :param width: width of the resulting image
        :param height: height of the resulting image
        :param fname: Name of the file with which to save the topic cloud images
        :param topic: Integer corresponding to the line of the topic matrix
        """
        make_wordcloud(words=self.vocab, counts=self.topics[topic, :], fname=('{}_{}.png').format(fname, topic), width=width, height=height)