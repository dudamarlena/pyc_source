# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/rumba/prototypes/ouroboros.py
# Compiled at: 2018-11-27 05:10:02
# Size of source mod 2**32: 14139 bytes
import time, subprocess, re
import rumba.ssh_support as ssh
import rumba.model as mod
import rumba.multiprocess as m_processing
import rumba.log as log
import rumba.testbeds.local as local
import rumba.testbeds.dockertb as docker
import rumba.storyboard as sb
logger = log.get_logger(__name__)

class OurServer(sb.Server):

    def __init__(self, server):
        super(OurServer, self).__init__(server.ap, server.arrival_rate, server.actual_parameter + server.min_duration, server.options, server.max_clients, server.clients, server.nodes, server.min_duration, server.id, server.as_root, server.difs)

    def _make_run_cmd(self, node):
        o_cmd = super(OurServer, self)._make_run_cmd(node)
        n_cmd = 'pid=$(%s) && ' % (o_cmd,)
        r_cmd = 'irm r n %s ' % (self.id,)
        if len(self.difs) == 0:
            r_cmd += ' '.join(('ipcp %s' % (ipcp.name,) for ipcp in node.ipcps))
        else:
            for dif in self.difs:
                for ipcp in node.ipcps:
                    if ipcp.dif is dif:
                        r_cmd += 'ipcp %s' % (ipcp.name,)

        r_cmd += ' && '
        n_cmd += r_cmd
        n_cmd += 'irm b process $pid name %s && ' % (self.id,)
        n_cmd += 'echo $pid'
        return n_cmd


