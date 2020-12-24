# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luoxi/Project/yunify/qingcloud-cli/qingcloud/cli/iaas_client/actions/instance/run_instances.py
# Compiled at: 2017-09-21 02:37:46
from qingcloud.cli.misc.utils import explode_array
from qingcloud.cli.iaas_client.actions.base import BaseAction

class RunInstancesAction(BaseAction):
    action = 'RunInstances'
    command = 'run-instances'
    usage = '%(prog)s --image_id <image_id> --instance_type <instance_type> [options] [-f <conf_file>]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-m', '--image_id', dest='image_id', action='store', type=str, default='', help='image ID')
        parser.add_argument('-t', '--instance_type', dest='instance_type', action='store', type=str, default=None, help='instance type: small_b, small_c, medium_a, medium_b, medium_c,                 large_a, large_b, large_c')
        parser.add_argument('-i', '--instance_class', dest='instance_class', action='store', type=int, default=None, help='instance class: 0 is performance; 1 is high performance, default 0.')
        parser.add_argument('-c', '--count', dest='count', action='store', type=int, default=1, help='the number of instances to launch, default 1.')
        parser.add_argument('-C', '--cpu', dest='cpu', action='store', type=int, default=None, help='cpu core: 1, 2, 4, 8, 16')
        parser.add_argument('-M', '--memory', dest='memory', action='store', type=int, default=None, help='memory size in MB: 512, 1024, 2048, 4096, 8192, 16384')
        parser.add_argument('-N', '--instance_name', dest='instance_name', action='store', type=str, default='', help='instance name')
        parser.add_argument('-n', '--vxnets', dest='vxnets', action='store', type=str, default=None, help='specifies the IDs of vxnets the instance will join.')
        parser.add_argument('-s', '--security_group', dest='security_group', action='store', type=str, default=None, help='the ID of security group that will be applied to instance')
        parser.add_argument('-l', '--login_mode', dest='login_mode', action='store', type=str, default=None, help='SSH login mode: keypair or passwd')
        parser.add_argument('-p', '--login_passwd', dest='login_passwd', action='store', type=str, default='', help='login_passwd, should specified when SSH login mode is "passwd".')
        parser.add_argument('-k', '--login_keypair', dest='login_keypair', action='store', type=str, default='', help='login_keypair, should specified when SSH login mode is "keypair".')
        parser.add_argument('--hostname', dest='hostname', action='store', type=str, default='', help='the hostname you want to specify for the new instance.')
        parser.add_argument('--need_userdata', dest='need_userdata', action='store_const', const=1, help='use userdata')
        parser.add_argument('--userdata_type', dest='userdata_type', action='store', type=str, default=None, help='userdata_type: plain, exec, tar')
        parser.add_argument('--userdata_value', dest='userdata_value', action='store', type=str, default=None, help='userdata_value')
        parser.add_argument('--userdata_path', dest='userdata_path', action='store', type=str, default=None, help='userdata_path')
        parser.add_argument('--target-user', dest='target_user', action='store', type=str, default=None, help='ID of user who will own this resource, should be one of your sub-account.')
        parser.add_argument('--cpu_max', dest='cpu_max', action='store', type=int, default=0, help='The cpu core, e.g. "1, 2, 4, 8, 16".')
        parser.add_argument('--mem_max', dest='mem_max', action='store', type=int, default=0, help='The memory size in MB, e.g. "1024, 2048, 4096"')
        return parser

    @classmethod
    def build_directive(cls, options):
        required_params = {'image_id': options.image_id}
        for param in required_params:
            if required_params[param] is None or required_params[param] == '':
                print 'error: [%s] should be specified' % param
                return

        if not options.instance_type:
            if not options.cpu or not options.memory:
                print 'error: [instance_type] should be specified or specify both [cpu] and [memory]'
                return
        return {'image_id': options.image_id, 
           'instance_type': options.instance_type, 
           'instance_class': options.instance_class, 
           'cpu': options.cpu, 
           'memory': options.memory, 
           'instance_name': options.instance_name, 
           'count': options.count, 
           'vxnets': explode_array(options.vxnets), 
           'security_group': options.security_group, 
           'login_mode': options.login_mode, 
           'login_passwd': options.login_passwd, 
           'login_keypair': options.login_keypair, 
           'hostname': options.hostname, 
           'need_userdata': options.need_userdata or 0, 
           'userdata_type': options.userdata_type, 
           'userdata_path': options.userdata_path, 
           'userdata_value': options.userdata_value, 
           'target_user': options.target_user, 
           'cpu_max': options.cpu_max, 
           'mem_max': options.mem_max}