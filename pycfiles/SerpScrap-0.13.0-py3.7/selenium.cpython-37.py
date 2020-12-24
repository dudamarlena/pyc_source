# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\scrapcore\scraper\selenium.py
# Compiled at: 2018-10-10 11:15:26
# Size of source mod 2**32: 32015 bytes
import datetime, json, logging, os
from random import randint
import re, tempfile, threading, time, signal
from urllib.parse import quote
from scrapcore.scraping import MaliciousRequestDetected
from scrapcore.scraping import SearchEngineScrape, SeleniumSearchError
from scrapcore.scraping import get_base_search_url_by_search_engine
from scrapcore.user_agent import random_user_agent
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support as EC
from selenium.webdriver.support.ui import WebDriverWait
logger = logging.getLogger(__name__)

def get_selenium_scraper_by_search_engine_name(config, search_engine_name, *args, **kwargs):
    """Get the appropriate selenium scraper for the given search engine name.

    Args:
        search_engine_name: The search engine name.
        args: The arguments for the target search engine instance creation.
        kwargs: The keyword arguments for the target search engine instance.
    Returns;
        Either a concrete SelScrape instance specific for the given
        search engine or the abstract SelScrape object.
    """
    class_name = search_engine_name[0].upper() + search_engine_name[1:].lower() + 'SelScrape'
    ns = globals()
    if class_name in ns:
        return (ns[class_name])(config, *args, **kwargs)
    return SelScrape(config, *args, **kwargs)


