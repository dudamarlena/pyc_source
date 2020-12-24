# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/html/pip.hannm.com/wikicivi-wcc-python-sdk/wcc/req.py
# Compiled at: 2019-01-03 03:00:11
# Size of source mod 2**32: 15954 bytes
"""
代码较多的依赖requests
参考文档：http://docs.python-requests.org/zh_CN/latest/user/quickstart.html
"""
import re, requests, time, chardet, traceback, json, os, random
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from .proxy import get_proxy

def getpage(url, **kwargs):
    """
    使用get方式获取url对应的网页源码,如果是访问接口的话，返回是json字符串.
    :param url: 网页的url 
    :param headers: 请求头,默认从请求头库中随机选择一个
    :param timeout: 超时时间，默认是10s
    :param use_proxy: 是否使用代理，默认为True
    :param browser: 是否使用浏览器，默认为None，可选择chrome/firefox/None
    :param params: GET请求附带的参数，requests会把这个字典的params做成?k1=v1&k2=v2形式发送出去.
    :param payload: POST请求附带的参数.
    :param http_method: GET/POST/PUT/DELETE,必须接口
    :param use_ssl: 使用浏览器时是否使用ssl.
    :param wait: 浏览器的等待时间.
    :param cookies: 访问时的cookies.
    :return:经过渲染之后的网页源代码，是一个字符串
    """
    DEFAULT_TIMEOUT = 60
    MAX_TRY_COUNT = 1
    headers = kwargs['headers'] if 'headers' in kwargs else {'User-Agent': getua()}
    timeout = kwargs['timeout'] if 'timeout' in kwargs else DEFAULT_TIMEOUT
    use_proxy = kwargs['use_proxy'] if 'use_proxy' in kwargs else False
    browser = kwargs['browser'] if 'browser' in kwargs else None
    params = kwargs['params'] if 'params' in kwargs else None
    payload = kwargs['payload'] if 'payload' in kwargs else None
    http_method = kwargs['http_method'] if 'http_method' in kwargs else 'GET'
    use_ssl = kwargs['use_ssl'] if 'use_ssl' in kwargs else False
    wait = kwargs['wait'] if 'wait' in kwargs else 0.5
    cookies = kwargs['cookies'] if 'cookies' in kwargs else None
    encoding = kwargs['encoding'] if 'encoding' in kwargs else None
    MAX_TRY_COUNT = int(kwargs['max_try']) if 'max_try' in kwargs else 1
    if cookies != None:
        cookies = json.loads(cookies)
    resp_text = ''
    resp_content = ''
    error_text = 'error'
    resp_status_code = 200
    try_count = 0
    error_flag = False
    for k in range(0, MAX_TRY_COUNT):
        try:
            requests_params = {}
            requests_params['headers'] = headers
            if timeout:
                requests_params['timeout'] = timeout
            if cookies is not None:
                requests_params['cookies'] = cookies
            if browser == 'chrome' or browser == 'firefox':
                requests_params['wait'] = wait
                if use_ssl:
                    requests_params['use_ssl'] = True
                if use_proxy:
                    proxy_iport = get_proxy(use_proxy)
                    if proxy_iport[0]:
                        requests_params['use_proxy'] = True
                        requests_params['proxy_ip'] = proxy_iport[0]
                        requests_params['proxy_port'] = proxy_iport[1]
                    else:
                        print('no proxy')
                        return
                if params:
                    requests_params['params'] = params
                if payload:
                    requests_params['data'] = payload
            else:
                if use_proxy:
                    proxy_iport = get_proxy(use_proxy)
                    if proxy_iport[0]:
                        proxy_http = 'http://' + proxy_iport[0] + ':' + str(proxy_iport[1])
                        proxy_https = 'https://' + proxy_iport[0] + ':' + str(proxy_iport[1])
                        requests_params['proxies'] = {'http':proxy_http,  'https':proxy_https}
                    else:
                        print('no proxy')
                        return
                if params:
                    requests_params['params'] = params
            if payload:
                requests_params['data'] = payload
            if browser == 'chrome':
                resp_status_code, resp_text = getpage_browser_chrome(url, **requests_params)
            else:
                if browser == 'firefox':
                    resp_status_code, resp_text = getpage_browser_firefox(url, **requests_params)
                else:
                    if http_method == 'GET':
                        resp = (requests.get)(url, **requests_params)
                        resp_status_code = resp.status_code
                        resp_text = resp.text
                        resp_content = resp.content
                    else:
                        if http_method == 'POST':
                            resp = (requests.post)(url, **requests_params)
                            resp_status_code = resp.status_code
                            resp_text = resp.text
                            resp_content = resp.content
                        else:
                            error_text = '不可预料的HTTP_METHOD'
                            print('url ' + error_text)
                            break
            if resp_status_code != 200:
                error_flag = True
                error_text = 'resp_status_code ' + str(resp_status_code)
                if resp_status_code == 503:
                    error_text = '503错误,您的IP可能被封'
                if resp_status_code == 504:
                    error_text = '504错误,您的IP可能被封'
                if resp_status_code == 405:
                    error_text = '405错误,您的方法是' + http_method
                time.sleep(0.5 * k)
                continue
            else:
                error_flag = False
                try_count = k
                break
        except requests.exceptions.ConnectTimeout:
            error_flag = True
            error_text = 'requests.exceptions.ConnectTimeout'
        except requests.exceptions.Timeout:
            error_flag = True
            error_text = 'requests.exceptions.Timeout:'
        except Exception as err:
            try:
                print(traceback.format_exc())
                error_flag = True
                error_text = str(err)
                print(url + ' error ' + error_text[:40])
            finally:
                err = None
                del err

        try_count = k

    if error_flag:
        print(url + ' error ' + '(' + str(try_count) + ' th)  ' + error_text[:40])
        return
    if encoding:
        resp_text = resp_content.decode(encoding)
    return resp_text


