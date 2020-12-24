# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/centinel/primitives/headless_browser.py
# Compiled at: 2016-04-08 15:42:28
import shutil, csv, json, logging, os, sys, time
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import foctor_core.foctor_core as fc

class HeadlessBrowser:

    def __init__(self):
        self.cur_path = os.path.dirname(os.path.abspath(__file__))
        self.display = Display(visible=False)
        self.binary = None
        self.profile = None
        self.driver = None
        self.parsed = 0
        return

    @fc.timing
    def setup_profile(self, firebug=True, netexport=True):
        """
        Setup the profile for firefox
        :param firebug: whether add firebug extension
        :param netexport: whether add netexport extension
        :return: a firefox profile object
        """
        profile = webdriver.FirefoxProfile()
        profile.set_preference('app.update.enabled', False)
        if firebug:
            profile.add_extension(os.path.join(self.cur_path, 'extensions/firebug-2.0.8.xpi'))
            profile.set_preference('extensions.firebug.currentVersion', '2.0.8')
            profile.set_preference('extensions.firebug.allPagesActivation', 'on')
            profile.set_preference('extensions.firebug.defaultPanelName', 'net')
            profile.set_preference('extensions.firebug.net.enableSites', True)
            profile.set_preference('extensions.firebug.delayLoad', False)
            profile.set_preference('extensions.firebug.onByDefault', True)
            profile.set_preference('extensions.firebug.showFirstRunPage', False)
            profile.set_preference('extensions.firebug.net.defaultPersist', True)
        if netexport:
            har_path = os.path.join(self.cur_path, 'har')
            if not os.path.exists(har_path):
                os.mkdir(har_path)
            profile.add_extension(os.path.join(self.cur_path, 'extensions/netExport-0.9b7.xpi'))
            profile.set_preference('extensions.firebug.DBG_NETEXPORT', True)
            profile.set_preference('extensions.firebug.netexport.alwaysEnableAutoExport', True)
            profile.set_preference('extensions.firebug.netexport.defaultLogDir', har_path)
            profile.set_preference('extensions.firebug.netexport.includeResponseBodies', True)
        return profile

    def open_virtual_display(self):
        self.display.start()

    def close_virtual_display(self):
        self.display.stop()

    def wrap_results(self, **kwargs):
        """
        Wrap returned http response into a well formatted dict
        :param kwargs: this dict param should contains following keys:
                           fd: file directory to
                           url: the test url fo the result
                           files_count: the number of files under har/ directory

        :return (dict): the results of all
        """
        if 'fd' not in kwargs or 'url' not in kwargs or 'files_count' not in kwargs:
            logging.error('Missing arguments in wrap_results function')
            return {}
        else:
            external = kwargs['external'] if 'external' in kwargs else None
            fd = kwargs['fd']
            url = kwargs['url']
            length = kwargs['files_count']
            results = {}
            files = []
            wait_time = 15
            host = self.divide_url(url)[0]
            time.sleep(0.5)
            while len(os.listdir(fd)) <= length + self.parsed:
                time.sleep(1)
                wait_time -= 1
                if wait_time == 0:
                    logging.warning('%s waiting har file result timed out' % url)
                    results['error'] = 'wrap har file timeout'
                    if external is not None:
                        external[url] = results
                    return results

            time.sleep(1)
            for fn in os.listdir(fd):
                if fn.endswith('.har') and host in fn:
                    path = os.path.join(fd, fn)
                    files.append((fn, os.stat(path).st_mtime))

            files.sort(key=lambda x: x[1])
            if len(files) > 0:
                with open(fd + '/' + files[(-1)][0]) as (f):
                    raw_data = json.load(f)['log']['entries']
                    results = [ {} for i in range(0, len(raw_data)) ]
                    for i in range(0, len(results)):
                        results[i]['request'] = {}
                        results[i]['request']['method'] = raw_data[i]['request']['method']
                        headers = {}
                        for header in raw_data[i]['request']['headers']:
                            headers[header['name']] = header['value']

                        results[i]['request']['headers'] = headers
                        results[i]['response'] = {}
                        results[i]['response']['status'] = raw_data[i]['response']['status']
                        results[i]['response']['reason'] = raw_data[i]['response']['statusText']
                        headers = {}
                        for header in raw_data[i]['response']['headers']:
                            headers[header['name']] = header['value']

                        results[i]['response']['headers'] = headers
                        results[i]['response']['redirect'] = raw_data[i]['response']['redirectURL']
                        results[i]['response']['body'] = raw_data[i]['response']['content']

                self.parsed += 1
            else:
                logging.warning('Cannot find har file for %s' % url)
            if external is not None:
                external[url] = results
            else:
                return results
            return

    def divide_url(self, url):
        """
        divide url into host and path two parts
        """
        if 'https://' in url:
            host = url[8:].split('/')[0]
            path = url[8 + len(host):]
        elif 'http://' in url:
            host = url[7:].split('/')[0]
            path = url[7 + len(host):]
        else:
            host = url.split('/')[0]
            path = url[len(host):]
        return (host, path)

    def get(self, host, files_count, path='/', ssl=False, external=None):
        """
        Send get request to a url and wrap the results
        :param host (str): the host name of the url
        :param path (str): the path of the url (start with "/")
        :return (dict): the result of the test url
        """
        theme = 'https' if ssl else 'http'
        url = host + path
        http_url = theme + '://' + url
        result = {}
        try:
            capture_path = os.getcwd() + '/'
            har_file_path = capture_path + 'har/'
            fc.switch_tab(self.driver)
            self.load_page(http_url)
            print 'driver get: ' + http_url
            time.sleep(2)
            result = self.wrap_results(url=http_url, files_count=files_count, fd=har_file_path)
            if external is not None:
                external[http_url] = result
        except Exception as e:
            result['error'] = e.message
            print e

        return result

    def run_file(self, input_file, results):
        """
        use foctor_core library do get requests
        :param input_file: the file name of the list of test urls
                        format: 
                            1, www.facebook.com
                            2, www.google.com
                            ...
        :param results: the object to save the responses from server
        """
        capture_path = self.cur_path
        display_mode = 0
        site_list = []
        file_name, file_contents = input_file
        result = {'file_name': file_name}
        file_metadata = {}
        file_comments = []
        run_start_time = time.time()
        index = 1
        csvreader = csv.reader(file_contents, delimiter=',', quotechar='"')
        for row in csvreader:
            if row[0][0] == '#':
                row = row[0][1:].strip()
                if len(row.split(':')) > 1:
                    key, value = row.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    file_metadata[key] = value
                else:
                    file_comments.append(row)
                continue
            if row[0].strip().lower() == 'url':
                index_row = row
                continue
            url = row[0].strip()
            if url is None:
                continue
            meta = row[1:]
            site_list.append([index, url])
            index += 1

        driver, display = fc.do_crawl(sites=site_list, driver=self.driver, display=self.display, capture_path=capture_path, callback=self.wrap_results, external=results, fd=os.path.join(capture_path, 'har/'), files_count=len(os.listdir(os.path.join(capture_path, 'har/'))))
        fc.teardown_driver(driver, display, display_mode)
        driver.quit()
        return

    def run(self, input_files, url=None, verbose=0):
        """
        run the headless browser with given input
        if url given, the proc will only run hlb with given url and ignore input_list.
        :param url:
        :param input_files: the name of the file in "index url" format. i.e.
                1, www.facebook.com
                1, www.google.com
                ...
        :param verbose:
        :return:
        """
        if not url and not input_files:
            logging.warning('No input file')
            return {'error': 'no inputs'}
        else:
            results = {}
            self.open_virtual_display()
            if verbose > 0:
                log_file = sys.stdout
            else:
                log_file = None
            self.binary = FirefoxBinary(os.path.join(self.cur_path, 'firefox/firefox'), log_file=log_file)
            self.profile = self.setup_profile()
            self.driver = webdriver.Firefox(firefox_profile=self.profile, firefox_binary=self.binary, timeout=60)
            self.driver.set_page_load_timeout(60)
            isfile = False
            if url:
                host, path = self.divide_url(url)
                results[url] = self.get(host, path)
            else:
                isfile = True
                for input_file in input_files.items():
                    logging.info('Testing input file %s...' % input_file[0])
                    self.run_file(input_file, results)

            if not isfile:
                logging.info('Quit driver')
                self.driver.quit()
                self.close_virtual_display()
            logging.debug('Deleting har folder')
            shutil.rmtree(os.path.join(self.cur_path, 'har'))
            return results