class Experiment(mod.Experiment):
    __doc__ = '\n    Represents an Ouroboros experiment.\n    '

    def __init__(self, testbed, nodes=None, git_repo='git://ouroboros.ilabt.imec.be/ouroboros', git_branch='master', enrollment_strategy='minimal', flows_strategy='full-mesh'):
        """
        Initializes the experiment class.

        :param testbed: The testbed to run the experiment on.
        :param nodes: The list of nodes.
        :param git_repo: The git repository to use for installation.
        :param git_branch: The branch of the git repository to use.
        :param enrollment_strategy: Can be 'full-mesh', 'minimal' or 'manual'.
        :param strategy: For flows, 'full-mesh', 'minimal' or 'manual'.
        """
        mod.Experiment.__init__(self,
          testbed,
          nodes,
          git_repo,
          git_branch,
          enrollment_strategy=enrollment_strategy,
          flows_strategy=flows_strategy,
          server_decorator=OurServer)
        self.r_ipcps = dict()
        self.set_startup_command('irmd')

    @staticmethod
    def make_executor(node, packages, testbed):

        def executor(commands):
            ssh.aptitude_install(testbed, node, packages)
            node.execute_commands(commands, time_out=None, use_proxy=True)

        return executor

    def prototype_name(self):
        return 'ouroboros'

    def exec_local_cmd(self, cmd):
        try:
            logger.info(cmd)
            subprocess.check_call(cmd.split(' '))
        except subprocess.CalledProcessError as e:
            try:
                logger.error('Return code was ' + str(e.returncode))
                raise
            finally:
                e = None
                del e

    def exec_local_cmds(self, cmds):
        for cmd in cmds:
            self.exec_local_cmd(cmd)

    def setup_ouroboros(self):
        if isinstance(self.testbed, docker.Testbed):
            return
        elif isinstance(self.testbed, local.Testbed):
            subprocess.check_call('sudo -v'.split())
            self.irmd = subprocess.Popen(['sudo', 'irmd'])
            logger.info('Started IRMd, sleeping 2 seconds...')
            time.sleep(2)
        else:
            for node in self.nodes:
                node.execute_command('sudo nohup irmd > /dev/null &', time_out=None)

    def install_ouroboros(self):
        if isinstance(self.testbed, local.Testbed):
            return
        packages = [
         'cmake', 'protobuf-c-compiler', 'git', 'libfuse-dev',
         'libgcrypt20-dev', 'libssl-dev']
        fs_loc = '/tmp/prototype'
        cmds = [
         'sudo apt-get install libprotobuf-c-dev --yes || true',
         'sudo rm -r ' + fs_loc + ' || true',
         'git clone -b ' + self.git_branch + ' ' + self.git_repo + ' ' + fs_loc,
         'cd ' + fs_loc + ' && mkdir build && cd build && ' + 'cmake .. && ' + 'sudo make install -j$(nproc)']
        names = []
        executors = []
        args = []
        for node in self.nodes:
            executor = self.make_executor(node, packages, self.testbed)
            names.append(node.name)
            executors.append(executor)
            args.append(cmds)

        m_processing.call_in_parallel(names, args, executors)

    def create_ipcps--- This code section failed: ---

 L. 187       0_2  SETUP_LOOP          544  'to 544'
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                nodes
                8  GET_ITER         
            10_12  FOR_ITER            542  'to 542'
               14  STORE_FAST               'node'

 L. 188        16  LOAD_GLOBAL              list
               18  CALL_FUNCTION_0       0  '0 positional arguments'
               20  STORE_FAST               'cmds'

 L. 189     22_24  SETUP_LOOP          526  'to 526'
               26  LOAD_FAST                'node'
               28  LOAD_ATTR                ipcps
               30  GET_ITER         
            32_34  FOR_ITER            524  'to 524'
               36  STORE_FAST               'ipcp'

 L. 190        38  LOAD_GLOBAL              list
               40  CALL_FUNCTION_0       0  '0 positional arguments'
               42  STORE_FAST               'cmds2'

 L. 191        44  LOAD_FAST                'ipcp'
               46  LOAD_ATTR                dif_bootstrapper
               48  POP_JUMP_IF_FALSE    62  'to 62'

 L. 192        50  LOAD_STR                 'irm i b n '
               52  LOAD_FAST                'ipcp'
               54  LOAD_ATTR                name
               56  BINARY_ADD       
               58  STORE_FAST               'cmd'
               60  JUMP_FORWARD         72  'to 72'
             62_0  COME_FROM            48  '48'

 L. 194        62  LOAD_STR                 'irm i c n '
               64  LOAD_FAST                'ipcp'
               66  LOAD_ATTR                name
               68  BINARY_ADD       
               70  STORE_FAST               'cmd'
             72_0  COME_FROM            60  '60'

 L. 196        72  LOAD_GLOBAL              isinstance
               74  LOAD_FAST                'ipcp'
               76  LOAD_ATTR                dif
               78  LOAD_GLOBAL              mod
               80  LOAD_ATTR                ShimEthDIF
               82  CALL_FUNCTION_2       2  '2 positional arguments'
               84  POP_JUMP_IF_FALSE   152  'to 152'

 L. 197        86  LOAD_GLOBAL              isinstance
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                testbed
               92  LOAD_GLOBAL              local
               94  LOAD_ATTR                Testbed
               96  CALL_FUNCTION_2       2  '2 positional arguments'
               98  POP_JUMP_IF_FALSE   118  'to 118'

 L. 198       100  LOAD_FAST                'cmd'
              102  LOAD_STR                 ' type local layer '
              104  LOAD_FAST                'ipcp'
              106  LOAD_ATTR                dif
              108  LOAD_ATTR                name
              110  BINARY_ADD       
              112  INPLACE_ADD      
              114  STORE_FAST               'cmd'
              116  JUMP_FORWARD        502  'to 502'
            118_0  COME_FROM            98  '98'

 L. 200       118  LOAD_FAST                'cmd'
              120  LOAD_STR                 ' type eth-dix dev '
              122  LOAD_FAST                'ipcp'
              124  LOAD_ATTR                ifname
              126  BINARY_ADD       
              128  INPLACE_ADD      
              130  STORE_FAST               'cmd'

 L. 201       132  LOAD_FAST                'cmd'
              134  LOAD_STR                 ' layer '
              136  LOAD_FAST                'ipcp'
              138  LOAD_ATTR                dif
              140  LOAD_ATTR                name
              142  BINARY_ADD       
              144  INPLACE_ADD      
              146  STORE_FAST               'cmd'
          148_150  JUMP_FORWARD        502  'to 502'
            152_0  COME_FROM            84  '84'

 L. 202       152  LOAD_GLOBAL              isinstance
              154  LOAD_FAST                'ipcp'
              156  LOAD_ATTR                dif
              158  LOAD_GLOBAL              mod
              160  LOAD_ATTR                NormalDIF
              162  CALL_FUNCTION_2       2  '2 positional arguments'
          164_166  POP_JUMP_IF_FALSE   448  'to 448'

 L. 203       168  LOAD_FAST                'cmd'
              170  LOAD_STR                 ' type normal'
              172  INPLACE_ADD      
              174  STORE_FAST               'cmd'

 L. 204       176  LOAD_FAST                'ipcp'
              178  LOAD_ATTR                dif_bootstrapper
          180_182  POP_JUMP_IF_FALSE   502  'to 502'

 L. 205       184  LOAD_FAST                'ipcp'
              186  LOAD_ATTR                dif
              188  LOAD_ATTR                policy
              190  LOAD_METHOD              get_policies
              192  CALL_METHOD_0         0  '0 positional arguments'
              194  STORE_FAST               'pols'

 L. 206       196  SETUP_LOOP          248  'to 248'
              198  LOAD_FAST                'pols'
              200  GET_ITER         
              202  FOR_ITER            246  'to 246'
              204  STORE_FAST               'comp'

 L. 207       206  SETUP_LOOP          244  'to 244'
              208  LOAD_FAST                'pols'
              210  LOAD_FAST                'comp'
              212  BINARY_SUBSCR    
              214  GET_ITER         
              216  FOR_ITER            242  'to 242'
              218  STORE_FAST               'pol'

 L. 208       220  LOAD_FAST                'cmd'
              222  LOAD_STR                 ' '
              224  LOAD_FAST                'comp'
              226  BINARY_ADD       
              228  LOAD_STR                 ' '
              230  BINARY_ADD       
              232  LOAD_FAST                'pol'
              234  BINARY_ADD       
              236  INPLACE_ADD      
              238  STORE_FAST               'cmd'
              240  JUMP_BACK           216  'to 216'
              242  POP_BLOCK        
            244_0  COME_FROM_LOOP      206  '206'
              244  JUMP_BACK           202  'to 202'
              246  POP_BLOCK        
            248_0  COME_FROM_LOOP      196  '196'

 L. 209       248  LOAD_FAST                'cmd'
              250  LOAD_STR                 ' layer '
              252  LOAD_FAST                'ipcp'
              254  LOAD_ATTR                dif
              256  LOAD_ATTR                name
              258  BINARY_ADD       
              260  LOAD_STR                 ' autobind'
              262  BINARY_ADD       
              264  INPLACE_ADD      
              266  STORE_FAST               'cmd'

 L. 211       268  LOAD_STR                 'irm r n '
              270  LOAD_FAST                'ipcp'
              272  LOAD_ATTR                name
              274  BINARY_ADD       
              276  STORE_FAST               'cmd2'

 L. 212       278  SETUP_LOOP          346  'to 346'
              280  LOAD_FAST                'node'
              282  LOAD_ATTR                dif_registrations
              284  LOAD_FAST                'ipcp'
              286  LOAD_ATTR                dif
              288  BINARY_SUBSCR    
              290  GET_ITER         
              292  FOR_ITER            344  'to 344'
              294  STORE_FAST               'dif_b'

 L. 213       296  SETUP_LOOP          340  'to 340'
              298  LOAD_FAST                'node'
              300  LOAD_ATTR                ipcps
              302  GET_ITER         
            304_0  COME_FROM           316  '316'
              304  FOR_ITER            338  'to 338'
              306  STORE_FAST               'ipcp_b'

 L. 214       308  LOAD_FAST                'ipcp_b'
              310  LOAD_FAST                'dif_b'
              312  LOAD_ATTR                ipcps
              314  COMPARE_OP               in
          316_318  POP_JUMP_IF_FALSE   304  'to 304'

 L. 215       320  LOAD_FAST                'cmd2'
              322  LOAD_STR                 ' ipcp '
              324  LOAD_FAST                'ipcp_b'
              326  LOAD_ATTR                name
              328  BINARY_ADD       
              330  INPLACE_ADD      
              332  STORE_FAST               'cmd2'
          334_336  JUMP_BACK           304  'to 304'
              338  POP_BLOCK        
            340_0  COME_FROM_LOOP      296  '296'
          340_342  JUMP_BACK           292  'to 292'
              344  POP_BLOCK        
            346_0  COME_FROM_LOOP      278  '278'

 L. 216       346  LOAD_FAST                'cmds2'
              348  LOAD_METHOD              append
              350  LOAD_FAST                'cmd2'
              352  CALL_METHOD_1         1  '1 positional argument'
              354  POP_TOP          

 L. 217       356  LOAD_STR                 'irm r n '
              358  LOAD_FAST                'ipcp'
              360  LOAD_ATTR                dif
              362  LOAD_ATTR                name
              364  BINARY_ADD       
              366  STORE_FAST               'cmd2'

 L. 218       368  SETUP_LOOP          436  'to 436'
              370  LOAD_FAST                'node'
              372  LOAD_ATTR                dif_registrations
              374  LOAD_FAST                'ipcp'
              376  LOAD_ATTR                dif
              378  BINARY_SUBSCR    
              380  GET_ITER         
              382  FOR_ITER            434  'to 434'
              384  STORE_FAST               'dif_b'

 L. 219       386  SETUP_LOOP          430  'to 430'
              388  LOAD_FAST                'node'
              390  LOAD_ATTR                ipcps
              392  GET_ITER         
            394_0  COME_FROM           406  '406'
              394  FOR_ITER            428  'to 428'
              396  STORE_FAST               'ipcp_b'

 L. 220       398  LOAD_FAST                'ipcp_b'
              400  LOAD_FAST                'dif_b'
              402  LOAD_ATTR                ipcps
              404  COMPARE_OP               in
          406_408  POP_JUMP_IF_FALSE   394  'to 394'

 L. 221       410  LOAD_FAST                'cmd2'
              412  LOAD_STR                 ' ipcp '
              414  LOAD_FAST                'ipcp_b'
              416  LOAD_ATTR                name
              418  BINARY_ADD       
              420  INPLACE_ADD      
              422  STORE_FAST               'cmd2'
          424_426  JUMP_BACK           394  'to 394'
              428  POP_BLOCK        
            430_0  COME_FROM_LOOP      386  '386'
          430_432  JUMP_BACK           382  'to 382'
              434  POP_BLOCK        
            436_0  COME_FROM_LOOP      368  '368'

 L. 222       436  LOAD_FAST                'cmds2'
              438  LOAD_METHOD              append
              440  LOAD_FAST                'cmd2'
              442  CALL_METHOD_1         1  '1 positional argument'
              444  POP_TOP          
              446  JUMP_FORWARD        502  'to 502'
            448_0  COME_FROM           164  '164'

 L. 223       448  LOAD_GLOBAL              isinstance
              450  LOAD_FAST                'ipcp'
              452  LOAD_ATTR                dif
              454  LOAD_GLOBAL              mod
              456  LOAD_ATTR                ShimUDPDIF
              458  CALL_FUNCTION_2       2  '2 positional arguments'
          460_462  POP_JUMP_IF_FALSE   490  'to 490'

 L. 225       464  LOAD_FAST                'cmd'
              466  LOAD_STR                 ' type udp'
            468_0  COME_FROM           116  '116'
              468  INPLACE_ADD      
              470  STORE_FAST               'cmd'

 L. 226       472  LOAD_FAST                'cmd'
              474  LOAD_STR                 ' layer '
              476  LOAD_FAST                'ipcp'
              478  LOAD_ATTR                dif
              480  LOAD_ATTR                name
              482  BINARY_ADD       
              484  INPLACE_ADD      
              486  STORE_FAST               'cmd'
              488  JUMP_FORWARD        502  'to 502'
            490_0  COME_FROM           460  '460'

 L. 228       490  LOAD_GLOBAL              logger
              492  LOAD_METHOD              error
              494  LOAD_STR                 'Unsupported IPCP type'
              496  CALL_METHOD_1         1  '1 positional argument'
              498  POP_TOP          

 L. 229       500  CONTINUE             32  'to 32'
            502_0  COME_FROM           488  '488'
            502_1  COME_FROM           446  '446'
            502_2  COME_FROM           180  '180'
            502_3  COME_FROM           148  '148'

 L. 231       502  LOAD_FAST                'cmds'
              504  LOAD_METHOD              append
              506  LOAD_FAST                'cmd'
              508  CALL_METHOD_1         1  '1 positional argument'
              510  POP_TOP          

 L. 233       512  LOAD_FAST                'cmds2'
              514  LOAD_FAST                'self'
              516  LOAD_ATTR                r_ipcps
              518  LOAD_FAST                'ipcp'
              520  STORE_SUBSCR     
              522  JUMP_BACK            32  'to 32'
              524  POP_BLOCK        
            526_0  COME_FROM_LOOP       22  '22'

 L. 235       526  LOAD_FAST                'node'
              528  LOAD_ATTR                execute_commands
              530  LOAD_FAST                'cmds'
              532  LOAD_CONST               None
              534  LOAD_CONST               ('time_out',)
              536  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              538  POP_TOP          
              540  JUMP_BACK            10  'to 10'
              542  POP_BLOCK        
            544_0  COME_FROM_LOOP        0  '0'

