# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notekeras/algorithm/FMLayer.py
# Compiled at: 2020-04-22 05:41:43
# Size of source mod 2**32: 2939 bytes
from tensorflow import keras

class Linear(keras.layers.Layer):

    def __init__(self, input_shape):
        super(Linear, self).__init__()
        self.name = 'liner-001'
        self.dense = keras.layers.Dense(name='line-dense1', units=32,
          activation=None)
        self.dense2 = keras.layers.Dense(name='line-dense2', units=32,
          activation=None)

    def build(self, input_shape):
        super(Linear, self).build(input_shape)

    def compute_output_shape(self, input_shape):
        return input_shape

    def call(self, input, **kwargs):
        output = self.dense(input)
        output = self.dense2(output)
        return output


docs = [
 'Well done!', 'Good work', 'Great effort', 'nice work', 'Excellent!',
 'Weak', 'Poor effort!', 'not good', 'poor work', 'Could have done better.']
labels = [
 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
vocab_size = 50
encoded_docs = [keras.preprocessing.text.one_hot(d, vocab_size) for d in docs]
print(encoded_docs)
max_length = 4
padded_docs = keras.preprocessing.sequence.pad_sequences(encoded_docs, maxlen=max_length, padding='post')
print(padded_docs)
model = keras.models.Sequential()
model.add(keras.layers.embeddings.Embedding(vocab_size, 8, input_length=max_length))
model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(1, activation='sigmoid'))
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
print(model.summary())
model.fit(padded_docs, labels, epochs=50, verbose=0)
loss, accuracy = model.evaluate(padded_docs, labels, verbose=0)
print('Accuracy: %f' % (accuracy * 100))
vocab = keras.Input(shape=(4, ), name='input_inner')
emb = keras.layers.embeddings.Embedding(vocab_size, 8, input_length=max_length)(vocab)
flat = keras.layers.Flatten()(emb)
liner = Linear((32, ))(flat)
d1 = keras.layers.Dense(1, activation='sigmoid')(liner)
model2 = keras.models.Model([vocab], d1)
model2.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
print(model2.summary())
model2.fit(padded_docs, labels, epochs=50, verbose=0)
loss, accuracy = model2.evaluate(padded_docs, labels, verbose=0)
print('Accuracy: %f' % (accuracy * 100))