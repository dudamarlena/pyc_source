# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/pytq-project/pytq/scheduler.py
# Compiled at: 2017-11-29 22:43:45
import types, pickle
from multiprocessing import cpu_count
from multiprocessing.dummy import Pool
try:
    from .task import Task
    from .per_class_logger import ClassWithLogger
    from .pkg.fingerprint import hash_data
    from .pkg.exception_mate import get_last_exc_info
except:
    from pytq.task import Task
    from pytq.per_class_logger import ClassWithLogger
    from pytq.pkg.fingerprint import hash_data
    from pytq.pkg.exception_mate import get_last_exc_info

class BaseScheduler(ClassWithLogger):
    """
    All Scheduler has to inherit from this base class.

    Step1. Workflow:

    Generate task queue, it is a list of input_data.

    Step2. Pre-process input data:

    1. remove duplicate.
    2. generate :class:`~pytq.task.Task`.

    :meth:`~BaseScheduler._default_batch_pre_process` method will be called by
    default.

    Step3. For each task, :meth:`~BaseScheduler._process` method will be called,
    includes:

    1. pre_process
    2. user_process, input_data -> output_data
    3. post_process
    """

    def __init__(self, logger=None):
        super(BaseScheduler, self).__init__(logger=logger)
        try:
            self.user_hash_input(None)
            self._hash_input = self.user_hash_input
        except NotImplementedError:
            self._hash_input = self._default_hash_input
        except:
            self._hash_input = self.user_hash_input

        try:
            self.user_is_duplicate(None)
            self._is_duplicate = self.user_is_duplicate
        except NotImplementedError:
            self._is_duplicate = self._default_is_duplicate
        except:
            self._is_duplicate = self.user_is_duplicate

        try:
            self.user_batch_pre_process(None)
            self._batch_pre_process = self.user_batch_pre_process
        except NotImplementedError:
            self._batch_pre_process = self._default_batch_pre_process
        except:
            self._batch_pre_process = self.user_batch_pre_process

        try:
            self.user_pre_process(None)
            self._pre_process = self.user_pre_process
        except NotImplementedError:
            self._pre_process = self._default_pre_process
        except:
            self._pre_process = self.user_pre_process

        try:
            self.user_post_process(None)
            self._post_process = self.user_post_process
        except NotImplementedError:
            self._post_process = self._default_post_process
        except:
            self._post_process = self.user_post_process

        self.ignore_error = None
        return

    def _default_hash_input(self, input_data):
        u"""
        Default hash method to get a identical fingerprint for input data.

        By default its: pickle the data and md5 it.

        This method will be used when :meth:`BaseScheduler.user_hash_input`
        are not defined.

        :returns: fingerprint for ``input_data``
        :rtype: string or integer. depends on use case.

        **中文文档**

        默认的 取 ``input_data`` 指纹的操作。
        实际上是对 ``pickle.dumps`` 后的数据取 md5 指纹。
        """
        return hash_data(input_data)

    def user_hash_input(self, input_data):
        u"""
        (Optional) Get identical fingerprint for input data.

        :returns: fingerprint for ``input_data``
        :rtype: string or integer. depends on use case.

        **中文文档**

        (可选自定义) 用户自己定义的取 ``input_data`` 指纹的操作。如果不定义，则使用

        :meth:`BaseScheduler._default_hash_input` 方法。
        """
        raise NotImplementedError

    def _hash_input(self, input_data):
        u"""
        The real hashing method will be called.

        :returns: fingerprint for ``input_data``
        :rtype: string or integer. depends on use case.

        **中文文档**

        实际被调用的取指纹方法。
        """
        raise NotImplementedError

    def _default_is_duplicate(self, task):
        u"""
        Default duplicate test method, always not duplicate.

        :return: return True, when it's a duplicate item.
        :rtype: boolean.

        **中文文档**

        默认的任务排重检测。实际上是全部视为 ``不重复``。
        """
        return False

    def user_is_duplicate(self, task):
        u"""
        (Optional) Check if a task is duplicate.

        :return: return True, when it's a duplicate item.
        :rtype: boolean.

        .. warning::

            If you customized this method, usually you also need to implement
            :meth:`~BaseScheduler.user_batch_pre_process` method.

            Because default batch pre-process includes duplicate filter.

        **中文文档**

        (可选自定义) 用户自定义的任务排重检测。
        """
        raise NotImplementedError

    def _is_duplicate(self, task):
        u"""
        The real duplicate test method will be called.

        :return: return True, when it's a duplicate item.
        :rtype: boolean.

        **中文文档**

        (可选自定义) 用户自定义的任务排重检测。
        """
        raise NotImplementedError

    def _remove_duplicate(self, input_data_queue):
        u"""
        Remove duplicate input_data. And pack ``input_data`` to
        :class:`pytq.task.Task`.

        This method will be used for default batch pre-process when
        ``pre_process`` are not given in :meth:`~BaseScheduler.do`.

        :param input_data_queue:
        :returns: task_queue.
        :rtype: types.GeneratorType.

        **中文文档**

        移除那些重复的输入数据，并将 ``input_data`` 打包成 :class:`pytq.task.Task`。
        """
        is_generator = isinstance(input_data_queue, types.GeneratorType)
        if not is_generator:
            left_counter = len(input_data_queue)
        nth_counter = 0
        for input_data in input_data_queue:
            if is_generator:
                left_counter = None
            else:
                left_counter -= 1
            task = Task(id=self._hash_input(input_data), input_data=input_data, nth_counter=nth_counter, left_counter=left_counter)
            if not self._is_duplicate(task):
                nth_counter += 1
                yield task

        return

    def user_batch_pre_process(self, input_data_queue):
        """
        A method will be called to pre process task queue before doing any real
        per task process. Usually it can be duplicate filter, statistic check.

        :param input_data_queue:
        :return: task_queue, iterable object, item in it has to be
        :class:`~pytq.task.Task`. Recommend to implement ``task.nth_counter``
        and ``task.left_counter`` variable.
        """
        raise NotImplementedError

    _default_batch_pre_process = _remove_duplicate
    _default_batch_pre_process.__doc__ = _remove_duplicate.__doc__

    def _batch_pre_process(self, input_data_queue):
        """
        The real method will be called for batch pre-process.
        """
        raise NotImplementedError

    def user_pre_process(self, task):
        """
        (Optional) Defines the action that before the
        :meth:`BaseScheduler.user_process() been called.
        Will be called when :attr:`pytq.task.Task.pre_process` are not defined.

        :param task: :class:`pytq.task.Task` instance.
        """
        raise NotImplementedError

    def _default_pre_process(self, task):
        """
        Default behavior of user_pre_process, do nothing.
        """
        pass

    def _pre_process(self, task):
        """
        The real method will be called for pre_process.
        """
        raise NotImplementedError

    def user_post_process(self, task):
        """
        (Optional) Defines the action that after the
        :meth:`~BaseScheduler.user_process() been called.
        Will be called when :attr:`pytq.task.Task.post_process` are not defined.

        .. warning::

            When you customized this method, usually you also need to update
            :meth:`~BaseScheduler.get` method. Because post process usually
            is used to write output_data to data persistence layer. If you
            changed the way you store it, you have to change the way you read
            it.

        :param task: :class:`pytq.task.Task` instance.
        """
        raise NotImplementedError

    def _default_post_process(self, task):
        """
        Default behavior of user_post_process, do nothing.
        """
        pass

    def _post_process(self, task):
        """
        The real method will be called for post_process.
        """
        raise NotImplementedError

    def user_process(self, input_data):
        """
        (Required) Defines the logic that process the input_data, returns
        output_data

        :param input_data:
        :return: the output_data
        """
        raise NotImplementedError

    def _process_one(self, task):
        u"""
        Process one task.

        **中文文档**

        处理数据。包含三个步骤：

        1. 预处理
        2. 处理
        3. 后处理
        """
        if task.pre_process is None:
            self._pre_process(task)
        else:
            task._pre_process()
        output_data = self.user_process(task.input_data)
        task.output_data = output_data
        if task.post_process is None:
            self._post_process(task)
        else:
            task._post_process()
        return

    def _process(self, task):
        """
        The real processing method will be called.
        """
        self.info(task.progress_msg())
        if self.ignore_error:
            try:
                self._process_one(task)
                self.info('Success!', 1)
            except Exception as e:
                self.info('Failed due to: %r' % get_last_exc_info(), 1)

        else:
            self._process_one(task)
            self.info('Success!', 1)

    def _do_single_process(self, task_queue):
        """
        Execute single thread process.

        :param task_queue: task queue/list.
        """
        for task in task_queue:
            self._process(task)

    def _do_multi_process(self, task_queue, processes=None):
        """
        Execute multi thread process.

        :param task_queue: task queue/list.
        """
        if processes is None:
            processes = cpu_count()
        pool = Pool(processes=processes)
        pool.map(self._process, task_queue)
        return

    def do(self, input_data_queue, pre_process=None, multiprocess=False, processes=None, ignore_error=True):
        u"""
        Process all input_data.

        :param input_data_queue: list of input data (or generator).
        :param pre_process: a callable function take input_data_queue, and
          pre-process it, returns a task_queue (iterable object, item are
          :class:`~pytq.task.Task`.
        :param multiprocess: trigger to use multiprocess.

        **中文文档**

        处理数据序列中的所有数据。

        1. 预处理所有数据，将其打包成 ``task_queue``。
        2. 进行单线程处理或是多线程处理。
        """
        if pre_process is None:
            task_queue = self._batch_pre_process(input_data_queue)
        else:
            task_queue = pre_process(input_data_queue)
        try:
            self.info('\nHas %s items todo.' % len(input_data_queue))
        except:
            self.info('\nHas UNKNOWN items todo')

        self.ignore_error = ignore_error
        if multiprocess:
            self._do_multi_process(task_queue, processes=processes)
        else:
            self._do_single_process(task_queue)
        self.info('Complete!')
        return

    def clear_all(self):
        u"""
        Clear all data.

        **中文文档**

        重置Filter至初始状态。
        """
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def get(self, id):
        u"""
        Get output data by fingerprint of input_data.

        **中文文档**

        根据输入的指纹, 直接获得已经完成的输出数据。
        """
        raise NotImplementedError

    def get_output(self, input_data):
        u"""
        Get output data of the input_data.

        **中文文档**

        根据输入的数据, 直接获得已经完成的输出的数据。
        """
        return self.get(self._hash_input(input_data))

    def keys(self):
        return iter(self)

    def items(self):
        for key in self:
            yield (key, self.get(key))