def getpage_browser_firefox(url, **kwargs):
    """
    使用火狐浏览器打开url并获取网页源码
    :param url:网页的url 
    :param use_proxy:是否使用代理，默认为True 
    :param user_agent:请求头的User_Agent，默认从请求头配置库中随机选择一个 
    :param wait:渲染页面的等待时间，默认是0.5
    :return:经过渲染之后的网页源代码，是一个字符串
    """
    use_proxy = kwargs['use_proxy'] if 'use_proxy' in kwargs else False
    user_agent = kwargs['user_agent'] if 'user_agent' in kwargs else getua()
    wait = kwargs['wait'] if 'wait' in kwargs else 0.5
    use_ssl = kwargs['use_ssl'] if 'use_ssl' in kwargs else False
    profile = FirefoxProfile()
    if use_proxy:
        profile.set_preference('network.proxy.type', 1)
        profile.set_preference('network.proxy.http', kwargs['proxy_ip'])
        profile.set_preference('network.proxy.http_port', kwargs['proxy_port'])
        if use_ssl:
            if url[0:6] == 'https:':
                profile.set_preference('network.proxy.ssl', ip)
                profile.set_preference('network.proxy.ssl_port', port)
        profile.set_preference('network.proxy.share_proxy_settings', True)
        profile.update_preferences()
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('user-agent=' + user_agent)
    resp_status_code = 0
    resp_text = ''
    try:
        browser = webdriver.Firefox(profile, options=options)
        browser.get(url)
        time.sleep(wait)
        resp_text = browser.page_source
    except Exception as err:
        try:
            print('打开浏览器失败:' + str(err))
        finally:
            err = None
            del err

    browser.quit()
    return (
     200 if resp_text else None, resp_text)


