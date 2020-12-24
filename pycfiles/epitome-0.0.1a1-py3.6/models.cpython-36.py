# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/epitome/models.py
# Compiled at: 2020-01-22 10:01:21
# Size of source mod 2**32: 28967 bytes
"""
======
Models
======
.. currentmodule:: epitome.models

.. autosummary::
  :toctree: _generate/

  VariationalPeakModel
  VLP
"""
from epitome import *
import tensorflow as tf, tensorflow_probability as tfp
from .functions import *
from .constants import *
from .generators import *
from .metrics import *
import numpy as np, tqdm, pickle
from operator import itemgetter
tf.config.experimental_run_functions_eagerly(True)

class VariationalPeakModel:
    __doc__ = ' Model for learning from ChIP-seq peaks.\n    '

    def __init__(self, assays, test_celltypes=[], matrix=None, assaymap=None, cellmap=None, debug=False, batch_size=64, shuffle_size=10, prefetch_size=10, l1=0.0, l2=0.0, lr=0.001, radii=[
 1, 3, 10, 30], train_indices=None, data=None, data_path=None):
        """
        Initializes Peak Model

        Args:
            :param assays: list of assays to train model on
            :param test_celltypes: list of cell types to hold out for test. Should be in cellmap
            :param matrix: numpy matrix of indices mapping assay and cell to index in data
            :param assaymap: map of assays mapping assay name to row in matrix
            :param cellmap: map of cell types mapping cell name to column in matrix
            :param debug: used to print out intermediate validation values
            :param batch_size: batch size (default is 64)
            :param shuffle_size: data shuffle size (default is 10)
            :param prefetch_size: data prefetch size (default is 10)
            :param l1: l1 regularization (default is 0)
            :param l2: l2 regularization (default is 0)
            :param lr: lr (default is 1e-3)
            :param radii: radius of DNase-seq to consider around a peak of interest (default is [1,3,10,30])
            :param train_indices: option numpy array of indices to train from data[Dataset.TRAIN]
            :param data: data loaded from datapath. This option is mostly for testing, so users dont have to load in data for 
            :param data_path: path to data. Directory should contain all.pos.bed.gz, feature_name,test.npz,train.npz,valid.npz
            each model.
        """
        tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.INFO)
        if assaymap is not None:
            if not (matrix is not None and cellmap is not None):
                raise AssertionError('matrix, cellmap, and assaymap must all be set')
        if cellmap is not None:
            if not (matrix is not None and assaymap is not None):
                raise AssertionError('matrix, cellmap, and assaymap must all be set')
        if matrix is not None:
            if not (assaymap is not None and cellmap is not None):
                raise AssertionError('matrix, cellmap, and assaymap must all be set')
        if assaymap is None:
            matrix, cellmap, assaymap = get_assays_from_feature_file(eligible_assays=assays)
            if not len(assays) == len(list(assaymap)) - 1:
                raise AssertionError
        else:
            assert set(test_celltypes) < set(list(cellmap)), 'test_celltypes %s must be subsets of available cell types %s' % (str(test_celltypes), str(list(cellmap)))
            self.eval_cell_types = list(cellmap).copy()
            self.test_celltypes = test_celltypes
            [self.eval_cell_types.remove(test_cell) for test_cell in self.test_celltypes]
            if data is not None:
                self.data = data
            else:
                self.data = load_epitome_data()
        if not data_path:
            data_path = GET_DATA_PATH()
        self.regionsFile = os.path.join(data_path, POSITIONS_FILE)
        input_shapes, output_shape, self.train_iter = generator_to_tf_dataset(load_data((self.data[Dataset.TRAIN]), (self.eval_cell_types),
          (self.eval_cell_types),
          matrix,
          assaymap,
          cellmap,
          radii=radii,
          mode=(Dataset.TRAIN)), batch_size, shuffle_size, prefetch_size)
        _, _, self.valid_iter = generator_to_tf_dataset(load_data((self.data[Dataset.VALID]), (self.eval_cell_types),
          (self.eval_cell_types),
          matrix,
          assaymap,
          cellmap,
          radii=radii,
          mode=(Dataset.VALID)), batch_size, 1, prefetch_size)
        if len(self.test_celltypes) > 0:
            _, _, self.test_iter = generator_to_tf_dataset(load_data((self.data[Dataset.TEST]), (self.test_celltypes),
              (self.eval_cell_types),
              matrix,
              assaymap,
              cellmap,
              radii=radii,
              mode=(Dataset.TEST)), batch_size, 1, prefetch_size)
        self.l1, self.l2 = l1, l2
        self.lr = lr
        self.batch_size = batch_size
        self.prefetch_size = prefetch_size
        self.shuffle_size = shuffle_size
        self.optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=(self.lr))
        self.num_outputs = output_shape[0]
        self.num_inputs = input_shapes
        self.radii = radii
        self.debug = debug
        self.assaymap = assaymap
        self.test_celltypes = test_celltypes
        self.matrix = matrix
        self.assaymap = assaymap
        self.cellmap = cellmap
        self.data = data
        self.model = self.create_model()

    def get_weight_parameters(self):
        """
        Extracts weight posterior statistics for layers with weight distributions.
        :param model: keras model

        :return triple of layer names, weight means for each layer and stddev for each layer.
        """
        names = []
        qmeans = []
        qstds = []
        for i, layer in enumerate(self.model.layers):
            try:
                q = layer.kernel_posterior
            except AttributeError:
                continue

            names.append('Layer {}'.format(i))
            qmeans.append(q.mean())
            qstds.append(q.stddev())

        return (names, qmeans, qstds)

    def save(self, checkpoint_path):
        """
        Saves model.
        :param checkpoint_path: string file path to save model to. 
        """
        weights_path = os.path.join(checkpoint_path, 'weights.h5')
        meta_path = os.path.join(checkpoint_path, 'model_params.pickle')
        if not os.path.exists(checkpoint_path):
            os.makedirs(checkpoint_path)
        file = h5py.File(weights_path, 'w')
        weight = self.model.get_weights()
        for i in range(len(weight)):
            file.create_dataset(('weight' + str(i)), data=(weight[i]))

        file.close()
        dict_ = {'assays':list(self.assaymap), 
         'test_celltypes':self.test_celltypes, 
         'matrix':self.matrix, 
         'assaymap':self.assaymap, 
         'cellmap':self.cellmap, 
         'debug':self.debug, 
         'batch_size':self.batch_size, 
         'shuffle_size':self.shuffle_size, 
         'prefetch_size':self.prefetch_size, 
         'radii':self.radii}
        fileObject = open(meta_path, 'wb')
        pickle.dump(dict_, fileObject)
        fileObject.close()

    def body_fn(self):
        raise NotImplementedError()

    def g(self, p, a=1, B=0, y=1):
        """ Normalization Function. Normalizes loss w.r.t. label proportion.

        Constraints: 
         1. g(p) = 1 when p = 1
         2. g(p) = a * p^y + B, where a, y and B are hyperparameters
        """
        return a * tf.math.pow(p, y) + B

    def loss_fn(self, y_true, y_pred, weights):
        loss = tf.compat.v1.losses.sigmoid_cross_entropy(y_true, y_pred,
          weights=weights,
          reduction=(tf.compat.v1.losses.Reduction.NONE))
        return tf.math.reduce_sum(loss, axis=0)

    def train(self, num_steps, lr=None, checkpoint_path=None):
        if lr == None:
            lr = self.lr
        tf.compat.v1.logging.info('Starting Training')

        @tf.function
        def train_step(f):
            features = f[:-2]
            labels = f[(-2)]
            weights = f[(-1)]
            with tf.GradientTape() as (tape):
                logits = self.model(features, training=True)
                kl_loss = tf.reduce_sum(self.model.losses)
                neg_log_likelihood = self.loss_fn(labels, logits, weights)
                elbo_loss = neg_log_likelihood + kl_loss
            gradients = tape.gradient(elbo_loss, self.model.trainable_variables)
            self.optimizer.apply_gradients(zip(gradients, self.model.trainable_variables))
            return (
             elbo_loss, neg_log_likelihood, kl_loss)

        for step, f in enumerate(self.train_iter.take(num_steps)):
            loss = train_step(f)
            if step % 1000 == 0:
                tf.compat.v1.logging.info(str(step) + ' ' + str(tf.reduce_mean(loss[0])) + str(tf.reduce_mean(loss[1])) + str(tf.reduce_mean(loss[2])))
                if self.debug:
                    tf.compat.v1.logging.info('On validation')
                    _, _, _, _, _ = self.test(40000, log=False)
                    tf.compat.v1.logging.info('')

    def test(self, num_samples, mode=Dataset.VALID, calculate_metrics=False):
        """
        Tests model on valid and test dataset handlers.
        """
        if mode == Dataset.VALID:
            handle = self.valid_iter
        elif mode == Dataset.TEST:
            if len(self.test_celltypes) > 0:
                handle = self.test_iter
        else:
            raise Exception('No data exists for %s. Use function test_from_generator() if you want to create a new iterator.' % mode)
        return self.run_predictions(num_samples, handle, calculate_metrics)

    def test_from_generator(self, num_samples, ds, calculate_metrics=True):
        """
        Runs test given a specified data generator 
        :param num_samples: number of samples to test
        :param ds: tensorflow dataset, created by dataset_to_tf_dataset
        :param cell_type: cell type to test on. Used to generate holdout indices.
        
        :return predictions
        """
        return self.run_predictions(num_samples, ds, calculate_metrics)

    def eval_vector(self, data, vector, indices):
        """
        Evaluates a new cell type based on its chromatin (DNase or ATAC-seq) vector. len(vector) should equal
        the data.shape[1]
        :param data: data to build features from 
        :param vector: vector of 0s/1s of binding sites TODO AM 4/3/2019: try peak strength instead of 0s/1s
        :param indices: indices of vector to actually score. You need all of the locations for the generator.

        :return predictions for all factors
        """
        input_shapes, output_shape, ds = generator_to_tf_dataset(load_data(data, (self.test_celltypes),
          (self.eval_cell_types),
          (self.matrix),
          (self.assaymap),
          (self.cellmap),
          radii=(self.radii),
          mode=(Dataset.RUNTIME),
          dnase_vector=vector,
          indices=indices), self.batch_size, 1, self.prefetch_size)
        num_samples = len(indices)
        results = self.run_predictions(num_samples, ds, calculate_metrics=False)
        return (
         results['preds_mean'], results['preds_std'])

    def run_predictions(self, num_samples, iter_, calculate_metrics=True, samples=50):
        """
        Runs predictions on num_samples records
        :param num_samples: number of samples to test
        :param iter_: output of self.sess.run(generator_to_one_shot_iterator()), handle to one shot iterator of records
        :param log: if true, logs individual factor accuracies
        
        :return preds, truth, assay_dict, auROC, auPRC, False
            preds = predictions, 
            truth = actual values, 
            sample_weight: 0/1 weights on predictions.  
            assay_dict = if log=True, holds predictions for individual factors
            auROC = average macro area under ROC for all factors with truth values
            auPRC = average area under PRC for all factors with truth values
        """
        inv_assaymap = {v:k for k, v in self.assaymap.items()}
        batches = int(num_samples / self.batch_size) + 1
        truth = []
        preds_mean = []
        preds_std = []
        sample_weight = []

        @tf.function
        def predict_step(inputs_b):
            inputs_tiled = [tf.tile(i, (samples, 1)) for i in inputs_b]
            tmp = self.model(inputs_tiled)
            y_pred = tf.sigmoid(tmp)
            preds = tf.stack(tf.split(y_pred, samples, axis=0), axis=0)
            return (tf.math.reduce_mean(preds, axis=0), tf.math.reduce_std(preds, axis=0))

        for f in tqdm.tqdm(iter_.take(batches)):
            inputs_b = f[:-2]
            truth_b = f[(-2)]
            weights_b = f[(-1)]
            preds_mean_b, preds_std_b = predict_step(inputs_b)
            preds_mean.append(preds_mean_b)
            preds_std.append(preds_std_b)
            truth.append(truth_b)
            sample_weight.append(weights_b)

        preds_mean = tf.concat(preds_mean, axis=0)
        preds_std = tf.concat(preds_std, axis=0)
        truth = tf.concat(truth, axis=0)
        sample_weight = tf.concat(sample_weight, axis=0)
        truth = truth[:num_samples, :]
        preds_mean = preds_mean[:num_samples, :]
        preds_std = preds_std[:num_samples, :]
        sample_weight = sample_weight[:num_samples, :]
        truth_reset = np.copy(truth)
        truth_reset[truth_reset < Label.UNBOUND.value] = 0
        if not calculate_metrics:
            return {'preds_mean':preds_mean, 
             'preds_std':preds_std, 
             'truth':truth, 
             'weights':sample_weight, 
             'assay_dict':None, 
             'auROC':None, 
             'auPRC':None}
        else:
            assert preds_mean.shape == sample_weight.shape
            try:
                assay_dict = get_performance(self.assaymap, preds_mean, truth_reset, sample_weight)
                auROC = np.nanmean(list(map(lambda x: x['AUC'], assay_dict.values())))
                auPRC = np.nanmean(list(map(lambda x: x['auPRC'], assay_dict.values())))
                avgGINI = np.nanmean(list(map(lambda x: x['GINI'], assay_dict.values())))
                tf.compat.v1.logging.info('macro auROC:     ' + str(auROC))
                tf.compat.v1.logging.info('auPRC:     ' + str(auPRC))
                tf.compat.v1.logging.info('GINI:     ' + str(avgGINI))
            except ValueError as v:
                auROC = None
                auPRC = None
                tf.compat.v1.logging.info('Failed to calculate metrics')

            return {'preds_mean':preds_mean, 
             'preds_std':preds_std, 
             'truth':truth, 
             'weights':sample_weight, 
             'assay_dict':assay_dict, 
             'auROC':auROC, 
             'auPRC':auPRC}

    def score_whole_genome(self, chromatin_peak_file, file_prefix, chrs=None, all_data=None):
        """
        Runs a whole genome scan for all available genomic regions in the dataset (about 3.2Million regions)
        Takes about 1 hour.

        Args:
            :param chromatin_peak_file: narrowpeak or bed file containing chromatin accessibility to score
            :param file_prefix: path to save compressed numpy file to. Adds '.npz' extension.
            :param chroms: list of chromosome names to score. If none, scores all chromosomes.
            :param all_data: for testing. If none, generates a concatenated matrix of all data when called.

        """
        peak_vector_chromatin, _ = bedFile2Vector(chromatin_peak_file, self.regionsFile)
        liRegions = enumerate(load_bed_regions(self.regionsFile))
        if chrs is not None:
            liRegions = [i for i in liRegions if i[1].chrom in chrs]
        idx = np.array([i[0] for i in liRegions])
        liRegions = [i[1] for i in liRegions]
        print('scoring %i regions' % idx.shape[0])
        if all_data is None:
            all_data = concatenate_all_data(self.data, self.regionsFile)
        predictions = self.eval_vector(all_data, peak_vector_chromatin, idx)
        print('finished predictions...', predictions[0].shape)
        npRegions = np.array(list(map(lambda x: np.array([x.chrom, x.start, x.end]), liRegions)))
        means = np.concatenate([npRegions, predictions[0]], axis=1)
        stds = np.concatenate([npRegions, predictions[1]], axis=1)
        np.savez_compressed(file_prefix, means=means, stds=stds, names=(np.array(['chr', 'start', 'end'] + list(self.assaymap)[1:])))
        print('columns for matrices are chr, start, end, %s' % ', '.join(list(self.assaymap)[1:]))

    def score_peak_file(self, chromatin_peak_file, regions_peak_file):
        peak_vector_chromatin, all_peaks_chromatin = bedFile2Vector(chromatin_peak_file, EPITOME_ALLTFS_BEDFILE + '.gz')
        peak_vector_regions, all_peaks_regions = bedFile2Vector(regions_peak_file, EPITOME_ALLTFS_BEDFILE + '.gz')
        print('finished loading peak file')
        idx = np.where(peak_vector_regions == True)[0]
        print('scoring %i regions' % idx.shape[0])
        if len(idx) == 0:
            raise ValueError('No positive peaks found in %s' % regions_peak_file)
        all_data = np.concatenate((self.data[Dataset.TRAIN], self.data[Dataset.VALID], self.data[Dataset.TEST]), axis=1)
        predictions = self.eval_vector(all_data, peak_vector_chromatin, idx)
        predictions = np.array(list(zip(predictions[0], predictions[1])))
        print('finished predictions...', predictions.shape)
        num_factors = predictions.shape[(-1)]
        liRegions = load_bed_regions(EPITOME_ALLTFS_BEDFILE + '.gz')
        prediction_positions = itemgetter(*idx)(liRegions)
        zipped = list(zip(prediction_positions, predictions))

        def reduceMeans(peak):
            if peak[1]:
                res = np.array(list(map(lambda k: k[1][0], filter(lambda x: Region.overlaps(peak[0], x[0], 1), zipped))))
                mean = np.mean(res, axis=0)
                if res.shape[0] == 0:
                    return (peak[0], np.zeros(num_factors))
                else:
                    return (
                     peak[0], mean)
            else:
                return (
                 peak[0], np.zeros(num_factors))

        grouped = list(map(lambda x: np.matrix(reduceMeans(x)[1]), zip(all_peaks_regions[0], all_peaks_regions[1])))
        final = np.concatenate(grouped, axis=0)
        df = pd.DataFrame(final, columns=(list(self.assaymap)[1:]))
        df_pos = pd.read_csv(regions_peak_file, sep='\t', header=None)[[0, 1, 2]]
        final_df = pd.concat([df_pos, df], axis=1)
        return final_df


