# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/clipon/history.py
# Compiled at: 2016-06-17 03:52:51
# Size of source mod 2**32: 9390 bytes
from __future__ import absolute_import
import sys, os
from time import time as sys_time
from gi.repository.GLib import get_user_data_dir
import helper
from helper import logger, INT_MAX, format_pretty
from defines import CLIPON_VERSION
from xml.dom import minidom
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class ClipHistory:
    """ClipHistory"""
    history = []
    ps_history = None
    cfg = None

    def __init__(self, cfg):
        self.cfg = cfg
        self.cfg.set_method('autosave', self.set_autosave)
        self.cfg.set_method('max_length', self.set_max_length)
        self.cfg.set_method('max_entry', self.set_max_entry)
        self.ps_history = PersistentHistory()
        self.ps_history.load_all(self.history)

    def add_entry(self, entry):
        max_entry = self.cfg.get_value('max_entry')
        if self.size() >= max_entry:
            self.del_entry(0)
        self.history.append(entry)
        if self.cfg.get_value('autosave'):
            self.ps_history.save_entry(entry)

    def add_text(self, text):
        max_length = self.cfg.get_value('max_length')
        if len(text) > max_length:
            text = text[0:max_length]
        text = text + '\n'
        entry = ClipEntry(text)
        self.add_entry(entry)

    def del_entry(self, index):
        self.history.pop(index)
        if self.cfg.get_value('autosave'):
            self.save()

    def del_range(self, start, end):
        if start < 0 or start >= self.size() or start > end:
            return
        if end > self.size():
            end = self.size()
        self.history = self.history[0:start] + self.history[end:self.size()]
        if self.cfg.get_value('autosave'):
            self.save()

    def clear(self):
        self.history.clear()
        if self.cfg.get_value('autosave'):
            self.ps_history.delete_all()
        logger.info('Cleared history')

    def get_entry(self, index):
        entry = self.history[index] if index < len(self.history) else None
        return entry

    def size(self):
        return len(self.history)

    def info(self):
        info = {}
        info['size'] = self.size()
        info['autosave'] = self.cfg.get_value('autosave')
        info['max_length'] = self.cfg.get_value('max_length')
        info['max_entry'] = self.cfg.get_value('max_entry')
        ps_info = self.ps_history.info()
        for k, v in ps_info.items():
            info[k] = v

        return info

    def save(self, start=0, end=INT_MAX):
        if end == INT_MAX:
            end = self.size()
        if start < 0 or end > self.size() or start >= end:
            return
        self.ps_history.delete_all()
        hist = self.history[start:end]
        for entry in hist:
            self.ps_history.save_entry(entry)

        logger.info('Saved history')

    def set_autosave(self, autosave):
        if bool(autosave):
            self.save()
        self.cfg.set_value('autosave', bool(autosave))
        return True

    def set_max_entry(self, num):
        if num <= 0:
            return False
        diff = self.size() - num
        if diff > 0:
            self.del_range(0, diff)
        self.cfg.set_value('max_entry', num)
        return True

    def set_max_length(self, num):
        if num <= 0:
            return False
        self.cfg.set_value('max_length', num)
        return True


