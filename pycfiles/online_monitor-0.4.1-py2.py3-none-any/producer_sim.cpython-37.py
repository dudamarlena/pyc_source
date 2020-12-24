# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidlp/git/online_monitor/online_monitor/utils/producer_sim.py
# Compiled at: 2019-06-25 09:08:43
# Size of source mod 2**32: 2834 bytes
import multiprocessing, zmq, logging, signal, time
import online_monitor.utils as utils

class ProducerSim(multiprocessing.Process):
    __doc__ = ' For testing we have to generate some random data to fake a DAQ. This is done with this Producer Simulation'

    def __init__(self, backend, kind='Test', name='Undefined', loglevel='INFO', **kwarg):
        multiprocessing.Process.__init__(self)
        self.backend_address = backend
        self.name = name
        self.kind = kind
        self.config = kwarg
        self.loglevel = loglevel
        self.exit = multiprocessing.Event()
        utils.setup_logging(loglevel)
        logging.info('Initialize %s producer %s at %s', self.kind, self.name, self.backend_address)

    def setup_producer_device(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        self.context = zmq.Context()
        self.sender = self.context.socket(zmq.PUB)
        self.sender.bind(self.backend_address)

    def run(self):
        utils.setup_logging(self.loglevel)
        logging.info('Start %s producer %s at %s', self.kind, self.name, self.backend_address)
        self.setup_producer_device()
        while not self.exit.wait(0.02):
            self.send_data()

        self.sender.close()
        self.context.term()
        logging.info('Close %s producer %s at %s', self.kind, self.name, self.backend_address)

    def shutdown(self):
        self.exit.set()

    def send_data(self):
        raise NotImplemented('This function has to be defined in derived simulation producer')


def main():
    args = utils.parse_arguments()
    configuration = utils.parse_config_file(args.config_file)
    try:
        daqs = []
        for actual_producer_name, actual_producer_cfg in configuration['producer_sim'].items():
            actual_producer_cfg['name'] = actual_producer_name
            daq = ProducerSim(loglevel=args.log, **actual_producer_cfg)
            daqs.append(daq)

        for daq in daqs:
            daq.start()

        while True:
            try:
                time.sleep(2)
            except KeyboardInterrupt:
                for daq in daqs:
                    daq.shutdown()

                for daq in daqs:
                    daq.join(timeout=500)

                return

    except KeyError:
        pass


if __name__ == '__main__':
    main()