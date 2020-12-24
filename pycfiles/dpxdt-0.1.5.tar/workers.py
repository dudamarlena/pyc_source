# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danvk/github/dpxdt/dpxdt/client/workers.py
# Compiled at: 2014-08-14 14:06:29
"""Workers for driving screen captures, perceptual diffs, and related work."""
import Queue, logging, sys, threading, gflags
FLAGS = gflags.FLAGS
gflags.DEFINE_float('polltime', 1.0, 'How long to sleep between polling for work from an input queue, a subprocess, or a waiting timer.')

class WorkItem(object):
    """Base work item that can be handled by a worker thread."""
    error = None
    done = False
    parent = None
    fire_and_forget = False

    def __init__(self):
        pass

    @staticmethod
    def _print_tree(obj):
        if isinstance(obj, dict):
            result = []
            for key, value in obj.iteritems():
                result.append('%s: %s' % (key, WorkItem._print_tree(value)))

            return '{%s}' % (', ').join(result)
        else:
            value_str = repr(obj)
            if len(value_str) > 100:
                return '%s...%s' % (value_str[:100], value_str[(-1)])
            return value_str

    def _get_dict_for_repr(self):
        return self.__dict__

    def __repr__(self):
        return '%s.%s(%s)#%d' % (
         self.__class__.__module__,
         self.__class__.__name__,
         self._print_tree(self._get_dict_for_repr()),
         id(self))

    def check_result(self):
        if self.error:
            raise self.error[0], self.error[1], self.error[2]


class WorkerThread(threading.Thread):
    """Base worker thread that handles items one at a time."""

    def __init__(self, input_queue, output_queue):
        """Initializer.

        Args:
            input_queue: Queue this worker consumes work from.
            output_queue: Queue where this worker puts new work items, if any.
        """
        threading.Thread.__init__(self)
        self.daemon = True
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.interrupted = False
        self.polltime = FLAGS.polltime

    def stop(self):
        """Stops the thread but does not join it."""
        if self.interrupted:
            return
        self.interrupted = True

    def run(self):
        while not self.interrupted:
            try:
                item = self.input_queue.get(True, self.polltime)
            except Queue.Empty:
                self.handle_nothing()
                continue

            try:
                try:
                    next_item = self.handle_item(item)
                except Exception as e:
                    item.error = sys.exc_info()
                    logging.exception('%s error item=%r', self.worker_name, item)
                    self.output_queue.put(item)

                logging.debug('%s processed item=%r', self.worker_name, item)
                if not isinstance(item, WorkflowItem):
                    item.done = True
                if next_item:
                    self.output_queue.put(next_item)
            finally:
                self.input_queue.task_done()

    @property
    def worker_name(self):
        return '%s:%s' % (self.__class__.__name__, self.ident)

    def handle_nothing(self):
        """Runs whenever there are no items in the queue."""
        pass

    def handle_item(self, item):
        """Handles a single item.

        Args:
            item: WorkItem to process.

        Returns:
            A WorkItem that should go on the output queue. If None, then
            the provided work item is considered finished and no
            additional work is needed.
        """
        raise NotImplemented


class WorkflowItem(WorkItem):
    """Work item for coordinating other work items.

    To use: Sub-class and override run(). Yield WorkItems you want processed
    as part of this workflow. Exceptions in child workflows will be reinjected
    into the run() generator at the yield point. Results will be available on
    the WorkItems returned by yield statements. Yield a list of WorkItems
    to do them in parallel. The first error encountered for the whole list
    will be raised if there's an exception.
    """
    result = None
    root = False

    def __init__(self, *args, **kwargs):
        WorkItem.__init__(self)
        self.args = args
        self.kwargs = kwargs

    def run(self, *args, **kwargs):
        raise NotImplemented


class WaitAny(object):
    """Return control to a workflow after any one of these items finishes.

    As soon as a single work item completes, the combined barrier will be
    fulfilled and control will return to the WorkflowItem. The return values
    will be WorkItem instances, the same ones passed into WaitAny. For
    WorkflowItems the return values will be WorkflowItems if the work is not
    finished yet, and the final return value once work is finished.
    """

    def __init__(self, items):
        """Initializer.

        Args:
            items: List of WorkItems to wait for.
        """
        self.items = items


class Barrier(list):
    """Barrier for running multiple WorkItems in parallel."""

    def __init__(self, workflow, generator, work):
        """Initializer.

        Args:
            workflow: WorkflowItem instance this is for.
            generator: Current state of the WorkflowItem's generator.
            work: Next set of work to do. May be a single WorkItem object or
                a list or tuple that contains a set of WorkItems to run in
                parallel.
        """
        list.__init__(self)
        self.workflow = workflow
        self.generator = generator
        if isinstance(work, (list, tuple)):
            self[:] = list(work)
            self.was_list = True
            self.wait_any = False
        else:
            if isinstance(work, WaitAny):
                self[:] = list(work.items)
                self.was_list = True
                self.wait_any = True
            else:
                self[:] = [
                 work]
                self.was_list = False
                self.wait_any = False
            for item in self:
                assert isinstance(item, WorkItem)
                item.parent = workflow

    @property
    def outstanding(self):
        """Returns whether or not this barrier has pending work."""
        done_count = 0
        for item in self:
            if not self.wait_any and item.fire_and_forget:
                done_count += 1
            elif item.done:
                done_count += 1

        if self.wait_any and done_count > 0:
            return False
        if done_count == len(self):
            return False
        return True

    @property
    def error(self):
        """Returns the error for this barrier and all work items, if any."""
        for item in self:
            if isinstance(item, WorkItem) and item.error:
                return item.error

        return

    def get_item(self):
        """Returns the item to send back into the workflow generator."""
        if self.was_list:
            blocking_items = self[:]
            self[:] = []
            for item in blocking_items:
                if isinstance(item, WorkflowItem) and item.done and not item.error:
                    self.append(item.result)
                else:
                    self.append(item)

            return self
        return self[0]


