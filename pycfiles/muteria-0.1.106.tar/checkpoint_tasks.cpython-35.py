# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mfi/mytools/muteria/muteria/controller/checkpoint_tasks.py
# Compiled at: 2019-12-05 12:33:57
# Size of source mod 2**32: 18483 bytes
""" This Module implement the data structore and format for the 
    Checkpointing of the main controller during the execution phase

    The importants classes or elements are:
    - `Tasks` enum: enum that defines the differents tasks that are 
                    checkpointed during the controller execution.    
    - `Status` enum: enum defining the different states that a task can 
                    have (untouched, executing or done)
    - `TaskOrderingDependency` class: That defines the dependency between
                    the different tasks as well as their status.
                    The state changes as well as the task to run next are 
                    also implemented in the class.
"""
from __future__ import print_function
import logging, collections, networkx, muteria.common.mix as common_mix
ERROR_HANDLER = common_mix.ErrorHandler

class Tasks(common_mix.EnumAutoName):
    STARTING = 0
    TESTS_GENERATION_GUIDANCE = 1
    TESTS_GENERATION = 2
    TESTS_GENERATION_USING_CRITERIA = 3
    TESTS_EXECUTION_SELECTION_PRIORITIZATION = 4
    PASS_FAIL_TESTS_EXECUTION = 5
    CRITERIA_GENERATION_GUIDANCE = 6
    CRITERIA_GENERATION = 7
    CRITERIA_EXECUTION_SELECTION_PRIORITIZATION = 8
    CRITERIA_TESTS_EXECUTION = 9
    PASS_FAIL_STATS = 10
    CRITERIA_STATS = 11
    AGGREGATED_STATS = 12
    FINISHED = 13


class Status(common_mix.EnumAutoName):
    UNTOUCHED = -1
    EXECUTING = 0
    DONE = 1


