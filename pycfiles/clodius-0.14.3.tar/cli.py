# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/MyKings/Documents/github/clocwalk/clocwalk/cli.py
# Compiled at: 2019-12-11 03:48:15
import json, os, pprint, sys
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
from clocwalk.libs.core.option import setConfigFile
from clocwalk.libs.core.update import Upgrade
from clocwalk.libs.core.clocwrapper import ClocWrapper

class ClocDetector(object):
    """"""

    def __init__(self, **kwargs):
        """
        Constructor
        """
        init()
        code_dir = kwargs.get('code_dir', None)
        skip_check_new_version = kwargs.get('skip_check_new_version', False)
        self.tag_filter = kwargs.get('tag_filter', [])
        self.timeout = kwargs.get('timeout', 5)
        if not code_dir:
            raise CodeDirIsNoneException('"code_dir" parameter cannot be empty!')
        self.code_dir = code_dir
        self.skip_check_new_version = skip_check_new_version
        self._result = {'cloc': None, 'depends': []}
        self.cloc = ClocWrapper()
        return

    def start(self):
        """

        :return:
        """
        retVal = False
        try:
            logger.info('analysis statistics code ...')
            self.cloc.start(code_dir=self.code_dir, args=conf.cloc['cloc']['args'])
            self._result['cloc'] = json.loads(self.cloc.result)
        except Exception as ex:
            logger.warning(ex)

        for func, product in kb.pluginFunctions:
            try:
                logger.debug("test item depends on package using '%s'" % product)
                result = func(code_dir=self.code_dir, skipNewVerCheck=self.skip_check_new_version, timeout=self.timeout, tag_filter=self.tag_filter)
            except Exception as ex:
                err = "exception occurred while running script for '%s' ('%s')" % (product, ex)
                logger.critical(err)
                result = None

            if result:
                retVal = True
                self._result['depends'].append({product: result})

        return retVal

    @property
    def getResult(self):
        return self._result

    @property
    def getPluginNames(self):
        return [ i for i in kb.pluginFunctions ]


def main():
    """
    main function
    """
    try:
        init()
        banner()
        cmdLineParser()
        setConfigFile()
        if conf.search:
            result = kb.cache.get(conf.search)
            print '=' * 55
            print ' cve | vendor | product | version | update '
            for item in result['cpe']:
                print '-' * 55
                print (' {0} | {1} | {2} | {3} | {4} ').format(result['cve'][item.cpe23uri].cve, item.vendor, item.product, item.version, item.update_v)

            print '=' * 55
            print ('[*] cve count: {0}\n[*] cve list: {1} \n[*] affect version: {2}').format(len(result['cve']), [ result['cve'][_].cve for _ in result['cve'] ], [ ('{0}:{1}').format(item.version, item.update_v) for item in result['cpe'] ])
            sys.exit(1)
        if conf.upgrade:
            up = Upgrade(proxies=conf['http']['proxies'], upgrade_interval_day=conf['upgrade']['interval_day'], http_timeout=conf['http']['timeout'])
            up.start()
            sys.exit(1)
        if not os.path.exists(conf.code_dir):
            msg = '[%s] path does not exist!' % conf.code_dir
            logger.critical(msg)
            raise Exception(msg)
        c = ClocDetector(code_dir=conf.code_dir, skip_check_new_version=conf.skip_check_new_version)
        logger.info('%d fingerprints plugin loaded.' % len(c.getPluginNames))
        logger.info('checking depends ...')
        c.start()
        pprint.pprint(c.getResult)
    except UserQuitException:
        logger.error('user quit')
    except KeyboardInterrupt:
        logger.error('user aborted')
    except EOFError:
        logger.error('exit')
    except SystemExit:
        raise


if __name__ == '__main__':
    main()