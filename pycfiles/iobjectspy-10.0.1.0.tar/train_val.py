# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\faster_rcnn\model\train_val.py
# Compiled at: 2019-12-31 04:09:02
# Size of source mod 2**32: 17754 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from model.config import cfg
from ..roi_data_layer import roidb as rdl_roidb
from roi_data_layer.layer import RoIDataLayer
from utils.timer import Timer
try:
    import cPickle as pickle
except ImportError:
    import pickle

import numpy as np, os, glob, time, tensorflow as tf
from tensorflow.python import pywrap_tensorflow

class SolverWrapper(object):
    __doc__ = '\n      A wrapper class for the training process\n    '

    def __init__(self, sess, network, imdb, roidb, valroidb, output_dir, tbdir, pretrained_model=None):
        self.net = network
        self.imdb = imdb
        self.roidb = roidb
        self.valroidb = valroidb
        self.output_dir = output_dir
        self.tbdir = tbdir
        self.tbvaldir = tbdir + '_val'
        if not os.path.exists(self.tbvaldir):
            os.makedirs(self.tbvaldir)
        self.pretrained_model = pretrained_model

    def snapshot(self, sess, iter):
        net = self.net
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        filename = cfg.TRAIN.SNAPSHOT_PREFIX + '_iter_{:d}'.format(iter) + '.ckpt'
        filename = os.path.join(self.output_dir, filename)
        self.saver.save(sess, filename)
        print('Wrote snapshot to: {:s}'.format(filename))
        nfilename = cfg.TRAIN.SNAPSHOT_PREFIX + '_iter_{:d}'.format(iter) + '.pkl'
        nfilename = os.path.join(self.output_dir, nfilename)
        st0 = np.random.get_state()
        cur = self.data_layer._cur
        perm = self.data_layer._perm
        cur_val = self.data_layer_val._cur
        perm_val = self.data_layer_val._perm
        with open(nfilename, 'wb') as (fid):
            pickle.dump(st0, fid, pickle.HIGHEST_PROTOCOL)
            pickle.dump(cur, fid, pickle.HIGHEST_PROTOCOL)
            pickle.dump(perm, fid, pickle.HIGHEST_PROTOCOL)
            pickle.dump(cur_val, fid, pickle.HIGHEST_PROTOCOL)
            pickle.dump(perm_val, fid, pickle.HIGHEST_PROTOCOL)
            pickle.dump(iter, fid, pickle.HIGHEST_PROTOCOL)
        return (filename, nfilename)

    def from_snapshot(self, sess, sfile, nfile):
        print('Restoring model snapshots from {:s}'.format(sfile))
        self.saver.restore(sess, sfile)
        print('Restored.')
        with open(nfile, 'rb') as (fid):
            st0 = pickle.load(fid)
            cur = pickle.load(fid)
            perm = pickle.load(fid)
            cur_val = pickle.load(fid)
            perm_val = pickle.load(fid)
            last_snapshot_iter = pickle.load(fid)
            np.random.set_state(st0)
            self.data_layer._cur = cur
            self.data_layer._perm = perm
            self.data_layer_val._cur = cur_val
            self.data_layer_val._perm = perm_val
        return last_snapshot_iter

    def get_variables_in_checkpoint_file(self, file_name):
        try:
            reader = pywrap_tensorflow.NewCheckpointReader(file_name)
            var_to_shape_map = reader.get_variable_to_shape_map()
            return var_to_shape_map
        except Exception as e:
            try:
                print(str(e))
                if 'corrupted compressed block contents' in str(e):
                    print("It's likely that your checkpoint file has been compressed with SNAPPY.")
            finally:
                e = None
                del e

    def construct_graph(self, sess):
        with sess.graph.as_default():
            tf.set_random_seed(cfg.RNG_SEED)
            layers = self.net.create_architecture('TRAIN', (self.imdb.num_classes), tag='default', anchor_scales=(cfg.ANCHOR_SCALES),
              anchor_ratios=(cfg.ANCHOR_RATIOS))
            loss = layers['total_loss']
            lr = tf.Variable((cfg.TRAIN.LEARNING_RATE), trainable=False)
            self.optimizer = tf.train.MomentumOptimizer(lr, cfg.TRAIN.MOMENTUM)
            gvs = self.optimizer.compute_gradients(loss)
            if cfg.TRAIN.DOUBLE_BIAS:
                final_gvs = []
                with tf.variable_scope('Gradient_Mult') as (scope):
                    for grad, var in gvs:
                        scale = 1.0
                        if cfg.TRAIN.DOUBLE_BIAS:
                            if '/biases:' in var.name:
                                scale *= 2.0
                        if not np.allclose(scale, 1.0):
                            grad = tf.multiply(grad, scale)
                        final_gvs.append((grad, var))

                train_op = self.optimizer.apply_gradients(final_gvs)
            else:
                train_op = self.optimizer.apply_gradients(gvs)
            self.saver = tf.train.Saver(max_to_keep=100000)
            self.writer = tf.summary.FileWriter(self.tbdir, sess.graph)
            self.valwriter = tf.summary.FileWriter(self.tbvaldir)
        return (lr, train_op)

    def find_previous(self, pretrained_model_path):
        sfiles = os.path.join(pretrained_model_path, cfg.TRAIN.SNAPSHOT_PREFIX + '_iter_*.ckpt.meta')
        sfiles = glob.glob(sfiles)
        sfiles.sort(key=(os.path.getmtime))
        redfiles = []
        for stepsize in cfg.TRAIN.STEPSIZE:
            redfiles.append(os.path.join(pretrained_model_path, cfg.TRAIN.SNAPSHOT_PREFIX + '_iter_{:d}.ckpt.meta'.format(stepsize + 1)))

        sfiles = [ss.replace('.meta', '') for ss in sfiles if ss not in redfiles]
        nfiles = os.path.join(pretrained_model_path, cfg.TRAIN.SNAPSHOT_PREFIX + '_iter_*.pkl')
        nfiles = glob.glob(nfiles)
        nfiles.sort(key=(os.path.getmtime))
        redfiles = [redfile.replace('.ckpt.meta', '.pkl') for redfile in redfiles]
        nfiles = [nn for nn in nfiles if nn not in redfiles]
        lsf = len(sfiles)
        assert len(nfiles) == lsf
        return (
         lsf, nfiles, sfiles)

    def initialize(self, sess):
        np_paths = []
        ss_paths = []
        if self.pretrained_model != None:
            print('Loading initial model weights from {:s}'.format(self.pretrained_model))
        variables = tf.global_variables()
        sess.run(tf.variables_initializer(variables, name='init'))
        var_keep_dic = self.get_variables_in_checkpoint_file(self.pretrained_model)
        variables_to_restore = self.net.get_variables_to_restore(variables, var_keep_dic)
        restorer = tf.train.Saver(variables_to_restore)
        restorer.restore(sess, self.pretrained_model)
        print('Loaded.')
        self.net.fix_variables(sess, self.pretrained_model)
        print('Fixed.')
        last_snapshot_iter = 0
        rate = cfg.TRAIN.LEARNING_RATE
        stepsizes = list(cfg.TRAIN.STEPSIZE)
        return (
         rate, last_snapshot_iter, stepsizes, np_paths, ss_paths)

    def restore(self, sess, sfile, nfile):
        np_paths = [
         nfile]
        ss_paths = [sfile]
        last_snapshot_iter = self.from_snapshot(sess, sfile, nfile)
        rate = cfg.TRAIN.LEARNING_RATE
        stepsizes = []
        for stepsize in cfg.TRAIN.STEPSIZE:
            if last_snapshot_iter > stepsize:
                rate *= cfg.TRAIN.GAMMA
            else:
                stepsizes.append(stepsize)

        return (
         rate, last_snapshot_iter, stepsizes, np_paths, ss_paths)

    def remove_snapshot(self, np_paths, ss_paths):
        to_remove = len(np_paths) - cfg.TRAIN.SNAPSHOT_KEPT
        for c in range(to_remove):
            nfile = np_paths[0]
            os.remove(str(nfile))
            np_paths.remove(nfile)

        to_remove = len(ss_paths) - cfg.TRAIN.SNAPSHOT_KEPT
        for c in range(to_remove):
            sfile = ss_paths[0]
            if os.path.exists(str(sfile)):
                os.remove(str(sfile))
            else:
                os.remove(str(sfile + '.data-00000-of-00001'))
                os.remove(str(sfile + '.index'))
            sfile_meta = sfile + '.meta'
            os.remove(str(sfile_meta))
            ss_paths.remove(sfile)

    def train_model(self, sess, max_iters, last_model_filename, pretrained_model_path):
        self.data_layer = RoIDataLayer(self.roidb, self.imdb.num_classes)
        self.data_layer_val = RoIDataLayer((self.valroidb), (self.imdb.num_classes), random=True)
        log_path = os.path.abspath(os.path.join(os.path.abspath(os.path.join(last_model_filename, os.path.pardir)), os.path.pardir))
        lr, train_op = self.construct_graph(sess)
        if pretrained_model_path is not None:
            lsf, nfiles, sfiles = self.find_previous(pretrained_model_path)
            if lsf == 0:
                rate, last_snapshot_iter, stepsizes, np_paths, ss_paths = self.initialize(sess)
            else:
                rate, last_snapshot_iter, stepsizes, np_paths, ss_paths = self.restore(sess, str(sfiles[(-1)]), str(nfiles[(-1)]))
        else:
            rate, last_snapshot_iter, stepsizes, np_paths, ss_paths = self.initialize(sess)
        timer = Timer()
        iter = last_snapshot_iter + 1
        last_summary_time = time.time()
        stepsizes.append(max_iters)
        stepsizes.reverse()
        next_stepsize = stepsizes.pop()
        while iter < max_iters + 1:
            if iter == next_stepsize + 1:
                self.snapshot(sess, iter)
                rate *= cfg.TRAIN.GAMMA
                sess.run(tf.assign(lr, rate))
                next_stepsize = stepsizes.pop()
            else:
                timer.tic()
                blobs = self.data_layer.forward()
                now = time.time()
                if iter == 1 or now - last_summary_time > cfg.TRAIN.SUMMARY_INTERVAL:
                    rpn_loss_cls, rpn_loss_box, loss_cls, loss_box, total_loss, summary = self.net.train_step_with_summary(sess, blobs, train_op)
                    self.writer.add_summary(summary, float(iter))
                    blobs_val = self.data_layer_val.forward()
                    summary_val = self.net.get_summary(sess, blobs_val)
                    self.valwriter.add_summary(summary_val, float(iter))
                    last_summary_time = now
                else:
                    rpn_loss_cls, rpn_loss_box, loss_cls, loss_box, total_loss = self.net.train_step(sess, blobs, train_op)
            timer.toc()
            if iter % cfg.TRAIN.DISPLAY == 0:
                print('iter: %d / %d, total loss: %.6f\n >>> rpn_loss_cls: %.6f\n >>> rpn_loss_box: %.6f\n >>> loss_cls: %.6f\n >>> loss_box: %.6f\n >>> lr: %f' % (
                 iter, max_iters, total_loss, rpn_loss_cls, rpn_loss_box, loss_cls, loss_box, lr.eval()))
                print('speed: {:.3f}s / iter'.format(timer.average_time))
            save_model = True
            if iter % cfg.TRAIN.SNAPSHOT_ITERS == 0:
                last_snapshot_iter = iter
                ss_path, np_path = self.snapshot(sess, iter)
                np_paths.append(np_path)
                ss_paths.append(ss_path)
                total_loss_val = self.net.val_loss(sess, self.data_layer_val.forward())
                total_loss_val_string = '%.6f' % total_loss_val
                total_loss_val = float(total_loss_val_string)
                if os.path.exists(os.path.join(log_path, 'val_total_loss.txt')):
                    with open(os.path.join(log_path, 'val_total_loss.txt'), 'rb') as (f):
                        all_lines = f.readline()
                        for line in all_lines:
                            log_total_loss_val = float(line)
                            log_total_loss_val_str = line

                        try:
                            if total_loss_val < log_total_loss_val:
                                self.saver.save(sess, last_model_filename)
                            else:
                                total_loss_val_string = log_total_loss_val_str
                        except:
                            pass

                with open(os.path.join(log_path, 'val_total_loss.txt'), 'w') as (f):
                    f.write(total_loss_val_string + '\n')
                save_model = False
                if len(np_paths) > cfg.TRAIN.SNAPSHOT_KEPT:
                    self.remove_snapshot(np_paths, ss_paths)
            iter += 1

        if last_snapshot_iter != iter - 1:
            self.snapshot(sess, iter - 1)
            if save_model:
                self.saver.save(sess, last_model_filename)
        self.writer.close()
        self.valwriter.close()


