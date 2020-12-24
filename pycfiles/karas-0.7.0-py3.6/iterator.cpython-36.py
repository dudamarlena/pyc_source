# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/karas/iterators/iterator.py
# Compiled at: 2019-01-08 04:39:39
# Size of source mod 2**32: 2421 bytes


class Iterator(object):

    def __init__(self, dataloader, repeat=False):
        self._iterator = iter(dataloader)
        self._loader = dataloader
        self._repeat = repeat
        self.reset()

    def reset(self):
        self._iterator = iter(self._loader)
        self._previous_epoch_detail = -1.0
        self._epoch = 0
        self._position = 0
        self._is_new_epoch = False

    def __next__(self):
        self._previous_epoch_detail = self.epoch_detail
        try:
            batch = next(self._iterator)
            self._position += 1
            self._is_new_epoch = False
        except:
            self._iterator = iter(self._loader)
            batch = next(self._iterator)
            self._epoch += 1
            self._position = 0
            self._is_new_epoch = True

        return batch

    @property
    def is_new_epoch(self):
        pass

    @property
    def epoch(self):
        return self._epoch

    @property
    def epoch_detail(self):
        return self._epoch + self.position / len(self._loader)

    @property
    def previous_epoch_detail(self):
        if self._previous_epoch_detail < 0:
            return
        else:
            return self._previous_epoch_detail

    @property
    def position(self):
        return self._position

    @property
    def iteration(self):
        return self.epoch * len(self._loader) + self.position

    def has_next(self):
        if self._repeat:
            return True
        else:
            return len(self._loader) > self._position

    def __len__(self):
        return len(self._loader)

    def __getstate__(self):
        state = {}
        state['_position'] = self._position
        state['_epoch'] = self._epoch
        state['_loader'] = self._loader
        state['_is_new_epoch'] = self._is_new_epoch
        state['_previous_epoch_detail'] = self._previous_epoch_detail
        state['_repeat'] = self._repeat
        return state

    def __setstate__(self, state):
        self._loader = state['_loader']
        self._iterator = iter(self._loader)
        self._position = state['_position']
        for i in range(self._position):
            next(self._iterator)

        self._position = state['_position']
        self._epoch = state['_epoch']
        self._is_new_epoch = state['_is_new_epoch']
        self._previous_epoch_detail = state['_previous_epoch_detail']
        self._repeat = state['_repeat']