class VLP(VariationalPeakModel):

    def __init__(self, *args, **kwargs):
        """ Creates a new model with 4 layers with 100 unites each.
            To resume model training on an old model, call:
            model = VLP(checkpoint=path_to_saved_model)
        """
        self.activation = tf.tanh
        self.layers = 2
        if 'checkpoint' in kwargs.keys():
            fileObject = open(kwargs['checkpoint'] + '/model_params.pickle', 'rb')
            metadata = pickle.load(fileObject)
            fileObject.close()
            (VariationalPeakModel.__init__)(self, **metadata, **kwargs)
            file = h5py.File(os.path.join(kwargs['checkpoint'], 'weights.h5'), 'r')
            weights = []
            for i in range(len(file.keys())):
                weights.append(file[('weight' + str(i))][:])

            self.model.set_weights(weights)
            file.close()
        else:
            (VariationalPeakModel.__init__)(self, *args, **kwargs)

    def create_model(self):
        cell_inputs = [tf.keras.layers.Input(shape=(self.num_inputs[i],)) for i in range(len(self.num_inputs))]
        cell_channels = []
        for i in range(len(self.num_inputs)):
            last = cell_inputs[i]
            for j in range(self.layers):
                num_units = int(self.num_inputs[i] / (2 * (j + 1)))
                d = tfp.layers.DenseFlipout(num_units, activation=(self.activation))(last)
                last = d

            cell_channels.append(last)

        last = tf.keras.layers.concatenate(cell_channels)
        outputs = tfp.layers.DenseFlipout((self.num_outputs), activity_regularizer=(tf.keras.regularizers.l1_l2(self.l1, self.l2)),
          name='output_layer')(last)
        model = tf.keras.models.Model(inputs=cell_inputs, outputs=outputs)
        return model

    def create_model_parse_connections(self):
        cell_inputs = [tf.keras.layers.Input(shape=(self.num_inputs[i],)) for i in range(len(self.num_inputs))]
        cell_channels = []
        for i in range(len(self.num_inputs)):
            last = cell_inputs[i]
            for j in range(self.layers):
                num_units = int(self.num_inputs[i] / (2 * (j + 1)))
                d = tfp.layers.DenseFlipout(num_units, name=('cell_layer_%s_%i' % (self.eval_cell_types[i], j)), activation=(self.activation))(last)
                last = d

            cell_channels.append(last)

        outputs = []
        for assay in list(self.assaymap)[1:]:
            tf_channels = []
            for cell, channel in zip(self.eval_cell_types, cell_channels):
                has_data = self.matrix[(self.cellmap[cell], self.assaymap[assay])] != -1
                if has_data:
                    tf_channels.append(channel)

            outputs.append(tfp.layers.DenseFlipout(1, activity_regularizer=(tf.keras.regularizers.l1_l2(self.l1, self.l2)),
              name=('output_layer_%s' % assay))(tf.keras.layers.concatenate(tf_channels)))

        output = tf.keras.layers.concatenate(outputs)
        model = tf.keras.models.Model(inputs=cell_inputs, outputs=output)
        return model