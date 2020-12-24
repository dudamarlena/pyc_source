# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/rumba/elements/experimentation.py
# Compiled at: 2018-11-27 05:09:47
# Size of source mod 2**32: 25628 bytes
import abc, os, shutil, time
import rumba.log as log
import rumba.elements.topology as topology
logger = log.get_logger(__name__)
tmp_dir = '/tmp/rumba'

class Testbed(object):
    __doc__ = '\n    Base class for every testbed plugin.\n    '

    def __init__(self, exp_name, username, password, proj_name, system_logs=None):
        """
        :param exp_name: The experiment name.
        :param username: The username.
        :param password: The password.
        :param proj_name: The project name.
        :param system_logs: Location of the system logs of
                            images of the testbed.
        """
        self.username = username
        self.password = password
        self.proj_name = proj_name
        self.exp_name = exp_name
        self.flags = {'no_vlan_offload': False}
        self.executor = None
        if system_logs is None:
            self.system_logs = [
             '/var/log/syslog']
        else:
            if isinstance(system_logs, str):
                self.system_logs = [
                 system_logs]
            else:
                self.system_logs = system_logs

    def swap_in(self, experiment):
        """
        Swaps experiment in on the testbed.

        :param experiment: The experiment.
        """
        for node in experiment.nodes:
            node.executor = self.executor

        self._swap_in(experiment)
        for dif in experiment.dif_ordering:
            if isinstance(dif, topology.ShimEthDIF):
                dif.link_quality.apply(dif)

    @abc.abstractmethod
    def _swap_in(self, experiment):
        logger.info('_swap_in(): nothing to do')

    def swap_out(self, experiment):
        """
        Swaps experiment out of the testbed.

        :param experiment: The experiment.
        """
        self._swap_out(experiment)

    @abc.abstractmethod
    def _swap_out(self, experiment):
        logger.info('swap_out(): nothing to do')


