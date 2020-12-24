# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xl_tensorflow\metrics\rafaelpadilla\Evaluator.py
# Compiled at: 2020-04-22 00:14:26
# Size of source mod 2**32: 23818 bytes
import os, sys
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from .BoundingBox import *
from .BoundingBoxes import *
from .utils import *
from xl_tool.data.image.annonation import get_bndbox

class Evaluator:

    def GetPascalVOCMetrics(self, boundingboxes, IOUThreshold=0.5, method=MethodAveragePrecision.EveryPointInterpolation):
        """Get the metrics used by the VOC Pascal 2012 challenge.
        Get
        Args:
            boundingboxes: Object of the class BoundingBoxes representing ground truth and detected
            bounding boxes;
            IOUThreshold: IOU threshold indicating which detections will be considered TP or FP
            (default value = 0.5);
            method (default = EveryPointInterpolation): It can be calculated as the implementation
            in the official PASCAL VOC toolkit (EveryPointInterpolation), or applying the 11-point
            interpolatio as described in the paper "The PASCAL Visual Object Classes(VOC) Challenge"
            or EveryPointInterpolation"  (ElevenPointInterpolation);
        Returns:
            A list of dictionaries. Each dictionary contains information and metrics of each class.
            The keys of each dictionary are:
            dict['class']: class representing the current dictionary;
            dict['precision']: array with the precision values;
            dict['recall']: array with the recall values;
            dict['AP']: average precision;
            dict['interpolated precision']: interpolated precision values;
            dict['interpolated recall']: interpolated recall values;
            dict['total positives']: total number of ground truth positives;
            dict['total TP']: total number of True Positive detections;
            dict['total FP']: total number of False Negative detections;
        """
        ret = []
        groundTruths = []
        detections = []
        classes = []
        for bb in boundingboxes.getBoundingBoxes():
            if bb.getBBType() == BBType.GroundTruth:
                groundTruths.append([
                 bb.getImageName(),
                 bb.getClassId(), 1,
                 bb.getAbsoluteBoundingBox(BBFormat.XYX2Y2)])
            else:
                detections.append([
                 bb.getImageName(),
                 bb.getClassId(),
                 bb.getConfidence(),
                 bb.getAbsoluteBoundingBox(BBFormat.XYX2Y2)])
            if bb.getClassId() not in classes:
                classes.append(bb.getClassId())

        classes = sorted(classes)
        for c in classes:
            dects = []
            [dects.append(d) for d in detections if d[1] == c]
            gts = []
            [gts.append(g) for g in groundTruths if g[1] == c]
            npos = len(gts)
            dects = sorted(dects, key=(lambda conf: conf[2]), reverse=True)
            TP = np.zeros(len(dects))
            FP = np.zeros(len(dects))
            det = Counter([cc[0] for cc in gts])
            for key, val in det.items():
                det[key] = np.zeros(val)

            for d in range(len(dects)):
                gt = [gt for gt in gts if gt[0] == dects[d][0]]
                iouMax = sys.float_info.min
                for j in range(len(gt)):
                    iou = Evaluator.iou(dects[d][3], gt[j][3])
                    if iou > iouMax:
                        iouMax = iou
                        jmax = j

                if iouMax >= IOUThreshold:
                    if det[dects[d][0]][jmax] == 0:
                        TP[d] = 1
                        det[dects[d][0]][jmax] = 1
                    else:
                        FP[d] = 1
                else:
                    FP[d] = 1

            acc_FP = np.cumsum(FP)
            acc_TP = np.cumsum(TP)
            rec = acc_TP / npos + 1e-08
            prec = np.divide(acc_TP, acc_FP + acc_TP + 1e-08)
            if method == MethodAveragePrecision.EveryPointInterpolation:
                ap, mpre, mrec, ii = Evaluator.CalculateAveragePrecision(rec, prec)
            else:
                ap, mpre, mrec, _ = Evaluator.ElevenPointInterpolatedAP(rec, prec)
            r = {'class':c, 
             'precision':prec, 
             'recall':rec, 
             'AP':ap, 
             'interpolated precision':mpre, 
             'interpolated recall':mrec, 
             'total positives':npos, 
             'total TP':np.sum(TP), 
             'total FP':np.sum(FP)}
            ret.append(r)

        return ret

    def PlotPrecisionRecallCurve(self, boundingBoxes, IOUThreshold=0.5, method=MethodAveragePrecision.EveryPointInterpolation, showAP=False, showInterpolatedPrecision=False, savePath=None, showGraphic=True):
        """PlotPrecisionRecallCurve
        Plot the Precision x Recall curve for a given class.
        Args:
            boundingBoxes: Object of the class BoundingBoxes representing ground truth and detected
            bounding boxes;
            IOUThreshold (optional): IOU threshold indicating which detections will be considered
            TP or FP (default value = 0.5);
            method (default = EveryPointInterpolation): It can be calculated as the implementation
            in the official PASCAL VOC toolkit (EveryPointInterpolation), or applying the 11-point
            interpolatio as described in the paper "The PASCAL Visual Object Classes(VOC) Challenge"
            or EveryPointInterpolation"  (ElevenPointInterpolation).
            showAP (optional): if True, the average precision value will be shown in the title of
            the graph (default = False);
            showInterpolatedPrecision (optional): if True, it will show in the plot the interpolated
             precision (default = False);
            savePath (optional): if informed, the plot will be saved as an image in this path
            (ex: /home/mywork/ap.png) (default = None);
            showGraphic (optional): if True, the plot will be shown (default = True)
        Returns:
            A list of dictionaries. Each dictionary contains information and metrics of each class.
            The keys of each dictionary are:
            dict['class']: class representing the current dictionary;
            dict['precision']: array with the precision values;
            dict['recall']: array with the recall values;
            dict['AP']: average precision;
            dict['interpolated precision']: interpolated precision values;
            dict['interpolated recall']: interpolated recall values;
            dict['total positives']: total number of ground truth positives;
            dict['total TP']: total number of True Positive detections;
            dict['total FP']: total number of False Negative detections;
        """
        results = self.GetPascalVOCMetrics(boundingBoxes, IOUThreshold, method)
        result = None
        for result in results:
            if result is None:
                raise IOError('Error: Class %d could not be found.' % classId)
            classId = result['class']
            precision = result['precision']
            recall = result['recall']
            average_precision = result['AP']
            mpre = result['interpolated precision']
            mrec = result['interpolated recall']
            npos = result['total positives']
            total_tp = result['total TP']
            total_fp = result['total FP']
            plt.close()
            if showInterpolatedPrecision:
                if method == MethodAveragePrecision.EveryPointInterpolation:
                    plt.plot(mrec, mpre, '--r', label='Interpolated precision (every point)')
                else:
                    if method == MethodAveragePrecision.ElevenPointInterpolation:
                        nrec = []
                        nprec = []
                        for idx in range(len(mrec)):
                            r = mrec[idx]
                            if r not in nrec:
                                idxEq = np.argwhere(mrec == r)
                                nrec.append(r)
                                nprec.append(max([mpre[int(id)] for id in idxEq]))

                        plt.plot(nrec, nprec, 'or', label='11-point interpolated precision')
                    else:
                        plt.plot(recall, precision, label='Precision')
                        plt.xlabel('recall')
                        plt.ylabel('precision')
                        if showAP:
                            ap_str = '{0:.2f}%'.format(average_precision * 100)
                            plt.title('Precision x Recall curve \nClass: %s, AP: %s' % (str(classId), ap_str))
                        else:
                            plt.title('Precision x Recall curve \nClass: %s' % str(classId))
                    plt.legend(shadow=True)
                    plt.grid()
                    if savePath is not None:
                        plt.savefig(os.path.join(savePath, classId + '.png'))
                if showGraphic is True:
                    plt.show()
                    plt.pause(0.05)

        return results

    @staticmethod
    def CalculateAveragePrecision(rec, prec):
        mrec = []
        mrec.append(0)
        [mrec.append(e) for e in rec]
        mrec.append(1)
        mpre = []
        mpre.append(0)
        [mpre.append(e) for e in prec]
        mpre.append(0)
        for i in range(len(mpre) - 1, 0, -1):
            mpre[i - 1] = max(mpre[(i - 1)], mpre[i])

        ii = []
        for i in range(len(mrec) - 1):
            if mrec[1:][i] != mrec[0:-1][i]:
                ii.append(i + 1)

        ap = 0
        for i in ii:
            ap = ap + np.sum((mrec[i] - mrec[(i - 1)]) * mpre[i])

        return [ap, mpre[0:len(mpre) - 1], mrec[0:len(mpre) - 1], ii]

    @staticmethod
    def ElevenPointInterpolatedAP(rec, prec):
        mrec = []
        [mrec.append(e) for e in rec]
        mpre = []
        [mpre.append(e) for e in prec]
        recallValues = np.linspace(0, 1, 11)
        recallValues = list(recallValues[::-1])
        rhoInterp = []
        recallValid = []
        for r in recallValues:
            argGreaterRecalls = np.argwhere(mrec[:] >= r)
            pmax = 0
            if argGreaterRecalls.size != 0:
                pmax = max(mpre[argGreaterRecalls.min():])
            recallValid.append(r)
            rhoInterp.append(pmax)

        ap = sum(rhoInterp) / 11
        rvals = []
        rvals.append(recallValid[0])
        [rvals.append(e) for e in recallValid]
        rvals.append(0)
        pvals = []
        pvals.append(0)
        [pvals.append(e) for e in rhoInterp]
        pvals.append(0)
        cc = []
        for i in range(len(rvals)):
            p = (rvals[i], pvals[(i - 1)])
            if p not in cc:
                cc.append(p)
            p = (
             rvals[i], pvals[i])
            if p not in cc:
                cc.append(p)

        recallValues = [i[0] for i in cc]
        rhoInterp = [i[1] for i in cc]
        return [ap, rhoInterp, recallValues, None]

    @staticmethod
    def _getAllIOUs(reference, detections):
        ret = []
        bbReference = reference.getAbsoluteBoundingBox(BBFormat.XYX2Y2)
        for d in detections:
            bb = d.getAbsoluteBoundingBox(BBFormat.XYX2Y2)
            iou = Evaluator.iou(bbReference, bb)
            ret.append((iou, reference, d))

        return sorted(ret, key=(lambda i: i[0]), reverse=True)

    @staticmethod
    def iou(boxA, boxB):
        if Evaluator._boxesIntersect(boxA, boxB) is False:
            return 0
        interArea = Evaluator._getIntersectionArea(boxA, boxB)
        union = Evaluator._getUnionAreas(boxA, boxB, interArea=interArea)
        iou = interArea / union
        assert iou >= 0
        return iou

    @staticmethod
    def _boxesIntersect(boxA, boxB):
        if boxA[0] > boxB[2]:
            return False
        if boxB[0] > boxA[2]:
            return False
        if boxA[3] < boxB[1]:
            return False
        if boxA[1] > boxB[3]:
            return False
        return True

    @staticmethod
    def _getIntersectionArea(boxA, boxB):
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])
        return (xB - xA + 1) * (yB - yA + 1)

    @staticmethod
    def _getUnionAreas(boxA, boxB, interArea=None):
        area_A = Evaluator._getArea(boxA)
        area_B = Evaluator._getArea(boxB)
        if interArea is None:
            interArea = Evaluator._getIntersectionArea(boxA, boxB)
        return float(area_A + area_B - interArea)

    @staticmethod
    def _getArea(box):
        return (box[2] - box[0] + 1) * (box[3] - box[1] + 1)


