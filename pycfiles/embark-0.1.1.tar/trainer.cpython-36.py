# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/naresh/Projects/embark/embark/tensorflow_classifier/trainer.py
# Compiled at: 2020-02-03 19:00:38
# Size of source mod 2**32: 4383 bytes
import time, tensorflow as tf
from tqdm import tqdm

class Trainer:

    def __init__(self, model, cuda_device):
        self.model = model
        self.cuda_device = cuda_device

    def _get_ckpt_manager_n_optimizer(self, checkpoints_dir, lr=0.001):
        optimizer = tf.keras.optimizers.Adam(lr=lr)
        ckpt = tf.train.Checkpoint(step=(tf.Variable(1)), optimizer=optimizer, net=(self.model))
        manager = tf.train.CheckpointManager(ckpt, checkpoints_dir, max_to_keep=None)
        if manager.latest_checkpoint:
            ckpt.restore(manager.latest_checkpoint)
            print('Restoring from {}'.format(manager.latest_checkpoint))
        else:
            print('No checkpoints found')
        return (
         optimizer, ckpt, manager)

    def train(self, datasets, loss, lr, epochs, save_model_iter, checkpoints_dir, tensorboard_dir, max_to_keep=10):
        since = time.time()
        is_val = True if 'val' in datasets else False
        is_test = True if 'test' in datasets else False
        optimizer, ckpt, manager = self._get_ckpt_manager_n_optimizer(checkpoints_dir, lr)
        train_summary_writer = tf.summary.create_file_writer(tensorboard_dir + '/train')
        val_summary_writer = tf.summary.create_file_writer(tensorboard_dir + '/val')
        test_summary_writer = tf.summary.create_file_writer(tensorboard_dir + '/test')
        test_acc = None
        best_val_acc = 0.0
        train_step, val_step, test_step = (0, 0, 0)
        for epoch in range(epochs):
            print()
            print('*' * 30)
            print('Epoch: {}/{}'.format(epoch, epochs - 1))
            print('Results directories: \nTensorboard: {}\nCheckpoints: {}'.format(tensorboard_dir, checkpoints_dir))
            print('*' * 30)
            with train_summary_writer.as_default():
                _, train_step = self._one_epoch('train', loss, datasets['train'], optimizer, train_step)
            ckpt.step.assign_add(1)
            if is_val:
                with val_summary_writer.as_default():
                    val_acc, val_step = self._one_epoch('val', loss, datasets['val'], optimizer, val_step)
                if val_acc > best_val_acc:
                    best_val_acc = val_acc
                    save_path = manager.save(checkpoint_number=(-1))
                    print('Saved best model: {}'.format(save_path))
                if (epoch + 1) % save_model_iter == 0:
                    save_path = manager.save()
                    print('Model saved: {}'.format(save_path))

        if is_test:
            with test_summary_writer.as_default():
                test_acc, test_step = self._one_epoch('test', loss, datasets['test'], optimizer, test_step)
        tf.saved_model.save(self.model, checkpoints_dir + '/saved_model')
        print('Time taken: {}'.format(time.time() - since))
        return (best_val_acc, test_acc)

    def _loss(self, loss, x, y, training):
        y_ = self.model(x, training=training)
        return (loss(y_true=tf.squeeze(y, axis=(-1)), y_pred=tf.squeeze(y_, axis=(-1))), y_)

    def _grad(self, inputs, targets, loss):
        with tf.GradientTape() as (tape):
            loss_value, y_ = self._loss(loss, inputs, targets, training=True)
        return (
         loss_value, tape.gradient(loss_value, self.model.trainable_variables), y_)

    def _one_epoch(self, phase, loss, dataset, optimizer, step):
        epoch_loss_avg = tf.keras.metrics.Mean()
        epoch_acc = tf.keras.metrics.BinaryAccuracy()
        pbar = tqdm(dataset)
        for x, y in pbar:
            if phase == 'train':
                loss_value, grads, y_ = self._grad(x, y, loss)
                optimizer.apply_gradients(zip(grads, self.model.trainable_variables))
            else:
                loss_value, y_ = self._loss(loss, x, y, training=False)
            epoch_loss_avg(loss_value)
            epoch_acc(tf.squeeze(y, axis=(-1)), tf.squeeze(y_, axis=(-1)))
            tf.summary.scalar(('{}_loss'.format(phase)), (epoch_loss_avg.result()), step=step)
            tf.summary.scalar(('{}_acc'.format(phase)), (epoch_acc.result()), step=step)
            step += 1
            pbar.set_description('Phase: {} \t Loss: {:.3f} \t Accuracy: {:.3f}'.format(phase, epoch_loss_avg.result(), epoch_acc.result()))

        return (
         epoch_acc.result(), step)