Parse error at or near `COME_FROM' instruction at offset 468_0

    def enroll_dif(self, el):
        for e in el:
            ipcp = e['enrollee']
            cmds = list()
            if e['enroller'] in self.r_ipcps:
                e['enroller'].node.execute_commands((self.r_ipcps[e['enroller']]), time_out=None)
                self.r_ipcps.pop(e['enroller'], None)
            cmd = 'irm r n ' + ipcp.name
            for dif_b in e['enrollee'].node.dif_registrations[ipcp.dif]:
                for ipcp_b in e['enrollee'].node.ipcps:
                    if ipcp_b in dif_b.ipcps:
                        cmd += ' ipcp ' + ipcp_b.name

            cmds.append(cmd)
            cmd = 'irm i e n ' + ipcp.name + ' layer ' + e['dif'].name + ' autobind'
            cmds.append(cmd)
            cmd = 'irm r n ' + ipcp.dif.name
            for dif_b in e['enrollee'].node.dif_registrations[ipcp.dif]:
                for ipcp_b in e['enrollee'].node.ipcps:
                    if ipcp_b in dif_b.ipcps:
                        cmd += ' ipcp ' + ipcp_b.name

            cmds.append(cmd)
            e['enrollee'].node.execute_commands(cmds, time_out=None)

    def setup_flows(self, el):
        for e in el:
            ipcp = e['src']
            cmd = 'irm i conn n ' + ipcp.name + ' dst ' + e['dst'].name
            retry = 0
            max_retries = 3
            while retry < max_retries:
                time.sleep(retry * 5)
                try:
                    ipcp.node.execute_command(cmd, time_out=None)
                    break
                except Exception as e:
                    try:
                        retry += 1
                        logger.error('Failed to connect IPCP, retrying: ' + str(retry) + '/' + str(max_retries) + ' retries')
                    finally:
                        e = None
                        del e

            if retry == max_retries:
                raise Exception('Failed to connect IPCP')

    def _install_prototype(self):
        logger.info('Installing Ouroboros...')
        self.install_ouroboros()
        logger.info('Installed on all nodes...')

    def _bootstrap_prototype(self):
        for dif in self.dif_ordering:
            if isinstance(dif, mod.NormalDIF) and len(dif.qos_cubes) != 0:
                logger.warn('QoS cubes not (yet) supported by the Ouroboros plugin. Will ignore.')

        logger.info('Starting IRMd on all nodes...')
        self.setup_ouroboros()
        logger.info('Creating IPCPs')
        self.create_ipcps()
        logger.info('Enrolling IPCPs...')
        for enrolls, flows in zip(self.enrollments, self.flows):
            self.enroll_dif(enrolls)
            self.setup_flows(flows)

        logger.info('All done, have fun!')

    def _terminate_prototype(self, force=False):
        cmds = list()
        if force is True:
            kill = 'killall -9 '
            cmds.append(kill + 'irmd')
            cmds.append(kill + 'ipcpd-normal')
            cmds.append(kill + 'ipcpd-shim-eth-llc')
            cmds.append(kill + 'ipcpd-local')
            cmds.append('kill -9 $(ps axjf | grep \'sudo irmd\' | grep -v grep | cut -f4 -d " "')
        else:
            cmds.append('killall -15 irmd')
        logger.info('Killing Ouroboros...')
        if isinstance(self.testbed, local.Testbed):
            cmds = list(map(lambda c: 'sudo %s' % (c,), cmds))
            for cmd in cmds:
                subprocess.check_call(cmd.split())

        else:
            for node in self.nodes:
                node.execute_commands(cmds, time_out=None, as_root=True)

    def destroy_dif(self, dif):
        for ipcp in dif.ipcps:
            ipcp.node.execute_command('irm i d n ' + ipcp.name)

    def parse_stats(self, lines, spaces=0):
        d = {}
        while len(lines):
            line = lines[0]
            if not re.match(' {%i}.*' % spaces, line):
                return d
            lines.pop(0)
            line = line.strip()
            if re.match('.*:.*', line):
                head, tail = line.split(':', 1)
                if len(tail) == 0:
                    d[head] = self.parse_stats(lines, spaces + 1)
                else:
                    d[head] = tail.strip()

        return d

    def export_dif_bandwidth(self, filename, dif):
        f = open(filename, 'w')
        for node in dif.members:
            ipcp = node.get_ipcp_by_dif(dif)
            if not hasattr(ipcp, 'address'):
                path = '/tmp/ouroboros/' + ipcp.name + '/dt*'
                dt_path = node.execute_command('ls -d %s' % path)
                dts = dt_path.split('.')
                ipcp.address = int(dts[(-1)])
                logger.info('IPCP %s has dt component with address %d' % (
                 ipcp.name, ipcp.address))

        for node in dif.members:
            ipcp = node.get_ipcp_by_dif(dif)
            dt_path = '/tmp/ouroboros/' + ipcp.name + '/dt.' + str(ipcp.address) + '/'
            fd = node.execute_command('ls --ignore=[01] %s' % dt_path)
            fds = fd.split('\n')
            for fd in fds:
                fd_path = dt_path + fd
                fd_file = node.execute_command('cat %s' % fd_path)
                d = self.parse_stats(fd_file.splitlines())
                remote = d['Endpoint address']
                ipcp2_name = ''
                for ipcp2 in dif.ipcps:
                    if ipcp2.address == int(remote):
                        ipcp2_name = ipcp2.name

                nr = d['Qos cube   0']['sent (bytes)']
                f.write('%s;%s;%s\n' % (ipcp.name, ipcp2_name, nr))

        f.close()
        logger.info('Wrote stats to %s', filename)