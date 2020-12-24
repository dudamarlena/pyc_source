# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/ipv6/server/worker.py
# Compiled at: 2017-06-20 18:44:46
# Size of source mod 2**32: 8233 bytes
"""
Worker process for handling requests using multiprocessing.
"""
import logging, logging.handlers, os, re, signal, sys
from multiprocessing import Queue, current_process
from dhcpkit.ipv6.messages import Message, RelayForwardMessage, RelayReplyMessage
from dhcpkit.ipv6.options import InterfaceIdOption, Option, RelayMessageOption
from dhcpkit.ipv6.server.listeners import IncomingPacketBundle, Replier
from dhcpkit.ipv6.server.message_handler import MessageHandler
from dhcpkit.ipv6.server.queue_logger import WorkerQueueHandler
from dhcpkit.ipv6.server.statistics import ServerStatistics
from dhcpkit.ipv6.server.transaction_bundle import TransactionBundle
from typing import Iterable
logger = None
logging_handler = None
current_message_handler = None
shared_statistics = None

def setup_worker(message_handler: MessageHandler, logging_queue: Queue, lowest_log_level: int, statistics: ServerStatistics, master_pid: int):
    """
    This function will be called after a new worker process has been created. Its purpose is to set the global
    variables in this specific worker process so that they can be reused across multiple requests. Otherwise we would
    have to pickle them each and every time, and because they are static that would be a waste.

    :param message_handler: The message handler for the incoming requests
    :param logging_queue: The queue where we can deposit log messages so the main process can log them
    :param lowest_log_level: The lowest log level that is going to be handled by the main process
    :param statistics: Container for shared memory with statistics counters
    :param master_pid: The PID of the master process, in case we have critical errors while initialising
    """
    global current_message_handler
    global logger
    global logging_handler
    global shared_statistics
    try:
        this_process = current_process()
        this_process.name = re.sub('^.*(Worker-\\d+)$', '\\1', this_process.name)
        signal.signal(signal.SIGINT, lambda signum, frame: None)
        signal.signal(signal.SIGTERM, lambda signum, frame: None)
        signal.signal(signal.SIGHUP, lambda signum, frame: None)
        logger = logging.getLogger()
        logger.setLevel(logging.NOTSET)
        logging_handler = WorkerQueueHandler(logging_queue)
        logging_handler.setLevel(lowest_log_level)
        logger.addHandler(logging_handler)
        current_message_handler = message_handler
        shared_statistics = statistics
        message_handler.worker_init()
    except Exception as e:
        if logger:
            logger.error('Error initialising worker: {}'.format(e))
        os.kill(master_pid, signal.SIGUSR1)
        sys.stderr = open(os.devnull, 'w')
        raise e


def parse_incoming_request(incoming_packet: IncomingPacketBundle) -> TransactionBundle:
    """
    Parse the incoming packet and add a RelayServerMessage around it containing the meta-data received from the
    listener.

    :param incoming_packet: The received packet
    :return: The parsed message in a transaction bundle
    """
    length, incoming_message = Message.parse(incoming_packet.data)
    incoming_message.validate()
    if isinstance(incoming_message, RelayForwardMessage):
        next_hop_count = incoming_message.hop_count + 1
    else:
        next_hop_count = 0
    relay_options = []
    relay_options.extend(incoming_packet.relay_options)
    relay_options.append(RelayMessageOption(relayed_message=incoming_message))
    wrapped_message = RelayForwardMessage(hop_count=next_hop_count, link_address=incoming_packet.link_address, peer_address=incoming_packet.source_address, options=relay_options)
    return TransactionBundle(incoming_message=wrapped_message, received_over_multicast=incoming_packet.received_over_multicast, received_over_tcp=incoming_packet.received_over_tcp, marks=incoming_packet.marks)


def verify_response(outgoing_message: Message):
    """
    generate the outgoing packet and check the RelayServerMessage around it.

    :param outgoing_message: The reply message
    """
    if not isinstance(outgoing_message, RelayReplyMessage):
        raise ValueError('The reply has to be wrapped in a RelayReplyMessage')
    reply = outgoing_message.relayed_message
    if not reply:
        raise ValueError('The RelayReplyMessage does not contain a message')


def get_interface_name_from_options(options: Iterable[Option]):
    """
    Get the interface name from the given options and decode it as unicode

    :param options: A list of options
    :return: The interface name
    """
    for option in options:
        if isinstance(option, InterfaceIdOption):
            try:
                return option.interface_id.decode(encoding='utf-8', errors='replace')
            except UnicodeDecodeError:
                pass

            continue

    return 'unknown'


def handle_message(incoming_packet: IncomingPacketBundle, replier: Replier):
    """
    Handle a single incoming request. This is supposed to be called in a separate worker thread that has been
    initialised with setup_worker().

    :param incoming_packet: The raw incoming request
    :param replier: The object that will send replies for us
    :returns: The packet to reply with and the destination
    """
    logging_handler.log_id = incoming_packet.message_id
    interface_name = get_interface_name_from_options(incoming_packet.relay_options)
    statistics = shared_statistics.get_update_set(interface_name=interface_name)
    try:
        try:
            bundle = parse_incoming_request(incoming_packet)
        except Exception as e:
            logger.error('Error while parsing request: {}'.format(e))
            statistics.count_incoming_packet()
            statistics.count_unparsable_packet()
            return

        statistics = shared_statistics.get_update_set(interface_name=interface_name, bundle=bundle)
        statistics.count_incoming_packet()
        try:
            current_message_handler.handle(bundle, statistics)
            for outgoing_message in bundle.outgoing_messages:
                verify_response(outgoing_message)
                statistics.count_outgoing_packet()
                try:
                    replier.send_reply(outgoing_message)
                except ValueError as e:
                    logger.error('Handler returned invalid message: {}'.format(e))

        except Exception as e:
            logger.exception('Error while handling request: {}'.format(e))
            statistics.count_handling_error()

    finally:
        logging_handler.log_id = None