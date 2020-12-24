# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\PyCharm Projects\NCryptoClient\NCryptoClient\UI\ui_chat_tab.py
# Compiled at: 2018-04-19 15:37:38
# Size of source mod 2**32: 7274 bytes
"""
Module which implements Chat area implemented as a QtabWidget.
"""
import datetime
from queue import Queue
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from NCryptoTools.Tools.utilities import get_formatted_date
from NCryptoTools.JIM.jim import JIMManager
from NCryptoTools.JIM.jim_base import JSONObjectType

class UiChat(QTabWidget):
    __doc__ = '\n    Widget-class which has a set of tabs, each of which is a separate chat.\n    '

    def __init__(self, parent=None):
        """
        Constructor. Initializes chat, creating an empty window without tabs.
        @param parent: parent window.
        """
        super().__init__(parent)
        self.parent = parent
        self.setGeometry(328, 64, 664, 816)
        self.setObjectName('chat_tw')
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_chat_tab)
        self.show()

    def add_chat_tab(self, chat_name):
        """
        Adds tab in the chat widget.
        @param chat_name: chat name.
        @return: -
        """
        tabs_amount = self.count()
        if self.count() == 0:
            self.show()
            chat_widget = UiChatTab(chat_name, self)
            self.addTab(chat_widget, chat_name)
            self.setCurrentIndex(0)
            chat_widget.show()
        else:
            index = self.find_tab(chat_name)
            if index is None:
                chat_widget = UiChatTab(chat_name, self)
                self.addTab(chat_widget, chat_name)
                self.setCurrentIndex(tabs_amount)
                chat_widget.show()
            else:
                self.setCurrentIndex(index)

    def close_chat_tab_by_name(self, tab_name):
        """
        Deletes tab by its name.
        @param tab_name: tab name (chat name).
        @return: -
        """
        index = self.find_tab(tab_name)
        self.close_chat_tab(index)

    def close_chat_tab(self, index):
        """
        Deletes tab by its index.
        @param index: tab index.
        @return: -
        """
        if index is not None:
            self.removeTab(index)
        if self.count() == 0:
            self.hide()
            self.parent.select_chat_st.show()

    def find_tab(self, tab_name):
        """
        Tries to to find the tab with needed name.
        @param tab_name: tab name (chat name).
        @return: tab index.
        """
        tabs_amount = self.count()
        if tabs_amount == 1:
            if self.widget(0).tab_name == tab_name:
                return 0
            else:
                return
        for i in range(0, tabs_amount):
            if self.widget(i).tab_name == tab_name:
                return i

    def add_tab_data(self, tab_index, data):
        """
        Adds new message (data) to the needed tab. This function is used
        when needs to load messages from history.
        @param tab_index: tab index.
        @param data: new data (message).
        @return: -
        """
        self.widget(tab_index).add_data(data)

    def add_tab_data_from_buffer(self, tab_index):
        """
        Adds new message (data) to the needed tab from the tab's internal
        buffer. This function is used when the current user sends messages.
        @param tab_index: tab index.
        @return: -
        """
        self.widget(tab_index).add_data_from_buffer()

    def remove_tab_data(self, tab_index, data):
        """
        Deletes row from the needed searching it by data.
        @param tab_index: tab index.
        @param data: data to be searched.
        @return: -
        """
        tab = self.widget(tab_index)
        row = tab.find_row(data)
        tab.remove_data(row)


class UiChatTab(QWidget):
    __doc__ = '\n    Since we use a set of widgets placing them on each tab,\n    we need a custom widget to group them. This class groups\n    tab widgets in oneself.\n    '

    def __init__(self, tab_name, parent=None):
        super().__init__(parent)
        self.parent = parent
        self._message_queue = Queue(30)
        self.tab_name = tab_name
        self._chat_lb = QListWidget(self)
        self._chat_lb.setGeometry(QRect(8, 8, 640, 744))
        self._chat_lb.setResizeMode(QListView.Adjust)
        self._chat_lb.setObjectName(tab_name + '_contacts_lb')
        self._msg_le = QLineEdit(self)
        self._msg_le.setGeometry(QRect(8, 760, 568, 24))
        self._msg_le.setMaxLength(128)
        self._msg_le.setAlignment(Qt.AlignLeft)
        self._msg_le.setObjectName(tab_name + '_msg_le')
        self._send_pb = QPushButton(self)
        self._send_pb.setText('Send')
        self._send_pb.setGeometry(QRect(584, 760, 64, 24))
        self._send_pb.setObjectName(tab_name + '_send_pb')
        self._send_pb.clicked.connect(self._send_msg)

    def _send_msg(self):
        """
        Sends message to the server when "Send" button is being pressed.
        @return: -
        """
        msg_text = self._msg_le.text()
        recipient = self.tab_name
        login = self.parent.parent.get_login()
        unix_time = datetime.datetime.now().timestamp()
        if recipient.startswith('#'):
            msg = JIMManager.create_jim_object(JSONObjectType.TO_SERVER_CHAT_MSG, unix_time, recipient, login, msg_text)
        else:
            msg = JIMManager.create_jim_object(JSONObjectType.TO_SERVER_PERSONAL_MSG, unix_time, recipient, login, 'utf-8', msg_text)
        self.parent.parent.msg_handler.write_to_output_buffer(msg.to_dict())
        msg_str = '[{}] @{}> {}'.format(get_formatted_date(unix_time), login, msg_text)
        self._message_queue.put(msg_str)

    def add_data(self, data):
        """
        Adds new data from the external buffer.
        @param data: new data (message).
        @return: -
        """
        self._chat_lb.addItem(data)

    def add_data_from_buffer(self):
        """
        Adds new data from the internal buffer. This function is being called
        only after receving server answer that out message has been successfully
        received by user.
        @return: -
        """
        self._msg_le.clear()
        message = self._message_queue.get()
        self._chat_lb.addItem(message)