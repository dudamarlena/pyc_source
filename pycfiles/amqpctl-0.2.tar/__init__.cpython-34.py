# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/AmqpConnector/__init__.py
# Compiled at: 2015-10-21 23:43:18
# Size of source mod 2**32: 14105 bytes
import amqp, socket, traceback, logging, threading, multiprocessing, queue, time

class Connector:

    def __init__(self, host=None, userid='guest', password='guest', virtual_host='/', task_queue='task.q', response_queue='response.q', task_exchange='tasks.e', task_exchange_type='direct', response_exchange='resps.e', response_exchange_type='direct', master=False, synchronous=True, flush_queues=False, heartbeat=300, ssl=None, poll_rate=0.25, prefetch=1, session_fetch_limit=None, durable=False):
        self.synchronous = synchronous
        self.poll_rate = poll_rate
        self.prefetch = prefetch
        self.durable = durable
        self.session_fetch_limit = session_fetch_limit
        self.session_fetched = 0
        self.queue_fetched = 0
        self.active = 0
        self.log = logging.getLogger('Main.Connector')
        self.log.info('Setting up AqmpConnector!')
        self.log.info("Fetch limit: '%s'", self.session_fetch_limit)
        self.log.info("Comsuming from queue '{conq}', emitting responses on '{tasq}'.".format(conq=task_queue, tasq=response_queue))
        self.master = master
        if not host:
            raise ValueError('You must specify a host to connect to!')
        assert task_queue.endswith('.q') == True
        assert response_queue.endswith('.q') == True
        assert task_exchange.endswith('.e') == True
        assert response_exchange.endswith('.e') == True
        self.task_q = task_queue
        self.response_q = response_queue
        self.task_exchange = task_exchange
        self.response_exchange = response_exchange
        self.sslopts = ssl
        self.connection = None
        self.channel = None
        if ':' not in host:
            if ssl:
                host += ':5671'
            else:
                host += ':5672'
        self.host = host
        self.userid = userid
        self.password = password
        self.virtual_host = virtual_host
        self.heartbeat = heartbeat
        self.task_exchange_type = task_exchange_type
        self.response_exchange_type = response_exchange_type
        self._connect()
        self._setupQueues()
        if flush_queues:
            self.channel.queue_purge(self.task_q)
            self.channel.queue_purge(self.response_q)
        self.taskQueue = multiprocessing.Queue()
        self.responseQueue = multiprocessing.Queue()
        self.run = True
        self.log.info('Starting AMQP interface thread.')
        self.thread = threading.Thread(target=self._poll_proxy, daemon=True)
        self.thread.start()

    def _connect(self):
        self.connection = amqp.connection.Connection(host=self.host, userid=self.userid, password=self.password, virtual_host=self.virtual_host, heartbeat=self.heartbeat, ssl=self.sslopts)
        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_size=0, prefetch_count=self.prefetch, a_global=False)

    def _setupQueues(self):
        self.channel.exchange_declare(self.task_exchange, type=self.task_exchange_type, auto_delete=False, durable=self.durable)
        self.channel.exchange_declare(self.response_exchange, type=self.response_exchange_type, auto_delete=False, durable=self.durable)
        if self.master:
            self.channel.queue_declare(self.response_q, auto_delete=False, durable=self.durable)
            self.channel.queue_bind(self.response_q, exchange=self.response_exchange, routing_key=self.response_q.split('.')[0])
            self.log.info('Binding queue {queue} to exchange {ex}.'.format(queue=self.response_q, ex=self.response_exchange))
        if not self.master:
            self.channel.queue_declare(self.task_q, auto_delete=False, durable=self.durable)
            self.channel.queue_bind(self.task_q, exchange=self.task_exchange, routing_key=self.task_q.split('.')[0])
            self.log.info('Binding queue {queue} to exchange {ex}.'.format(queue=self.task_q, ex=self.task_exchange))
        self.channel.queue_declare('nak.q', auto_delete=False, durable=self.durable)
        self.channel.queue_bind('nak.q', exchange=self.response_exchange, routing_key='nak')

    def _poll_proxy(self):
        if not self.synchronous:
            if self.master:
                in_queue = self.response_q
            else:
                in_queue = self.task_q
            self.channel.basic_consume(queue=in_queue, callback=self._message_callback)
        self.log.info('AMQP interface thread started.')
        try:
            self._poll()
        except KeyboardInterrupt:
            self.log.warning('AQMP Connector thread interrupted by keyboard interrupt!')
            self._poll()

    def _poll(self):
        """
                Internal function.
                Polls the AMQP interface, processing any messages received on it.
                Received messages are ack-ed, and then placed into the appropriate local queue.
                messages in the outgoing queue are transmitted.

                NOTE: Maximum throughput is 4 messages-second, limited by the internal poll-rate.
                """
        lastHeartbeat = self.connection.last_heartbeat_received
        print_time = 15
        integrator = 0
        loop_delay = self.poll_rate
        while self.run or self.responseQueue.qsize():
            try:
                if self.connection.last_heartbeat_received != lastHeartbeat:
                    lastHeartbeat = self.connection.last_heartbeat_received
                    if integrator > print_time:
                        self.log.info('Heartbeat tick received: %s', lastHeartbeat)
                    self.connection.heartbeat_tick()
                    self.connection.send_heartbeat()
                    time.sleep(loop_delay)
                    if not self.synchronous:
                        pass
                    try:
                        self.connection.drain_events(timeout=1)
                    except socket.timeout:
                        pass

                else:
                    if self.active == 0 and self.synchronous and self.run:
                        if integrator > print_time:
                            self.log.info('Looping, waiting for job.')
                        self.active += self._processReceiving()
                    elif integrator > print_time:
                        self.log.info('Active task running.')
                    self._publishOutgoing()
                    if integrator > 5:
                        integrator = 0
                    integrator += loop_delay
            except amqp.Connection.connection_errors:
                self.log.error('Connection dropped! Attempting to reconnect!')
                traceback.print_exc()
                try:
                    self.connection.close()
                except Exception:
                    self.log.error('Failed pre-emptive closing before reconnection. May not be a problem?')
                    for line in traceback.format_exc().split('\n'):
                        self.log.error(line)

                self._connect()
                self._setupQueues()

        self.log.info('AMQP Thread Exiting')
        self.channel.flow(False)
        self.channel.close()
        self.connection.close()
        self.log.info('AMQP Thread exited')

    def _message_callback(self, msg):
        self.log.info('Received packet via callback! Processing.')
        msg.channel.basic_ack(msg.delivery_info['delivery_tag'])
        self.taskQueue.put(msg.body)

    def _processReceiving(self):
        if self.master:
            in_queue = self.response_q
        else:
            in_queue = self.task_q
        ret = 0
        while True:
            if ret > self.prefetch:
                break
            if self.atFetchLimit():
                break
            item = self.channel.basic_get(queue=in_queue)
            if item:
                self.log.info("Received packet from queue '{queue}'! Processing.".format(queue=in_queue))
                item.channel.basic_ack(item.delivery_info['delivery_tag'])
                self.taskQueue.put(item.body)
                ret += 1
                self.session_fetched += 1
                if self.atFetchLimit():
                    self.log.info('Session fetch limit reached. Not fetching any additional content.')
            else:
                break

        if ret:
            self.log.info('Retreived %s items!', ret)
        return ret

    def _publishOutgoing(self):
        if self.master:
            out_queue = self.task_exchange
            out_key = self.task_q.split('.')[0]
        else:
            out_queue = self.response_exchange
            out_key = self.response_q.split('.')[0]
        while True:
            try:
                put = self.responseQueue.get_nowait()
                message = amqp.basic_message.Message(body=put)
                if self.durable:
                    message.properties['delivery_mode'] = 2
                self.channel.basic_publish(message, exchange=out_queue, routing_key=out_key)
                self.active -= 1
            except queue.Empty:
                break

    def atFetchLimit(self):
        """
                Track the fetch-limit for the active session. Used to allow an instance to connect,
                fetch one (and only one) item, and then do things with the fetched item without
                having the background thread fetch and queue a bunch more items while it's working.
                """
        if not self.session_fetch_limit:
            return False
        return self.session_fetched >= self.session_fetch_limit

    def atQueueLimit(self):
        """
                Track the fetch-limit for the active session. Used to allow an instance to connect,
                fetch one (and only one) item, and then do things with the fetched item without
                having the background thread fetch and queue a bunch more items while it's working.
                """
        if not self.session_fetch_limit:
            return False
        return self.queue_fetched >= self.session_fetch_limit

    def getMessage(self):
        """
                Try to fetch a message from the receiving Queue.
                Returns the method if there is one, False if there is not.
                Non-Blocking.
                """
        if self.atQueueLimit():
            raise ValueError('Out of fetchable items!')
        try:
            put = self.taskQueue.get_nowait()
            self.queue_fetched += 1
            return put
        except queue.Empty:
            return

    def putMessage(self, message, synchronous=False):
        """
                Place a message into the outgoing queue.

                if synchronous is true, this call will block until
                the items in the outgoing queue are less then the
                value of synchronous
                """
        if synchronous:
            while self.responseQueue.qsize() > synchronous:
                time.sleep(0.1)

        self.responseQueue.put(message)

    def stop(self):
        """
                Tell the AMQP interface thread to halt, and then join() on it.
                Will block until the queue has been cleanly shut down.
                """
        self.log.info('Stopping AMQP interface thread.')
        self.run = False
        while self.responseQueue.qsize() > 0:
            self.log.info('%s remaining outgoing AMQP items.', self.responseQueue.qsize())
            time.sleep(1)

        self.log.info('%s remaining outgoing AMQP items.', self.responseQueue.qsize())
        self.thread.join()
        self.log.info('AMQP interface thread halted.')


def test():
    import json, sys, os.path
    logging.basicConfig(level=logging.INFO)
    sPaths = [
     './settings.json', '../settings.json']
    for sPath in sPaths:
        if not os.path.exists(sPath):
            continue
        with open(sPath, 'r') as (fp):
            settings = json.load(fp)

    isMaster = len(sys.argv) > 1
    con = Connector(userid=settings['RABBIT_LOGIN'], password=settings['RABBIT_PASWD'], host=settings['RABBIT_SRVER'], virtual_host=settings['RABBIT_VHOST'], master=isMaster, synchronous=not isMaster, flush_queues=isMaster)
    while True:
        try:
            time.sleep(1)
            new = con.getMessage()
            if new:
                print(new)
                if not isMaster:
                    con.putMessage('Hi Thar!')
            if isMaster:
                con.putMessage('Oh HAI')
        except KeyboardInterrupt:
            break

    con.stop()


if __name__ == '__main__':
    test()