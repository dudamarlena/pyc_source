# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/MyKings/Documents/github/clocwalk/clocwalk/libs/core/update.py
# Compiled at: 2019-12-10 05:10:48
import datetime, glob, gzip, json, os, shutil, time, gevent, requests
from gevent.threadpool import ThreadPool
from clocwalk.libs.core.data import logger
from clocwalk.libs.core.db_helper import DBHelper
from clocwalk.libs.core.settings import DB_FILE
from clocwalk.libs.detector.cvecpe import cpe_parse

class Upgrade(object):

    def __init__(self, work_path, proxies=None, upgrade_interval_day=7, http_timeout=15):
        """

        :param work_path:
        :param proxies:
        :param upgrade_interval_day:
        :param http_timeout:
        """
        self.http_timeout = int(http_timeout)
        self.work_root = os.path.join(work_path, 'db')
        self.cve_path = os.path.join(self.work_root, 'json')
        self.cve_cpe_db = DB_FILE
        self.cpe_file = os.path.join(self.cve_path, 'nvdcpematch-1.0.json')
        self.upgrade_interval_day = int(upgrade_interval_day)
        self.headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3', 
           'Accept-Encoding': 'gzip, deflate, br', 
           'Accept-Language': 'en;q=0.9', 
           'Connection': 'keep-alive', 
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108'}
        self.pool = ThreadPool(10)
        self.proxies = {'http': 'socks5://127.0.0.1:1086', 
           'https': 'socks5://127.0.0.1:1086'}

    def download_cpe_match_file(self):
        """

        :return:
        """
        try:
            url = 'https://nvd.nist.gov/feeds/json/cpematch/1.0/nvdcpematch-1.0.json.gz'
            logger.info(('[DOWNLOAD] {0}').format(url))
            with requests.get(url, headers=self.headers, stream=True, proxies=self.proxies, timeout=self.http_timeout) as (r):
                r.raise_for_status()
                with open(('{0}.gz').format(self.cpe_file), 'wb') as (f):
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

            logger.info(("Start extracting '{0}' files...").format(self.cve_path))
            with gzip.open(('{0}.gz').format(self.cpe_file), 'rb') as (f_in):
                with open(self.cpe_file, 'wb') as (f_out):
                    shutil.copyfileobj(f_in, f_out)
            os.unlink(('{0}.gz').format(self.cpe_file))
        except Exception as ex:
            raise ex

    def download_cve_file(self):
        """

        :return:
        """

        def download_file(year):
            try:
                cve_file = os.path.join(self.cve_path, ('nvdcve-1.1-{0}.json.gz').format(year))
                url = ('https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-{0}.json.gz').format(year)
                logger.info(('[DOWNLOAD] {0}').format(url))
                with requests.get(url, headers=self.headers, stream=True, proxies=self.proxies, timeout=self.http_timeout) as (r):
                    r.raise_for_status()
                    with open(cve_file, 'wb') as (f):
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)

                logger.info(("Start extracting '{0}' files...").format(cve_file))
                with gzip.open(cve_file, 'rb') as (f_in):
                    with open(os.path.join(self.cve_path, ('nvdcve-1.1-{0}.json').format(year)), 'wb') as (f_out):
                        shutil.copyfileobj(f_in, f_out)
                os.unlink(cve_file)
            except Exception as ex:
                raise ex

        current_year = datetime.datetime.now().year
        for i in range(2002, current_year + 1):
            self.pool.spawn(download_file, i)

        gevent.wait()

    def cve_upgrade(self):
        """
        :return:
        """
        db = DBHelper(self.cve_cpe_db)
        db.create_cve_table()
        json_path = ('{0}/nvdcve-1.1*.json').format(self.cve_path)
        json_list = glob.glob(json_path)
        cve_list = []
        for cve_file in json_list:
            with open(cve_file, 'rb') as (fp):
                print cve_file
                json_obj = json.load(fp)
                for _ in json_obj['CVE_Items']:
                    if not _['configurations']['nodes']:
                        continue
                    cve = _['cve']['CVE_data_meta']['ID']
                    description = _['cve']['description']['description_data'][0]['value']
                    if 'cpe_match' not in _['configurations']['nodes'][0]:
                        if 'children' not in _['configurations']['nodes'][0]:
                            print _['configurations']['nodes'][0]
                        elif 'cpe_match' not in _['configurations']['nodes'][0]['children'][0]:
                            print _['configurations']['nodes'][0]['children'][0]
                        else:
                            cpe_match = _['configurations']['nodes'][0]['children'][0]['cpe_match']
                    else:
                        cpe_match = _['configurations']['nodes'][0]['cpe_match']
                    for item in cpe_match:
                        v3 = _['impact']['baseMetricV3']['impactScore'] if 'baseMetricV3' in _['impact'] else ''
                        cve_list.append((
                         cve,
                         item['cpe23Uri'],
                         description,
                         '',
                         _['impact']['baseMetricV2']['severity'],
                         _['impact']['baseMetricV2']['impactScore'],
                         v3))
                        if len(cve_list) % 100000 == 0:
                            db.create_cve_bulk(cve_list)
                            cve_list = []

        if cve_list:
            db.create_cve_bulk(cve_list)

    @property
    def is_update(self):
        result = False
        if os.path.isfile(self.cve_cpe_db):
            stat = os.stat(self.cve_cpe_db)
            if int(time.time()) - int(stat.st_mtime) > 86400 * self.upgrade_interval_day:
                result = True
                try:
                    if os.path.isdir(self.cve_path):
                        shutil.rmtree(self.cve_path)
                    os.makedirs(self.cve_path)
                    if os.path.isfile(self.cve_cpe_db):
                        shutil.move(self.cve_cpe_db, ('{0}.bak').format(self.cve_cpe_db))
                except Exception as ex:
                    logger.warn(ex)

        return result

    def cpe_upgrade(self):
        """

        :return:
        """
        db = DBHelper(self.cve_cpe_db)
        db.create_cpe_table()
        with open(self.cpe_file, 'rb') as (fp):
            json_obj = json.load(fp)
            obj_list = []
            for cpes in json_obj['matches']:
                cpe23_uri = cpes['cpe23Uri']
                version_start_including = cpes['versionStartIncluding'] if 'versionStartIncluding' in cpes else ''
                version_end_including = cpes['versionEndIncluding'] if 'versionEndIncluding' in cpes else ''
                version_start_excluding = cpes['versionStartExcluding'] if 'versionStartExcluding' in cpes else ''
                version_end_excluding = cpes['versionEndExcluding'] if 'versionEndExcluding' in cpes else ''
                for item in cpes['cpe_name']:
                    vendor, product, version, update = cpe_parse(item['cpe23Uri'])
                    obj_list.append((
                     vendor,
                     product,
                     version,
                     update,
                     cpe23_uri,
                     version_start_including,
                     version_end_including,
                     version_start_excluding,
                     version_end_excluding))

                if len(obj_list) % 100000 == 0:
                    db.create_cpe_bulk(obj_list)
                    obj_list = []

            if obj_list:
                db.create_cpe_bulk(obj_list)

    def start(self):
        try:
            try:
                s_time = time.time()
                if self.is_update:
                    self.download_cpe_match_file()
                    self.download_cve_file()
                    self.cpe_upgrade()
                    self.cve_upgrade()
                else:
                    raise Exception('No upgrade required.')
                logger.info(('total seconds: {0}').format(time.time() - s_time))
            except Exception as ex:
                logger.error(ex)
                bak_file = ('{0}.bak').format(self.cve_cpe_db)
                if os.path.isfile(bak_file):
                    shutil.move(bak_file, self.cve_cpe_db)

        finally:
            bak_file = ('{0}.bak').format(self.cve_cpe_db)
            if os.path.isfile(bak_file):
                os.unlink(bak_file)