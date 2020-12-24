# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\ROC\roc.py
# Compiled at: 2018-08-07 07:24:09
import matplotlib.pyplot as plt
from Analyze_xml import Analyze_xml
import os.path, random

def roc(standard_path='truth', test_path='test', result_roc='result_roc', image='image'):
    db = []
    db, pos = Analyze_xml(standard_path, test_path)
    for i in range(len(db)):
        a = random.random()
        db[i][2] = round(a, 5)

    db = sorted(db, key=lambda x: x[2], reverse=True)
    xy_arr = []
    score = []
    tp, fp = (0.0, 0.0)
    for i in range(len(db)):
        tp += db[i][1]
        fp += db[i][0]
        xy_arr.append([tp, fp / pos])
        score.append(db[i][2])

    auc = 0.0
    prev_x = 0
    for x, y in xy_arr:
        if x != prev_x:
            auc += (x - prev_x) * y
            prev_x = x

    print db
    x = [ _a[0] for _a in xy_arr ]
    y = [ _a[1] for _a in xy_arr ]
    z = [ _a for _a in score ]
    result_roc += '.txt'
    image += '.png'
    plt.title('ROC (AUC = %.4f)' % auc)
    plt.xlabel('False Count')
    plt.ylabel('True Positive Rate')
    plt.plot(x, y)
    plt.plot(x, z)
    plt.savefig(image)
    plt.show()
    with open(result_roc, 'w') as (fp):
        for i in range(len(db)):
            fp.write('%d %f %f \n' % (x[i], y[i], z[i]))


if __name__ == '__main__':
    roc()