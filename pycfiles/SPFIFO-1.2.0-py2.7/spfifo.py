# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spfifo.py
# Compiled at: 2019-03-14 01:09:08
import PArray as pa, fcntl, time, os, numpy as np
from fcntl import LOCK_EX, LOCK_SH, LOCK_NB

def touch_file(path):
    with open(path, 'a'):
        os.utime(path, None)
    return


class OSLock:

    def lock(self, timeout=0, flags=fcntl.LOCK_EX | fcntl.LOCK_NB):
        if timeout != None:
            endTime = time.time() + timeout
        while 1:
            try:
                self.file = open(self.filePath, 'a+')
                fcntl.flock(self.file, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return 0
            except Exception as e:
                if timeout == None:
                    return 1
                if timeout == 0:
                    continue
                elif time.time() > endTime:
                    return 2
                time.sleep(0.001)

        return

    def unlock(self):
        if self.islock():
            try:
                fcntl.flock(self.file, fcntl.LOCK_UN)
                self.file.close()
                return 0
            except Exception as e:
                return 2

        return 1

    def islock(self):
        try:
            file = open(self.filePatdh, 'a+')
            file.close()
            return 0
        except Exception as e:
            return 1

    def __init__(self, filePath, mode=438):
        self.filePath = filePath
        touch_file(filePath)

    def __exit__(self, exc_type, exc_value, traceback):
        return self.unlock()


class SPFIFO:

    def keyIsExists(self, key):
        for l in pa.list():
            if l[0].decode('UTF-8') == key:
                return True

        return False

    def raiseIfKeyIsDelete(self):
        if self.raseOtherDelete:
            if not self.inited:
                raise Exception('Key %s is not init' % self.KEYSHARE)
            if not self.keyIsExists(self.KEYSHARE):
                raise Exception('Key %s is deleted' % self.KEYSHARE)

    def reset(self, number_element, element_perblock):
        self.number_element = number_element
        self.element_perblock = element_perblock
        self.index[0] = number_element
        self.index[1] = 0
        self.index[2] = 0
        self.index[3] = 0
        self.index[4] = element_perblock
        self.size = number_element * element_perblock

    def __init__(self):
        self.raseOtherDelete = True
        self.inited = False

    def init(self, key='sonnt', number_element=32, dtype='uint8', element_perblock=1, reNewFlag=False, timeout=0, raseOtherDelete=True, share_mode=438):
        self.KEYSHARE = key
        self.inited = True
        self.re_new_flag = reNewFlag
        self.lockFifo = OSLock('/dev/shm/' + key.replace('shm://', '') + '_lock', mode=share_mode)
        self.raseOtherDelete = raseOtherDelete
        if reNewFlag:
            if self.keyIsExists(key):
                self.delete()
            self.buff = pa.create(self.KEYSHARE, number_element * element_perblock, dtype)
            self.index = pa.create(self.KEYSHARE + '_index', 5, 'uint64')
            os.chmod('/dev/shm/' + key.replace('shm://', ''), share_mode)
            os.chmod('/dev/shm/' + key.replace('shm://', '') + '_index', share_mode)
            touch_file('/dev/shm/' + key.replace('shm://', '') + '_lock')
            os.chmod('/dev/shm/' + key.replace('shm://', '') + '_lock', share_mode)
            self.reset(number_element, element_perblock)
            return 0
        else:
            if timeout != None:
                endTime = time.time() + timeout
            while not self.keyIsExists(key):
                time.sleep(0.01)
                if timeout == None:
                    return 1
                if timeout == 0:
                    continue
                elif time.time() > endTime:
                    return 2

            self.buff = pa.attach(self.KEYSHARE)
            self.index = pa.attach(self.KEYSHARE + '_index')
            self.number_element = self.index[0]
            self.element_perblock = self.index[4]
            self.size = self.number_element * self.element_perblock
            return 0
            return

    def count(self):
        self.raiseIfKeyIsDelete()
        return self.index[1]

    def pop(self):
        self.raiseIfKeyIsDelete()
        if self.index[1]:
            self.lockFifo.lock()
            head = self.index[2]
            if self.element_perblock > 1:
                retval = self.buff[head:head + self.element_perblock]
            else:
                retval = self.buff[head]
            self.index[1] -= 1
            head += self.element_perblock
            if head >= self.size:
                head = 0
            self.index[2] = head
            self.lockFifo.unlock()
            return retval
        else:
            return
            return

    def push(self, element):
        self.raiseIfKeyIsDelete()
        self.lockFifo.lock()
        celement = self.index[1]
        tail = self.index[3]
        celement += 1
        retval = 0
        if celement > self.number_element:
            retval = 0
            celement = 1
        self.index[1] = celement
        if tail >= self.size:
            tail = 0
        if self.element_perblock > 1:
            lene = len(element)
            if self.element_perblock < lene:
                self.lockFifo.unlock()
                return 0
            for i in np.arange(self.element_perblock):
                if i < lene:
                    self.buff[np.uint64(tail + i)] = element[i]

        else:
            self.buff[tail] = element
        tail += self.element_perblock
        self.index[3] = tail
        self.lockFifo.unlock()
        return retval

    def delete(self):
        self.raiseIfKeyIsDelete()
        self.lockFifo.lock()
        pa.delete(self.KEYSHARE)
        pa.delete(self.KEYSHARE + '_index')
        os.remove('/dev/shm/' + self.KEYSHARE.replace('shm://', '') + '_lock')
        self.buff = None
        self.index = None
        self.lockFifo.unlock()
        return

    def flush(self):
        self.raiseIfKeyIsDelete()
        while self.count():
            self.pop()

    def __del__(self):
        return

    def __exit__(self, exc_type, exc_value, traceback):
        return