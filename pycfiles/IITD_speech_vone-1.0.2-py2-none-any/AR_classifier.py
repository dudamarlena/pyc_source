# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ravijayanth/Desktop/project/library/Accept_Reject/AR_classifier.py
# Compiled at: 2019-11-07 09:25:36
import numpy as np, csv
from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
import pickle
from sklearn.model_selection import KFold
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt, seaborn as sn

def plotConfusionMatrix(confusionMatrix, classes, fname):
    plt.figure(figsize=(10, 7))
    ax = sn.heatmap(confusionMatrix, fmt='d', annot=True, cbar=False, cmap=sn.cubehelix_palette(15), xticklabels=classes, yticklabels=classes)
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    ax.set(xlabel='Predicted', ylabel='Actual')
    figure = fname + '.jpg'
    plt.title(fname, y=1.08, loc='center')
    plt.savefig(figure)
    plt.show()
    plt.close()


def train_model_SVM(train_Data, test_Data, model_name):
    x_train = train_Data[:, 0:137]
    y_train = train_Data[:, 137]
    x_test = test_Data[:, 0:137]
    y_test = test_Data[:, 137]
    scaler = StandardScaler()
    scaler.fit(x_train)
    x_train = scaler.transform(x_train)
    x_test = scaler.transform(x_test)
    svm = SVC(C=2, gamma=0.03).fit(x_train, y_train)
    print ('Accuracy on training set: {:.3f}').format(svm.score(x_train, y_train))
    accuracy = svm.score(x_test, y_test)
    print ('Accuracy on test set: {:.3f}').format(accuracy)
    y_pred = svm.predict(x_test)
    pickle.dump(svm, open(model_name, 'wb'))
    return (
     y_test, y_pred, accuracy)


def k_fold_validation_train_model(input_file, k=10):
    rows = []
    with open(input_file, 'r') as (csvfile):
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if int(row[137]) < 3:
                rows.append(row)

    rows = np.array(rows)
    print rows.shape
    kf = KFold(n_splits=k, shuffle=True)
    kf.get_n_splits(rows)
    accuracies = []
    test_true = np.array([])
    test_predicted = np.array([])
    i = 0
    for train_index, test_index in kf.split(rows):
        print 'Chunk OF Data for iteration : ' + str(i)
        train_data = rows[train_index]
        test_data = rows[test_index]
        y_true, y_pred, accuracy = train_model_SVM(train_data, test_data)
        accuracies.append(accuracy)
        test_true = np.append(test_true, y_true)
        test_predicted = np.append(test_predicted, y_pred)
        i = i + 1
        break

    accuracies = np.array(accuracies)
    print ('Accuracies : ', accuracies)
    print ('Average Accuracy : {:.3f}').format(np.average(accuracies))
    print ('F1_score', f1_score(test_true, test_predicted, average=None))
    classes = list(sorted(set(test_true)))
    results = confusion_matrix(test_true, test_predicted, labels=classes)
    plotConfusionMatrix(results, classes, 'accept_reject_classifier_confusion_matrix')
    y_true, y_pred, accuracy = train_model_SVM(rows, rows, 'accept_reject_model')
    return