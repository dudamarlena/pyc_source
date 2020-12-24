# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Zeras/data_batcher.py
# Compiled at: 2020-03-15 07:46:43
# Size of source mod 2**32: 8796 bytes
import time, random, queue as Queue

def run_through_list_data(list_data, single_pass):
    """
    """
    while 1:
        for item in list_data:
            yield item

        if single_pass:
            break


class DataBatcher(object):
    __doc__ = ' This class is meant to be task-agnostic\n    '
    BATCH_TIME_OUT = 6
    EXAMPLE_TIME_OUT = 3

    def __init__(self, example_gen_or_list, batch_standardizer, batch_size, single_pass, with_bucket=False, worker_type='thread', num_workers_example_single=1, num_workers_batch_single=3, num_workers_example_multi=12, num_workers_batch_multi=12, bucketing_cahce_size=10000, batch_queue_max=300):
        """
        """
        if isinstance(example_gen_or_list, list):
            self.example_gen = lambda single_pass: run_through_list_data(example_gen_or_list, single_pass)
        else:
            self.example_gen = example_gen_or_list
        self.batch_standardizer = batch_standardizer
        self.batch_size = batch_size
        self.with_bucket = with_bucket
        self.single_pass = single_pass
        if single_pass:
            self.num_workers_example = num_workers_example_single
            self.num_workers_batch = num_workers_batch_single
        else:
            self.num_workers_example = num_workers_example_multi
            self.num_workers_batch = num_workers_batch_multi
        self.bucketing_cache_size = bucketing_cahce_size
        self.batch_queue_max = batch_queue_max
        self.worker_type = worker_type
        self.build_queue_and_workers(self.worker_type)

    def get_next_batch(self):
        """
        """
        if self._batch_queue.qsize() == 0:
            print('batch_q_size: %i, example_q_size: %i' % (
             self._batch_queue.qsize(), self._example_queue.qsize()))
        try:
            batch = self._batch_queue.get(timeout=(self.BATCH_TIME_OUT))
            return batch
        except BaseException:
            print('batch queue finished')
            return

    def build_queue_and_workers(self, worker_type='thread'):
        """
        """
        self.worker_type = worker_type
        if worker_type == 'process':
            from multiprocessing import Process
        else:
            from multiprocessing.dummy import Process
        self.Process = Process
        self._batch_queue = Queue.Queue(self.batch_queue_max)
        self._example_queue = Queue.Queue(self.batch_queue_max * self.batch_size)
        self._finished_reading = False
        self.count_put_examples = 0
        self.count_get_examples = 0
        self._example_q_workers = []
        for _ in range(self.num_workers_example):
            self._example_q_workers.append(self.Process(target=(self.fill_example_queue)))
            self._example_q_workers[(-1)].daemon = True
            self._example_q_workers[(-1)].start()

        self._batch_q_workers = []
        for _ in range(self.num_workers_batch):
            self._batch_q_workers.append(self.Process(target=(self.fill_batch_queue)))
            self._batch_q_workers[(-1)].daemon = True
            self._batch_q_workers[(-1)].start()

        if not self.single_pass:
            self._watch_worker = self.Process(target=(self.watch_workers))
            self._watch_worker.daemon = True
            self._watch_worker.start()

    def fill_example_queue(self):
        """
        """
        example_iter = self.example_gen(single_pass=(self.single_pass))
        while True:
            try:
                base_example = next(example_iter)
            except BaseException:
                if self.single_pass:
                    print('single_pass on, data finished, break loop')
                    self._finished_reading = True
                    break
                else:
                    raise Exception('single_pass mode is off but the example generator is out of data; ERROR!')

            self._example_queue.put(base_example)
            self.count_put_examples += 1

    def fill_batch_queue(self):
        """
        """
        while True:
            if self.with_bucket:
                inputs = []
                for _ in range(self.batch_size * self.bucketing_cache_size):
                    inputs.append(self._example_queue.get(timeout=(self.EXAMPLE_TIME_OUT)))

                inputs = sorted(inputs, key=(lambda item: item.seq_len))
                batches = []
                for i in range(0, len(inputs), self.batch_size):
                    batches.append(inputs[i:i + self.batch_size])

                if not self.single_pass:
                    random.shuffle(batches)
                for b in batches:
                    self._batch_queue.put(self.batch_standardizer(b))

            else:
                b = []
                flag_succeed = 1
                for eid in range(self.batch_size):
                    try:
                        example = self._example_queue.get(timeout=(self.EXAMPLE_TIME_OUT))
                        b.append(example)
                        self.count_get_examples += 1
                    except BaseException:
                        flag_succeed = 0
                        break

                if flag_succeed == 1:
                    self._batch_queue.put(self.batch_standardizer(b))
                else:
                    if self._finished_reading:
                        if len(b) > 0:
                            self._batch_queue.put(self.batch_standardizer(b))
                            print('put last batch')
                    else:
                        for example in b:
                            self._example_queue.put(example)

                        print('reput examples: %d.' % len(b))
                    print('batch thread finished, break loop')
                    break

    def watch_workers(self):
        """
        """
        while True:
            time.sleep(60)
            if self._finished_reading:
                break
            for idx, t in enumerate(self._example_q_workers):
                if not t.is_alive():
                    print('found example queue worker dead. Restarting.')
                    new_t = self.Process(target=(self.fill_example_queue))
                    self._example_q_workers[idx] = new_t
                    new_t.daemon = True
                    new_t.start()

            for idx, t in enumerate(self._batch_q_workers):
                if not t.is_alive():
                    print('found batch queue worker dead. Restarting.')
                    new_t = self.Process(target=(self.fill_batch_queue))
                    self._batch_q_workers[idx] = new_t
                    new_t.daemon = True
                    new_t.start()


if __name__ == '__main__':
    pass