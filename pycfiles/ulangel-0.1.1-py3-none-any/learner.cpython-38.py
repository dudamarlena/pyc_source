# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./ulangel/utils/learner.py
# Compiled at: 2020-03-05 08:23:54
# Size of source mod 2**32: 4662 bytes
import torch
from ulangel.utils.callbacks import CancelBatchException, CancelEpochException, CancelTrainException, listify

class Learner:
    __doc__ = 'An object to use the defined RNN model, the databunch, all callbacks,\n    the loss function ,the optimization function to train.\n    '

    def __init__(self, model, data, loss_func, opt_func, lr=0.01, cbs=None, cb_funcs=None):
        self.model = model
        self.data = data
        self.loss_func = loss_func
        self.opt_func = opt_func
        self.lr = lr
        self.in_train = False
        self.logger = print
        self.opt = None
        self.cbs = []
        self.add_cbs(cbs)
        self.add_cbs((cbf() for cbf in listify(cb_funcs)))

    def add_cbs(self, cbs):
        for cb in listify(cbs):
            self.add_cb(cb)

    def add_cb(self, cb):
        cb.set_runner(self)
        setattr(self, cb.name, cb)
        self.cbs.append(cb)

    def remove_cbs(self, cbs):
        for cb in listify(cbs):
            self.cbs.remove(cb)

    def one_batch--- This code section failed: ---

 L.  49         0  SETUP_FINALLY       188  'to 188'
                2  SETUP_FINALLY       156  'to 156'

 L.  50         4  LOAD_FAST                'i'
                6  LOAD_FAST                'self'
                8  STORE_ATTR               iter

 L.  51        10  LOAD_FAST                'xb'
               12  LOAD_FAST                'self'
               14  STORE_ATTR               xb

 L.  52        16  LOAD_FAST                'yb'
               18  LOAD_FAST                'self'
               20  STORE_ATTR               yb

 L.  55        22  LOAD_FAST                'self'
               24  LOAD_ATTR                yb
               26  LOAD_METHOD              long
               28  CALL_METHOD_0         0  ''
               30  LOAD_FAST                'self'
               32  STORE_ATTR               yb

 L.  56        34  LOAD_FAST                'self'
               36  LOAD_STR                 'begin_batch'
               38  CALL_FUNCTION_1       1  ''
               40  POP_TOP          

 L.  58        42  LOAD_FAST                'self'
               44  LOAD_METHOD              model
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                xb
               50  CALL_METHOD_1         1  ''
               52  LOAD_FAST                'self'
               54  STORE_ATTR               pred

 L.  59        56  LOAD_FAST                'self'
               58  LOAD_STR                 'after_pred'
               60  CALL_FUNCTION_1       1  ''
               62  POP_TOP          

 L.  60        64  LOAD_FAST                'self'
               66  LOAD_METHOD              loss_func
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                pred
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                yb
               76  CALL_METHOD_2         2  ''
               78  LOAD_FAST                'self'
               80  STORE_ATTR               loss

 L.  61        82  LOAD_FAST                'self'
               84  LOAD_STR                 'after_loss'
               86  CALL_FUNCTION_1       1  ''
               88  POP_TOP          

 L.  62        90  LOAD_FAST                'self'
               92  LOAD_ATTR                in_train
               94  POP_JUMP_IF_TRUE    106  'to 106'

 L.  63        96  POP_BLOCK        
               98  POP_BLOCK        
              100  CALL_FINALLY        188  'to 188'
              102  LOAD_CONST               None
              104  RETURN_VALUE     
            106_0  COME_FROM            94  '94'

 L.  64       106  LOAD_FAST                'self'
              108  LOAD_ATTR                loss
              110  LOAD_METHOD              backward
              112  CALL_METHOD_0         0  ''
              114  POP_TOP          

 L.  65       116  LOAD_FAST                'self'
              118  LOAD_STR                 'after_backward'
              120  CALL_FUNCTION_1       1  ''
              122  POP_TOP          

 L.  66       124  LOAD_FAST                'self'
              126  LOAD_ATTR                opt
              128  LOAD_METHOD              step
              130  CALL_METHOD_0         0  ''
              132  POP_TOP          

 L.  67       134  LOAD_FAST                'self'
              136  LOAD_STR                 'after_step'
              138  CALL_FUNCTION_1       1  ''
              140  POP_TOP          

 L.  68       142  LOAD_FAST                'self'
              144  LOAD_ATTR                opt
              146  LOAD_METHOD              zero_grad
              148  CALL_METHOD_0         0  ''
              150  POP_TOP          
              152  POP_BLOCK        
              154  JUMP_FORWARD        184  'to 184'
            156_0  COME_FROM_FINALLY     2  '2'

 L.  69       156  DUP_TOP          
              158  LOAD_GLOBAL              CancelBatchException
              160  COMPARE_OP               exception-match
              162  POP_JUMP_IF_FALSE   182  'to 182'
              164  POP_TOP          
              166  POP_TOP          
              168  POP_TOP          

 L.  70       170  LOAD_FAST                'self'
              172  LOAD_STR                 'after_cancel_batch'
              174  CALL_FUNCTION_1       1  ''
              176  POP_TOP          
              178  POP_EXCEPT       
              180  JUMP_FORWARD        184  'to 184'
            182_0  COME_FROM           162  '162'
              182  END_FINALLY      
            184_0  COME_FROM           180  '180'
            184_1  COME_FROM           154  '154'
              184  POP_BLOCK        
              186  BEGIN_FINALLY    
            188_0  COME_FROM           100  '100'
            188_1  COME_FROM_FINALLY     0  '0'

 L.  72       188  LOAD_FAST                'self'
              190  LOAD_STR                 'after_batch'
              192  CALL_FUNCTION_1       1  ''
              194  POP_TOP          
              196  END_FINALLY      