def getpage_browser_chrome(url, **kwargs):
    """
    使用谷歌浏览器打开url并获取网页源码
    浏览器暂时不支持referer，selenium不支持referer
    如果确实需要，就必须使用一个新的工具：browsermob-proxy
    这个工具的开源地址是：https://github.com/webmetrics/browsermob-proxy
    :param url:网页的url 
    :param use_proxy:是否使用代理，默认为True 
    :param user_agent:请求头的User_Agent，默认从请求头配置库中随机选择一个 
    :param wait:渲染页面的等待时间，默认是0.5
    :param cookies:访问网站时的cookies
    :return:经过渲染之后的网页源代码，是一个字符串
    """
    use_proxy = kwargs['use_proxy'] if 'use_proxy' in kwargs else False
    wait = kwargs['wait'] if 'wait' in kwargs else 0.5
    use_ssl = kwargs['use_ssl'] if 'use_ssl' in kwargs else False
    cookies = kwargs['cookies'] if 'cookies' in kwargs else None
    timeout = kwargs['timeout'] if 'timeout' in kwargs else 60
    user_agent = kwargs['headers']['User-Agent'] if ('headers' in kwargs and 'User-Agent' in kwargs['headers']) else None
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        PROXY = kwargs['proxy_ip'] + ':' + str(kwargs['proxy_port'])
        chrome_options.add_argument('--proxy-server={0}'.format(PROXY))
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    if user_agent:
        chrome_options.add_argument('user-agent=' + user_agent)
    resp_text = ''
    try:
        try:
            browser = webdriver.Chrome(options=chrome_options)
            browser.set_page_load_timeout(timeout)
            browser.get(url)
            cookiesList = []
            if cookies:
                for cookieName, cookieValue in cookies.items():
                    cookie_item = {}
                    cookie_item['name'] = cookieName
                    cookie_item['value'] = cookieValue
                    cookiesList.append(cookie_item)
                    browser.add_cookie(cookie_item)

                browser.refresh()
            time.sleep(wait)
            resp_text = browser.page_source
        except Exception as err:
            try:
                print('打开浏览器失败:' + str(err))
            finally:
                err = None
                del err

    finally:
        browser.quit()

    return (
     200 if resp_text else None, resp_text)


def getcookie(url, **kwargs):
    """
    使用谷歌浏览器打开url并获取网页cookie
    :param url:网页的url 
    :param use_proxy:是否使用代理，默认为True 
    :param user_agent:请求头的User_Agent，默认从请求头配置库中随机选择一个 
    :param wait:渲染页面的等待时间，默认是0.5
    :return:经过渲染之后的网页源代码，是一个字符串
    """
    use_proxy = kwargs['use_proxy'] if 'use_proxy' in kwargs else False
    user_agent = kwargs['User-Agent'] if 'User-Agent' in kwargs else getua()
    wait = kwargs['wait'] if 'wait' in kwargs else 0.5
    use_ssl = kwargs['use_ssl'] if 'use_ssl' in kwargs else False
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        proxy_iport = get_proxy(use_proxy)
        if not proxy_iport[0]:
            return
        if proxy_iport[0]:
            proxy_ip = proxy_iport[0]
            proxy_port = proxy_iport[1]
            PROXY = proxy_ip + ':' + str(proxy_port)
            chrome_options.add_argument('--proxy-server={0}'.format(PROXY))
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('user-agent=' + user_agent)
    cookie_str = ''
    try:
        browser = webdriver.Chrome(options=chrome_options)
        browser.get(url)
        cookie_items = browser.get_cookies()
        post = {}
        for cookie_item in cookie_items:
            post[cookie_item['name']] = cookie_item['value']

        cookie_str = json.dumps(post)
    except Exception as err:
        try:
            print('打开浏览器失败:' + str(err))
        finally:
            err = None
            del err

    browser.quit()
    return cookie_str


def getua(path='user_agents.json'):
    """
    从配置文件user_agents.json中随机获取一个User_Agent
    :return:一个随机获取的User_Agent字符串
    """
    current_path = os.path.abspath(os.path.dirname(__file__))
    json_path = os.path.join(current_path, path)
    try:
        with open(json_path, 'r', encoding='utf-8') as (f):
            user_agents = json.load(f)
            num = random.randint(0, len(user_agents) - 1)
            return user_agents[num]
    except:
        print('打开配置文件失败')
        return