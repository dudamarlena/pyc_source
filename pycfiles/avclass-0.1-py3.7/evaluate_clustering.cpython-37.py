# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/avclass/evaluate_clustering.py
# Compiled at: 2019-11-13 14:15:27
# Size of source mod 2**32: 4212 bytes
import sys

def tp_fp_fn(CORRECT_SET, GUESS_SET):
    """
    INPUT: dictionary with the elements in the cluster from the ground truth
    (CORRECT_SET) and dictionary with the elements from the estimated cluster
    (ESTIMATED_SET).

    OUTPUT: number of True Positives (elements in both clusters), False
    Positives (elements only in the ESTIMATED_SET), False Negatives (elements
    only in the CORRECT_SET).
    """
    tp = 0
    fp = 0
    fn = 0
    for elem in GUESS_SET:
        if elem in CORRECT_SET:
            tp += 1
        else:
            fp += 1

    for elem in CORRECT_SET:
        if elem not in GUESS_SET:
            fn += 1

    return (
     tp, fp, fn)


def eval_precision_recall_fmeasure(GROUNDTRUTH_DICT, ESTIMATED_DICT):
    """
    INPUT: dictionary with the mapping "element:cluster_id" for both the ground
    truth and the ESTIMATED_DICT clustering.

    OUTPUT: average values of Precision, Recall and F-Measure.
    """
    tmp_precision = 0
    tmp_recall = 0
    rev_est_dict = {}
    for k, v in ESTIMATED_DICT.items():
        if v not in rev_est_dict:
            rev_est_dict[v] = set([k])
        else:
            rev_est_dict[v].add(k)

    gt_rev_dict = {}
    for k, v in GROUNDTRUTH_DICT.items():
        if v not in gt_rev_dict:
            gt_rev_dict[v] = set([k])
        else:
            gt_rev_dict[v].add(k)

    counter, l = 0, len(ESTIMATED_DICT)
    sys.stderr.write('Calculating precision and recall\n')
    for element in ESTIMATED_DICT:
        if counter % 1000 == 0:
            sys.stderr.write('\r%d out of %d' % (counter, l))
            sys.stderr.flush()
        counter += 1
        guess_cluster_id = ESTIMATED_DICT[element]
        correct_cluster_id = GROUNDTRUTH_DICT[element]
        tp, fp, fn = tp_fp_fn(gt_rev_dict[correct_cluster_id], rev_est_dict[guess_cluster_id])
        p = 1.0 * tp / (tp + fp)
        tmp_precision += p
        r = 1.0 * tp / (tp + fn)
        tmp_recall += r

    sys.stderr.write('\r%d out of %d' % (counter, l))
    sys.stderr.write('\n')
    precision = 100.0 * tmp_precision / len(ESTIMATED_DICT)
    recall = 100.0 * tmp_recall / len(ESTIMATED_DICT)
    fmeasure = 2 * precision * recall / (precision + recall)
    return (precision, recall, fmeasure)


if __name__ == '__main__':
    diz_grth = {'a':1, 
     'b':1, 
     'c':2, 
     'd':3}
    diz_estim = {'a':66, 
     'b':'malware', 
     'c':'goodware', 
     'd':'trojan'}
    diz_estim_grth = {'a':2, 
     'b':2, 
     'c':66, 
     'd':9}
    print('Ground truth')
    print('%8s --> %10s' % ('Element', 'Cluster_ID'))
    for k, v in diz_grth.iteritems():
        print('%8s --> %10s' % (k, v))

    print('Estimated clustering')
    print('%8s --> %10s' % ('Element', 'Cluster_ID'))
    for k, v in diz_estim.iteritems():
        print('%8s --> %10s' % (k, v))

    p, r, f = eval_precision_recall_fmeasure(diz_grth, diz_estim)
    print('Precison: %s%%' % p)
    print('Recall: %s%%' % r)
    print('F-Measure: %s%%' % f)