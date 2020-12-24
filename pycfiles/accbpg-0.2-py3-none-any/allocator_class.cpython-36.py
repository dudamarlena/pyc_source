# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\accasim\base\allocator_class.py
# Compiled at: 2018-07-09 17:24:41
# Size of source mod 2**32: 20946 bytes
__doc__ = '\nMIT License\n\nCopyright (c) 2017 cgalleguillosm, AlessioNetti\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n'
import logging
from random import seed
from sys import maxsize
from sortedcontainers import SortedList
from abc import abstractmethod, ABC
from accasim.base.resource_manager_class import ResourceManager

class AllocatorBase(ABC):
    """AllocatorBase"""
    MAXSIZE = maxsize

    def __init__(self, _seed, **kwargs):
        """
    
        Allocator constructor (based on scheduler)

        :param seed: Seed if there is any random event
        :param res_man: resource manager for the system.
        :param kwargs: Nothing for the moment
                 
        """
        seed(_seed)
        self.avl_resources = None
        self.node_names = None
        self.resource_manager = None
        self._logger = logging.getLogger('accasim')
        self.nec_res_types = [
         'core', 'mem']

    @abstractmethod
    def get_id(self):
        """
    
        Abstract method. Must be implemented by the subclass. 
        Must return the identification of the allocator. 
        
        :return: Allocator identification (for instance its name).    
    
        """
        raise NotImplementedError

    @abstractmethod
    def set_resources(self, res):
        """
    
        Abstract method. Must be implemented by the subclass.
        This method sets the internal reference to the dictionary of available resources in the system.
        If the reference points to a list used also outside of this class, the object should be deepcopied.
        
        If necessary, the resources are also sorted.
            
        :param res: the list of currently available resources in the system.       
    
        """
        raise NotImplementedError

    def get_resources(self):
        """
            Returns the internal reference to the dictionary of available resources in the system. 
            It includes the last virtual allocations.
        """
        return self.avl_resources

    @abstractmethod
    def set_attr(self, **kwargs):
        """
    
        Abstract method. Must be implemented by the subclass.
        Method used to set internal parameters and meta-data for the allocator.
        
        Its behavior depends on the specific allocator that is being used, and some arguments may be discarded.
        
        :param kwargs: the internal parameters to be set, depending on the allocator
    
        """
        raise NotImplementedError

    @abstractmethod
    def allocating_method(self, es, cur_time, skip=False, reserved_time=None, reserved_nodes=None):
        """
    
        Abstract method. Must be implemented by the subclass.
        This method must try to allocate the scheduled events contained in es. It will stop as soon as an event cannot
        be allocated, to avoid violations of the scheduler's priority rules, or proceed with other events depending
        on the skip parameter.
        
        The method must support both list of events for es, in which case it will return a list, or single events.
        If there is at least one successful allocation, avl_resources is updated and sorted again efficiently.

        :param es: the event(s) to be allocated
        :param cur_time: current time, needed to build the schedule list
        :param skip: determines if the allocator can skip jobs
        :param reserved_time: beginning of the next reservation slot (used for backfilling)
        :param reserved_nodes: nodes already reserved (used for backfilling)

        :return: a list of assigned nodes of length e.requested_nodes, for all events that could be allocated. The list is in the format (time,event,nodes) where time can be either cur_time or None.
        
        """
        raise NotImplementedError

    def allocate(self, es, cur_time, skip=False, reserved_time=None, reserved_nodes=None):
        """
    
        This is the method that is called by the Scheduler to allocate the scheduled jobs. First, It verifies the data consistency and availability, 
        and then call to the implemented allocation policy.   
        
        
        :param es: the event(s) to be allocated
        :param cur_time: current time, needed to build the schedule list
        :param skip: determines if the allocator can skip jobs
        :param reserved_time: beginning of the next reservation slot (used for backfilling)
        :param reserved_nodes: nodes already reserved (used for backfilling)
        :param debug: Debugging flag
        
        :return: the return of the implemented allocation policy.

        """
        assert self.resource_manager is not None, 'The resource manager is not defined. It must defined prior to run the simulation.'
        self._logger.debug('{}: {} queued jobs to be considered in the dispatching plan'.format(cur_time, len(es) if isinstance(es, (list, tuple, SortedList)) else 1))
        self.set_resources(self.resource_manager.current_availability)
        dispatching_decision = self.allocating_method(es, cur_time, skip=skip, reserved_time=reserved_time, reserved_nodes=reserved_nodes)
        return dispatching_decision

    def set_resource_manager(self, _resource_manager):
        """
        Internally set the resource manager to deal with resource availability.
        
        :param _resource_manager: A resource manager instance or None. If a resource manager is already instantiated,
             it's used for set internally set it and obtain the system capacity for dealing with the request verifications.
             The dispathing process can't start without a resource manager. 
             
        """
        assert isinstance(_resource_manager, ResourceManager), 'Resource Manager not valid for scheduler'
        self.resource_manager = _resource_manager
        self._define_mappers()

    def _define_mappers(self):
        if not self.node_names:
            self.node_names = self.resource_manager.node_names

    def __str__(self):
        """
        
            Retrieves the identification of the allocator.
        
        """
        return self.get_id()


