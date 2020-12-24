# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/deeplab/evaluation/panoptic_quality.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 10446 bytes
"""Implementation of the Panoptic Quality metric.

Panoptic Quality is an instance-based metric for evaluating the task of
image parsing, aka panoptic segmentation.

Please see the paper for details:
"Panoptic Segmentation", Alexander Kirillov, Kaiming He, Ross Girshick,
Carsten Rother and Piotr Dollar. arXiv:1801.00868, 2018.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import collections, numpy as np, prettytable, six
from deeplab.evaluation import base_metric

def _ids_to_counts(id_array):
    """Given a numpy array, a mapping from each unique entry to its count."""
    ids, counts = np.unique(id_array, return_counts=True)
    return dict(six.moves.zip(ids, counts))


class PanopticQuality(base_metric.SegmentationMetric):
    __doc__ = 'Metric class for Panoptic Quality.\n\n  "Panoptic Segmentation" by Alexander Kirillov, Kaiming He, Ross Girshick,\n  Carsten Rother, Piotr Dollar.\n  https://arxiv.org/abs/1801.00868\n  '

    def compare_and_accumulate(self, groundtruth_category_array, groundtruth_instance_array, predicted_category_array, predicted_instance_array):
        """See base class."""
        pred_segment_id = self._naively_combine_labels(predicted_category_array, predicted_instance_array)
        gt_segment_id = self._naively_combine_labels(groundtruth_category_array, groundtruth_instance_array)
        gt_segment_areas = _ids_to_counts(gt_segment_id)
        pred_segment_areas = _ids_to_counts(pred_segment_id)
        void_segment_id = self.ignored_label * self.max_instances_per_category
        ignored_segment_ids = {gt_segment_id for gt_segment_id in six.iterkeys(gt_segment_areas) if gt_segment_id // self.max_instances_per_category == self.ignored_label}
        intersection_id_array = gt_segment_id.astype(np.uint32) * self.offset + pred_segment_id.astype(np.uint32)
        intersection_areas = _ids_to_counts(intersection_id_array)

        def prediction_void_overlap(pred_segment_id):
            void_intersection_id = void_segment_id * self.offset + pred_segment_id
            return intersection_areas.get(void_intersection_id, 0)

        def prediction_ignored_overlap(pred_segment_id):
            total_ignored_overlap = 0
            for ignored_segment_id in ignored_segment_ids:
                intersection_id = ignored_segment_id * self.offset + pred_segment_id
                total_ignored_overlap += intersection_areas.get(intersection_id, 0)

            return total_ignored_overlap

        gt_matched = set()
        pred_matched = set()
        for intersection_id, intersection_area in six.iteritems(intersection_areas):
            gt_segment_id = intersection_id // self.offset
            pred_segment_id = intersection_id % self.offset
            gt_category = gt_segment_id // self.max_instances_per_category
            pred_category = pred_segment_id // self.max_instances_per_category
            if gt_category != pred_category:
                continue
            union = gt_segment_areas[gt_segment_id] + pred_segment_areas[pred_segment_id] - intersection_area - prediction_void_overlap(pred_segment_id)
            iou = intersection_area / union
            if iou > 0.5:
                self.tp_per_class[gt_category] += 1
                self.iou_per_class[gt_category] += iou
                gt_matched.add(gt_segment_id)
                pred_matched.add(pred_segment_id)

        for gt_segment_id in six.iterkeys(gt_segment_areas):
            if gt_segment_id in gt_matched:
                continue
            category = gt_segment_id // self.max_instances_per_category
            if category == self.ignored_label:
                continue
            self.fn_per_class[category] += 1

        for pred_segment_id in six.iterkeys(pred_segment_areas):
            if pred_segment_id in pred_matched:
                continue
            if prediction_ignored_overlap(pred_segment_id) / pred_segment_areas[pred_segment_id] > 0.5:
                continue
            category = pred_segment_id // self.max_instances_per_category
            self.fp_per_class[category] += 1

        return self.result()

    def _valid_categories(self):
        """Categories with a "valid" value for the metric, have > 0 instances.

    We will ignore the `ignore_label` class and other classes which have
    `tp + fn + fp = 0`.

    Returns:
      Boolean array of shape `[num_categories]`.
    """
        valid_categories = np.not_equal(self.tp_per_class + self.fn_per_class + self.fp_per_class, 0)
        if self.ignored_label >= 0:
            if self.ignored_label < self.num_categories:
                valid_categories[self.ignored_label] = False
        return valid_categories

    def detailed_results(self, is_thing=None):
        """See base class."""
        valid_categories = self._valid_categories()
        category_sets = collections.OrderedDict()
        category_sets['All'] = valid_categories
        if is_thing is not None:
            category_sets['Things'] = np.logical_and(valid_categories, is_thing)
            category_sets['Stuff'] = np.logical_and(valid_categories, np.logical_not(is_thing))
        sq = base_metric.realdiv_maybe_zero(self.iou_per_class, self.tp_per_class)
        rq = base_metric.realdiv_maybe_zero(self.tp_per_class, self.tp_per_class + 0.5 * self.fn_per_class + 0.5 * self.fp_per_class)
        pq = np.multiply(sq, rq)
        results = {}
        for category_set_name, in_category_set in six.iteritems(category_sets):
            if np.any(in_category_set):
                results[category_set_name] = {'pq':np.mean(pq[in_category_set]),  'sq':np.mean(sq[in_category_set]), 
                 'rq':np.mean(rq[in_category_set]), 
                 'n':np.sum(in_category_set.astype(np.int32))}
            else:
                results[category_set_name] = {'pq':0, 
                 'sq':0,  'rq':0,  'n':0}

        return results

    def result_per_category(self):
        """See base class."""
        sq = base_metric.realdiv_maybe_zero(self.iou_per_class, self.tp_per_class)
        rq = base_metric.realdiv_maybe_zero(self.tp_per_class, self.tp_per_class + 0.5 * self.fn_per_class + 0.5 * self.fp_per_class)
        return np.multiply(sq, rq)

    def print_detailed_results(self, is_thing=None, print_digits=3):
        """See base class."""
        results = self.detailed_results(is_thing=is_thing)
        tab = prettytable.PrettyTable()
        tab.add_column('', [], align='l')
        for fieldname in ('PQ', 'SQ', 'RQ', 'N'):
            tab.add_column(fieldname, [], align='r')

        for category_set, subset_results in six.iteritems(results):
            data_cols = [round(subset_results[col_key], print_digits) * 100 for col_key in ('pq',
                                                                                            'sq',
                                                                                            'rq')]
            data_cols += [subset_results['n']]
            tab.add_row([category_set] + data_cols)

        print(tab)

    def result(self):
        """See base class."""
        pq_per_class = self.result_per_category()
        valid_categories = self._valid_categories()
        if not np.any(valid_categories):
            return 0.0
        return np.mean(pq_per_class[valid_categories])

    def merge(self, other_instance):
        """See base class."""
        self.iou_per_class += other_instance.iou_per_class
        self.tp_per_class += other_instance.tp_per_class
        self.fn_per_class += other_instance.fn_per_class
        self.fp_per_class += other_instance.fp_per_class

    def reset(self):
        """See base class."""
        self.iou_per_class = np.zeros((self.num_categories), dtype=(np.float64))
        self.tp_per_class = np.zeros((self.num_categories), dtype=(np.float64))
        self.fn_per_class = np.zeros((self.num_categories), dtype=(np.float64))
        self.fp_per_class = np.zeros((self.num_categories), dtype=(np.float64))