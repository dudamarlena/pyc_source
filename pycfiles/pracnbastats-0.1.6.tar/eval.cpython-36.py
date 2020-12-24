# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /data/code/pracmln/python3/pracmln/utils/eval.py
# Compiled at: 2019-02-27 05:10:32
# Size of source mod 2**32: 12681 bytes
import pickle
from subprocess import Popen, PIPE
from ..mln.util import logx

def KLDivergence(p, q):
    """
        Computes the Kullback-Leibler Divergence of two distributions p and q.
        """
    if type(p) is str:
        p = pickle.load(open(p))
    if type(q) is str:
        q = pickle.load(open(q))
    kl_div = 0
    for p_, q_ in zip(p, q):
        p_ = max(1e-10, p_)
        q_ = max(1e-10, q_)
        kl_div += p_ * logx(float(p_) / q_)

    return kl_div


class ConfusionMatrix(object):
    """ConfusionMatrix"""

    def __init__(self):
        self.matrix = {}
        self.instanceCount = 0
        self.labels = []

    def addClassificationResult(self, prediction, groundTruth, inc=1):
        """
                Add a new classification result to the confusion matrix.
                
                - gndTruth:     the correct label of an example
                - prediction:   the predicted class label of an example
                - inc:          the increment (default: 1)
                """
        if prediction not in self.labels:
            self.labels.append(prediction)
        else:
            if groundTruth not in self.labels:
                self.labels.append(groundTruth)
            gndTruths = self.matrix.get(prediction, None)
            if gndTruths is None:
                gndTruths = {}
                self.matrix[prediction] = gndTruths
            if self.matrix.get(groundTruth, None) is None:
                self.matrix[groundTruth] = {groundTruth: 0}
        gndTruths[groundTruth] = gndTruths.get(groundTruth, 0) + inc
        self.instanceCount += inc

    def getMatrixEntry(self, pred, clazz):
        """
                Returns the matrix entry for the prediction pred and ground truth clazz.
                """
        if self.matrix.get(pred, None) is None or self.matrix[pred].get(clazz, None) is None:
            return 0
        else:
            return self.matrix[pred][clazz]

    def countClassifications(self, classname):
        """
                Returns the true positive, true negative, false positive, false negative
                classification counts (in this order).
                """
        tp = self.matrix.get(classname, {}).get(classname, 0)
        classes = list(self.matrix.keys())
        fp = 0
        for c in classes:
            if c != classname:
                fp += self.getMatrixEntry(classname, c)

        fn = 0
        for c in classes:
            if c != classname:
                fn += self.getMatrixEntry(c, classname)

        tn = 0
        for c in classes:
            if c != classname:
                for c2 in classes:
                    if c2 != classname:
                        tn += self.getMatrixEntry(c, c2)

        assert sum([tp, tn, fp, fn]) == self.instanceCount
        return (
         tp, tn, fp, fn)

    def getMetrics(self, classname):
        """
                Returns the classifier evaluation metrices in the following order:
                Accuracy, Precision, Recall, F1-Score.
                """
        classes = []
        for classification in self.matrix:
            for truth in self.matrix.get(classification, {}):
                try:
                    classes.index(truth)
                except ValueError:
                    classes.append(truth)

        classes = sorted(classes)
        tp, tn, fp, fn = self.countClassifications(classname)
        acc = None
        if tp + tn + fp + fn > 0:
            acc = (tp + tn) / float(tp + tn + fp + fn)
        pre = 0.0
        if tp + fp > 0:
            pre = tp / float(tp + fp)
        rec = 0.0
        if tp + fn > 0:
            rec = tp / float(tp + fn)
        f1 = 0.0
        if pre + rec > 0:
            f1 = 2.0 * pre * rec / (pre + rec)
        return (
         acc, pre, rec, f1)

    def getTotalAccuracy(self):
        """
                Returns the fraction of correct predictions and
                total predictions.
                """
        true = 0
        total = 0
        for label in self.labels:
            tp, _, _, _ = self.countClassifications(label)
            true += tp

        return true / float(self.instanceCount)

    def getLatexTable(self):
        """
                Returns LaTex code for the confusion matrix.
                """
        grid = '|l|'
        for cl in sorted(self.labels):
            grid += 'l|'

        endl = '\n'
        result = ''
        result += '\\footnotesize' + endl
        result += '\\begin{tabular}{' + grid + '}' + endl
        headerRow = 'Prediction/Ground Truth'
        for cl in sorted(self.labels):
            headerRow += ' & \\begin{turn}{90}' + cl.replace('_', '\\_') + '\\end{turn}'

        examplesPerClass = {}
        for label in self.labels:
            tp, tn, fp, fn = self.countClassifications(label)
            examplesPerClass[label] = sum([tp, fp, fn])

        result += '\\hline' + endl
        result += headerRow + '\\\\ \\hline' + endl
        for clazz in sorted(self.labels):
            values = []
            for cl2 in sorted(self.labels):
                counts = self.getMatrixEntry(clazz, cl2)
                values.append('\\cellcolor{cfmcolor!%d}%s' % (int(round(float(counts) / examplesPerClass[clazz] * 100)),
                 ('\\textbf{%d}' if clazz == cl2 else '%d') % counts))

            result += clazz.replace('_', '\\_') + ' & ' + ' & '.join(values) + '\\\\ \\hline' + endl

        result += '\\end{tabular}' + endl
        return result

    def printPrecisions(self):
        """
                Prints to the standard out a table of the class-specific error measures accurracy, precision, recall, F score.
                """
        classes = []
        for classification in self.matrix:
            for truth in self.matrix.get(classification, {}):
                try:
                    classes.index(truth)
                except ValueError:
                    classes.append(truth)

        classes = sorted(classes)
        for cf in classes:
            acc, pre, rec, f1 = self.getMetrics(cf)
            print('%s: - Acc=%.2f, Pre=%.2f, Rec=%.2f F1=%.2f' % (cf, acc, pre, rec, f1))

        print('')

    def printAveragePrecision(self):
        classes = []
        for classification in self.matrix:
            for truth in self.matrix.get(classification, {}):
                try:
                    classes.index(truth)
                except ValueError:
                    classes.append(truth)

        classes = sorted(classes)
        aAcc = 0.0
        aPre = 0.0
        aRec = 0.0
        aF1 = 0.0
        for cf in classes:
            acc, pre, rec, f1 = self.getMetrics(cf)
            aAcc += acc
            aPre += pre
            aRec += rec
            aF1 += f1

        print('%s: - Acc=%.2f, Pre=%.2f, Rec=%.2f F1=%.2f' % (
         'Average: ', aAcc / len(classes), aPre / len(classes), aRec / len(classes), aF1 / len(classes)))
        print('')

    @staticmethod
    def compareConfusionMatrices(*matricesPath):
        for path in matricesPath:
            cm = ConfusionMatrix.load(path)
            print(path)
            cm.printAveragePrecision()

    def iteritems(self):
        """
                Iterates over triples of the form (prediction, class, count) of this confusion matrix.
                """
        for prediction in self.labels:
            for clazz in self.labels:
                yield (
                 prediction, clazz, self.getMatrixEntry(prediction, clazz))

    def combine(self, matrix):
        """
                Combines another confusion matrix with this one.
                """
        for pred, clazz, count in matrix.items():
            self.addClassificationResult(pred, clazz, inc=count)

    def __str__(self):
        maxNumDigits = max(max([list(x.values()) for x in list(self.matrix.values())], key=max))
        maxNumDigits = len(str(maxNumDigits))
        maxClassLabelLength = max(list(map(len, list(self.matrix.keys()))))
        padding = 1
        numLabels = len(list(self.matrix.keys()))
        cellwidth = max(maxClassLabelLength, maxNumDigits, 3) + 2 * padding
        print(maxNumDigits)
        hline = '|' + '-' * cellwidth + '+'
        hline += '+'.join(['-' * cellwidth] * numLabels) + '|'
        sep = '|'
        outerHLine = '-' * len(hline)

        def createTableRow(args):
            return sep + sep.join([str(a).rjust(cellwidth - padding) + ' ' * padding for a in args]) + sep

        endl = '\n'
        table = outerHLine + endl
        table += createTableRow(['P\\C'] + sorted(self.matrix.keys())) + endl
        table += hline + endl
        for i, clazz in enumerate(sorted(self.labels)):
            table += createTableRow([clazz] + [self.getMatrixEntry(clazz, x) for x in sorted(self.labels)]) + endl
            if i < len(list(self.matrix.keys())) - 1:
                table += hline + endl

        table += outerHLine
        return table

    def printTable(self):
        """
                Prints the confusion matrix nicely formatted onto the standard out.
                """
        print(self)

    def toFile(self, filename):
        """
                Pickles the confusion matrix to a file with the given name.
                """
        pickle.dump(self, open(filename, 'w+'))

    def writeLatexFile(self, filename):
        texFileName = filename + '.tex'
        texFile = open(texFileName, 'w+')
        texFile.write('\n\t\t\\documentclass[10pt]{article}\n\t\t\\usepackage{color}\n\t\t\\usepackage{rotating}\n\t\t\\usepackage[table]{xcolor}\n\t\t\\definecolor{cfmcolor}{rgb}{0.2,0.4,0.6}\n\t\t\\begin{document}\n\t\t\\pagenumbering{gobble}\n\t\t\\resizebox{\\columnwidth}{!}{\n\t\t%s}\n\t\t\\end{document}\n\t\t' % self.getLatexTable())
        texFile.close()

    @staticmethod
    def load(filename):
        return pickle.load(open(filename))

    def toPDF(self, filename):
        """
                Creates a PDF file of this matrix. Requires 'pdflatex' and 'pdfcrop' installed.
                """
        texFileName = filename + '.tex'
        texFile = open(texFileName, 'w+')
        texFile.write('\n\t\t\\documentclass[10pt]{article}\n\t\t\\usepackage{color}\n\t\t\\usepackage{rotating}\n\t\t\\usepackage[table]{xcolor}\n\t\t\\definecolor{cfmcolor}{rgb}{0.2,0.4,0.6}\n\t\t\\begin{document}\n\t\t\\pagenumbering{gobble}\n\t\t\\resizebox{\\columnwidth}{!}{\n\t\t%s}\n\t\t\\end{document}\n\t\t' % self.getLatexTable())
        texFile.close()
        cmd = 'pdflatex -halt-on-error %s' % texFileName
        p = Popen(cmd, shell=True)
        if p.wait() != 0:
            raise Exception("Couldn't compile LaTex.")
        else:
            cmd = 'pdfcrop %s.pdf %s.pdf' % (filename, filename)
            p = Popen(cmd, shell=True)
        if p.wait() != 0:
            raise Exception("Couldn't crop pdf")


if __name__ == '__main__':
    cm = ConfusionMatrix()
    for _ in range(10):
        cm.addClassificationResult('AAA', 'A')

    cm.addClassificationResult('AAA', 'AAA')
    cm.addClassificationResult('AAA', 'AAA')
    cm.addClassificationResult('AAA', 'AAA')
    cm.addClassificationResult('AAA', 'AAA')
    cm.addClassificationResult('AAA', 'B')
    cm.addClassificationResult('AAA', 'B')
    cm.addClassificationResult('AAA', 'C')
    cm.addClassificationResult('B', 'AAA')
    cm.addClassificationResult('B', 'AAA')
    cm.addClassificationResult('B', 'C')
    cm.addClassificationResult('B', 'B')
    cm.printTable()
    cm.printPrecisions()
    print(cm.getLatexTable())
    cm.toPDF('tmp')
    print(pickle.loads(pickle.dumps(cm)))