class Experiment(object):
    __doc__ = '\n    Base class for experiments.\n    '
    __metaclass__ = abc.ABCMeta

    def __init__(self, testbed, nodes=None, git_repo=None, git_branch=None, log_dir=None, prototype_logs=None, enrollment_strategy='minimal', flows_strategy='full-mesh', server_decorator=None):
        """
        :param testbed: The testbed of the experiment.
        :param nodes: The list of nodes in the experiment.
        :param git_repo: The git repository of the prototype.
        :param git_branch: The git branch of the repository.
        :param log_dir: Where to log output of the experiment.
        :param prototype_logs: Where the prototype logs its output.
        :param enrollment_strategy: Can be 'full-mesh', 'minimal' or 'manual'.
        :param dt_strategy: For data flows, 'full-mesh', 'minimal' or 'manual'.
        :param server_decorator: a decorator function which will be applied to
                                 storyboard.server instances when using
                                 this prototype
        """
        if nodes is None:
            nodes = list()
        else:
            self.nodes = nodes
            if server_decorator is None:

                def server_decorator(server):
                    return server

            self.server_decorator = server_decorator
            self.git_repo = git_repo
            self.git_branch = git_branch
            self.testbed = testbed
            self.enrollment_strategy = enrollment_strategy
            self.flows_strategy = flows_strategy
            self.dif_ordering = []
            self.enrollments = []
            self.flows = []
            if self.enrollment_strategy not in ('full-mesh', 'minimal', 'manual'):
                raise Exception('Unknown enrollment strategy "%s"' % self.enrollment_strategy)
            if self.flows_strategy not in ('full-mesh', 'minimal', 'manual'):
                raise Exception('Unknown flows strategy "%s"' % self.flows_strategy)
            if log_dir is None:
                exp_name = self.testbed.exp_name.replace('/', '_')
                log_dir = os.path.join(tmp_dir, exp_name)
                shutil.rmtree(log_dir, ignore_errors=True)
                os.mkdir(log_dir)
            self.log_dir = log_dir
            assert os.path.isdir(self.log_dir), 'Destination "%s" is not a directory. Cannot fetch logs.' % self.log_dir
        self.prototype_logs = prototype_logs if prototype_logs is not None else []
        self.generate()

    def __repr__(self):
        s = ''
        for n in self.nodes:
            s += '\n' + str(n)

        return s

    def add_node(self, node):
        """
        Adds a node to the experiment.

        :param node: A node.
        """
        self.nodes.append(node)
        self.generate()

    def del_node(self, node):
        """
        Deletes a node from the experiment.

        :param node: A node.
        """
        self.nodes.remove(node)
        self.generate()

    def compute_dif_ordering(self):
        difsdeps_adj = dict()
        difsdeps_inc = dict()
        for node in self.nodes:
            for dif in node.difs:
                if dif not in difsdeps_adj:
                    difsdeps_adj[dif] = set()

            for upper in node.dif_registrations:
                for lower in node.dif_registrations[upper]:
                    if upper not in difsdeps_inc:
                        difsdeps_inc[upper] = set()
                    if lower not in difsdeps_inc:
                        difsdeps_inc[lower] = set()
                    if upper not in difsdeps_adj:
                        difsdeps_adj[upper] = set()
                    if lower not in difsdeps_adj:
                        difsdeps_adj[lower] = set()
                    difsdeps_inc[upper].add(lower)
                    difsdeps_adj[lower].add(upper)

        difsdeps_inc_cnt = dict()
        for dif in difsdeps_inc:
            difsdeps_inc_cnt[dif] = len(difsdeps_inc[dif])

        del difsdeps_inc
        for node in self.nodes:
            for dif in node.difs:
                if dif not in difsdeps_inc_cnt:
                    difsdeps_inc_cnt[dif] = 0

        frontier = set()
        self.dif_ordering = []
        for dif in difsdeps_inc_cnt:
            if difsdeps_inc_cnt[dif] == 0:
                frontier.add(dif)

        while len(frontier):
            cur = frontier.pop()
            self.dif_ordering.append(cur)
            for nxt in difsdeps_adj[cur]:
                difsdeps_inc_cnt[nxt] -= 1
                if difsdeps_inc_cnt[nxt] == 0:
                    frontier.add(nxt)

            difsdeps_adj[cur] = set()

        circular_set = [dif for dif in difsdeps_inc_cnt if difsdeps_inc_cnt[dif] != 0]
        if len(circular_set):
            raise Exception('Fatal error: The specified DIFs topologyhas one or morecircular dependencies, involving the following DIFs: %s' % circular_set)
        logger.debug('DIF topological ordering: %s', self.dif_ordering)

    def compute_enrollments(self):
        dif_graphs = dict()
        self.enrollments = []
        self.flows = []
        for dif in self.dif_ordering:
            neighsets = dict()
            dif_graphs[dif] = dict()
            first = None
            for node in self.nodes:
                if dif in node.dif_registrations:
                    dif_graphs[dif][node] = []
                    if first is None:
                        first = node
                    for lower_dif in node.dif_registrations[dif]:
                        if lower_dif not in neighsets:
                            neighsets[lower_dif] = []
                        neighsets[lower_dif].append(node)

            for lower_dif in neighsets:
                for node1 in neighsets[lower_dif]:
                    for node2 in neighsets[lower_dif]:
                        if node1 != node2:
                            dif_graphs[dif][node1].append((node2, lower_dif))

            self.enrollments.append([])
            self.flows.append([])
            if first is None:
                continue
            er = []
            for node in dif_graphs[dif]:
                for edge in dif_graphs[dif][node]:
                    er.append('%s --[%s]--> %s' % (node.name,
                     edge[1].name,
                     edge[0].name))

            logger.debug('DIF graph for %s: %s', dif, ', '.join(er))
            enrolled = {
             first}
            frontier = {first}
            edges_covered = set()
            while len(frontier):
                cur = frontier.pop()
                for edge in dif_graphs[dif][cur]:
                    if edge[0] not in enrolled:
                        enrolled.add(edge[0])
                        enrollee = edge[0].get_ipcp_by_dif(dif)
                        assert enrollee is not None
                        enroller = cur.get_ipcp_by_dif(dif)
                        assert enroller is not None
                        edges_covered.add((enrollee, enroller))
                        self.enrollments[(-1)].append({'dif':dif,  'enrollee':enrollee, 
                         'enroller':enroller, 
                         'lower_dif':edge[1]})
                        self.flows[(-1)].append({'src':enrollee,  'dst':enroller})
                        frontier.add(edge[0])

            if len(dif.members) != len(enrolled):
                raise Exception('Disconnected DIF found: %s' % (dif,))
            for cur in dif_graphs[dif]:
                for edge in dif_graphs[dif][cur]:
                    if cur.name < edge[0].name:
                        enrollee = cur.get_ipcp_by_dif(dif)
                        assert enrollee is not None
                        enroller = edge[0].get_ipcp_by_dif(dif)
                        assert enroller is not None
                        if (enrollee, enroller) not in edges_covered:
                            if (
                             enroller, enrollee) not in edges_covered:
                                if self.enrollment_strategy == 'full-mesh':
                                    self.enrollments[(-1)].append({'dif':dif,  'enrollee':enrollee, 
                                     'enroller':enroller, 
                                     'lower_dif':edge[1]})
                                if self.flows_strategy == 'full-mesh':
                                    self.flows[(-1)].append({'src':enrollee,  'dst':enroller})
                            edges_covered.add((enrollee, enroller))

            if self.flows_strategy == 'minimal' or self.flows_strategy == 'full-mesh':
                if not (self.enrollment_strategy == 'full-mesh' or self.enrollment_strategy == 'minimal' or False):
                    raise AssertionError

        log_string = 'Enrollments:\n'
        for el in self.enrollments:
            for e in el:
                log_string += '    [%s] %s --> %s through N-1-DIF %s\n' % (
                 e['dif'],
                 e['enrollee'].name,
                 e['enroller'].name,
                 e['lower_dif'])

        logger.debug(log_string)
        log_string = 'Flows:\n'
        for el in self.flows:
            for e in el:
                log_string += '    %s --> %s \n' % (
                 e['src'].name,
                 e['dst'].name)

        logger.debug(log_string)

    def compute_ipcps(self):
        for node in self.nodes:
            node.ipcps = []
            for dif in self.dif_ordering:
                if dif not in node.difs:
                    continue
                ipcp = dif.get_ipcp_class()(name=('%s.%s' % (dif.name, node.name)),
                  node=node,
                  dif=dif)
                if dif in node.dif_registrations:
                    for lower in node.dif_registrations[dif]:
                        ipcp.registrations.append(lower)

                node.ipcps.append(ipcp)
                dif.ipcps.append(ipcp)

    def compute_bootstrappers(self):
        for node in self.nodes:
            for ipcp in node.ipcps:
                ipcp.dif_bootstrapper = True
                for el in self.enrollments:
                    for e in el:
                        if e['dif'] != ipcp.dif:
                            break
                        if e['enrollee'] == ipcp:
                            ipcp.dif_bootstrapper = False
                            break

                    if not ipcp.dif_bootstrapper:
                        break

    def dump_ssh_info(self):
        f = open(os.path.join(tmp_dir, 'ssh_info'), 'w')
        for node in self.nodes:
            f.write('%s;%s;%s;%s;%s\n' % (node.name,
             self.testbed.username,
             node.ssh_config.hostname,
             node.ssh_config.port,
             node.ssh_config.proxy_server))

        f.close()

    def generate(self):
        start = time.time()
        self.compute_dif_ordering()
        self.compute_ipcps()
        self.compute_enrollments()
        self.compute_bootstrappers()
        for node in self.nodes:
            logger.info('IPCPs for node %s: %s', node.name, node.ipcps)

        end = time.time()
        logger.info('Layer ordering computation took %.2f seconds', end - start)

    def install_prototype(self):
        """
        Installs the prototype on the nodes.
        """
        start = time.time()
        self._install_prototype()
        end = time.time()
        logger.info('Install took %.2f seconds', end - start)

    def set_startup_command(self, command):
        for node in self.nodes:
            node.startup_command = command

    def bootstrap_prototype(self):
        """
        Bootstraps the prototype on the nodes.
        """
        start = time.time()
        self._bootstrap_prototype()
        end = time.time()
        logger.info('Bootstrap took %.2f seconds', end - start)

    @abc.abstractmethod
    def destroy_dif(self, dif):
        raise Exception('destroy_dif() method not implemented')

    @abc.abstractmethod
    def _install_prototype(self):
        raise Exception('install_prototype() method not implemented')

    @abc.abstractmethod
    def _bootstrap_prototype(self):
        raise Exception('bootstrap_prototype() method not implemented')

    @abc.abstractmethod
    def prototype_name(self):
        raise Exception('prototype_name() method not implemented')

    @abc.abstractmethod
    def _terminate_prototype(self, force=False):
        raise Exception('terminate_prototype() method not implemented')

    def swap_in(self):
        """
        Swap the experiment in on the testbed.
        """
        start = time.time()
        self.testbed.swap_in(self)
        self.dump_ssh_info()
        end = time.time()
        logger.info('Swap-in took %.2f seconds', end - start)

    def swap_out(self):
        """
        Swap the experiment out of the testbed.
        """
        start = time.time()
        for node in self.nodes:
            if node.ssh_config.client is not None:
                node.ssh_config.client.close()
            if node.ssh_config.proxy_client is not None:
                node.ssh_config.proxy_client.close()

        self.testbed.swap_out(self)
        end = time.time()
        logger.info('Swap-out took %.2f seconds', end - start)

    def terminate_prototype(self, force=False):
        """
        Terminate the prototype in the experiment.
        """
        self._terminate_prototype()

    def reboot_nodes(self):
        """
        Reboot all nodes in the experiment.
        """
        for node in self.nodes:
            node.execute_command('reboot', as_root=True)

    @abc.abstractmethod
    def export_dif_bandwidth(self, filename, dif):
        raise Exception('Export DIF bandwidth method not implemented')

    def to_dms_yaml(self, filename):
        """
        Generate a YAML file of the experiment which can be fed to the
        ARCFIRE DMS.

        :param filename: The output YAML filename.
        """
        mode = 'w'
        with open(filename, mode) as (f):
            for node in self.nodes:
                f.write('---\n')
                node.to_dms_yaml(f)

            f.write('...\n')
        logger.info('Generated DMS YAML file')

    def export_connectivity_graph(self, filename):
        """
        Generate a PDF of the physical connectivity graph.

        :param filename: The output PDF filename.
        """
        try:
            import pydot
            colors = [
             'red', 'green', 'blue', 'orange', 'yellow']
            fcolors = ['black', 'black', 'white', 'black', 'black']
            gvizg = pydot.Dot(graph_type='graph')
            i = 0
            try:
                for node in self.nodes:
                    g_node = pydot.Node((node.name), label=(node.name),
                      style='filled',
                      fillcolor=(colors[i]),
                      fontcolor=(fcolors[i]))
                    gvizg.add_node(g_node)
                    i += 1
                    if i == len(colors):
                        i = 0

            except Exception as e:
                try:
                    logger.error('Failed to create pydot Node: ' + str(e))
                    return
                finally:
                    e = None
                    del e

            try:
                for dif in self.dif_ordering:
                    if isinstance(dif, topology.ShimEthDIF):
                        edge = pydot.Edge((dif.members[0].name), (dif.members[1].name),
                          label=(dif.name),
                          color='black')
                        gvizg.add_edge(edge)

            except Exception as e:
                try:
                    logger.error('Failed to create pydot Edge: ' + str(e))
                    return
                finally:
                    e = None
                    del e

            try:
                gvizg.write_pdf(filename)
                logger.info('Generated pdf of connectivity graph')
            except Exception as e:
                try:
                    logger.error('Failed to write PDF: ' + str(e))
                finally:
                    e = None
                    del e

        except:
            logger.error('Warning: pydot module not installed, cannot produce graph images')

    def export_dif_graph(self, filename, dif):
        """
        Generate a PDF of a DIF graph.

        :param filename: The output PDF filename.
        :param dif: The DIF to export.
        """
        try:
            import pydot
            colors = [
             'red', 'green', 'blue', 'orange', 'yellow']
            fcolors = ['black', 'black', 'white', 'black', 'black']
            gvizg = pydot.Dot(graph_type='digraph')
            i = 0
            try:
                for node in dif.members:
                    g_node = pydot.Node((node.name), label=(node.name),
                      style='filled',
                      fillcolor=(colors[i]),
                      fontcolor=(fcolors[i]))
                    gvizg.add_node(g_node)
                    i += 1
                    if i == len(colors):
                        i = 0

            except Exception as e:
                try:
                    logger.error('Failed to create pydot Node: ' + str(e))
                    return
                finally:
                    e = None
                    del e

            try:
                for enroll, dt in zip(self.enrollments, self.flows):
                    for e in enroll:
                        if e['dif'] is not dif:
                            continue
                        edge = pydot.Edge((e['enrollee'].node.name), (e['enroller'].node.name),
                          color='black')
                        gvizg.add_edge(edge)

                    for e in dt:
                        if e['src'].dif is not dif:
                            continue
                        edge = pydot.Edge((e['src'].node.name), (e['dst'].node.name),
                          color='red')
                        gvizg.add_edge(edge)

            except Exception as e:
                try:
                    logger.error('Failed to create pydot Edge: ' + str(e))
                    return
                finally:
                    e = None
                    del e

            try:
                gvizg.write_pdf(filename)
                logger.info('Generated PDF of DIF graph')
            except Exception as e:
                try:
                    logger.error('Failed to write PDF: ' + str(e))
                finally:
                    e = None
                    del e

        except:
            logger.error('Warning: pydot module not installed, cannot produce DIF graph images')


class Executor:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def execute_command(self, node, command, as_root=False, time_out=3):
        pass

    def execute_commands(self, node, commands, as_root=False, time_out=3):
        for command in commands:
            self.execute_command(node, command, as_root, time_out)

    @abc.abstractmethod
    def copy_file(self, node, path, destination):
        pass

    def copy_files(self, node, paths, destination):
        for path in paths:
            self.copy_file(node, path, destination)

    @abc.abstractmethod
    def fetch_file(self, node, path, destination, sudo=False):
        pass

    def fetch_files(self, node, paths, destination, sudo=False):
        for path in paths:
            self.fetch_file(node, path, destination, sudo)