def map_raf_from_lists(detections, ground_truths, iou_threshold=0.5, box_format='xywh', method='interpolation'):
    """
    Args:
        detections:[[image_id,[[label,confidence,x,y,w,h],[label,confidence,x,y,w,h]]],]
        ground_truths:[[image_id,[[label,x,y,w,h],[label,x,y,w,h]]],]
        iou_threshold:

    Returns:

    """
    box_format = BBFormat.XYWH if box_format == 'xywh' else BBFormat.XYX2Y2
    method = MethodAveragePrecision.EveryPointInterpolation if method == 'interpolation' else MethodAveragePrecision.ElevenPointInterpolation
    allBoundingBoxes = BoundingBoxes()
    for boxes in ground_truths:
        image_id = boxes[0]
        for box in boxes[1]:
            idClass = box[0]
            x = float(box[1])
            y = float(box[2])
            w = float(box[3])
            h = float(box[4])
            bb = BoundingBox(image_id,
              idClass,
              x,
              y,
              w,
              h,
              (CoordinatesType.Absolute),
              (416, 416), (BBType.GroundTruth),
              format=box_format)
            allBoundingBoxes.addBoundingBox(bb)

    for boxes in detections:
        image_id = boxes[0]
        for box in boxes[1]:
            idClass = box[0]
            confidence = float(box[1])
            x = float(box[2])
            y = float(box[3])
            w = float(box[4])
            h = float(box[5])
            bb = BoundingBox(image_id,
              idClass,
              x,
              y,
              w,
              h,
              (CoordinatesType.Absolute),
              (416, 416), (BBType.Detected),
              confidence,
              format=box_format)
            allBoundingBoxes.addBoundingBox(bb)

    evaluator = Evaluator()
    metricsPerClasses = evaluator.GetPascalVOCMetrics(allBoundingBoxes, IOUThreshold=iou_threshold,
      method=method)
    acc_AP = 0
    validClasses = 0
    for metricsPerClass in metricsPerClasses:
        cl = metricsPerClass['class']
        ap = metricsPerClass['AP']
        precision = metricsPerClass['precision']
        recall = metricsPerClass['recall']
        totalPositives = metricsPerClass['total positives']
        total_TP = metricsPerClass['total TP']
        total_FP = metricsPerClass['total FP']
        if totalPositives > 0:
            validClasses = validClasses + 1
            acc_AP = acc_AP + ap
            prec = ['%.2f' % p for p in precision]
            rec = ['%.2f' % r for r in recall]
            ap_str = '{0:.2f}%'.format(ap * 100)
            print('AP: %s (%s)' % (ap_str, cl))

    mAP = acc_AP / validClasses
    print(validClasses)
    mAP_str = '{0:.2f}%'.format(mAP * 100)
    print('mAP: %s' % mAP_str)
    return (mAP, metricsPerClasses)


def voc2ratxt(xml_file, box_format='xywh'):
    """
    Args:
        xml_file:
        box_format:
    Returns:
    """
    boxes = get_bndbox(xml_file)
    image_id = os.path.basename(xml_file).split('.')[0]
    boxes = [[box['name'], *box['coordinates']] for box in boxes]
    if box_format == 'xywh':
        for box in boxes:
            x, y = box[1:3]
            w, h = box[2] - box[0], box[3] - box[1]
            box[1:] = [x, y, w, h]

    return [
     image_id, boxes]