def get_training_roidb(imdb):
    """Returns a roidb (Region of Interest database) for use in training."""
    if cfg.TRAIN.USE_FLIPPED:
        print('Appending horizontally-flipped training examples...')
        imdb.append_flipped_images()
        print('done')
    print('Preparing training data...')
    rdl_roidb.prepare_roidb(imdb)
    print('done')
    return imdb.roidb


def filter_roidb(roidb):
    """Remove roidb entries that have no usable RoIs."""

    def is_valid(entry):
        overlaps = entry['max_overlaps']
        fg_inds = np.where(overlaps >= cfg.TRAIN.FG_THRESH)[0]
        bg_inds = np.where((overlaps < cfg.TRAIN.BG_THRESH_HI) & (overlaps >= cfg.TRAIN.BG_THRESH_LO))[0]
        valid = len(fg_inds) > 0 or len(bg_inds) > 0
        return valid

    num = len(roidb)
    filtered_roidb = [entry for entry in roidb if is_valid(entry)]
    num_after = len(filtered_roidb)
    print('Filtered {} roidb entries: {} -> {}'.format(num - num_after, num, num_after))
    return filtered_roidb


def train_net(network, imdb, roidb, valroidb, pretrained_model_path, output_dir, out_name, tb_dir, pretrained_model=None, max_iters=40000):
    """Train a Faster R-CNN network."""
    roidb = filter_roidb(roidb)
    valroidb = filter_roidb(valroidb)
    tfconfig = tf.ConfigProto(allow_soft_placement=True)
    tfconfig.gpu_options.allow_growth = True
    last_model_filename = os.path.join(output_dir, out_name)
    with tf.Session(config=tfconfig) as (sess):
        sw = SolverWrapper(sess, network, imdb, roidb, valroidb, output_dir, tb_dir, pretrained_model=pretrained_model)
        print('Solving...')
        sw.train_model(sess, max_iters, last_model_filename, pretrained_model_path)
        print('done solving')