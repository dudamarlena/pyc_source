# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/master.py
# Compiled at: 2012-10-12 07:02:39
import logging, multiprocessing, datetime, time
from service import Service
from packet import Packet

class MasterService(Service):
    __service__ = 'coils.master.##'
    __auto_dispatch__ = True
    __is_worker__ = False

    def __init__(self):
        Service.__init__(self)
        self._workers = {}
        self._counter = 0

    def prepare(self):
        try:
            import procname
            procname.setprocname(self.__service__)
        except:
            self.log.info('Failed to set process name for service')

    def start(self):
        self.__TimeOut__ = 2
        log = logging.getLogger('bootstrap')
        for name in self.service_list:
            try:
                service = self.get_service(name)
                p = multiprocessing.Process(target=service.run, args=())
                self.append_process(name, p)
                self.get_process(name).start()
            except Exception, e:
                log.warn(('Failed to start service {0}').format(name))
                log.exception(e)
            else:
                log.info(('Started service {0} as PID#{1}').format(name, self.get_process(name).pid))

        log.info('All services started.')

    @property
    def service_list(self):
        return self._workers.keys()

    def append_service(self, name, target):
        self._workers[name] = [
         target]

    def append_process(self, name, process):
        self._workers[name].append(process)

    def drop_process(self, name, process):
        self._workers[name].remove(process)

    def get_service(self, name):
        return self._workers[name][0]

    def get_process(self, name):
        return self._workers[name][1]

    def work(self):
        self._counter += 1
        if self._counter % 5 == 0:
            for name in self.service_list:
                worker = self.get_process(name)
                worker.join(0.1)
                if worker.is_alive():
                    pass
                else:
                    try:
                        print ('Component {0} has failed').format(name)
                        self.log.debug(('Component {0} has failed').format(name))
                        self.send_administrative_notice(subject=('Component {0} has failed.').format(name), message=('Component {0} has failed.').format(name), urgency=8, category='core')
                        self.drop_process(name, worker)
                        self.log.debug(('Dropped failed worker for {0}.').format(name))
                        service = self.get_service(name)
                        p = multiprocessing.Process(target=service.run, args=())
                        self.append_process(name, p)
                        self.get_process(name).start()
                        self.log.debug(('Component {0} restarted').format(name))
                        self.send_administrative_notice(subject=('Component {0} restart.').format(name), message=('Component {0} restart.').format(name), urgency=8, category='core')
                    except Exception, e:
                        self.log.exception(e)