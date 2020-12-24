# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanghunkang/dev/aascraw/venv/lib/python3.7/site-packages/aascraw/deliverer.py
# Compiled at: 2019-08-24 10:36:46
# Size of source mod 2**32: 5559 bytes
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
chrome_options = Options()
chrome_options.add_argument('--headless')

def find_all_event_listeners(preceding_xpath, element):
    elements = element.find_elements_by_xpath('./*')
    if len(elements) == 0:
        return [f"{preceding_xpath}-{element.tag_name}"]
    event_listeners = []
    for element in elements:
        print(f"{preceding_xpath}-{element.tag_name}")
        event_listeners = event_listeners + find_all_event_listeners(f"{preceding_xpath}-{element.tag_name}", element)

    return event_listeners


def find_all_hrefs(element):
    actions = []
    elements = element.find_elements_by_xpath('//a[@href]')
    for element in elements:
        href = element.get_attribute('href')
        actions.append(f"HREF::{href}")

    return actions


def parse_get_params(url):
    get_params = {}
    for pair in url.split('?')[1].split('&'):
        get_params[pair.split('=')[0]] = pair.split('=')[1]

    return get_params


def find_get_params_candidates(url):
    actions = []
    get_params = parse_get_params(url)
    for param_name, param_value in get_params.items():
        try:
            int(value)
            actions.append(f"GET_PARAMS::++>{param_name}")
        except:
            actions.append(f"GET_PARAMS::OTHER_OPERATION>{param_name}")

    return actions


def format_url(url, action):
    operator = action.split('>')[0]
    param = action.split('>')[1]
    get_params = parse_get_params(url)
    param_value = get_params[param]
    if operator == '++':
        param_value = (f"{int(param_value) + 1}").rjust('0', len(param_value))
    elif operator == '--':
        param_value = (f"{int(param_value) - 1}").rjust('0', len(param_value))
    elif operator == 'OTHER_OPERATION':
        pass
    else:
        raise Exception('Update operation undefined')
    return re.sub('&' + param + '=.+', '&', url) + f"&{param}={param_value}"


class Deliverer:

    def __init__(self, entry_point):
        super().__init__()
        self.new_action_default_rank = 0
        self.sum_rank = 0
        self.driver = webdriver.PhantomJS('./drivers/phantomjs')
        self.state = {'actions_taken':'', 
         'page':''}
        self.actions = {f"href::{entry_point}": {'action_type':'HREF', 
                                  'rank':self.new_action_default_rank, 
                                  'url':entry_point}}

    def proceed(self):
        action = self._Deliverer__randomly_select_action()
        if action['action_type'] == 'HREF':
            self.driver.get(action)
        elif action['action_type'] == 'GET_PARAM':
            self.url = format_url(self.url, action)
            self.driver.get(self.url)
        elif action['action_type'] == 'EVENT':
            pass
        self.state = {'action_taken':action, 
         'page':self.driver.execute_script('return document.documentElement.outerHTML;')}

    def __randomly_select_action(self):
        for _, action in self.actions.items():
            return action

    def __sort_actions(self):
        self.actions = sorted((self.actions), key=(lambda key, rank: rank))

    def update_action_space(self):
        print('This function will look for possible event triggers and get queries')
        for href in find_all_hrefs(self.page):
            if href not in self.actions:
                self.actions[href] = self.new_action_default_rank

        for param in find_get_params_candidates(self.driver.current_url):
            if param not in self.actions:
                self.actions[param] = self.new_action_default_rank

    def update_policy(self, rank_deltas):
        for rank_delta in rank_deltas:
            self.actions[rank_delta[0]][1] += rank_delta[1]
            self.sum_rank += rank_delta[1]

        self._Deliverer__sort_actions()