class SelScrape(SearchEngineScrape, threading.Thread):
    __doc__ = '\n    Instances of this class make use of selenium browser objects\n    to query the search engines on a high level.\n    '
    next_page_selectors = {'google':'#pnnext', 
     'yandex':'.pager__button_kind_next', 
     'bing':'.sb_pagN', 
     'yahoo':'.compPagination .next', 
     'baidu':'.n', 
     'ask':'#paging div a.txt3.l_nu', 
     'duckduckgo':'', 
     'googleimg':'#pnnext', 
     'baiduimg':'.n'}
    input_field_selectors = {'google':(
      By.NAME, 'q'), 
     'yandex':(
      By.NAME, 'text'), 
     'bing':(
      By.NAME, 'q'), 
     'yahoo':(
      By.NAME, 'p'), 
     'baidu':(
      By.NAME, 'wd'), 
     'duckduckgo':(
      By.NAME, 'q'), 
     'ask':(
      By.NAME, 'q'), 
     'google':(
      By.NAME, 'q'), 
     'googleimg':(
      By.NAME, 'as_q'), 
     'baiduimg':(
      By.NAME, 'word')}
    param_field_selectors = {'googleimg': {'image_type':(
                    By.ID, 'imgtype_input'), 
                   'image_size':(
                    By.ID, 'imgsz_input')}}
    search_params = {'googleimg': {'image_type':None, 
                   'image_size':None}}
    normal_search_locations = {'google':'https://www.google.com/', 
     'yandex':'http://www.yandex.ru/', 
     'bing':'http://www.bing.com/', 
     'yahoo':'https://yahoo.com/', 
     'baidu':'http://baidu.com/', 
     'duckduckgo':'https://duckduckgo.com/', 
     'ask':'http://ask.com/'}
    image_search_locations = {'google':'https://www.google.com/imghp', 
     'yandex':'http://yandex.ru/images/', 
     'bing':'https://www.bing.com/?scope=images', 
     'yahoo':'http://images.yahoo.com/', 
     'baidu':'http://image.baidu.com/', 
     'duckduckgo':None, 
     'ask':'http://www.ask.com/pictures/', 
     'googleimg':'https://www.google.com/advanced_image_search', 
     'baiduimg':'http://image.baidu.com/'}

    def __init__(self, config, *args, captcha_lock=None, browser_num=1, **kwargs):
        """Create a new SelScraper thread Instance.

        Args:
            captcha_lock: To sync captcha solving (stdin)
            proxy: Optional, if set, use the proxy to route all scrapign through it.
            browser_num: A unique, semantic number for each thread.
        """
        self.search_input = None
        threading.Thread.__init__(self)
        (SearchEngineScrape.__init__)(self, config, *args, **kwargs)
        self.browser_type = self.config.get('sel_browser', 'chrome').lower()
        self.browser_num = browser_num
        self.captcha_lock = captcha_lock
        self.scrape_method = 'selenium'
        self.xvfb_display = self.config.get('xvfb_display', None)
        self.search_param_values = self._get_search_param_values()
        self.base_search_url = get_base_search_url_by_search_engine(self.config, self.search_engine_name, self.scrape_method)
        super().instance_creation_info(self.__class__.__name__)

    def set_proxy(self):
        """Install a proxy on the communication channel."""
        pass

    def switch_proxy(self, proxy):
        """Switch the proxy on the communication channel."""
        pass

    def proxy_check(self, proxy):
        if not (self.proxy and self.webdriver):
            raise AssertionError('Scraper instance needs valid\n        webdriver and proxy instance to make the proxy check')
        online = False
        status = 'Proxy check failed: {host}:{port}\n        is not used while requesting'.format(host=(self.proxy.host),
          port=(self.proxy.port))
        ipinfo = {}
        try:
            self.webdriver.get(self.config.get('proxy_info_url'))
            time.sleep(2)
            try:
                text = re.search('(\\{.*?\\})',
                  (self.webdriver.page_source),
                  flags=(re.DOTALL)).group(0)
                ipinfo = json.loads(text)
            except ValueError as v:
                try:
                    logger.critical(v)
                finally:
                    v = None
                    del v

        except Exception as e:
            try:
                status = str(e)
            finally:
                e = None
                del e

        if 'ip' in ipinfo and ipinfo['ip']:
            online = True
            status = 'Proxy is working.'
        else:
            logger.warning(status)
        super().update_proxy_status(status, ipinfo, online)
        return online

    def _save_debug_screenshot(self):
        """
        Saves a debug screenshot of the browser window to figure
        out what went wrong.
        """
        screendir = '{}/{}'.format(self.config['dir_screenshot'], self.config['today'])
        if not os.path.exists(screendir):
            os.makedirs(screendir)
        location = os.path.join(screendir, '{}_{}-p{}.png'.format(self.search_engine_name, self.query, str(self.page_number)))
        if self.config.get('sel_browser') == 'chrome':
            if self.config.get('chrome_headless') is True:
                self._enable_download_in_headless_chrome(self.webdriver, screendir)
                total_height = self.webdriver.execute_script('return document.body.parentNode.scrollHeight')
                self.webdriver.set_window_size('1024', total_height)
        try:
            self.webdriver.get_screenshot_as_file(location)
        except Exception as err:
            try:
                logger.error(err)
            finally:
                err = None
                del err

    def _set_xvfb_display(self):
        if self.xvfb_display:
            os.environ['DISPLAY'] = self.xvfb_display

    def _get_webdriver(self):
        """Return a webdriver instance and set it up
        with the according profile/ proxies.
        Chrome is quite fast, but not as stealthy as PhantomJS.
        Returns:
            The appropriate webdriver mode according to self.browser_type.
            If no webdriver mode could be found, return False.
        """
        if self.browser_type == 'chrome':
            return self._get_Chrome()
        if self.browser_type == 'firefox':
            return self._get_Firefox()
        if self.browser_type == 'phantomjs':
            return self._get_PhantomJS()
        return False

    def _enable_download_in_headless_chrome(self, browser, download_dir):
        browser.command_executor._commands['send_command'] = ('POST', '/session/$sessionId/chromium/send_command')
        params = {'cmd':'Page.setDownloadBehavior', 
         'params':{'behavior':'allow',  'downloadPath':download_dir}}
        browser.execute('send_command', params)

    def _get_Chrome(self):
        try:
            chrome_ops = webdriver.ChromeOptions()
            if self.proxy:
                chrome_ops = webdriver.ChromeOptions()
                chrome_ops.add_argument('--proxy-server={}://{}:{}'.format(self.proxy.proto, self.proxy.host, self.proxy.port))
                self.webdriver = webdriver.Chrome(executable_path=(self.config['executable_path']),
                  chrome_options=chrome_ops)
            if self.config.get('chrome_headless') is True:
                chrome_ops.add_argument('--headless')
            chrome_ops.add_argument('--no-sandbox')
            chrome_ops.add_argument('--start-maximized')
            chrome_ops.add_argument('--disable-gpu')
            chrome_ops.add_argument('--verbose')
            chrome_ops.add_argument('--window-position={},{}'.format(randint(10, 30), randint(10, 30)))
            chrome_ops.add_argument('--window-size={},{}'.format(randint(800, 1024), randint(600, 900)))
            self.webdriver = webdriver.Chrome(executable_path=(self.config['executable_path']),
              chrome_options=chrome_ops)
            return True
        except WebDriverException as e:
            try:
                logger.error(e)
                raise
            finally:
                e = None
                del e

        return False

    def _get_Firefox(self):
        try:
            if self.proxy:
                profile = webdriver.FirefoxProfile()
                profile.set_preference('network.proxy.type', 1)
                if self.proxy.proto.lower().startswith('socks'):
                    profile.set_preference('network.proxy.socks', self.proxy.host)
                    profile.set_preference('network.proxy.socks_port', self.proxy.port)
                    profile.set_preference('network.proxy.socks_version', 5 if self.proxy.proto[(-1)] == '5' else 4)
                    profile.update_preferences()
                else:
                    if self.proxy.proto == 'http':
                        profile.set_preference('network.proxy.http', self.proxy.host)
                        profile.set_preference('network.proxy.http_port', self.proxy.port)
                    else:
                        raise ValueError('Invalid protocol given in proxyfile.')
                profile.update_preferences()
                self.webdriver = webdriver.Firefox(firefox_profile=profile)
            else:
                self.webdriver = webdriver.Firefox()
            return True
        except WebDriverException as e:
            try:
                logger.error(e)
            finally:
                e = None
                del e

        return False

    def _get_PhantomJS(self):
        try:
            service_args = []
            if self.proxy:
                service_args.extend([
                 '--proxy={}:{}'.format(self.proxy.host, self.proxy.port),
                 '--proxy-type={}'.format(self.proxy.proto)])
                if self.proxy.username:
                    if self.proxy.password:
                        service_args.append('--proxy-auth={}:{}'.format(self.proxy.username, self.proxy.password))
            useragent = random_user_agent(mobile=False)
            logger.info('useragent: {}'.format(useragent))
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap['phantomjs.page.settings.userAgent'] = useragent
            try:
                self.webdriver = webdriver.PhantomJS(executable_path=(self.config['executable_path']),
                  service_args=service_args,
                  desired_capabilities=dcap)
                return True
            except (ConnectionError, ConnectionRefusedError, ConnectionResetError) as err:
                try:
                    logger.error(err)
                    return False
                finally:
                    err = None
                    del err

        except WebDriverException as e:
            try:
                logger.error(e)
            finally:
                e = None
                del e

        return False

    def handle_request_denied(self, status_code):
        super().handle_request_denied('400')
        needles = self.malicious_request_needles[self.search_engine_name]
        if needles:
            if needles['inurl'] in self.webdriver.current_url:
                if needles['inhtml'] in self.webdriver.page_source:
                    if self.config.get('manual_captcha_solving', False):
                        with self.captcha_lock:
                            tf = tempfile.NamedTemporaryFile('wb')
                            tf.write(self.webdriver.get_screenshot_as_png())
                            import webbrowser
                            webbrowser.open('file://{}'.format(tf.name))
                            solution = input('enter the captcha please...')
                            self.webdriver.find_element_by_name('submit').send_keys(solution + Keys.ENTER)
                            try:
                                self.search_input = WebDriverWait(self.webdriver, 5).until(EC.visibility_of_element_located(self._get_search_input_field()))
                            except TimeoutException:
                                raise MaliciousRequestDetected('Requesting with this ip is not possible at the moment.')

                            tf.close()
                    else:
                        logger.info('Waiting for user to solve captcha')
                        return self._wait_until_search_input_field_appears(36000)

    def build_search(self):
        """Build the search for SelScrapers"""
        assert self.webdriver, 'Webdriver needs to be ready to build the search'
        if self.config.get('search_type', 'normal') == 'image':
            starting_point = self.image_search_locations[self.search_engine_name]
        else:
            starting_point = self.base_search_url
            if self.config.get('num_results_per_page', 10) > 10:
                starting_point = '{}num={}'.format(starting_point, str(self.config.get('num_results_per_page', 10)))
            if 'Any' not in self.config.get('results_age'):
                starting_point = '{}&tbs=qdr:={}'.format(starting_point, str(self.config.get('results_age', 'y')))
            logger.info(starting_point)
        self.webdriver.get(starting_point)

    def _get_search_param_values(self):
        search_param_values = {}
        if self.search_engine_name in self.search_params:
            for param_key in self.search_params[self.search_engine_name]:
                cfg = self.config.get(param_key, None)
                if cfg:
                    search_param_values[param_key] = cfg

        return search_param_values

    def _get_search_input_field(self):
        """Get the search input field for the current search_engine.

        Returns:
            A tuple to locate the search field as used by seleniums function presence_of_element_located()
        """
        return self.input_field_selectors[self.search_engine_name]

    def _get_search_param_fields(self):
        if self.search_engine_name in self.param_field_selectors:
            return self.param_field_selectors[self.search_engine_name]
        return {}

    def _wait_until_search_input_field_appears(self, max_wait=10):
        """Waits until the search input field can be located for the current search engine

        Args:
            max_wait: How long to wait maximally before returning False.

        Returns: False if the search input field could not be located within the time
                or the handle to the search input field.
        """

        def find_visible_search_input(driver):
            input_field = (driver.find_element)(*self._get_search_input_field())
            return input_field

        try:
            search_input = WebDriverWait(self.webdriver, max_wait).until(find_visible_search_input)
            return search_input
        except TimeoutException as e:
            try:
                logger.error('{}: TimeoutException waiting for search input field: {}'.format(self.name, e))
                return False
            finally:
                e = None
                del e

    def _wait_until_search_param_fields_appears(self, max_wait=5):
        """Waits until the search input field contains the query.

        Args:
            max_wait: How long to wait maximally before returning False.
        """

        def find_visible_search_param(driver):
            for _, field in self._get_search_param_fields().items():
                input_field = (driver.find_element)(*field)
                if not input_field:
                    return False

            return True

        try:
            fields = WebDriverWait(self.webdriver, max_wait).until(find_visible_search_param)
            return fields
        except TimeoutException as e:
            try:
                logger.error('{}: TimeoutException waiting for search param field: {}'.format(self.name, e))
                return False
            finally:
                e = None
                del e

    def _goto_next_page(self):
        """
        Click the next page element,

        Returns:
            The url of the next page or False if there is no such url
                (end of available pages for instance).
        """
        next_url = ''
        element = self._find_next_page_element()
        if hasattr(element, 'click'):
            next_url = element.get_attribute('href')
            try:
                element.click()
            except WebDriverException:
                selector = self.next_page_selectors[self.search_engine_name]
                if selector:
                    try:
                        next_element = WebDriverWait(self.webdriver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                        webdriver.ActionChains(self.webdriver).move_to_element(next_element).perform()
                        WebDriverWait(self.webdriver, 8).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
                        element = self.webdriver.find_element_by_css_selector(selector)
                        next_url = element.get_attribute('href')
                        element.click()
                    except WebDriverException:
                        pass

        else:
            return next_url or False
        return next_url

    def _find_next_page_element(self):
        """Finds the element that locates the next page for any search engine.

        Returns:
            The element that needs to be clicked to get to the next page or a boolean value to
            indicate an error condition.
        """
        if self.search_type == 'normal':
            selector = self.next_page_selectors[self.search_engine_name]
            try:
                WebDriverWait(self.webdriver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            except (WebDriverException, TimeoutException):
                self._save_debug_screenshot()

            try:
                return self.webdriver.find_element_by_css_selector(selector)
            except Exception:
                logger.error('failed find_element_by_css_selector, sleep 30 sec')
                time.sleep(30)

        else:
            if self.search_type == 'image':
                self.page_down()
                if self.search_engine_name == 'google':
                    return self.webdriver.find_element_by_css_selector('input._kvc')
                return True

    def wait_until_serp_loaded(self):
        """
        This method tries to wait until the page requested is loaded.

        We know that the correct page is loaded when self.page_number appears
        in the navigation of the page.
        """
        if self.search_type == 'normal':
            if self.search_engine_name == 'google':
                selector = '#resultStats'
            else:
                if self.search_engine_name == 'yandex':
                    selector = '.pager__item_current_yes font font'
                else:
                    if self.search_engine_name == 'bing':
                        selector = 'nav li a.sb_pagS'
                    else:
                        if self.search_engine_name == 'yahoo':
                            selector = '.compPagination strong'
                        else:
                            if self.search_engine_name == 'baidu':
                                selector = '#page .fk_cur + .pc'
                            else:
                                if self.search_engine_name == 'duckduckgo':
                                    pass
                                elif self.search_engine_name == 'ask':
                                    selector = '#paging .pgcsel .pg'
                                try:
                                    WebDriverWait(self.webdriver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
                                except NoSuchElementException:
                                    logger.error('No such element. Seeing if title matches before raising SeleniumSearchError')
                                    self._save_debug_screenshot()
                                    try:
                                        self.wait_until_title_contains_keyword()
                                    except TimeoutException:
                                        self.quit()
                                        raise SeleniumSearchError('Stop Scraping, seems we are blocked')

                                except Exception as e:
                                    try:
                                        logger.error('Scrape Exception pass. Selector: ' + str(selector))
                                        logger.error('Error: ' + str(e))
                                        self._save_debug_screenshot()
                                    finally:
                                        e = None
                                        del e

        else:
            self.wait_until_title_contains_keyword()

    def wait_until_title_contains_keyword(self):
        try:
            WebDriverWait(self.webdriver, 5).until(EC.title_contains(self.query))
        except TimeoutException:
            logger.debug(SeleniumSearchError('{}: Keyword "{}" not found in title: {}'.format(self.name, self.query, self.webdriver.title)))

    def search--- This code section failed: ---

 L. 634         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _wait_until_search_input_field_appears
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  LOAD_FAST                'self'
                8  STORE_ATTR               search_input

 L. 635        10  LOAD_GLOBAL              time
               12  LOAD_METHOD              sleep
               14  LOAD_CONST               0.25
               16  CALL_METHOD_1         1  '1 positional argument'
               18  POP_TOP          

 L. 637        20  LOAD_FAST                'self'
               22  LOAD_ATTR                search_input
               24  LOAD_CONST               False
               26  COMPARE_OP               is
               28  POP_JUMP_IF_FALSE    52  'to 52'
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                config
               34  LOAD_METHOD              get
               36  LOAD_STR                 'stop_on_detection'
               38  CALL_METHOD_1         1  '1 positional argument'
               40  POP_JUMP_IF_FALSE    52  'to 52'

 L. 638        42  LOAD_STR                 'Malicious request detected'
               44  LOAD_FAST                'self'
               46  STORE_ATTR               status

 L. 639        48  LOAD_CONST               None
               50  RETURN_VALUE     
             52_0  COME_FROM            40  '40'
             52_1  COME_FROM            28  '28'

 L. 641        52  LOAD_FAST                'self'
               54  LOAD_ATTR                search_input
               56  LOAD_CONST               False
               58  COMPARE_OP               is
               60  POP_JUMP_IF_FALSE    72  'to 72'

 L. 643        62  LOAD_FAST                'self'
               64  LOAD_METHOD              handle_request_denied
               66  CALL_METHOD_0         0  '0 positional arguments'
               68  LOAD_FAST                'self'
               70  STORE_ATTR               search_input
             72_0  COME_FROM            60  '60'

 L. 645        72  LOAD_FAST                'self'
               74  LOAD_ATTR                search_input
            76_78  POP_JUMP_IF_FALSE   546  'to 546'

 L. 646        80  SETUP_EXCEPT        144  'to 144'

 L. 647        82  LOAD_FAST                'self'
               84  LOAD_ATTR                config
               86  LOAD_METHOD              get
               88  LOAD_STR                 'sel_browser'
               90  CALL_METHOD_1         1  '1 positional argument'
               92  LOAD_STR                 'chrome'
               94  COMPARE_OP               !=
               96  POP_JUMP_IF_TRUE    130  'to 130'
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                config
              102  LOAD_METHOD              get
              104  LOAD_STR                 'sel_browser'
              106  CALL_METHOD_1         1  '1 positional argument'
              108  LOAD_STR                 'chrome'
              110  COMPARE_OP               ==
              112  POP_JUMP_IF_FALSE   140  'to 140'
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                config
              118  LOAD_METHOD              get
              120  LOAD_STR                 'chrome_headless'
              122  CALL_METHOD_1         1  '1 positional argument'
              124  LOAD_CONST               False
              126  COMPARE_OP               is
              128  POP_JUMP_IF_FALSE   140  'to 140'
            130_0  COME_FROM            96  '96'

 L. 648       130  LOAD_FAST                'self'
              132  LOAD_ATTR                search_input
              134  LOAD_METHOD              clear
              136  CALL_METHOD_0         0  '0 positional arguments'
              138  POP_TOP          
            140_0  COME_FROM           128  '128'
            140_1  COME_FROM           112  '112'
              140  POP_BLOCK        
              142  JUMP_FORWARD        214  'to 214'
            144_0  COME_FROM_EXCEPT     80  '80'

 L. 649       144  DUP_TOP          
              146  LOAD_GLOBAL              Exception
              148  COMPARE_OP               exception-match
              150  POP_JUMP_IF_FALSE   212  'to 212'
              152  POP_TOP          
              154  STORE_FAST               'e'
              156  POP_TOP          
              158  SETUP_FINALLY       200  'to 200'

 L. 650       160  LOAD_GLOBAL              logger
              162  LOAD_METHOD              error
              164  LOAD_STR                 'Possible blocked search, sleep 30 sec, Scrape Exception: '
              166  LOAD_GLOBAL              str
              168  LOAD_FAST                'e'
              170  CALL_FUNCTION_1       1  '1 positional argument'
              172  BINARY_ADD       
              174  CALL_METHOD_1         1  '1 positional argument'
              176  POP_TOP          

 L. 651       178  LOAD_FAST                'self'
              180  LOAD_METHOD              _save_debug_screenshot
              182  CALL_METHOD_0         0  '0 positional arguments'
              184  POP_TOP          

 L. 652       186  LOAD_GLOBAL              time
              188  LOAD_METHOD              sleep
              190  LOAD_CONST               30
              192  CALL_METHOD_1         1  '1 positional argument'
              194  POP_TOP          
              196  POP_BLOCK        
              198  LOAD_CONST               None
            200_0  COME_FROM_FINALLY   158  '158'
              200  LOAD_CONST               None
              202  STORE_FAST               'e'
              204  DELETE_FAST              'e'
              206  END_FINALLY      
              208  POP_EXCEPT       
              210  JUMP_FORWARD        214  'to 214'
            212_0  COME_FROM           150  '150'
              212  END_FINALLY      
            214_0  COME_FROM           210  '210'
            214_1  COME_FROM           142  '142'

 L. 653       214  LOAD_GLOBAL              time
              216  LOAD_METHOD              sleep
              218  LOAD_CONST               0.25
              220  CALL_METHOD_1         1  '1 positional argument'
              222  POP_TOP          

 L. 655       224  LOAD_FAST                'self'
              226  LOAD_METHOD              _get_search_param_fields
              228  CALL_METHOD_0         0  '0 positional arguments'
              230  LOAD_FAST                'self'
              232  STORE_ATTR               search_param_fields

 L. 657       234  LOAD_FAST                'self'
              236  LOAD_ATTR                search_param_fields
          238_240  POP_JUMP_IF_FALSE   378  'to 378'

 L. 658       242  LOAD_FAST                'self'
              244  LOAD_METHOD              _wait_until_search_param_fields_appears
              246  CALL_METHOD_0         0  '0 positional arguments'
              248  STORE_FAST               'wait_res'

 L. 659       250  LOAD_FAST                'wait_res'
              252  LOAD_CONST               False
              254  COMPARE_OP               is
          256_258  POP_JUMP_IF_FALSE   276  'to 276'

 L. 660       260  LOAD_FAST                'self'
              262  LOAD_METHOD              quit
              264  CALL_METHOD_0         0  '0 positional arguments'
              266  POP_TOP          

 L. 661       268  LOAD_GLOBAL              Exception
              270  LOAD_STR                 'Waiting search param input fields time exceeds'
              272  CALL_FUNCTION_1       1  '1 positional argument'
              274  RAISE_VARARGS_1       1  'exception instance'
            276_0  COME_FROM           256  '256'

 L. 663       276  SETUP_LOOP          378  'to 378'
              278  LOAD_FAST                'self'
              280  LOAD_ATTR                search_param_fields
              282  LOAD_METHOD              items
              284  CALL_METHOD_0         0  '0 positional arguments'
              286  GET_ITER         
              288  FOR_ITER            376  'to 376'
              290  UNPACK_SEQUENCE_2     2 
              292  STORE_FAST               'param'
              294  STORE_FAST               'field'

 L. 664       296  LOAD_FAST                'field'
              298  LOAD_CONST               0
              300  BINARY_SUBSCR    
              302  LOAD_GLOBAL              By
              304  LOAD_ATTR                ID
              306  COMPARE_OP               ==
          308_310  POP_JUMP_IF_FALSE   318  'to 318'

 L. 668       312  LOAD_STR                 '\n                        var field = document.getElementById("%s");\n                        field.setAttribute("value", "%s");\n                        '
              314  STORE_FAST               'js_tpl'
              316  JUMP_FORWARD        338  'to 338'
            318_0  COME_FROM           308  '308'

 L. 669       318  LOAD_FAST                'field'
              320  LOAD_CONST               0
              322  BINARY_SUBSCR    
              324  LOAD_GLOBAL              By
              326  LOAD_ATTR                NAME
              328  COMPARE_OP               ==
          330_332  POP_JUMP_IF_FALSE   338  'to 338'

 L. 675       334  LOAD_STR                 '\n                        var fields = document.getElementsByName("%s");\n                        for (var f in fields) {\n                            f.setAttribute("value", "%s");\n                        }\n                        '
              336  STORE_FAST               'js_tpl'
            338_0  COME_FROM           330  '330'
            338_1  COME_FROM           316  '316'

 L. 676       338  LOAD_FAST                'js_tpl'
              340  LOAD_FAST                'field'
              342  LOAD_CONST               1
              344  BINARY_SUBSCR    
              346  LOAD_FAST                'self'
              348  LOAD_ATTR                search_param_values
              350  LOAD_FAST                'param'
              352  BINARY_SUBSCR    
              354  BUILD_TUPLE_2         2 
              356  BINARY_MODULO    
              358  STORE_FAST               'js_str'

 L. 677       360  LOAD_FAST                'self'
              362  LOAD_ATTR                webdriver
              364  LOAD_METHOD              execute_script
              366  LOAD_FAST                'js_str'
              368  CALL_METHOD_1         1  '1 positional argument'
              370  POP_TOP          
          372_374  JUMP_BACK           288  'to 288'
              376  POP_BLOCK        
            378_0  COME_FROM_LOOP      276  '276'
            378_1  COME_FROM           238  '238'

 L. 679       378  SETUP_EXCEPT        404  'to 404'

 L. 680       380  LOAD_FAST                'self'
              382  LOAD_ATTR                search_input
              384  LOAD_METHOD              send_keys
              386  LOAD_FAST                'self'
              388  LOAD_ATTR                query
              390  LOAD_GLOBAL              Keys
              392  LOAD_ATTR                ENTER
              394  BINARY_ADD       
              396  CALL_METHOD_1         1  '1 positional argument'
              398  POP_TOP          
              400  POP_BLOCK        
              402  JUMP_FORWARD        532  'to 532'
            404_0  COME_FROM_EXCEPT    378  '378'

 L. 681       404  DUP_TOP          
              406  LOAD_GLOBAL              ElementNotVisibleException
              408  COMPARE_OP               exception-match
          410_412  POP_JUMP_IF_FALSE   500  'to 500'
              414  POP_TOP          
              416  POP_TOP          
              418  POP_TOP          

 L. 682       420  LOAD_GLOBAL              time
              422  LOAD_METHOD              sleep
              424  LOAD_CONST               2
              426  CALL_METHOD_1         1  '1 positional argument'
              428  POP_TOP          

 L. 683       430  SETUP_EXCEPT        456  'to 456'

 L. 684       432  LOAD_FAST                'self'
              434  LOAD_ATTR                search_input
              436  LOAD_METHOD              send_keys
              438  LOAD_FAST                'self'
              440  LOAD_ATTR                query
              442  LOAD_GLOBAL              Keys
              444  LOAD_ATTR                ENTER
              446  BINARY_ADD       
              448  CALL_METHOD_1         1  '1 positional argument'
              450  POP_TOP          
              452  POP_BLOCK        
              454  JUMP_FORWARD        496  'to 496'
            456_0  COME_FROM_EXCEPT    430  '430'

 L. 685       456  DUP_TOP          
              458  LOAD_GLOBAL              Exception
              460  COMPARE_OP               exception-match
          462_464  POP_JUMP_IF_FALSE   494  'to 494'
              466  POP_TOP          
              468  POP_TOP          
              470  POP_TOP          

 L. 686       472  LOAD_GLOBAL              logger
              474  LOAD_METHOD              error
              476  LOAD_STR                 'send keys not possible, maybe page cannot loaded'
              478  CALL_METHOD_1         1  '1 positional argument'
              480  POP_TOP          

 L. 687       482  LOAD_FAST                'self'
              484  LOAD_METHOD              quit
              486  CALL_METHOD_0         0  '0 positional arguments'
              488  POP_TOP          
              490  POP_EXCEPT       
              492  JUMP_FORWARD        496  'to 496'
            494_0  COME_FROM           462  '462'
              494  END_FINALLY      
            496_0  COME_FROM           492  '492'
            496_1  COME_FROM           454  '454'
              496  POP_EXCEPT       
              498  JUMP_FORWARD        532  'to 532'
            500_0  COME_FROM           410  '410'

 L. 688       500  DUP_TOP          
              502  LOAD_GLOBAL              Exception
              504  COMPARE_OP               exception-match
          506_508  POP_JUMP_IF_FALSE   530  'to 530'
              510  POP_TOP          
              512  POP_TOP          
              514  POP_TOP          

 L. 689       516  LOAD_GLOBAL              logger
              518  LOAD_METHOD              error
              520  LOAD_STR                 'send keys not possible'
              522  CALL_METHOD_1         1  '1 positional argument'
              524  POP_TOP          

 L. 690       526  POP_EXCEPT       
              528  JUMP_FORWARD        532  'to 532'
            530_0  COME_FROM           506  '506'
              530  END_FINALLY      
            532_0  COME_FROM           528  '528'
            532_1  COME_FROM           498  '498'
            532_2  COME_FROM           402  '402'

 L. 692       532  LOAD_GLOBAL              datetime
              534  LOAD_ATTR                datetime
              536  LOAD_METHOD              utcnow
              538  CALL_METHOD_0         0  '0 positional arguments'
              540  LOAD_FAST                'self'
              542  STORE_ATTR               requested_at
              544  JUMP_FORWARD        568  'to 568'
            546_0  COME_FROM            76  '76'

 L. 694       546  LOAD_GLOBAL              logger
              548  LOAD_METHOD              debug
              550  LOAD_STR                 '{}: Cannot get handle to the input form for keyword {}.'
              552  LOAD_METHOD              format
              554  LOAD_FAST                'self'
              556  LOAD_ATTR                name
              558  LOAD_FAST                'self'
              560  LOAD_ATTR                query
              562  CALL_METHOD_2         2  '2 positional arguments'
              564  CALL_METHOD_1         1  '1 positional argument'
              566  POP_TOP          
            568_0  COME_FROM           544  '544'

 L. 696       568  LOAD_GLOBAL              super
              570  CALL_FUNCTION_0       0  '0 positional arguments'
              572  LOAD_METHOD              detection_prevention_sleep
              574  CALL_METHOD_0         0  '0 positional arguments'
              576  POP_TOP          

 L. 697       578  LOAD_GLOBAL              super
              580  CALL_FUNCTION_0       0  '0 positional arguments'
              582  LOAD_METHOD              keyword_info
              584  CALL_METHOD_0         0  '0 positional arguments'
              586  POP_TOP          

 L. 699   588_590  SETUP_LOOP          868  'to 868'
              592  LOAD_FAST                'self'
              594  LOAD_ATTR                pages_per_keyword
              596  GET_ITER         
            598_0  COME_FROM           856  '856'
            598_1  COME_FROM           820  '820'
          598_600  FOR_ITER            866  'to 866'
              602  LOAD_FAST                'self'
              604  STORE_ATTR               page_number

 L. 701       606  LOAD_FAST                'self'
              608  LOAD_METHOD              wait_until_serp_loaded
              610  CALL_METHOD_0         0  '0 positional arguments'
              612  POP_TOP          

 L. 703       614  SETUP_EXCEPT        670  'to 670'

 L. 704       616  LOAD_FAST                'self'
              618  LOAD_ATTR                config
              620  LOAD_METHOD              get
              622  LOAD_STR                 'screenshot'
              624  CALL_METHOD_1         1  '1 positional argument'
              626  LOAD_CONST               True
              628  COMPARE_OP               is
          630_632  POP_JUMP_IF_FALSE   652  'to 652'

 L. 705       634  LOAD_FAST                'self'
              636  LOAD_METHOD              _save_debug_screenshot
              638  CALL_METHOD_0         0  '0 positional arguments'
              640  POP_TOP          

 L. 706       642  LOAD_GLOBAL              time
              644  LOAD_METHOD              sleep
              646  LOAD_CONST               0.5
              648  CALL_METHOD_1         1  '1 positional argument'
              650  POP_TOP          
            652_0  COME_FROM           630  '630'

 L. 707       652  LOAD_FAST                'self'
              654  LOAD_ATTR                webdriver
              656  LOAD_METHOD              execute_script
              658  LOAD_STR                 'return document.body.innerHTML;'
              660  CALL_METHOD_1         1  '1 positional argument'
              662  LOAD_FAST                'self'
              664  STORE_ATTR               html
              666  POP_BLOCK        
              668  JUMP_FORWARD        796  'to 796'
            670_0  COME_FROM_EXCEPT    614  '614'

 L. 708       670  DUP_TOP          
              672  LOAD_GLOBAL              ConnectionError
              674  LOAD_GLOBAL              ConnectionRefusedError
              676  LOAD_GLOBAL              ConnectionResetError
              678  BUILD_TUPLE_3         3 
              680  COMPARE_OP               exception-match
          682_684  POP_JUMP_IF_FALSE   720  'to 720'
              686  POP_TOP          
              688  STORE_FAST               'err'
              690  POP_TOP          
              692  SETUP_FINALLY       708  'to 708'

 L. 709       694  LOAD_GLOBAL              logger
              696  LOAD_METHOD              error
              698  LOAD_FAST                'err'
              700  CALL_METHOD_1         1  '1 positional argument'
              702  POP_TOP          
              704  POP_BLOCK        
              706  LOAD_CONST               None
            708_0  COME_FROM_FINALLY   692  '692'
              708  LOAD_CONST               None
              710  STORE_FAST               'err'
              712  DELETE_FAST              'err'
              714  END_FINALLY      
              716  POP_EXCEPT       
              718  JUMP_FORWARD        796  'to 796'
            720_0  COME_FROM           682  '682'

 L. 710       720  DUP_TOP          
              722  LOAD_GLOBAL              WebDriverException
              724  COMPARE_OP               exception-match
          726_728  POP_JUMP_IF_FALSE   750  'to 750'
              730  POP_TOP          
              732  POP_TOP          
              734  POP_TOP          

 L. 711       736  LOAD_FAST                'self'
              738  LOAD_ATTR                webdriver
              740  LOAD_ATTR                page_source
              742  LOAD_FAST                'self'
              744  STORE_ATTR               html
              746  POP_EXCEPT       
              748  JUMP_FORWARD        796  'to 796'
            750_0  COME_FROM           726  '726'

 L. 712       750  DUP_TOP          
              752  LOAD_GLOBAL              Exception
              754  COMPARE_OP               exception-match
          756_758  POP_JUMP_IF_FALSE   794  'to 794'
              760  POP_TOP          
              762  STORE_FAST               'err'
              764  POP_TOP          
              766  SETUP_FINALLY       782  'to 782'

 L. 713       768  LOAD_GLOBAL              logger
              770  LOAD_METHOD              error
              772  LOAD_FAST                'err'
              774  CALL_METHOD_1         1  '1 positional argument'
              776  POP_TOP          
              778  POP_BLOCK        
              780  LOAD_CONST               None
            782_0  COME_FROM_FINALLY   766  '766'
              782  LOAD_CONST               None
              784  STORE_FAST               'err'
              786  DELETE_FAST              'err'
              788  END_FINALLY      
              790  POP_EXCEPT       
              792  JUMP_FORWARD        796  'to 796'
            794_0  COME_FROM           756  '756'
              794  END_FINALLY      
            796_0  COME_FROM           792  '792'
            796_1  COME_FROM           748  '748'
            796_2  COME_FROM           718  '718'
            796_3  COME_FROM           668  '668'

 L. 715       796  LOAD_GLOBAL              super
              798  CALL_FUNCTION_0       0  '0 positional arguments'
              800  LOAD_METHOD              after_search
              802  CALL_METHOD_0         0  '0 positional arguments'
              804  POP_TOP          

 L. 719       806  LOAD_FAST                'self'
              808  LOAD_ATTR                page_number
              810  LOAD_CONST               1
              812  BINARY_ADD       
              814  LOAD_FAST                'self'
              816  LOAD_ATTR                pages_per_keyword
              818  COMPARE_OP               in
          820_822  POP_JUMP_IF_FALSE   598  'to 598'

 L. 720       824  LOAD_GLOBAL              logger
              826  LOAD_METHOD              info
              828  LOAD_STR                 'Requesting the next page'
              830  CALL_METHOD_1         1  '1 positional argument'
              832  POP_TOP          

 L. 721       834  LOAD_FAST                'self'
              836  LOAD_METHOD              _goto_next_page
              838  CALL_METHOD_0         0  '0 positional arguments'
              840  STORE_FAST               'next_url'

 L. 722       842  LOAD_GLOBAL              datetime
              844  LOAD_ATTR                datetime
              846  LOAD_METHOD              utcnow
              848  CALL_METHOD_0         0  '0 positional arguments'
              850  LOAD_FAST                'self'
              852  STORE_ATTR               requested_at

 L. 724       854  LOAD_FAST                'next_url'
          856_858  POP_JUMP_IF_TRUE    598  'to 598'

 L. 725       860  BREAK_LOOP       
          862_864  JUMP_BACK           598  'to 598'
              866  POP_BLOCK        
            868_0  COME_FROM_LOOP      588  '588'

Parse error at or near `POP_BLOCK' instruction at offset 866

    def page_down(self):
        """Scrolls down a page with javascript.

        Used for next page in image search mode or when the
        next results are obtained by scrolling down a page.
        """
        js = 'window.scrollTo(0,document.body.scrollHeight);'
        time.sleep(5)
        self.webdriver.execute_script(js)

    def run(self):
        for self.query, self.pages_per_keyword in self.jobs.items():
            self._set_xvfb_display()
            if not self._get_webdriver():
                raise Exception('{}: Aborting due to no available selenium webdriver.'.format(self.name))
            try:
                x = randint(800, 1024)
                y = randint(600, 900)
                self.webdriver.set_window_size(x, y)
                self.webdriver.set_window_position(x * (self.browser_num % 4), randint(1, 10))
            except WebDriverException as e:
                try:
                    logger.error('Cannot set window size: {}'.format(e))
                finally:
                    e = None
                    del e

            super().before_search()
            if self.startable:
                self.build_search()
                self.search()
            self.quit()

    def quit(self):
        if self.webdriver:
            self.webdriver.close()
            self.webdriver.quit()


class DuckduckgoSelScrape(SelScrape):
    __doc__ = "\n    Duckduckgo is a little special since new results are obtained by ajax.\n    next page thus is then to scroll down.\n\n    Furthermore duckduckgo.com doesn't seem to work with Phantomjs. Maybe they block it, but I\n    don't know how ??!\n\n    It cannot be the User-Agent, because I already tried this.\n    "

    def __init__(self, *args, **kwargs):
        (SelScrape.__init__)(self, *args, **kwargs)
        self.largest_id = 0

    def _goto_next_page(self):
        super().page_down()
        return 'No more results' not in self.html

    def wait_until_serp_loaded(self):
        super()._wait_until_search_input_field_appears()


class AskSelScrape(SelScrape):

    def __init__(self, *args, **kwargs):
        (SelScrape.__init__)(self, *args, **kwargs)

    def wait_until_serp_loaded(self):

        def wait_until_keyword_in_url(driver):
            try:
                return quote(self.query) in driver.current_url or self.query.replace(' ', '+') in driver.current_url
            except WebDriverException:
                pass

        WebDriverWait(self.webdriver, 5).until(wait_until_keyword_in_url)