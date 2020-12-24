# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/fate_flow/utils/setting_utils.py
# Compiled at: 2020-04-28 09:19:05
# Size of source mod 2**32: 3165 bytes
from urllib import parse
from kazoo.client import KazooClient
from kazoo.security import make_digest_acl
from arch.api.utils import file_utils
from arch.api.utils.core_utils import get_lan_ip

class CenterConfig(object):
    SERVERS = None
    USE_ACL = False
    ZK_USERNAME = 'fate'
    ZK_PASSWORD = 'fate'

    @staticmethod
    def get_settings(path, servings_zk_path=None, use_zk=False, hosts=None, server_conf_path=''):
        if servings_zk_path:
            if use_zk:
                return CenterConfig.get_servings_from_zookeeper(servings_zk_path, hosts)
        return CenterConfig.get_settings_from_file(path, server_conf_path)

    @staticmethod
    def get_settings_from_file(path, server_conf_path):
        server_conf = file_utils.load_json_conf(server_conf_path)
        data = server_conf
        for k in path.split('/')[1:]:
            data = data.get(k, None)

        return data

    @staticmethod
    def get_zk(hosts):
        if CenterConfig.USE_ACL:
            default_acl = make_digest_acl((CenterConfig.ZK_USERNAME), (CenterConfig.ZK_PASSWORD), all=True)
            zk = KazooClient(hosts=hosts, default_acl=[default_acl], auth_data=[
             ('digest',
              '{}:{}'.format(CenterConfig.ZK_USERNAME, CenterConfig.ZK_PASSWORD))])
        else:
            zk = KazooClient(hosts=hosts)
        return zk

    @staticmethod
    def get_servings_from_zookeeper(path, hosts):
        try:
            zk = CenterConfig.get_zk(hosts)
            zk.start()
            nodes = zk.get_children(path)
            CenterConfig.SERVERS = nodes_unquote(nodes)
            zk.stop()
            return CenterConfig.SERVERS
        except Exception as e:
            try:
                raise Exception('loading servings node  failed from zookeeper: {}'.format(e))
            finally:
                e = None
                del e

    @staticmethod
    def init(hosts, use_configuation_center, fate_flow_zk_path, fate_flow_port, model_transfer_path):
        if use_configuation_center:
            zk = CenterConfig.get_zk(hosts)
            zk.start()
            model_host = 'http://{}:{}{}'.format(get_lan_ip(), fate_flow_port, model_transfer_path)
            fate_flow_zk_path = '{}/{}'.format(fate_flow_zk_path, parse.quote(model_host, safe=' '))
            try:
                zk.create(fate_flow_zk_path, makepath=True)
            except:
                pass

            zk.stop()


def nodes_unquote(nodes):
    urls = [parse.unquote(node) for node in nodes]
    servings = []
    for url in urls:
        try:
            servings.append(url.split('/')[2])
        except:
            pass

    return servings