# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\accasim\base\scheduler_class.py
# Compiled at: 2018-12-20 08:04:39
# Size of source mod 2**32: 26009 bytes
"""
MIT License

Copyright (c) 2017 cgalleguillosm, AlessioNetti

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import logging
from sys import maxsize
from random import seed
from abc import abstractmethod, ABC
from sortedcontainers.sortedlist import SortedListWithKey
from enum import Enum
from copy import deepcopy
from accasim.base.resource_manager_class import ResourceManager
from accasim.base.allocator_class import AllocatorBase

class DispatcherError(Exception):
    pass


class JobVerification(Enum):
    REJECT = -1
    NO_CHECK = 0
    CHECK_TOTAL = 1
    CHECK_REQUEST = 2


class SchedulerBase(ABC):
    __doc__ = '\n    \n        This class allows to implement dispatching methods by integrating with an implementation of this class an allocator (:class:`accasim.base.allocator_class.AllocatorBase`). \n        An implementation of this class could also serve as a entire dispatching method if the allocation class is not used as default (:class:`.allocator` = None), but the resource manager must\n        be set on the allocator using :func:`accasim.base.allocator_class.AllocatorBase.set_resource_manager`.\n        \n    '
    MAXSIZE = maxsize
    ALLOW_MAPPING_SAME_NODE = True

    def __init__(self, _seed, allocator=None, job_check=JobVerification.CHECK_REQUEST, **kwargs):
        """
        
        Construct a scheduler
            
        :param seed: Seed for the random state
        :param resource_manager: A Resource Manager object for dealing with system resources.
        :param allocator: Allocator object to be used by the scheduler to allocater after schedule generation. If an allocator isn't defined, the scheduler class must generate the entire dispatching plan.
        :param job_check: A job may be rejected if it doesnt comply with:
                    - JobVerification.REJECT: Any job is rejected
                    - JobVerification.NO_CHECK: All jobs are accepted
                    - JobVerification.CHECK_TOTAL: If the job requires more resources than the available in the system.
                    - JobVerification.CHECK_REQUEST: if an individual request by node requests more resources than the available one.
                    
                    
        :param kwargs:
            - skip_jobs_on_allocation: If the allocator is predefined and this parameter is true, the allocator will try to allocate jobs as much as possible. 
                Otherwise, the allocation will stop after the first fail.
                
        """
        seed(_seed)
        self._counter = 0
        self.allocator = None
        self._logger = logging.getLogger('accasim')
        self._system_capacity = None
        self._nodes_capacity = None
        self.resource_manager = None
        if allocator:
            assert isinstance(allocator, AllocatorBase), 'Allocator not valid for scheduler'
            self.allocator = allocator
        elif not isinstance(job_check, JobVerification):
            raise AssertionError('job_check invalid type. {}'.format(job_check.__class__))
        if job_check == JobVerification.REJECT:
            print('All jobs will be rejected, and for performance purposes the rejection messages will be omitted.')
        self._job_check = job_check
        self._min_required_availability = kwargs.pop('min_resources', None)
        self.skip_jobs_on_allocation = kwargs.pop('skip_jobs_on_allocation', False)

    @property
    def name(self):
        """
        
        Name of the schedulign method
        
        """
        raise NotImplementedError

    @abstractmethod
    def get_id(self):
        """
        
        Must return the full ID of the scheduler, including policy and allocator.
        
        :return: the scheduler's id.
        
        """
        raise NotImplementedError

    @abstractmethod
    def scheduling_method(self, cur_time, es_dict, es):
        """
        
        This function must map the queued events to available nodes at the current time.
            
        :param cur_time: current time
        :param es_dict: dictionary with full data of the job events
        :param es: events to be scheduled
            
        :return a tuple of (time to schedule, event id, list of assigned nodes), an array jobs id of rejected jobs  
        
        """
        raise Exception('This function must be implemented!!')

    def set_resource_manager(self, resource_manager):
        """
        
        Set a resource manager. 

        :param resource_manager: An instantiation of a resource_manager class or None 
        
        """
        if resource_manager:
            if self.allocator:
                self.allocator.set_resource_manager(resource_manager)
            elif not isinstance(resource_manager, ResourceManager):
                raise AssertionError('Resource Manager not valid for scheduler')
            self.resource_manager = resource_manager
        else:
            self.resource_manager = None

    def schedule(self, cur_time, es_dict, es):
        """
        
        Method for schedule. It calls the specific scheduling method.
        
        :param cur_time: current time
        :param es_dict: dictionary with full data of the events
        :param es: events to be scheduled
        
        :return: a tuple of (time to schedule, event id, list of assigned nodes), array of rejected job ids.
        
        """
        assert self.resource_manager is not None, 'The resource manager is not defined. It must defined prior to run the simulation.'
        self._counter += 1
        self._logger.debug('{} Dispatching: #{} decision'.format(cur_time, self._counter))
        self._logger.debug('{} Dispatching: {} queued jobs'.format(cur_time, len(es)))
        self._logger.debug('{} Dispatching: {}'.format(cur_time, self.resource_manager.current_usage))
        rejected = []
        if self._min_required_availability and any([self.resource_manager.resources.full[res] for res in self._min_required_availability]):
            self._logger.debug('There is no availability of one of the min required resource to run a job. The dispatching process will be delayed until there is enough resources.')
            return (
             [(None, e, []) for e in es], rejected)
        else:
            accepted = []
            for e in es:
                job = es_dict[e]
                if not job.get_checked() and not self._check_job_request(job):
                    if self._job_check != JobVerification.REJECT:
                        self._logger.warning('{} has been rejected by the dispatcher. ({})'.format(e, self._job_check))
                    rejected.append(e)
                else:
                    accepted.append(job)

            to_allocate = []
            if accepted:
                to_allocate, to_reject = self.scheduling_method(cur_time, accepted, es_dict)
                rejected += to_reject
                for e in to_reject:
                    self._logger.warning('{} has been rejected by the dispatcher. (Scheduling policy)'.format(e))

            elif to_allocate and self.allocator:
                dispatching_plan = self.allocator.allocate(to_allocate, cur_time, skip=(self.skip_jobs_on_allocation))
            else:
                dispatching_plan = to_allocate
            return (dispatching_plan, rejected)

    def _check_job_request(self, _job):
        """

        Simple method that checks if the loaded _job violates the system's resource constraints.

        :param _job: Job object

        :return: True if the _job is valid, false otherwise

        """
        _job.set_checked(True)
        if self._job_check == JobVerification.REJECT:
            return False
        if self._job_check == JobVerification.NO_CHECK:
            return True
        if self._job_check == JobVerification.CHECK_TOTAL:
            if not self._system_capacity:
                self._system_capacity = self.resource_manager.system_capacity('total')
            return not any([_job.requested_resources[res] * _job.requested_nodes > self._system_capacity[res] for res in _job.requested_resources.keys()])
        if self._job_check == JobVerification.CHECK_REQUEST:
            if not self._nodes_capacity:
                self._nodes_capacity = self.resource_manager.system_capacity('nodes')
            _requested_resources = _job.requested_resources
            _requested_nodes = _job.requested_nodes
            _fits = 0
            _diff_node = 0
            for _node, _attrs in self._nodes_capacity.items():
                _nfits = min([_attrs[_attr] // req for _attr, req in _requested_resources.items() if req > 0])
                if _nfits > 0:
                    _fits += _nfits
                    _diff_node += 1
                if self.ALLOW_MAPPING_SAME_NODE:
                    if _fits >= _requested_nodes:
                        return True
                else:
                    if _diff_node >= _requested_nodes:
                        return True

            return False
        raise DispatcherError('Invalid option.')

    def __str__(self):
        return self.get_id()


class SimpleHeuristic(SchedulerBase):
    __doc__ = '\n    \n    Simple scheduler, sorts the event depending on the chosen policy.\n    \n    If a single job allocation fails, all subsequent jobs fail too.\n    Sorting as name, sort funct parameters\n    \n    '

    def __init__(self, seed, allocator, name, sorting_parameters, **kwargs):
        (SchedulerBase.__init__)(self, seed, allocator, **kwargs)
        self.name = name
        self.sorting_parameters = sorting_parameters

    def get_id(self):
        """
        
        Returns the full ID of the scheduler, including policy and allocator.

        :return: the scheduler's id.
        
        """
        return '-'.join([self.__class__.__name__, self.name, self.allocator.get_id()])

    def scheduling_method(self, cur_time, jobs, es_dict):
        """
        
        This function must map the queued events to available nodes at the current time.
        
        :param cur_time: current time
        :param es_dict: dictionary with full data of the events
        :param es: events to be scheduled
        
        :return: a tuple of (time to schedule, event id, list of assigned nodes), an array jobs id of rejected jobs  
        
        """
        to_reject = []
        to_schedule = SortedListWithKey(jobs, **self.sorting_parameters)
        return (to_schedule, to_reject)


class FirstInFirstOut(SimpleHeuristic):
    __doc__ = '\n\n    **FirstInFirstOut scheduling policy.** \n    \n    The first come, first served (commonly called FirstInFirstOut ‒ first in, first out) \n    process scheduling algorithm is the simplest process scheduling algorithm. \n        \n    '
    name = 'FIFO'
    sorting_arguments = {'key': lambda x: x.queued_time}

    def __init__(self, _allocator, _seed=0, **kwargs):
        """
        
        FirstInFirstOut Constructor
        
        """
        (SimpleHeuristic.__init__)(self, _seed, _allocator, (self.name), (self.sorting_arguments), **kwargs)


class LongestJobFirst(SimpleHeuristic):
    __doc__ = '\n    \n    **LJF scheduling policy.**\n    \n    Longest Job First (LJF) sorts the jobs, where the longest jobs are preferred over the shortest ones.  \n        \n    '
    name = 'LJF'
    sorting_arguments = {'key': lambda x: -x.expected_duration}

    def __init__(self, _allocator, _resource_manager=None, _seed=0, **kwargs):
        """
        
        LJF Constructor
        
        """
        (SimpleHeuristic.__init__)(self, _seed, _allocator, (self.name), (self.sorting_arguments), **kwargs)


class ShortestJobFirst(SimpleHeuristic):
    __doc__ = '\n    \n    **SJF scheduling policy.**\n    \n    Shortest Job First (SJF) sorts the jobs, where the shortest jobs are preferred over the longest ones.\n    \n    '
    name = 'SJF'
    sorting_arguments = {'key': lambda x: x.expected_duration}

    def __init__(self, _allocator, _resource_manager=None, _seed=0, **kwargs):
        """
    
        SJF Constructor
    
        """
        (SimpleHeuristic.__init__)(self, _seed, _allocator, (self.name), (self.sorting_arguments), **kwargs)


class EASYBackfilling(SchedulerBase):
    __doc__ = "\n   \n   EASY Backfilling scheduler.\n   \n   Whenever a job cannot be allocated, a reservation is made for it. After this, the following jobs are used to\n   backfill the schedule, not allowing them to use the reserved nodes.\n     \n   This dispatching methods includes its own calls to the allocator over the dispatching process.\n   Then it isn't use the auto allocator call, after the schedule generation.    \n   \n   "
    name = 'EBF'

    def __init__(self, allocator, seed=0, **kwargs):
        """
   
       Easy BackFilling Constructor
      
       """
        (SchedulerBase.__init__)(self, seed, allocator=None, **kwargs)
        self._blocked_job_id = None
        self._reserved_slot = (None, [])
        self.nonauto_allocator = allocator
        self.allocator_rm_set = False

    def get_id(self):
        """
   
       Returns the full ID of the scheduler, including policy and allocator.
       :return: the scheduler's id.
   
       """
        return '-'.join([self.name, self.nonauto_allocator.name])

    def scheduling_method(self, cur_time, queued_jobs, es_dict):
        """
        This function must map the queued events to available nodes at the current time.
       
        :param cur_time: current time
        :param queued_jobs: Jobs to be dispatched
        :param es_dict: dictionary with full data of the events
        
        
        :return: a list of tuples (time to schedule, event id, list of assigned nodes), and a list of rejected job ids  
        """
        if not self.allocator_rm_set:
            self.nonauto_allocator.set_resource_manager(self.resource_manager)
            self.allocator_rm_set = True
        else:
            avl_resources = self.resource_manager.current_availability
            self.nonauto_allocator.set_resources(avl_resources)
            to_dispatch = []
            to_reject = []
            _to_fill = []
            _prev_blocked = None
            _time_reached = False
            if self._reserved_slot[0]:
                if self._reserved_slot[0] <= cur_time:
                    _time_reached = True
                    self._logger.trace('There is a blocked job {} with {}'.format(self._blocked_job_id, self._reserved_slot))
                    blocked_job = queued_jobs[0]
                    queued_jobs = queued_jobs[1:]
                    allocation = self.nonauto_allocator.allocating_method(blocked_job, cur_time, skip=False)
                    if allocation[(-1)]:
                        self._logger.trace('{}: {} blocked job can be allocated. Unblocking'.format(cur_time, self._blocked_job_id))
                        self._blocked_job_id = None
                        self._reserved_slot = (None, [])
                        _prev_blocked = [allocation]
                    else:
                        self._logger.trace('{} job is still blocked. Reservation {}'.format(self._blocked_job_id, self._reserved_slot))
                    to_dispatch += [allocation]
            if self._blocked_job_id is None:
                if queued_jobs:
                    _allocated_jobs, blocked_idx = self._try_fifo_allocation(queued_jobs, cur_time)
                    if blocked_idx is not None:
                        if not self._reserved_slot[0]:
                            blocked_job = queued_jobs[blocked_idx]
                            self._logger.trace('Blocked {} Job: Calculate the reservation'.format(self._blocked_job_id))
                            self._reserved_slot = self._calculate_slot(cur_time, deepcopy(avl_resources), _allocated_jobs[:blocked_idx], _prev_blocked, blocked_job, es_dict)
                            self._logger.trace('Blocked {} Job: Nodes {} are reserved at {}'.format(self._blocked_job_id, self._reserved_slot[1], self._reserved_slot[0]))
                        to_dispatch += _allocated_jobs[:blocked_idx + 1]
                        _to_fill = queued_jobs[blocked_idx + 1:]
                    else:
                        to_dispatch += _allocated_jobs
                else:
                    _time_reached or to_dispatch += [(None, self._blocked_job_id, [])]
                    _to_fill = queued_jobs[1:]
            else:
                _to_fill = queued_jobs
            if _to_fill:
                self._logger.trace('Blocked job {}. {} jobs candidates to fill the gap'.format(self._blocked_job_id, len(_to_fill)))
                reserved_time, reserved_nodes = self._reserved_slot
                filling_allocation = self.nonauto_allocator.allocating_method(_to_fill, cur_time, reserved_time=reserved_time,
                  reserved_nodes=[],
                  skip=True)
                to_dispatch += filling_allocation
        return (
         to_dispatch, to_reject)

    def _try_fifo_allocation(self, queued_jobs, cur_time):
        """
         Allocates as many jobs as possible using the FIFO approach. As soon as one allocation fails, all subsequent jobs fail too. 
         Then, the return tuple contains info about the allocated jobs (assigned nodes and such) and also the position of the blocked job.
        
         :param queued_jobs: List of job objects
         :param cur_time: current time
         
         :return job allocation, and position of the blocked job in the list
         
        """
        _allocated_jobs = self.nonauto_allocator.allocating_method(queued_jobs, cur_time, skip=False)
        blocked_idx = None
        for i, (_, job_id, allocated_nodes) in enumerate(_allocated_jobs):
            if not allocated_nodes:
                self._blocked_job_id = job_id
                blocked_idx = i
                break

        return (
         _allocated_jobs, blocked_idx)

    def _calculate_slot(self, cur_time, avl_resources, decided_allocations, prev_blocked, blocked_job, es_dict):
        """
           Computes a reservation for the blocked job, by releasing incrementally the resources used by the running
           events and recently allocated jobs. The earliest slot in which blocked_job fits is chosen.
       
        :param avl_resources: Actual available resources
        :param decided_allocations: Allocated jobs on the current iteration.
        :param prev_blocked: Allocation corresponding to the previous blocked job which has been unblocked during this iteration
        :param blocked_jobs: Event to be fitted in the time slot
        :param es_dist: Job dictionary
       
        :return: a tuple of time of the slot and nodes
        """
        current_allocations = self.resource_manager.current_allocations
        future_endings = SortedListWithKey(key=(lambda x: x[1]))
        for job_id, resources in current_allocations.items():
            future_endings.add((job_id, es_dict[job_id].start_time + es_dict[job_id].expected_duration, resources))

        if prev_blocked:
            decided_allocations += prev_blocked
        for _, job_id, nodes in decided_allocations:
            _dec_alloc = {}
            for node in nodes:
                if node not in _dec_alloc:
                    _dec_alloc[node] = {k:v for k, v in es_dict[job_id].requested_resources.items()}
                else:
                    for res, v in es_dict[job_id].requested_resources.items():
                        _dec_alloc[node][res] += v

            future_endings.add((job_id, cur_time + es_dict[job_id].expected_duration, _dec_alloc))

        _required_alloc = blocked_job.requested_nodes
        _requested_resources = blocked_job.requested_resources
        _partial_alloc = {}
        for node, resources in avl_resources.items():
            new_alloc = min([resources[req] // _requested_resources[req] for req in _requested_resources])
            if new_alloc > 0:
                _partial_alloc[node] = new_alloc

        for job_id, res_time, used_nodes in future_endings:
            for node, used_resources in used_nodes.items():
                if node not in avl_resources:
                    avl_resources[node] = {r:0 for r in _requested_resources}
                for r, v in used_resources.items():
                    avl_resources[node][r] += v

                cur_alloc = _partial_alloc.get(node, 0)
                new_alloc = min([avl_resources[node][req] // _requested_resources[req] for req in _requested_resources])
                _diff = new_alloc - cur_alloc
                if _diff > 0:
                    _partial_alloc[node] = _partial_alloc.get(node, 0) + _diff

            if sum(_partial_alloc.values()) >= _required_alloc:
                ctimes = 0
                nodes = []
                for node, times in _partial_alloc.items():
                    ctimes += times
                    nodes.append(node)
                    if ctimes >= _required_alloc:
                        break

                return (
                 res_time, nodes)

        raise DispatcherError("Can't find the slot.... no end? :(")