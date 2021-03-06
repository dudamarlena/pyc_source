# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: bzt/resources/selenium_extras.py
# Compiled at: 2020-03-01 07:17:27
from selenium.common.exceptions import NoSuchWindowException, NoSuchFrameException, NoSuchElementException
from apiritif import get_transaction_handlers, set_transaction_handlers, get_from_thread_store
from selenium.webdriver.common.by import By

def add_flow_markers():
    handlers = get_transaction_handlers()
    handlers['enter'].append(_send_start_flow_marker)
    handlers['exit'].append(_send_exit_flow_marker)
    set_transaction_handlers(handlers)


def _send_marker(stage, params):
    driver = get_from_thread_store('driver')
    driver.execute_script('/* FLOW_MARKER test-case-%s */' % stage, params)


def _send_start_flow_marker(test_case, test_suite):
    _send_marker('start', {'testCaseName': test_case, 'testSuiteName': test_suite})


def _send_exit_flow_marker(status, message):
    _send_marker('stop', {'status': status, 'message': message})


class FrameManager:

    def __init__(self, driver):
        self.driver = driver

    def switch(self, frame_name=None):
        try:
            if not frame_name or frame_name == 'relative=top':
                self.driver.switch_to_default_content()
            elif frame_name.startswith('index='):
                self.driver.switch_to.frame(int(frame_name.split('=')[1]))
            elif frame_name == 'relative=parent':
                self.driver.switch_to.parent_frame()
            else:
                self.driver.switch_to.frame(frame_name)
        except NoSuchFrameException:
            raise NoSuchFrameException('Invalid Frame ID: %s' % frame_name)


class WindowManager:

    def __init__(self, driver):
        self.driver = driver
        self.windows = {}

    def switch(self, window_name=None):
        try:
            if not window_name:
                self.driver.switch_to.window(self.driver.window_handles[(-1)])
            elif window_name.isdigit():
                self._switch_by_idx(int(window_name))
            elif window_name.startswith('win_ser_'):
                self._switch_by_win_ser(window_name)
            else:
                self.driver.switch_to.window(window_name)
        except NoSuchWindowException:
            raise NoSuchWindowException('Invalid Window ID: %s' % window_name)

    def _switch_by_idx(self, win_index):
        wnd_handlers = self.driver.window_handles
        if len(wnd_handlers) <= win_index and win_index >= 0:
            self.driver.switch_to.window(wnd_handlers[win_index])
        else:
            raise NoSuchWindowException('Invalid Window ID: %s' % str(win_index))

    def _switch_by_win_ser(self, window_name):
        if window_name == 'win_ser_local':
            wnd_handlers = self.driver.window_handles
            if len(wnd_handlers) > 0:
                self.driver.switch_to.window(wnd_handlers[0])
            else:
                raise NoSuchWindowException('Invalid Window ID: %s' % window_name)
        else:
            if window_name not in self.windows:
                self.windows[window_name] = self.driver.window_handles[(-1)]
            self.driver.switch_to.window(self.windows[window_name])

    def close(self, window_name=None):
        if window_name:
            self.switch(window_name)
        self.driver.close()


class LocatorsManager:
    BYS = {'xpath': By.XPATH, 
       'css': By.CSS_SELECTOR, 
       'name': By.NAME, 
       'id': By.ID, 
       'linktext': By.LINK_TEXT}

    def __init__(self, driver, timeout=30):
        self.driver = driver
        self.timeout = timeout

    def get_locator(self, locators):
        """
        :param locators: List of Dictionaries holding the locators, e.g. [{'id': 'elem_id'},
        {css: 'my_cls'}]
        :return: first valid locator from the passed List, if no locator is valid then returns the
        first one
        """
        first_locator = None
        for locator in locators:
            locator_type = list(locator.keys())[0]
            locator_value = locator[locator_type]
            if not first_locator:
                first_locator = (
                 self.BYS[locator_type.lower()], locator_value)
            else:
                self.driver.implicitly_wait(0)
            elements = self.driver.find_elements(self.BYS[locator_type.lower()], locator_value)
            if len(elements) > 0:
                locator = (
                 self.BYS[locator_type.lower()], locator_value)
                break
        else:
            self.driver.implicitly_wait(self.timeout)
            msg = 'Element not found: (%s, %s)' % first_locator
            raise NoSuchElementException(msg)

        self.driver.implicitly_wait(self.timeout)
        return locator