class FirstFit(AllocatorBase):
    """FirstFit"""
    name = 'FF'

    def __init__(self, seed=0, **kwargs):
        """
    
        Constructor for the class.
        
        :param seed: seed for random events (not used)
        :param resource_manager: reference to the system resource manager
        :param kwargs: None at the moment
    
        """
        (AllocatorBase.__init__)(self, seed, **kwargs)
        self.sorted_keys = None

    def get_id(self):
        return self.__class__.__name__

    def set_resources(self, res):
        """
    
        Sets in the internal variable avl_resources the current available resources for the system. It also sorts
        them, if the sort_resources method is implemented.
        
        :param res: the list of currently available resources for the system
    
        """
        self.avl_resources = res
        self._adjust_resources()

    def set_attr(self, **kwargs):
        """
    
        Method used to set internal parameters and meta-data for the allocator.

        Its behavior depends on the specific allocator that is being used, and some arguments may be discarded.
        It is not actively used in this simple allocator (for the moment).

        :param kwargs: None for the moment
    
        """
        pass

    def allocating_method(self, es, cur_time, skip=False, reserved_time=None, reserved_nodes=None):
        """
    
        Given a job list es, this method searches for a suitable allocation for as many jobs as possible.
        
        In normal allocation, the method stops as soon as an event in the list cannot be allocated. In this case,
        ths list of already allocated jobs is returned. This is done to be coherent with the scheduler's rules.
        As an alternative, the skip parameter can be supplied to allow the scheduler to skip unallocated jobs.
        This method also support backfilling schedule. In this case, the backfilling parameters are supplied,
        and the allocator tries to fit jobs without delaying the reserved job. In this second case,
        the method does not stop when a job cannot be allocated, but simply skips it.
        
        es can be a list or a single event object. The return type (list or single tuple) changes accordingly.
        
        :param es: the event(s) to be allocated
        :param cur_time: current time, needed to build the schedule list
        :param skip: determines if the allocator can skip jobs
        :param reserved_time: beginning of the next reservation slot (used for backfilling)
        :param reserved_nodes: nodes already reserved (used for backfilling)

        :return: a list of assigned nodes of length e.requested_nodes, for all events that could be allocated. The list is in the format (time,event,nodes) where time can be either cur_time or None.
    
        """
        if not isinstance(es, (list, tuple, SortedList)):
            listAsInput = False
            es = [es]
        else:
            listAsInput = True
        allocation = []
        success_counter = 0
        for e in es:
            requested_nodes = e.requested_nodes
            requested_resources = e.requested_resources
            nodes_to_discard = self._compute_reservation_overlaps(e, cur_time, reserved_time, reserved_nodes)
            backfilling_overlap = False if len(nodes_to_discard) == 0 else True
            assigned_nodes = []
            nodes_left = requested_nodes
            for node in self.sorted_keys:
                if backfilling_overlap:
                    pass
                else:
                    resources = self.avl_resources[node]
                    fits = self._event_fits_node(resources, requested_resources)
                    if fits == 0:
                        pass
                    else:
                        if nodes_left <= fits:
                            assigned_nodes += [node] * nodes_left
                            nodes_left = 0
                        else:
                            assigned_nodes += [node] * fits
                            nodes_left -= fits
                        if nodes_left == 0:
                            break

            if nodes_left > 0:
                assigned_nodes = []
            assert len(assigned_nodes) in (0, requested_nodes), 'Requested' + str(requested_nodes) + ' got ' + str(len(assigned_nodes))
            if assigned_nodes:
                allocation.append((cur_time, e.id, assigned_nodes))
                self._update_resources(assigned_nodes, requested_resources)
                self._adjust_resources(assigned_nodes)
                success_counter += 1
                self._logger.trace('Allocation successful for event {}'.format(e.id))
            else:
                self._logger.trace('Allocation failed for event {} with {} nodes left'.format(e.id, nodes_left))
                allocation.append((None, e.id, []))
                if not skip:
                    for e in es[success_counter + 1:]:
                        allocation.append((None, e.id, []))

                    self._logger.trace('Cannot skip jobs, {} additional pending allocations failed {}'.format(len(es) - success_counter - 1, es[success_counter:]))
                    self._logger.trace('')
                    break

        self._logger.trace('{}/{} successful allocations of events'.format(success_counter, len(es)))
        if listAsInput:
            return allocation
        else:
            return allocation[0]

    def _compute_reservation_overlaps(self, e, cur_time, reserved_time, reserved_nodes):
        """
    
        This method considers an event e, the current time, and a list of reservation start times with relative
        reserved nodes, and returns the list of reserved nodes that cannot be accessed by event e because of overlap.
        
        :param e: the event to be allocated
        :param cur_time: the current time
        :param reserved_time: the list (or single element) of reservation times
        :param reserved_nodes: the list of lists (or single list) of reserved nodes for each reservation
        
        :return: the list of nodes that cannot be used by event e
    
        """
        if reserved_time is None or reserved_nodes is None:
            return []
        else:
            if not isinstance(reserved_time, (list, tuple)):
                if cur_time + e.expected_duration > reserved_time:
                    return reserved_nodes
                else:
                    return []
            else:
                overlap_list = []
                for ind, evtime in enumerate(reserved_time):
                    if cur_time + e.expected_duration > evtime:
                        overlap_list += reserved_nodes[ind]

            return list(set(overlap_list))

    def _update_resources(self, reserved_nodes, requested_resources):
        """
    
        Updates the internal avl_resources list after a successful allocation.
        
        :param reserved_nodes: the list of nodes assigned to the allocated job
        :param requested_resources: the list of resources requested by the job per each node
    
        """
        for node in reserved_nodes:
            resource = self.avl_resources[node]
            for attr, v in requested_resources.items():
                if v == 0:
                    pass
                else:
                    cur_q = resource[attr]
                    assert cur_q - v >= 0, 'In node {}, the resource {} is going below to 0'.format(node, attr)
                    resource[attr] -= v

    def _adjust_resources(self, nodes=None):
        """

        Method which must sort the node list at the beginning and after a successful allocation. 
        It must sort the self.sorted_keys attribute.

        """
        if not nodes:
            self.sorted_keys = []
            for node in self.node_names:
                add = True
                for res, avl in self.avl_resources[node].items():
                    if res in self.nec_res_types:
                        if avl == 0:
                            add = False
                            break

                if add:
                    self.sorted_keys.append(node)

        else:
            to_remove = set()
            for node in nodes:
                for res, avl in self.avl_resources[node].items():
                    if res in self.nec_res_types:
                        if avl == 0:
                            to_remove.add(node)
                            break

            for node in to_remove:
                self.sorted_keys.remove(node)

    def _event_fits_node(self, resources, requested_resources):
        _fits = self.MAXSIZE
        for res_type, req in requested_resources.items():
            if req == 0:
                pass
            else:
                fit = resources[res_type] // req
                if fit == 0:
                    return 0
                if _fits > fit:
                    _fits = fit

        return _fits


class BestFit(FirstFit):
    """BestFit"""
    name = 'BF'

    def __init__(self, seed=0, **kwargs):
        """
        
        Constructor for the class.

        :param seed: seed for random events (not used)
        :param resource_manager: reference to the system resource manager
        :param kwargs: None at the moment
        
        """
        FirstFit.__init__(self, seed)
        self.ranking = lambda x: sum(self.avl_resources[x].values())

    def _adjust_resources(self, nodes=None):
        """

        Method which must sort the node list at the beginning and after a successful allocation. 
        It must sort the self.sorted_keys attribute.

        """
        if not nodes:
            self.sorted_keys = []
            for node in self.node_names:
                add = True
                for res, avl in self.avl_resources[node].items():
                    if res in self.nec_res_types:
                        if avl == 0:
                            add = False
                            break

                if add:
                    self.sorted_keys.append(node)

        else:
            to_remove = set()
            for node in nodes:
                for res, avl in self.avl_resources[node].items():
                    if res in self.nec_res_types:
                        if avl == 0:
                            to_remove.add(node)
                            break

            for node in to_remove:
                self.sorted_keys.remove(node)

        self.sorted_keys.sort(key=(self.ranking), reverse=False)