# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/street/python/decoder.py
# Compiled at: 2020-04-05 19:50:58
# Size of source mod 2**32: 10098 bytes
"""Basic CTC+recoder decoder.

Decodes a sequence of class-ids into UTF-8 text.
For basic information on CTC See:
Alex Graves et al. Connectionist Temporal Classification: Labelling Unsegmented
Sequence Data with Recurrent Neural Networks.
http://www.cs.toronto.edu/~graves/icml_2006.pdf
"""
import collections, re, errorcounter as ec
from six.moves import xrange
import tensorflow as tf
Part = collections.namedtuple('Part', 'utf8 index, num_codes')

class Decoder(object):
    __doc__ = 'Basic CTC+recoder decoder.'

    def __init__(self, filename):
        r"""Constructs a Decoder.

    Reads the text file describing the encoding and build the encoder.
    The text file contains lines of the form:
    <code>[,<code>]*\t<string>
    Each line defines a mapping from a sequence of one or more integer codes to
    a corresponding utf-8 string.
    Args:
      filename:   Name of file defining the decoding sequences.
    """
        self.decoder = []
        if filename:
            self._InitializeDecoder(filename)

    def SoftmaxEval(self, sess, model, num_steps):
        """Evaluate a model in softmax mode.

    Adds char, word recall and sequence error rate events to the sw summary
    writer, and returns them as well
    TODO(rays) Add LogisticEval.
    Args:
      sess:  A tensor flow Session.
      model: The model to run in the session. Requires a VGSLImageModel or any
        other class that has a using_ctc attribute and a RunAStep(sess) method
        that reurns a softmax result with corresponding labels.
      num_steps: Number of steps to evaluate for.
    Returns:
      ErrorRates named tuple.
    Raises:
      ValueError: If an unsupported number of dimensions is used.
    """
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess=sess, coord=coord)
        total_label_counts = ec.ErrorCounts(0, 0, 0, 0)
        total_word_counts = ec.ErrorCounts(0, 0, 0, 0)
        sequence_errors = 0
        for _ in xrange(num_steps):
            softmax_result, labels = model.RunAStep(sess)
            predictions = softmax_result.argmax(axis=(-1))
            num_dims = len(predictions.shape) - 1
            batch_size = predictions.shape[0]
            null_label = softmax_result.shape[(-1)] - 1
            for b in xrange(batch_size):
                if num_dims == 2:
                    raise ValueError('2-d label data not supported yet!')
                else:
                    if num_dims == 1:
                        pred_batch = predictions[b, :]
                        labels_batch = labels[b, :]
                    else:
                        pred_batch = [
                         predictions[b]]
                        labels_batch = [labels[b]]
                    text = self.StringFromCTC(pred_batch, model.using_ctc, null_label)
                    truth = self.StringFromCTC(labels_batch, False, null_label)
                    total_word_counts = ec.AddErrors(total_word_counts, ec.CountWordErrors(text, truth))
                    total_label_counts = ec.AddErrors(total_label_counts, ec.CountErrors(text, truth))
                if text != truth:
                    sequence_errors += 1

        coord.request_stop()
        coord.join(threads)
        return ec.ComputeErrorRates(total_label_counts, total_word_counts, sequence_errors, num_steps * batch_size)

    def StringFromCTC(self, ctc_labels, merge_dups, null_label):
        """Decodes CTC output to a string.

    Extracts only sequences of codes that are allowed by self.decoder.
    Labels that make illegal code sequences are dropped.
    Note that, by its nature of taking only top choices, this is much weaker
    than a full-blown beam search that considers all the softmax outputs.
    For languages without many multi-code sequences, this doesn't make much
    difference, but for complex scripts the accuracy will be much lower.
    Args:
      ctc_labels: List of class labels including null characters to remove.
      merge_dups: If True, Duplicate labels will be merged
      null_label: Label value to ignore.

    Returns:
      Labels decoded to a string.
    """
        codes = self._CodesFromCTC(ctc_labels, merge_dups, null_label)
        length = len(codes)
        if length == 0:
            return ''
        strings = []
        partials = []
        for pos in xrange(length):
            code = codes[pos]
            parts = self.decoder[code]
            partials.append([])
            strings.append('')
            for utf8, index, num_codes in parts:
                if index > pos:
                    continue
                if index == 0 or partials[(pos - 1)].count(Part(utf8, index - 1, num_codes)) > 0:
                    if index < num_codes - 1:
                        partials[(-1)].append(Part(utf8, index, num_codes))
                    elif strings[(-1)] or pos >= num_codes:
                        strings[-1] = strings[(pos - num_codes)] + utf8
                    else:
                        strings[-1] = utf8

            if strings[(-1)] or pos > 0:
                strings[-1] = strings[(-2)]

        return strings[(-1)]

    def _InitializeDecoder(self, filename):
        """Reads the decoder file and initializes self.decoder from it.

    Args:
      filename: Name of text file mapping codes to utf8 strings.
    Raises:
      ValueError: if the input file is not parsed correctly.
    """
        line_re = re.compile('(?P<codes>\\d+(,\\d+)*)\\t(?P<utf8>.+)')
        with tf.gfile.GFile(filename) as (f):
            for line in f:
                m = line_re.match(line)
                if m is None:
                    raise ValueError('Unmatched line:', line)
                str_codes = m.groupdict()['codes'].split(',')
                codes = []
                for code in str_codes:
                    codes.append(int(code))

                utf8 = m.groupdict()['utf8']
                num_codes = len(codes)
                for index, code in enumerate(codes):
                    while code >= len(self.decoder):
                        self.decoder.append([])

                    self.decoder[code].append(Part(utf8, index, num_codes))

    def _CodesFromCTC(self, ctc_labels, merge_dups, null_label):
        """Collapses CTC output to regular output.

    Args:
      ctc_labels: List of class labels including null characters to remove.
      merge_dups: If True, Duplicate labels will be merged.
      null_label: Label value to ignore.

    All trailing zeros are removed!!
    TODO(rays) This may become a problem with non-CTC models.
    If using charset, this should not be a problem as zero is always space.
    tf.pad can only append zero, so we have to be able to drop them, as a
    non-ctc will have learned to output trailing zeros instead of trailing
    nulls. This is awkward, as the stock ctc loss function requires that the
    null character be num_classes-1.
    Returns:
      (List of) Labels with null characters removed.
    """
        out_labels = []
        prev_label = -1
        zeros_needed = 0
        for label in ctc_labels:
            if label == null_label:
                prev_label = -1

        return out_labels