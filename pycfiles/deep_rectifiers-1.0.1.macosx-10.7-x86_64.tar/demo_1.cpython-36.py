# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/aidanrocke/anaconda/envs/py3k/lib/python3.6/site-packages/deep_rectifiers/demo_1.py
# Compiled at: 2017-04-27 07:39:25
# Size of source mod 2**32: 5098 bytes
"""
Created on Mon Apr 24 13:50:22 2017

@author: aidanrocke
"""
import sys
sys.path.insert(0, '/path/to/mod_directory')

def sort(x):
    n = len(x)
    if min(x[1:n - 1] - x[0:n - 2]) < 0:
        for passnum in range(len(x) - 1, 0, -1):
            for i in range(passnum):
                if x[i] > x[(i + 1)]:
                    temp = x[i]
                    x[i] = x[(i + 1)]
                    x[i + 1] = temp

    return x


X_train1, Y_train1, X_test1, Y_test1 = datasets(0, 100, 10000, 10, 1)
X_train2, Y_train2, X_test2, Y_test2 = datasets(-100, 100, 10000, 10, 1)
X_train3, Y_train3, X_test3, Y_test3 = datasets(-1, 1, 10000, 10, 0.5)
X_train4, Y_train4, X_test4, Y_test4 = datasets(-100, 100, 10000, 10, 0.5)
W = []
for layer in model.layers:
    W.append(layer.get_weights())

history = model.fit(X_train1, Y_train1, nb_epoch=20, batch_size=500, verbose=1)
evaluation1 = model.evaluate(X_test1, Y_test1, verbose=1)
evaluation2 = model.evaluate(X_test2, Y_test2, verbose=1)
evaluation3 = model.evaluate(X_test3, Y_test3, verbose=1)
evaluation4 = model.evaluate(X_test4, Y_test4, verbose=1)
history = model.fit((X_train3 / 100), Y_train3, nb_epoch=20, batch_size=500, verbose=1)
evaluation = model.evaluate((X_test3 / 100), Y_test3, verbose=1)
evaluation = model.evaluate(X_test3, Y_test3, verbose=1)
evaluation = model.evaluate((X_test3 / 1000), Y_test3, verbose=1)
history = model.fit(X_train2, Y_train2, nb_epoch=20, batch_size=500, verbose=1)
evaluation = model.evaluate(X_test2, Y_test2, verbose=1)
history = model.fit(X_train3, Y_train3, nb_epoch=20, batch_size=500, verbose=1)
evaluation = model.evaluate(X_test3, Y_test3, verbose=1)
history = model.fit(X_train4, Y_train4, nb_epoch=20, batch_size=500, verbose=1)
evaluation = model.evaluate(X_test4, Y_test4, verbose=1)
X_train5, Y_train5, X_test5, Y_test5 = datasets(3, 4, 10000, 10, 0.5)
evaluation = model.evaluate(X_test5, Y_test5, verbose=1)
evaluation = model.evaluate(X_test_2, Y_test_2, verbose=1)
X_unsorted = np.random.uniform(low=(-1), high=1, size=(10000, 10))
X_sorted = np.sort(X_unsorted, axis=1)
X_train = np.vstack((X_unsorted, X_sorted))
Y_train = np.vstack((np.zeros((10000, 1)), np.ones((10000, 1))))
X_test1 = np.random.randint(low=(-1), high=1, size=(10000, 10))
X_test2 = np.sort(X_test1, axis=1)
X_test = np.vstack((X_test1, X_test2))
Y_test = np.vstack((np.zeros((10000, 1)), np.ones((10000, 1))))
permutation = np.random.permutation(range(len(X_train)))
X_train, Y_train = X_train[permutation], Y_train[permutation]
X_test_3, Y_test_3 = X_test[permutation], Y_test[permutation]
evaluation = model.evaluate(X_test_3, Y_test_3, verbose=1)