class BaseDBTableBackedScheduler(BaseScheduler):
    """
    Scheduler that use database table as backend storage.

    - Task.id as primary_key
    - Other column / field for input_data, output_data storage.
    """

    def _get_finished_id_set(self):
        """
        A method that returns all saved id set.
        (For all processed input_data)

        :returns: a id set.
        :rtype: set.
        """
        raise NotImplementedError

    def _default_batch_pre_process(self, input_data_queue):
        """
        Default method to pre-process input_data_queue in Database Table backed
        scheduler. The logic is:

        1. get all finished _id set.
        2. filter out all input_data that fingerprint falls in that set.
        """
        finished_id_set = self._get_finished_id_set()
        is_generator = isinstance(input_data_queue, types.GeneratorType)
        if not is_generator:
            left_counter = len(input_data_queue)
        nth_counter = 0
        for input_data in input_data_queue:
            if is_generator:
                left_counter = None
            else:
                left_counter -= 1
            id = self._hash_input(input_data)
            if id not in finished_id_set:
                nth_counter += 1
                task = Task(id=id, input_data=input_data, nth_counter=nth_counter, left_counter=left_counter)
                yield task

        return


class Encoder(object):

    def link_encode_method(self):
        """
        Bind encode method.
        """
        try:
            self.user_encode(None)
            self._encode = self.user_encode
        except NotImplementedError:
            self._encode = self._default_encode
        except:
            self._encode = self.user_encode

        try:
            self.user_decode(None)
            self._decode = self.user_decode
        except NotImplementedError:
            self._decode = self._default_decode
        except:
            self._decode = self.user_decode

        return

    def _default_encode(self, obj):
        return pickle.dumps(obj)

    def user_encode(self, obj):
        u"""
        (Optional) User defined serializer for output_data.

        :returns: bytes or string.

        **中文文档**

        用于对处理结果序列化的函数。默认使用pickle。
        """
        raise NotImplementedError

    def _encode(self, obj):
        raise NotImplementedError

    def _default_decode(self, bytes_or_str):
        return pickle.loads(bytes_or_str)

    def user_decode(self, bytes_or_str):
        u"""
        (Optional) User defined deserializer for output_data.

        :returns: python object.

        **中文文档**

        用于对处理结果反序列化的函数。默认使用pickle。
        """
        raise NotImplementedError

    def _decode(self, bytes_or_str):
        raise NotImplementedError


