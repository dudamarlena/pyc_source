# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\ROC\conRoc.py
# Compiled at: 2018-08-08 08:51:50
import os, os.path, matplotlib.pyplot as plt
cnames = ('aquamarine', 'black', 'blue', 'blueviolet', 'brown', 'burlywood', 'cadetblue',
          'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'crimson', 'cyan',
          'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkkhaki',
          'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred',
          'darkseagreen', 'darkslateblue', 'darkslategray', 'darkturquoise', 'darkviolet',
          'deeppink', 'deepskyblue', 'dimgray', 'firebrick', 'forestgreen', 'fuchsia',
          'gold', 'goldenrod', 'gray', 'green', 'hotpink', 'indianred', 'indigo',
          'lawngreen', 'lime', 'limegreen', 'magenta', 'maroon', 'navy', 'olive',
          'olivedrab', 'orange', 'orchid', 'palevioletred', 'peru', 'plum', 'purple',
          'red', 'sienna', 'skyblue', 'slateblue', 'slategray', 'springgreen', 'steelblue',
          'tan', 'teal', 'thistle', 'turquoise', 'violet', 'yellow')

def conRoc(pre_file='file', image='image', titlestr='roc'):
    data = []
    ab = []
    aa = []
    files1 = os.listdir(pre_file)
    for File in files1:
        aa.append(File)
        tt = File[-4:]
        if tt != '.txt':
            break
        path = os.path.join(pre_file, File)
        f = open(path)
        line = f.readline()
        db = []
        while line:
            data = line.split()
            if data == []:
                break
            data[0] = float(data[0])
            data[1] = float(data[1])
            data[2] = float(data[2])
            db.append(data)
            line = f.readline()

        db = sorted(db, key=lambda x: x[2], reverse=True)
        ab.append(db)

    for i in range(len(ab)):
        x = [ _a[0] for _a in ab[i] ]
        y = [ _a[1] for _a in ab[i] ]
        z = [ _a[2] for _a in ab[i] ]
        plt.xlabel('False Count')
        plt.ylabel('True Positive Rate')
        plt.title(titlestr)
        plt.plot(x, y, color=cnames[(i % 69)], label=aa[i][:-4])
        plt.plot(x, z, color=cnames[(i % 69)])

    image += '.jpg'
    plt.legend(bbox_to_anchor=(0.0, 1.02, 1.0, 0.102), loc=2, ncol=3, mode='expand', borderaxespad=0.0)
    plt.grid()
    plt.grid(color='y', linestyle='--')
    plt.savefig(image)
    plt.show()
    print 'Run successfully'


if __name__ == '__main__':
    conRoc()