Parse error at or near `POP_BLOCK' instruction at offset 98

    def all_batches(self):
        self.iters = len(self.dl)
        try:
            for i, (xb, yb) in enumerate(self.dl):
                self.one_batch(i, xb, yb)

        except CancelEpochException:
            self('after_cancel_epoch')

    def do_begin_fit(self, epochs):
        self.epochs = epochs
        self.loss = torch.as_tensor(0.0)
        self('begin_fit')

    def do_begin_epoch(self, epoch):
        self.epoch = epoch
        self.dl = self.data.train_dl
        print(self.epoch)
        return self('begin_epoch')

    def fit(self, epochs, cbs=None, reset_opt=False):
        self.add_cbs(cbs)
        if not (reset_opt or self.opt):
            self.opt = self.opt_func((self.model.parameters), lr=(self.lr))
        try:
            try:
                self.do_begin_fit(epochs)
                for epoch in range(epochs):
                    self.do_begin_epoch(epoch)
                    if not self('begin_epoch'):
                        self.all_batches
                    with torch.no_grad:
                        self.dl = self.data.valid_dl
                        if not self('begin_validate'):
                            self.all_batches
                    self('after_epoch')

            except CancelTrainException:
                self('after_cancel_train')

        finally:
            self('after_fit')
            self.remove_cbs(cbs)

    ALL_CBS = {
     'begin_batch',
     'after_pred',
     'after_loss',
     'after_backward',
     'after_step',
     'after_cancel_batch',
     'after_batch',
     'after_cancel_epoch',
     'begin_fit',
     'begin_epoch',
     'begin_validate',
     'after_epoch',
     'after_cancel_train',
     'after_fit'}

    def __call__(self, cb_name):
        res = False
        assert cb_name in self.ALL_CBS
        for cb in sorted((self.cbs), key=(lambda x: x._order)):
            res = cb(cb_name) and res
        else:
            return res


def freeze_all(model_all_layers):
    for layer in model_all_layers:
        for operation in layer:
            for param in operation.parameters:
                param.requires_grad = False


def unfreeze_all(model_all_layers):
    for layer in model_all_layers:
        for operation in layer:
            for param in operation.parameters:
                param.requires_grad = True


def freeze_upto(model_all_layers, nb_layer):
    freeze_all(model_all_layers)
    unfreeze_layers = model_all_layers[nb_layer:]
    for layer in unfreeze_layers:
        for operation in layer:
            for param in operation.parameters:
                param.requires_grad = True