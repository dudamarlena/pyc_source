# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ai_tools/roc_yolo.py
# Compiled at: 2018-08-24 08:17:02
import pylab as pl
from Analyze_txt import Analyze_txt
from roc_matrix import get_roc_matrix
import sys
from ai_tools import draw
from ai_tools import save2server
from zprint import *
import os, pdb

def txt2xml(xmlfilename, txtfilename):
    with open(xmlfilename, 'r') as (fs):
        managerList = []
        doc = xml.dom.minidom.Document()
        root = doc.createElement('Recognition')
        root.setAttribute('type', 'face')
        doc.appendChild(root)
        str = fs.read()
        line = str.split()
        print line
        for i in range(0, int(line[1])):
            managerList.append([{'xmin': line[(2 + i * 4)], 'ymin': line[(3 + i * 4)], 'xmax': line[(4 + i * 4)], 'ymax': line[(5 + i * 4)]}])

        for i in managerList:
            for j in range(len(i)):
                nodeManager = doc.createElement('bndbox')
                nodeXmin = doc.createElement('xmin')
                nodeXmin.appendChild(doc.createTextNode(i[j]['xmin']))
                nodeYmin = doc.createElement('ymin')
                nodeYmin.appendChild(doc.createTextNode(i[j]['ymin']))
                nodeXmax = doc.createElement('xmax')
                nodeXmax.appendChild(doc.createTextNode(i[j]['xmax']))
                nodeYmax = doc.createElement('ymax')
                nodeYmax.appendChild(doc.createTextNode(i[j]['ymax']))
                nodeManager.appendChild(nodeXmin)
                nodeManager.appendChild(nodeYmin)
                nodeManager.appendChild(nodeXmax)
                nodeManager.appendChild(nodeYmax)
                root.appendChild(nodeManager)

        print line[0]
        fp = open(txtfilename, 'w')
        doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding='utf-8')


def roc(standard_path='truth', test_path='test', result_roc='roc.txt', result_jpg='roc.jpg'):
    db = []
    print 'analyze_xml:'
    db, pos = Analyze_txt(standard_path, test_path)
    db = sorted(db, key=lambda x: x[2], reverse=True)
    print pos
    xy_arr = []
    tp, fp = (0.0, 0.0)
    for i in range(len(db)):
        fp += db[i][1]
        tp += db[i][0]
        xy_arr.append([fp, tp / pos, db[i][2]])

    auc = 0.0
    prev_x = 0
    for x, y, t in xy_arr:
        if x != prev_x:
            auc += (x - prev_x) * y
            prev_x = x

    print xy_arr[(-1)]
    x = [ _a[0] for _a in xy_arr ]
    y = [ _a[1] for _a in xy_arr ]
    y1 = [ _a[2] for _a in xy_arr ]
    xl = [
     x, x]
    yl = [y, y1]
    img = draw.draw_curve_new(xl, yl, width=512, height=512, title='ROC (AUC=%.4F)' % (auc / float(x[(-1)])), xlabel='FalseAlarm Count', ylabel='True Positive Rate')
    save2server.save2server(result_jpg, img)
    with open(result_roc, 'w') as (fp):
        for i in range(len(xy_arr)):
            fp.write('%f %f %f \n' % (xy_arr[i][0], xy_arr[i][1], xy_arr[i][2]))


def sort_matrix(db, pos, max_fa):
    db = sorted(db, key=lambda x: x[2], reverse=True)
    xy_arr = []
    tp, fp = (0.0, 0.0)
    for i in range(len(db)):
        fp += db[i][1]
        tp += db[i][0]
        xy_arr.append([fp, tp / pos, db[i][2]])

    auc = 0.0
    prev_x = 0
    inds = 0
    for x, y, t in xy_arr:
        inds += 1 if x <= max_fa else 0
        if x != prev_x and x <= max_fa:
            auc += (x - prev_x) * y
            prev_x = x

    print xy_arr[(-1)]
    x = [ _a[0] for _a in xy_arr ]
    y = [ _a[1] for _a in xy_arr ]
    y1 = [ _a[2] for _a in xy_arr ]
    func = lambda x: x[:inds]
    x = func(x)
    y = func(y)
    y1 = func(y1)
    xl = [
     x, x]
    yl = [y, y1]
    return (
     xl, yl, auc)


def roc_title(gt_dir, pre_dir, title_add='merge', save_path='./', max_fa=3500):
    roc_m, pos_number = get_roc_matrix(gt_dir, pre_dir)
    zprint('%r,ig%r' % (len(roc_m), pos_number))
    xl, yl, auc = sort_matrix(roc_m, pos_number, max_fa)
    result_txt = os.path.join(save_path, '%s_roc.txt' % title_add)
    with open(result_txt, 'w') as (fp):
        for i in range(len(xl[0])):
            fp.write('%f %f %f \n' % (xl[0][i], yl[0][i], yl[1][i]))

    xl0 = xl
    yl0 = yl
    zprint('%f,%f' % (auc, xl[0][(-1)]))
    img = draw.draw_curve_new(xl0, yl0, width=512, height=512, title='ROC (AUC=%.4F)%s' % (auc / float(xl[0][(-1)]), title_add), xlabel='FalseAlarm Count', ylabel='True Positive Rate')
    result_jpg = os.path.join(save_path, '%s_roc.jpg' % title_add)
    save2server.save2server(result_jpg, img)


if __name__ == '__main__':
    gt_dir = sys.argv[1]
    resultdir = sys.argv[2]
    print gt_dir
    print resultdir
    roc(gt_dir, resultdir, 'result_roc.txt', 'roc.jpg')