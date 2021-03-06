# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/MyKings/Documents/github/clocwalk/clocwalk/cli.py
# Compiled at: 2020-02-03 02:02:51
# Size of source mod 2**32: 6465 bytes
import json, os, sys, pprint, time
from gevent.threadpool import ThreadPool
base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(base_path)
from clocwalk.libs.core.common import banner
from clocwalk.libs.core.cmdline import cmdLineParser
from clocwalk.libs.core.data import conf
from clocwalk.libs.core.data import kb
from clocwalk.libs.core.data import logger
from clocwalk.libs.core.exception import UserQuitException
from clocwalk.libs.core.exception import CodeDirIsNoneException
from clocwalk.libs.core.option import init
from clocwalk.libs.core.update import Upgrade
from clocwalk.libs.core.clocwrapper import ClocWrapper

def query_cve--- This code section failed: ---

 L.  33         0  LOAD_STR                 ''
                2  STORE_FAST               'result'

 L.  34         4  LOAD_GLOBAL              kb
                6  LOAD_ATTR                db
                8  POP_JUMP_IF_FALSE    24  'to 24'

 L.  35        10  LOAD_GLOBAL              kb
               12  LOAD_ATTR                db
               14  LOAD_METHOD              query_cve_by_id
               16  LOAD_FAST                'cve'
               18  CALL_METHOD_1         1  ''
               20  STORE_FAST               'result'
               22  JUMP_FORWARD         24  'to 24'
             24_0  COME_FROM            22  '22'
             24_1  COME_FROM             8  '8'

 L.  38        24  LOAD_FAST                'result'
               26  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 26


class ClocDetector(object):
    """ClocDetector"""

    def __init__(self, **kwargs):
        """
        Constructor
        """
        init()
        code_dir = kwargs.get('code_dir', None)
        self.enable_vuln_scan = kwargs.get('enable_vuln_scan', False)
        self.enable_upgrade = kwargs.get('enable_upgrade', False)
        self.skip_check_new_version = kwargs.get('skip_check_new_version', False)
        self.cloc_args = kwargs.get('cloc_args', [])
        self.tag_filter = kwargs.get('tag_filter', [])
        self.timeout = kwargs.get('timeout', 5)
        if not code_dir:
            raise CodeDirIsNoneException('"code_dir" parameter cannot be empty!')
        self.code_dir = code_dir
        self._result = {'cloc':None,  'depends':[]}
        self.cloc = ClocWrapper()
        self.pool = ThreadPool(20)
        self._vuln_list = []
        if self.enable_upgrade:
            up = Upgrade(proxies=(conf['http']['proxies']),
              upgrade_interval=(conf['upgrade_interval']),
              http_timeout=(conf['http']['timeout']))
            up.start()

    def start(self):
        """

        :return:
        """
        logger.info('%d analyzer plugin loaded.' % len(self.getPluginNames))
        try:
            logger.info('analysis statistics code ...')
            self.cloc.start(code_dir=(self.code_dir), args=(self.cloc_args))
            self._result['cloc'] = json.loads(self.cloc.result)
        except Exception as ex:
            try:
                import traceback
                traceback.print_exc()
                logger.warning(ex)
            finally:
                ex = None
                del ex

        for func, product in kb.pluginFunctions:
            try:
                logger.debug("test item depends on package using '%s'" % product)
                result = func(code_dir=(self.code_dir),
                  skipNewVerCheck=(self.skip_check_new_version),
                  timeout=(self.timeout),
                  tag_filter=(self.tag_filter))
                if self.enable_vuln_scan:
                    logger.info('Start using CPE rules for matching ...')
                    for item in result:
                        rule_list = kb.cpe_cache.get(item['product'])
                        for rule in rule_list:
                            if rule.compare(vendor=(item['vendor']), product=(item['product']), version=(item['version'])):
                                if 'cve' not in item:
                                    item['cve'] = {}
                                if rule.cve_info:
                                    item['cve'][rule.cve] = rule.cve_info.description

            except Exception as ex:
                try:
                    import traceback
                    traceback.print_exc()
                    err = "exception occurred while running script for '%s' ('%s')" % (product, str(ex))
                    logger.critical(err)
                    result = None
                finally:
                    ex = None
                    del ex

            if result:
                self._result['depends'].append({product: result})

    @property
    def getResult(self):
        return self._result

    @property
    def getPluginNames(self):
        return [i for i in kb.pluginFunctions]


def main():
    """
    main function
    """
    t1 = time.time()
    try:
        try:
            init()
            banner()
            cmdLineParser()
            if conf.search:
                result = kb.cpe_cache.get(conf.search)
                print('=======================================================')
                print(' cve | vendor | product | version | update ')
                for item in result:
                    print('-------------------------------------------------------')
                    print(' {0} | {1} | {2} | {3} | {4} '.format(item.cve, item.vendor, item.product, item.version, item.update))

                print('=======================================================')
                print('[*] cve count: {0}\n[*] cve list: {1} \n[*] affect version: {2}'.format(len(result), [_.cve for _ in result], ['{0}:{1}'.format(_.version, _.update) for _ in result]))
                sys.exit(1)
            if conf.upgrade:
                up = Upgrade(proxies=(conf['http']['proxies']),
                  upgrade_interval=(conf['upgrade_interval']),
                  http_timeout=(conf['http']['timeout']))
                up.start()
                sys.exit(1)
            if conf.code_dir:
                if not os.path.exists(conf.code_dir):
                    msg = '[%s] path does not exist!' % conf.code_dir
                    logger.critical(msg)
                    raise IOError(msg)
                else:
                    c = ClocDetector(code_dir=(conf.code_dir),
                      skip_check_new_version=(conf.skip_check_new_version),
                      enable_vuln_scan=(conf.vuln_scan),
                      cloc_args=(conf.cloc['args']))
                    c.start()
                    if conf.output:
                        with open(conf.output, 'wb') as (fp):
                            fp.write(json.dumps((c.getResult), indent=2).encode())
                        logger.info('The scan is complete and the results have been saved to the "{0}" file.'.format(conf.output))
                    else:
                        pprint.pprint(c.getResult)
        except UserQuitException:
            logger.error('user quit')
        except KeyboardInterrupt:
            logger.error('user aborted')
        except EOFError:
            logger.error('exit')
        except SystemExit:
            raise

    finally:
        logger.info('Total time consumption: {0}(s)'.format(round(time.time() - t1, 2)))


if __name__ == '__main__':
    main()