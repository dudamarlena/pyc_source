# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/subaligner/hyperparameters.py
# Compiled at: 2020-05-06 18:17:25
# Size of source mod 2**32: 6283 bytes
import sys, json

class Hyperparameters(object):
    __doc__ = ' The configuration on hyper parameters used for training\n    '

    def __init__(self):
        """Hyper parameters initialiser setting default values"""
        self._Hyperparameters__learning_rate = 0.001
        self._Hyperparameters__hidden_size = {'front_layers':[
          64], 
         'back_layers':[
          32, 16]}
        self._Hyperparameters__dropout = 0.2
        self._Hyperparameters__epochs = 100
        self._Hyperparameters__optimizer = 'Adam'
        self._Hyperparameters__loss = 'binary_crossentropy'
        self._Hyperparameters__metrics = ['accuracy']
        self._Hyperparameters__batch_size = 32
        self._Hyperparameters__validation_split = 0.25
        self._Hyperparameters__monitor = 'val_loss'
        self._Hyperparameters__es_mode = 'min'
        self._Hyperparameters__es_min_delta = 1e-05
        self._Hyperparameters__es_patience = sys.maxsize
        self._Hyperparameters__network_type = 'lstm'

    def __eq__(self, other):
        """Comparator for Hyperparameters objects"""
        if isinstance(other, Hyperparameters):
            return all([
             self._Hyperparameters__learning_rate == other.learning_rate,
             self._Hyperparameters__hidden_size['front_layers'] == other.front_hidden_size,
             self._Hyperparameters__hidden_size['back_layers'] == other.back_hidden_size,
             self._Hyperparameters__dropout == other.dropout,
             self._Hyperparameters__epochs == other.epochs,
             self._Hyperparameters__optimizer == other.optimizer,
             self._Hyperparameters__loss == other.loss,
             self._Hyperparameters__metrics == other.metrics,
             self._Hyperparameters__batch_size == other.batch_size,
             self._Hyperparameters__validation_split == other.validation_split,
             self._Hyperparameters__monitor == other.monitor,
             self._Hyperparameters__es_mode == other.es_mode,
             self._Hyperparameters__es_min_delta == other.es_min_delta,
             self._Hyperparameters__es_patience == other.es_patience,
             self._Hyperparameters__network_type == other.network_type])
        else:
            return False

    @property
    def learning_rate(self):
        return self._Hyperparameters__learning_rate

    @learning_rate.setter
    def learning_rate(self, value):
        self._Hyperparameters__learning_rate = value

    @property
    def front_hidden_size(self):
        return self._Hyperparameters__hidden_size['front_layers']

    @front_hidden_size.setter
    def front_hidden_size(self, value):
        self._Hyperparameters__hidden_size['front_layers'] = value

    @property
    def back_hidden_size(self):
        return self._Hyperparameters__hidden_size['back_layers']

    @back_hidden_size.setter
    def back_hidden_size(self, value):
        self._Hyperparameters__hidden_size['back_layers'] = value

    @property
    def dropout(self):
        return self._Hyperparameters__dropout

    @dropout.setter
    def dropout(self, value):
        self._Hyperparameters__dropout = value

    @property
    def epochs(self):
        return self._Hyperparameters__epochs

    @epochs.setter
    def epochs(self, value):
        self._Hyperparameters__epochs = value

    @property
    def optimizer(self):
        return self._Hyperparameters__optimizer

    @optimizer.setter
    def optimizer(self, value):
        if value.lower() == 'adam':
            self._Hyperparameters__optimizer = 'Adam'
        else:
            if value.lower() == 'adagrad':
                self._Hyperparameters__optimizer = 'Adagrad'
            else:
                if value.lower() == 'rms':
                    self._Hyperparameters__optimizer = 'RMSprop'
                else:
                    if value.lower() == 'sgd':
                        self._Hyperparameters__optimizer = 'SGD'
                    else:
                        raise ValueError('Optimizer {} is not supported'.format(value))

    @property
    def loss(self):
        return self._Hyperparameters__loss

    @property
    def metrics(self):
        return self._Hyperparameters__metrics

    @metrics.setter
    def metrics(self, value):
        self._Hyperparameters__metrics = value

    @property
    def batch_size(self):
        return self._Hyperparameters__batch_size

    @batch_size.setter
    def batch_size(self, value):
        self._Hyperparameters__batch_size = value

    @property
    def validation_split(self):
        return self._Hyperparameters__validation_split

    @validation_split.setter
    def validation_split(self, value):
        self._Hyperparameters__validation_split = value

    @property
    def monitor(self):
        return self._Hyperparameters__monitor

    @monitor.setter
    def monitor(self, value):
        self._Hyperparameters__monitor = value

    @property
    def es_mode(self):
        return self._Hyperparameters__es_mode

    @es_mode.setter
    def es_mode(self, value):
        self._Hyperparameters__es_mode = value

    @property
    def es_min_delta(self):
        return self._Hyperparameters__es_min_delta

    @es_min_delta.setter
    def es_min_delta(self, value):
        self._Hyperparameters__es_min_delta = value

    @property
    def es_patience(self):
        return self._Hyperparameters__es_patience

    @es_patience.setter
    def es_patience(self, value):
        self._Hyperparameters__es_patience = value

    @property
    def network_type(self):
        return self._Hyperparameters__network_type

    @network_type.setter
    def network_type(self, value):
        self._Hyperparameters__network_type = value

    def to_json(self):
        """Serialise hyper parameters into JSON string

        Returns:
            string -- The serialised hyper parameters in JSON
        """
        return json.dumps(self, default=(lambda o: o.__dict__), sort_keys=True, indent=4)

    def to_file(self, file_path):
        """Serialise hyper parameters into JSON and save the content to a file

        Arguments:
            file_path {string} -- The path to the file containing saved hyper parameters.
        """
        with open(file_path, 'w', encoding='utf8') as (file):
            file.write(self.to_json())

    def clone(self):
        """Make a cloned hyper parameters object

        Returns:
            Hyperparameters -- The cloned Hyperparameters object.
        """
        return self.from_json(self.to_json())

    @classmethod
    def from_json(cls, json_str):
        """Deserialise JSON string into a Hyperparameters object

        Arguments:
            json_str {string} -- Hyper parameters in JSON.

        Returns:
            Hyperparameters -- The deserialised Hyperparameters object.
        """
        hp = cls()
        hp.__dict__ = json.loads(json_str)
        return hp

    @classmethod
    def from_file(cls, file_path):
        """Deserialise a file content into a Hyperparameters object

        Arguments:
            file_path {string} -- The path to the file containing hyper parameters.

        Returns:
            Hyperparameters -- The deserialised Hyperparameters object.
        """
        with open(file_path, 'r', encoding='utf8') as (file):
            return cls.from_json(file.read())