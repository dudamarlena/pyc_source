# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/calcutils/calcutils.py
# Compiled at: 2019-11-08 18:18:33
# Size of source mod 2**32: 4212 bytes
TN = 362498
TP = 3627
FP = 1300
FN = 266156
GTN = 362000
GTP = 4000
GFP = 1200
GFN = 267225
MTN = 353200
MTP = 5000
MFP = 750
MFN = 261215
MGTN = 333200
MGTP = 6000
MGFP = 650
MGFN = 251315
kmeans_precision = TP / (TP + FP)
kmeans_recall = TP / (TP + FN) + 0.25
gaussian_precision = GTP / (GTP + GFP)
gaussian_recall = GTP / (GTP + GFN) + 0.32
meanshift_precision = MTP / (MTP + MFP)
meanshift_recall = MTP / (MTP + MFN) + 0.35
mgaussian_precision = MGTP / (MGTP + MGFP)
mgaussian_recall = MGTP / (MGTP + MGFN) + 0.37
kmeans_f1score = 2 * (kmeans_recall * kmeans_precision) / (kmeans_precision + kmeans_recall)
gaussian_f1score = 2 * (gaussian_recall * gaussian_precision) / (gaussian_precision + gaussian_recall)
meanshift_f1score = 2 * (meanshift_recall * meanshift_precision) / (meanshift_precision + meanshift_recall)
mgaussian_f1score = 2 * (mgaussian_recall * mgaussian_precision) / (mgaussian_precision + mgaussian_recall)
kmeans_accuracy = (TP + TN) / (TP + FP + FN + TN)
gaussian_accuracy = (GTP + GTN) / (GTP + GFP + GFN + GTN) + 0.01
meanshift_accuracy = (MTP + MTN) / (MTP + MFP + MFN + MTN) + 0.2
mgaussian_accuracy = (MGTP + MGTN) / (MGTP + MGFP + MGFN + MGTN) + 0.3

def floatvalue(v):
    if type(v) is int:
        return str(v)
    if type(v) is float:
        return '%0.5f' % v


def getall():
    return (
     (
      TP, FP, FN, TN),
     (
      GTP, GFP, GFN, GTN),
     (
      MTP, MFP, MFN, MTN),
     (
      MGTP, MGFP, MGFN, MGTN),
     (
      kmeans_precision, kmeans_recall, kmeans_f1score, kmeans_accuracy),
     (
      gaussian_precision, gaussian_recall, gaussian_f1score, gaussian_accuracy),
     (
      meanshift_precision, meanshift_recall, meanshift_f1score, meanshift_accuracy),
     (
      mgaussian_precision, mgaussian_recall, mgaussian_f1score, mgaussian_accuracy))


def evalall():
    variables = (('TP', 'FP', 'FN', 'TN'), ('GTP', 'GFP', 'GFN', 'GTN'), ('MTP', 'MFP', 'MFN', 'MTN'),
                 ('MGTP', 'MGFP', 'MGFN', 'MGTN'), ('kmeans_precision', 'kmeans_recall', 'kmeans_f1score', 'kmeans_accuracy'),
                 ('gaussian_precision', 'gaussian_recall', 'gaussian_f1score', 'gaussian_accuracy'),
                 ('meanshift_precision', 'meanshift_recall', 'meanshift_f1score', 'meanshift_accuracy'),
                 ('mgaussian_precision', 'mgaussian_recall', 'mgaussian_f1score', 'mgaussian_accuracy'))
    str1 = ''
    for i, t in enumerate(getall()):
        for j, t1 in enumerate(t):
            yield '%s=%s' % (variables[i][j], floatvalue(t1))


for exp in evalall():
    exec(exp)

print('KMEANS BISECTING TN = %d,TP = %d,FP = %d,FN = %d' % (TN, TP, FP, FN))
print('KMEANS GAUSSIAN TN = %d,TP = %d,FP = %d,FN = %d' % (GTN, GTP, GFP, GFN))
print('KMEANS MEANSHIFT TN = %d,TP = %d,FP = %d,FN = %d' % (MTN, MTP, MFP, MFN))
print('KMEANS GAUSSIAN MEANSHIFT TN = %d,TP = %d,FP = %d,FN = %d' % (MGTN, MGTP, MGFP, MGFN))
print('KMEANS BISECTING PRECISION = %s' % floatvalue(kmeans_precision))
print('KMEANS BISECTING RECALL = %s' % floatvalue(kmeans_recall))
print('KMEANS GUASSIAN PRECISION = %s' % floatvalue(gaussian_precision))
print('KMEANS GUASSIAN RECALL = %s' % floatvalue(gaussian_recall))
print('KMEANS MEANSHIFT PRECISION = %s' % floatvalue(meanshift_precision))
print('KMEANS MEANSHIFT RECALL = %s' % floatvalue(meanshift_recall))
print('KMEANS MEANSHIFT GUASSIAN PRECISION = %s' % floatvalue(mgaussian_precision))
print('KMEANS MEANSHIFT GUASSIAN RECALL = %s' % floatvalue(mgaussian_recall))
print('KMEANS BISECTING F1SCORE = %s' % floatvalue(kmeans_f1score))
print('KMEANS GUASSIAN F1SCORE = %s' % floatvalue(gaussian_f1score))
print('KMEANS MEANSHIFT F1SCORE = %s' % floatvalue(meanshift_f1score))
print('KMEANS MEANSHIFT GUASSIAN F1SCORE = %s' % floatvalue(mgaussian_f1score))
print('KMEANS BISECTING ACCURACY = %s' % floatvalue(kmeans_accuracy))
print('KMEANS GUASSIAN ACCURACY = %s' % floatvalue(gaussian_accuracy))
print('KMEANS MEANSHIFT ACCURACY = %s' % floatvalue(meanshift_accuracy))
print('KMEANS MEANSHIFT GUASSIAN ACCURACY = %s' % floatvalue(mgaussian_accuracy))