# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/whatsappy/_whatsappy.py
# Compiled at: 2019-11-13 11:25:24
# Size of source mod 2**32: 4968 bytes
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import sys, re, datetime
from dataclasses import dataclass
this = sys.modules[__name__]
this.browser = None

def run():
    """Function to initialize webdriver and go to web.whatsapp.com"""
    this.browser = webdriver.Firefox()
    this.browser.get('https://web.whatsapp.com/')
    input('Scan QR Code with mobile Whatsapp Application and then press any key.')


def send_message(chat: str, message: str) -> bool:
    """Simple function to send 'message' to user/group 'chat'."""
    if not check_browser_initialized():
        return
    else:
        return open_chat(chat) or None
    msg_box_candidates = this.browser.find_elements_by_xpath('//div[contains(concat(" ", normalize-space(@class), " "), " selectable-text ")]')
    msg_box = None
    for element in msg_box_candidates:
        if element.get_attribute('contenteditable'):
            msg_box = element
            break

    if msg_box is None:
        return
    msg_box.send_keys(message)
    msg_box.send_keys(webdriver.common.keys.Keys.ENTER)


def read_messages(minimal_timestamp=0):
    main_element = this.browser.find_element_by_id('main')
    chat_elements = main_element.find_elements_by_xpath('div/div/div/div/div')
    chat_elements.reverse()
    for chat_element in chat_elements:
        chatbox = identify_chat_element(chat_element)
        if chatbox:
            if chatbox.timestamp < minimal_timestamp:
                break
            print(chatbox.timestamp, chatbox.sender, chatbox.message)


def check_browser_initialized() -> bool:
    """Check if run() has been called and webdriver is initalized"""
    is_initialized = this.browser is not None
    if not is_initialized:
        print('Tried to execute a command before browser was initialized. Execute whatsappy.run() first.')
    return is_initialized


def open_chat(chat_name: str) -> bool:
    """Convenience function to open chat with user/group 'chat_name'
  
  Looks for chat_name by checking if <span> with said title can be found.
  If yes, the name is clicked and thereby the chat opened. 
  If no, an message is printed accordingly and False is returned"""
    if not check_browser_initialized():
        return
    try:
        chat = this.browser.find_element_by_xpath(f'//span[@title = "{chat_name}"]')
        chat.click()
        return True
    except NoSuchElementException:
        print(f'User/Group with name "{chat_name}" not found.')
        return False


def read_source_code() -> str:
    """Get the source code of the current view"""
    return this.browser.page_source


def get_new_messages():
    """Read new messages from all groups/users that were received"""
    number_pattern = re.compile('\\d+')
    candidates = this.browser.find_elements_by_xpath('//div/span/div/span')
    new_message_elements = []
    for element in candidates:
        match = number_pattern.match(element.text)
        if match:
            new_message_elements.append(new_message_elements)

    if len(new_message_elements) == 0:
        return


@dataclass
class ChatBox:
    sender: str
    timestamp: int
    message: str
    is_incoming_message: bool


def identify_chat_element(chat_element):
    is_incoming_message = False
    chat_element_class = chat_element.get_attribute('class')
    if 'message-in' in chat_element_class:
        is_incoming_message = True
    else:
        if 'message-out' in chat_element_class:
            is_incoming_message = False
        else:
            return
    try:
        chat_childs = chat_element.find_elements_by_xpath('div/div/div/div')
    except NoSuchElementException:
        return
    else:
        text_containing_child = None
        timestamp_name = None
        for chat_child in chat_childs:
            timestamp_name = chat_child.get_attribute('data-pre-plain-text')
            if timestamp_name:
                text_containing_child = chat_child
                break

        if text_containing_child is None:
            return
        chat_text = None
        try:
            chat_text = text_containing_child.find_element_by_xpath('div/span/span')
        except NoSuchElementException:
            return
        else:
            message = chat_text.text
            matchObj = re.match('\\[(\\d{2}:\\d{2}), (\\d+.\\d+.\\d+)\\] (\\D+):', timestamp_name)
            time = matchObj.group(1)
            date = matchObj.group(2)
            sender = matchObj.group(3)
            timestamp = datetime.datetime.strptime(date + ' ' + time, '%d.%m.%Y %H:%M').timestamp()
            chatbox = ChatBox(sender, timestamp, message, is_incoming_message)
            return chatbox