class PersistentHistory:
    """PersistentHistory"""
    data_dir = None
    data_file = None
    data_fd = None
    meta_file = None
    meta_man = None

    def __init__(self):
        self.data_dir = get_user_data_dir()
        self.data_dir = os.path.join(self.data_dir, 'clipon')
        self.data_file = os.path.join(self.data_dir, 'history.txt')
        self.data_fd = helper.open_file(self.data_dir, self.data_file, 'r+')
        if self.data_fd is None:
            raise Exception('Failed to open data file')
        self.meta_file = os.path.join(self.data_dir, 'clipon.xml')
        self.meta_fd = helper.open_file(self.data_dir, self.meta_file, 'r+')
        if self.meta_fd is None:
            raise Exception('Failed to open meta file')
        self.meta_man = MetaManager(self.meta_file)

    def save_entry(self, entry):
        entry.offset = self.data_fd.seek(0, 2)
        entry.length = len(entry.text)
        try:
            self.data_fd.seek(entry.offset, 0)
            self.data_fd.write(entry.text)
            self.data_fd.flush()
        except:
            logging.error('Write error when saving entry\n')
            return

        attrs = {'time': entry.time, 'offset': entry.offset, 'length': entry.length}
        elem = self.meta_man.new_element('clip', attrs)
        self.meta_man.add_element(elem)

    def load_entry(self, index):
        attrs = self.meta_man.get_element('clip', index)
        if attrs is None:
            return
        try:
            offset = attrs['offset']
            length = attrs['length']
            time = attrs['time']
        except KeyError:
            logging.error('Element attribute error')
            return

        offset = int(offset)
        length = int(length)
        time = float(time)
        text = None
        try:
            self.data_fd.seek(offset, 0)
            text = self.data_fd.read(length)
        except:
            logging.error('Read error at offset %d length %d\n' % (int(offset), int(length)))
            return

        entry = ClipEntry(text, float(time), int(offset), int(length))
        return entry

    def load_all(self, entry_list):
        fsize = 0
        num = self.meta_man.size()
        for i in range(num):
            entry = self.load_entry(i)
            if entry is not None:
                entry_list.append(entry)
                if entry.offset + entry.length > fsize:
                    fsize = entry.offset + entry.length

        self.data_fd.truncate(fsize)
        self.data_fd.flush()

    def delete_entry(self, entry, index):
        pass

    def delete_all(self):
        self.meta_man.del_all()
        self.meta_man = MetaManager(self.meta_file)
        self.data_fd.truncate(0)
        self.data_fd.seek(0, 0)
        self.data_fd.flush()

    def info(self):
        info = {}
        info['data file'] = self.data_file
        info['meta file'] = self.meta_file
        return info


class ClipEntry:
    """ClipEntry"""

    def __init__(self, text=None, time=None, offset=-1, length=0):
        self.text = text
        self.time = time if time is not None else sys_time()
        self.offset = offset
        self.length = length

    def info(self):
        d = {'time': self.time, 'text': self.text}
        return d


class MetaManager:
    """MetaManager"""
    file_name = None
    tree = None
    root = None
    ROOT_TAG = 'clipon_history'

    def __init__(self, file_name):
        try:
            self.tree = self.parse(file_name)
        except ET.ParseError:
            logger.error(str(ET.ParseError))
            if os.path.getsize(file_name) > 0:
                raise Exception('Error parsing file %s' % file_name)
            self.create_tree()

        if self.tree is None:
            return
        self.root = self.tree.getroot()
        if self.root is None:
            self.create_tree()
        if self.root.tag != self.ROOT_TAG:
            raise Exception('Invalid root element')
        self.file_name = file_name
        self.save()

    def create_tree(self):
        self.root = self.create_root(self.ROOT_TAG, CLIPON_VERSION)
        self.tree = ET.ElementTree(self.root)

    def size(self):
        return len(self.root)

    def parse(self, file_name):
        return ET.parse(file_name)

    def save(self):
        if self.root is not None:
            pretty_xml = format_pretty(self.root)
            f = open(self.file_name, 'w')
            f.write(pretty_xml)
            f.close()

    def create_root(self, name, version):
        root = ET.Element(name)
        root.set('version', version)
        return root

    def new_element(self, name, attrs):
        elem = ET.Element(name)
        for key, value in attrs.items():
            elem.set(key, str(value))

        return elem

    def add_element(self, elem):
        parent = self.root
        parent.append(elem)
        self.save()

    def get_element(self, name, index):
        root = self.root
        if index >= self.size():
            return
        elem = root[index]
        return elem.attrib

    def del_element(self, elem):
        root = self.root
        root.remove(elem)
        self.save()

    def del_all(self):
        self.root = self.create_root(self.ROOT_TAG, CLIPON_VERSION)
        self.tree = ET.ElementTree(self.root)
        self.save()