class StatusFlag(object):
    """
    MongoDB collection backed scheduler.

    Feature:

    1. there's pre-defined integer - ``duplicate_flag``, will be stored in
        ``status`` column / field.
    2. there's a ``edit_at`` datetime field, represent the
        last time the document been edited.

    .. note::

        Any value greater or equal than ``duplicate_flag``, AND the ``edit_at``
        time is smaller ``update_interval`` seconds ago, means it is a duplicate
        item.

    :param duplicate_flag: int, represent a status code for finished / duplicate
    :param update_interval: int, represent need-to-update interval (unit: seconds)
    :param status_key: str.
    :param edit_key: str.
    """
    duplicate_flag = None
    update_interval = None
    status_key = '_status'
    edit_at_key = '_edit_at'

    def pre_process_duplicate_flag_and_update_interval(self, duplicate_flag, update_interval):
        """
        bind settings.
        """
        if duplicate_flag is not None:
            self.duplicate_flag = duplicate_flag
        if update_interval is not None:
            self.update_interval = update_interval
        return

    @property
    def duplicate_flag(self):
        """
        A integer value represent its a duplicate item. Any value greater or equal
        than this will be a duplicate item, otherwise its not.

        You could define that when you initiate the scheduler.
        """
        raise NotImplementedError

    @property
    def update_interval(self):
        """
        If a item has been finished more than ``update_interval`` seconds, then
        it should be re-do, and it is NOT a duplicate item.

        You could define that when you initiate the scheduler.
        """
        raise NotImplementedError