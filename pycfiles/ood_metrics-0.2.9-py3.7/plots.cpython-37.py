# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ood_metrics/plots.py
# Compiled at: 2020-01-10 16:10:53
# Size of source mod 2**32: 3330 bytes
from sklearn.metrics import roc_curve, auc, precision_recall_curve
import matplotlib.pyplot as plt
import numpy as np
from .metrics import fpr_at_95_tpr, auroc, aupr

def plot_roc(preds, labels, title='Receiver operating characteristic'):
    """Plot an ROC curve based on unthresholded predictions and true binary labels.
    
    preds: array, shape = [n_samples]
           Target scores, can either be probability estimates of the positive class, confidence values, or non-thresholded measure of decisions.
           
    labels: array, shape = [n_samples]
            True binary labels in range {0, 1} or {-1, 1}.

    title: string, optional (default="Receiver operating characteristic")
           The title for the chart
    """
    fpr, tpr, _ = roc_curve(labels, preds)
    tpr95 = fpr_at_95_tpr(preds, labels)
    roc_auc = auroc(preds, labels)
    plt.figure()
    lw = 2
    plt.plot(fpr, tpr, color='darkorange', lw=lw,
      label=('AUROC = %0.2f' % roc_auc))
    plt.plot([0, 1], [0.95, 0.95], color='black', lw=lw, linestyle=':', label=('FPR (95%% TPR) = %0.2f' % tpr95))
    plt.plot([tpr95, tpr95], [0, 1], color='black', lw=lw, linestyle=':')
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--', label='Random detector ROC')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(title)
    plt.legend(loc='lower right')
    plt.show()


def plot_pr(preds, labels, title='Precision recall curve'):
    """Plot an Precision-Recall curve based on unthresholded predictions and true binary labels.
    
    preds: array, shape = [n_samples]
           Target scores, can either be probability estimates of the positive class, confidence values, or non-thresholded measure of decisions.
           
    labels: array, shape = [n_samples]
            True binary labels in range {0, 1} or {-1, 1}.

    title: string, optional (default="Receiver operating characteristic")
           The title for the chart
    """
    precision, recall, _ = precision_recall_curve(labels, preds)
    prc_auc = auc(recall, precision)
    plt.figure()
    lw = 2
    plt.plot(recall, precision, color='darkorange', lw=lw,
      label=('PRC curve (area = %0.2f)' % prc_auc))
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title(title)
    plt.legend(loc='lower right')
    plt.show()


def plot_barcode(preds, labels):
    """Plot a visualization showing inliers and outliers sorted by their prediction of novelty."""
    x = sorted([a for a in zip(preds, labels)], key=(lambda x: x[0]))
    x = np.array([[49, 163, 84] if a[1] == 1 else [173, 221, 142] for a in x])
    axprops = dict(xticks=[], yticks=[])
    barprops = dict(aspect='auto', cmap=(plt.cm.binary_r), interpolation='nearest')
    fig = plt.figure()
    ax = (fig.add_axes)([0.3, 0.1, 0.6, 0.1], **axprops)
    (ax.imshow)((x.reshape((1, -1, 3))), **barprops)
    plt.show()