class Return(Exception):
    """Raised in WorkflowItem.run to return a result to the caller."""

    def __init__(self, result=None):
        """Initializer.

        Args:
            result: Result of a WorkflowItem, if any.
        """
        self.result = result


class WorkflowThread(WorkerThread):
    """Worker thread for running workflows."""

    def __init__(self, input_queue, output_queue):
        """Initializer.

        Args:
            input_queue: Queue this worker consumes work from. These should be
                WorkflowItems to process, or any WorkItems registered with this
                class using the register() method.
            output_queue: Queue where this worker puts finished work items,
                if any.
        """
        WorkerThread.__init__(self, input_queue, output_queue)
        self.pending = {}
        self.work_map = {}
        self.worker_threads = []
        self.register(WorkflowItem, input_queue)

    def start(self):
        """Starts the coordinator thread and all related worker threads."""
        assert not self.interrupted
        for thread in self.worker_threads:
            thread.start()

        WorkerThread.start(self)

    def stop(self):
        """Stops the coordinator thread and all related threads."""
        if self.interrupted:
            return
        for thread in self.worker_threads:
            thread.interrupted = True

        self.interrupted = True

    def join(self):
        """Joins the coordinator thread and all worker threads."""
        for thread in self.worker_threads:
            thread.join()

        WorkerThread.join(self)

    def wait_one(self):
        """Waits until this worker has finished one work item or died."""
        while True:
            try:
                item = self.output_queue.get(True, 1)
            except Queue.Empty:
                continue
            except KeyboardInterrupt:
                logging.debug('Exiting')
                return
            else:
                item.check_result()
                return

    def register(self, work_type, queue):
        """Registers where work for a specific type can be executed.

        Args:
            work_type: Sub-class of WorkItem to register.
            queue: Queue instance where WorkItems of the work_type should be
                enqueued when they are yielded by WorkflowItems being run by
                this worker.
        """
        self.work_map[work_type] = queue

    def enqueue_barrier(self, barrier):
        for item in barrier:
            if item.done:
                continue
            next_types = [
             type(item)]
            while next_types:
                try_types = next_types[:]
                next_types[:] = []
                for current_type in try_types:
                    target_queue = self.work_map.get(current_type)
                    if target_queue:
                        next_types = []
                        break
                    next_types.extend(current_type.__bases__)

            if not target_queue:
                raise AssertionError('Could not find queue to handle %r' % item)
                self.pending[item] = item.fire_and_forget or barrier
            target_queue.put(item)

    def dequeue_barrier(self, item):
        barrier = self.pending.pop(item, None)
        if not barrier:
            return
        else:
            if barrier.outstanding and not barrier.error:
                return
            for work in barrier:
                self.pending.pop(work, None)

            return barrier

    def handle_item(self, item):
        if isinstance(item, WorkflowItem) and not item.done:
            workflow = item
            try:
                generator = item.run(*item.args, **item.kwargs)
            except TypeError as e:
                raise TypeError('Bad workflow function item=%r error=%s' % (
                 item, str(e)))

            item = None
        else:
            barrier = self.dequeue_barrier(item)
            if not barrier:
                logging.debug('Could not find barrier for finished item=%r', item)
                return
            item = barrier.get_item()
            workflow = barrier.workflow
            generator = barrier.generator
        while True:
            try:
                try:
                    error = item is not None and item.error
                    if error:
                        logging.debug('Throwing workflow=%r error=%r', workflow, error)
                        next_item = generator.throw(*error)
                    elif isinstance(item, WorkflowItem) and item.done:
                        logging.debug('Sending workflow=%r finished item=%r', workflow, item)
                        next_item = generator.send(item.result)
                    else:
                        logging.debug('Sending workflow=%r finished item=%r', workflow, item)
                        next_item = generator.send(item)
                except StopIteration:
                    logging.debug('Exhausted workflow=%r', workflow)
                    workflow.done = True
                except Return as e:
                    logging.debug('Return from workflow=%r result=%r', workflow, e.result)
                    workflow.done = True
                    workflow.result = e.result
                except Exception as e:
                    logging.exception('Error in workflow=%r from item=%r, error=%r', workflow, item, error)
                    workflow.done = True
                    workflow.error = sys.exc_info()

            finally:
                if workflow.done:
                    if workflow.root:
                        return workflow
                    else:
                        self.input_queue.put(workflow)
                        return

            barrier = Barrier(workflow, generator, next_item)
            self.enqueue_barrier(barrier)
            if barrier.outstanding:
                break
            item = barrier.get_item()

        return


class PrintWorkflow(WorkflowItem):
    """Prints a message to stdout."""

    def run(self, message):
        yield []
        print message


def get_coordinator():
    """Creates a coordinator and returns it."""
    workflow_queue = Queue.Queue()
    complete_queue = Queue.Queue()
    coordinator = WorkflowThread(workflow_queue, complete_queue)
    coordinator.register(WorkflowItem, workflow_queue)
    return coordinator