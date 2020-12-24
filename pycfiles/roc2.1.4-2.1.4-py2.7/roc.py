# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\ROC\roc.py
# Compiled at: 2018-08-19 23:57:41
import matplotlib.pyplot as plt
from Analyze import Analyze
import os.path, random
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

def roc(standard_path='truth', test_path='test', stdscore=0.32, result_roc='result_roc', image='image'):
    db = []
    dd = []
    conpos = 0
    pos, db, temp = Analyze(standard_path, test_path)
    if temp == 0:
        print 'there are not tag "score" in xml files'
        return
    db = sorted(db, key=lambda x: x[2], reverse=True)
    for i in range(0, len(db)):
        dbscore = db[i][2]
        if dbscore >= stdscore and db[i][0] == 0 and db[i][1] == 1:
            dd.append([0, 1, dbscore])
            conpos += 1
        elif dbscore < stdscore and db[i][0] == 1 and db[i][1] == 0:
            dd.append([0, 1, dbscore])
            conpos += 1
        elif dbscore < stdscore and db[i][0] == 0 and db[i][1] == 1:
            dd.append([1, 0, dbscore])
        elif dbscore < stdscore and db[i][0] == 0 and db[i][1] == 1:
            dd.append([1, 0, dbscore])

    for i in range(len(dd)):
        a = random.random()
        dd[i][2] = round(a, 5)

    dd = sorted(dd, key=lambda x: x[2], reverse=True)
    xy_arr = []
    score = []
    tp, fp = (0.0, 0.0)
    for i in range(len(dd)):
        tp += dd[i][0]
        fp += dd[i][1]
        xy_arr.append([tp, fp / conpos])
        score.append(dd[i][2])

    auc = 0.0
    prev_x = 0
    for x, y in xy_arr:
        if x != prev_x:
            auc += (x - prev_x) * y
            prev_x = x

    x = [ _a[0] for _a in xy_arr ]
    y = [ _a[1] for _a in xy_arr ]
    z = [ _a for _a in score ]
    result_roc += '.txt'
    image += '.png'
    plt.title('ROC (AUC = %.4f)' % auc)
    plt.xlabel('False Count')
    plt.ylabel('True Positive Rate')
    plt.plot(x, y, color='blue', label='rate')
    plt.plot(x, z, color='black', label='score')
    xmajorLocator = MultipleLocator(tp / 8)
    xminorLocator = MultipleLocator(tp / 16)
    ymajorLocator = MultipleLocator(0.2)
    yminorLocator = MultipleLocator(0.05)
    ax = plt.subplot()
    ax.xaxis.set_major_locator(xmajorLocator)
    ax.yaxis.set_major_locator(ymajorLocator)
    ax.xaxis.set_minor_locator(xminorLocator)
    ax.yaxis.set_minor_locator(yminorLocator)
    ax.xaxis.grid(True, which='major')
    ax.yaxis.grid(True, which='minor')
    plt.legend(bbox_to_anchor=(0.0, 1.08, 1.0, 0.102), loc=2, ncol=2, mode='expand', borderaxespad=0.0)
    plt.grid()
    plt.grid(color='y', linestyle='--')
    plt.savefig(image)
    plt.show()
    with open(result_roc, 'w') as (fp):
        for i in range(len(dd)):
            fp.write('%d %f %f \n' % (x[i], y[i], z[i]))


if __name__ == '__main__':
    roc()