class TaskOrderingDependency(object):
    __doc__ = '\n    The task dependency structure is following(The structure neve change):\n    ----------------------------------------------------------------------\n        TESTS_GENERATION_GUIDANCE --> STARTING\n        CRITERIA_GENERATION_GUIDANCE --> STARTING\n\n        TESTS_GENERATION --> TESTS_GENERATION_GUIDANCE\n\n                                            | TESTS_GENERATION_GUIDANCE\n        TESTS_GENERATION_USING_CRITERIA --> | CRITERIA_GENERATION \n\n                                                     | TESTS_GENERATION_USING_CRITERIA \n        TESTS_EXECUTION_SELECTION_PRIORITIZATION --> | TESTS_GENERATION\n\n        PASS_FAIL_TESTS_EXECUTION --> TESTS_EXECUTION_SELECTION_PRIORITIZATION\n\n        CRITERIA_GENERATION --> CRITERIA_GENERATION_GUIDANCE\n\n        CRITERIA_EXECUTION_SELECTION_PRIORITIZATION --> CRITERIA_GENERATION \n\n                                     | CRITERIA_EXECUTION_SELECTION_PRIORITIZATION\n        CRITERIA_TESTS_EXECUTION --> | PASS_FAIL_TESTS_EXECUTION\n\n        PASS_FAIL_STATS --> PASS_FAIL_TESTS_EXECUTION\n\n        CRITERIA_STATS --> CRITERIA_TESTS_EXECUTION\n\n                             | PASS_FAIL_STATS\n        AGGREGATED_STATS --> | CRITERIA_STATS\n\n        FINISHED --> AGGREGATED_STATS\n    ------------------------------------------------------------------------\n\n    '

    def __init__(self, json_obj=None):
        if json_obj is None:
            self.initialize_data_graph()
        else:
            if type(json_obj) != dict:
                ERROR_HANDLER.error_exit('{} {}'.format('Invalid object to initialize', "TaskOrderingDependency, must be a 'dict'"), __file__)
            if len(json_obj) != len(Tasks):
                ERROR_HANDLER.error_exit('{} {}'.format('Invalid object to initialize', 'TaskOrderingDependency. Size mismatch'), __file__)
            for key_t in Tasks:
                if key_t.get_str() not in json_obj:
                    ERROR_HANDLER.error_exit('{} {} {} {}'.format('Invalid object to initialize TaskOrderingDependency', 'The task', key_t.get_str(), 'is absent in json_obj'), __file__)
                if not Status.has_element_named(json_obj[key_t.get_str()]):
                    ERROR_HANDLER.error_exit('{} {} {} {}'.format('Invalid object to initialize TaskOrderingDependency', 'The task', key_t.get_str(), 'has invalid status'), __file__)

            decoded_json_obj = {}
            for k_str, v_str in json_obj.items():
                decoded_json_obj[Tasks[k_str]] = Status[v_str]

            self.initialize_data_graph(decoded_json_obj)

    def get_as_json_object(self):
        ret_obj = {}
        for key_t in Tasks:
            ret_obj[key_t.get_str()] = self._lookup_task_cell(key_t).get_status().get_str()

        return ret_obj

    def export_graph(self, graph_out_filename):
        graph = networkx.Graph()
        for key_t in Tasks:
            graph.add_node(key_t.get_str())

        visited = set()
        queue = collections.deque()
        visited.add(self.root)
        queue.append(self.root)
        while queue:
            cur_node = queue.popleft()
            for d in cur_node.get_dependencies():
                graph.add_edge(d.get_task_name().get_str(), cur_node.get_task_name().get_str())
                if d not in visited:
                    visited.add(d)
                    queue.append(d)

        d_graph = networkx.DiGraph(graph)
        networkx.write_graphml(d_graph, graph_out_filename)

    def initialize_data_graph(self, task_status_map=None):
        """
        Each param is the status of the corresponding task 
        """
        if task_status_map is None:
            task_status_map = {}
            for key_t in Tasks:
                task_status_map[key_t] = Status.UNTOUCHED

        finished = self.Cell(Tasks.FINISHED)
        finished.set_status(task_status_map[Tasks.FINISHED])
        self.root = finished
        agg_stats = self.Cell(Tasks.AGGREGATED_STATS)
        agg_stats.set_status(task_status_map[Tasks.AGGREGATED_STATS])
        finished.add_dependency(agg_stats)
        passfail_stats = self.Cell(Tasks.PASS_FAIL_STATS)
        passfail_stats.set_status(task_status_map[Tasks.PASS_FAIL_STATS])
        agg_stats.add_dependency(passfail_stats)
        crit_stats = self.Cell(Tasks.CRITERIA_STATS)
        crit_stats.set_status(task_status_map[Tasks.CRITERIA_STATS])
        agg_stats.add_dependency(crit_stats)
        crit = self.Cell(Tasks.CRITERIA_TESTS_EXECUTION)
        crit.set_status(task_status_map[Tasks.CRITERIA_TESTS_EXECUTION])
        crit_stats.add_dependency(crit)
        passfail = self.Cell(Tasks.PASS_FAIL_TESTS_EXECUTION)
        passfail.set_status(task_status_map[Tasks.PASS_FAIL_TESTS_EXECUTION])
        passfail_stats.add_dependency(passfail)
        crit.add_dependency(passfail)
        ce_sp = self.Cell(Tasks.CRITERIA_EXECUTION_SELECTION_PRIORITIZATION)
        ce_sp.set_status(task_status_map[Tasks.CRITERIA_EXECUTION_SELECTION_PRIORITIZATION])
        crit.add_dependency(ce_sp)
        t_sp = self.Cell(Tasks.TESTS_EXECUTION_SELECTION_PRIORITIZATION)
        t_sp.set_status(task_status_map[Tasks.TESTS_EXECUTION_SELECTION_PRIORITIZATION])
        passfail.add_dependency(t_sp)
        t_gen_crit = self.Cell(Tasks.TESTS_GENERATION_USING_CRITERIA)
        t_gen_crit.set_status(task_status_map[Tasks.TESTS_GENERATION_USING_CRITERIA])
        t_sp.add_dependency(t_gen_crit)
        crit_gen = self.Cell(Tasks.CRITERIA_GENERATION)
        crit_gen.set_status(task_status_map[Tasks.CRITERIA_GENERATION])
        ce_sp.add_dependency(crit_gen)
        t_gen_crit.add_dependency(crit_gen)
        t_gen = self.Cell(Tasks.TESTS_GENERATION)
        t_gen.set_status(task_status_map[Tasks.TESTS_GENERATION])
        t_sp.add_dependency(t_gen)
        t_gguide = self.Cell(Tasks.TESTS_GENERATION_GUIDANCE)
        t_gguide.set_status(task_status_map[Tasks.TESTS_GENERATION_GUIDANCE])
        t_gen.add_dependency(t_gguide)
        t_gen_crit.add_dependency(t_gguide)
        c_gguide = self.Cell(Tasks.CRITERIA_GENERATION_GUIDANCE)
        c_gguide.set_status(task_status_map[Tasks.CRITERIA_GENERATION_GUIDANCE])
        crit_gen.add_dependency(c_gguide)
        starting = self.Cell(Tasks.STARTING)
        starting.set_status(task_status_map[Tasks.STARTING])
        c_gguide.add_dependency(starting)
        t_gguide.add_dependency(starting)
        visited = set()
        self._compute_uses_recursive(self.root, visited)
        number_of_tasks = len(Tasks)
        if len(visited) != number_of_tasks:
            ERROR_HANDLER.error_exit('%s %s' % (
             'BUG in the Task Ordering Dependency. got',
             '%d but expects %d' % (len(visited), number_of_tasks)), __file__)
        visited = {}
        self._recursive_verify(self.root, visited)

    def set_task_completed(self, task_name):
        t = self._lookup_task_cell(task_name)
        self._recursive_check_deps_are_done(t)
        t.set_done()
        logging.info('checkpoint_tasks:COMPLETED:' + task_name.get_str())

    def set_task_executing(self, task_name):
        t = self._lookup_task_cell(task_name)
        self._recursive_check_deps_are_done(t)
        t.set_executing()
        logging.info('checkpoint_tasks:EXECUTING:' + task_name.get_str())

    def task_is_complete(self, task_name):
        t = self._lookup_task_cell(task_name)
        return t.is_done()

    def task_is_executing(self, task_name):
        t = self._lookup_task_cell(task_name)
        return t.is_executing()

    def task_is_untouched(self, task_name):
        t = self._lookup_task_cell(task_name)
        return t.is_untouched()

    def get_next_todo_tasks(self):
        task_node_set = set()
        self._recursive_get_next_todo_tasks(task_node_set, self.root)
        task_set = {x.get_task_name() for x in task_node_set}
        if len(task_set) != len(task_node_set):
            ERROR_HANDLER.error_exit('{}'.format('(BUG) same task appears in multiple nodes'), __file__)
        logging.info('checkpoint_tasks:NEXT_TODO:' + str([t.get_str() for t in task_set]))
        return task_set

    def set_all_tasks_to_completed(self):
        task_name_set = self.get_next_todo_tasks()
        for task_name in task_name_set:
            t = self._lookup_task_cell(task_name)
            self._recursive_set_task_as_done(t)

    def set_task_back_as_todo_executing(self, task_name):
        t = self._lookup_task_cell(task_name)
        if not t.is_executing():
            t.set_executing()
            for u in t.get_uses():
                self._recursive_set_task_back_as_todo_untouched(u)

    def set_task_back_as_todo_untouched(self, task_name):
        t = self._lookup_task_cell(task_name)
        self._recursive_set_task_back_as_todo_untouched(t)

    class Cell:

        def __init__(self, task_name, status=Status.UNTOUCHED):
            self.dependencies = set()
            self.uses = set()
            self.status = status
            self.task_name = task_name
            if not Status.is_valid(self.status):
                ERROR_HANDLER.error_exit("Invalid value passed as status, use 'Status.'", __file__)

        def add_dependency(self, cell):
            self.dependencies.add(cell)

        def add_use(self, cell):
            self.uses.add(cell)

        def set_status(self, status):
            if not Status.is_valid(status):
                ERROR_HANDLER.error_exit("Invalid status value passed in set_status.use 'Status.'", __file__)
            self.status = status

        def set_done(self):
            self.status = Status.DONE

        def set_executing(self):
            self.status = Status.EXECUTING

        def set_untouched(self):
            self.status = Status.UNTOUCHED

        def get_dependencies(self):
            return self.dependencies

        def get_uses(self):
            return self.uses

        def get_status(self):
            return self.status

        def get_task_name(self):
            return self.task_name

        def is_done(self):
            return self.status == Status.DONE

        def is_executing(self):
            return self.status == Status.EXECUTING

        def is_untouched(self):
            return self.status == Status.UNTOUCHED

    def _compute_uses_recursive(self, start_node, visited):
        """
        Recursively set the use of the nodes (in the dependencies)
        Using DFS, just update the already visited deps, no recursive call

        :param start_node: currently explored node
        :param visited: set of visited nodes (already called recusively)
        """
        if start_node not in visited:
            visited.add(start_node)
            for d in start_node.get_dependencies():
                d.add_use(start_node)
                self._compute_uses_recursive(d, visited)

    def _recursive_verify(self, start_node, visited):
        if start_node in visited:
            ERROR_HANDLER.error_exit('There is a loop involving task {}'.format(start_node.get_task_name().get_str()), __file__)
        for d in start_node.get_dependencies():
            if not start_node.is_untouched():
                if not d.is_done():
                    ERROR_HANDLER.error_exit('{} {} {} {} {}'.format('Unsoundness of status. dependency', d.get_task_name().get_str(), 'not done while use', start_node.get_task_name().get_str(), 'is either executing or done'), __file__)
                self._recursive_verify(d, visited.copy())

    def _recursive_lookup(self, task_name, start_node):
        if start_node.task_name == task_name:
            return start_node
        for d_node in start_node.get_dependencies():
            ret = self._recursive_lookup(task_name, d_node)
            if ret is not None:
                return ret

    def _lookup_task_cell(self, task_name):
        cell = self._recursive_lookup(task_name, self.root)
        if cell is None:
            ERROR_HANDLER.error_exit('%s %s' % (
             'The Task looked up does not exist in dep graph', task_name), __file__)
        return cell

    def _recursive_check_deps_are_done(self, start_node):
        problem = None
        for d in start_node.get_dependencies():
            if not d.is_done():
                problem = d.get_task_name
                break
            self._recursive_check_deps_are_done(d)

        if problem is not None:
            ERROR_HANDLER.error_exit('%s %s %s %s' % (
             'task', start_node.get_task_name,
             'is done while the dependencies are not:', problem), __file__)

    def _recursive_set_task_as_done(self, start_node):
        if not start_node.is_done():
            start_node.set_done()
            for u in start_node.get_uses():
                self._recursive_set_task_as_done(u)

    def _recursive_set_task_back_as_todo_executing(self, start_node):
        if not start_node.is_executing():
            start_node.set_executing()
            for u in start_node.get_uses():
                self._recursive_set_task_back_as_todo_executing(u)

    def _recursive_set_task_back_as_todo_untouched(self, start_node):
        if not start_node.is_untouched():
            start_node.set_untouched()
            for u in start_node.get_uses():
                self._recursive_set_task_back_as_todo_untouched(u)

    def _recursive_get_next_todo_tasks(self, task_set, start_node):
        if start_node.is_done():
            return
        is_leaf = True
        for d in start_node.get_dependencies():
            if not d.is_done():
                is_leaf = False
                self._recursive_get_next_todo_tasks(task_set, d)

        if is_leaf:
            task_set.add(start_node)