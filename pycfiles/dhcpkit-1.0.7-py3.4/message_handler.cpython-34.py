# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/ipv6/server/message_handler.py
# Compiled at: 2017-06-08 11:09:29
# Size of source mod 2**32: 14418 bytes
"""
The code to handle a message
"""
import logging, multiprocessing
from typing import Iterable, List, Optional
from dhcpkit.common.server.logging import DEBUG_HANDLING
from dhcpkit.ipv6.duids import DUID
from dhcpkit.ipv6.extensions.leasequery import LeasequeryMessage, LeasequeryReplyMessage, STATUS_MALFORMED_QUERY, STATUS_NOT_ALLOWED, STATUS_UNKNOWN_QUERY_TYPE
from dhcpkit.ipv6.extensions.prefix_delegation import IAPDOption, IAPrefixOption
from dhcpkit.ipv6.messages import AdvertiseMessage, ConfirmMessage, DeclineMessage, InformationRequestMessage, RebindMessage, ReleaseMessage, RenewMessage, ReplyMessage, RequestMessage, SolicitMessage
from dhcpkit.ipv6.options import ClientIdOption, IAAddressOption, IANAOption, IATAOption, STATUS_USE_MULTICAST, ServerIdOption, StatusCodeOption
from dhcpkit.ipv6.server.extension_registry import server_extension_registry
from dhcpkit.ipv6.server.filters import Filter
from dhcpkit.ipv6.server.handlers import CannotRespondError, Handler, ReplyWithLeasequeryError, ReplyWithStatusError, UseMulticastError
from dhcpkit.ipv6.server.handlers.client_id import ClientIdHandler
from dhcpkit.ipv6.server.handlers.interface_id import InterfaceIdOptionHandler
from dhcpkit.ipv6.server.handlers.rapid_commit import RapidCommitHandler
from dhcpkit.ipv6.server.handlers.server_id import ForOtherServerError, ServerIdHandler
from dhcpkit.ipv6.server.handlers.status_option import AddMissingStatusOptionHandler
from dhcpkit.ipv6.server.handlers.unanswered_ia import UnansweredIAOptionHandler
from dhcpkit.ipv6.server.handlers.unicast import RejectUnwantedUnicastHandler
from dhcpkit.ipv6.server.statistics import StatisticsSet
from dhcpkit.ipv6.server.transaction_bundle import TransactionBundle
logger = logging.getLogger(__name__)

class MessageHandler:
    __doc__ = '\n    Message processing class\n    '

    def __init__(self, server_id: DUID, sub_filters: Iterable[Filter]=None,
                 sub_handlers: Iterable[Handler]=None, allow_rapid_commit: bool=False,
                 rapid_commit_rejections: bool=False):
        self.server_id = server_id
        self.sub_filters = list(sub_filters or [])
        self.sub_handlers = list(sub_handlers or [])
        self.allow_rapid_commit = allow_rapid_commit
        self.rapid_commit_rejections = rapid_commit_rejections
        self.setup_handlers = self.get_setup_handlers()
        self.cleanup_handlers = self.get_cleanup_handlers()

    def worker_init(self):
        """
        Separate initialisation that will be called in each worker process that is created. Things that can't be forked
        (think database connections etc) have to be initialised here.
        """
        logger.debug('Initialising MessageHandler in {}'.format(multiprocessing.current_process().name))
        for sub_filter in self.sub_filters:
            sub_filter.worker_init()

        for sub_handler in self.sub_handlers:
            sub_handler.worker_init()

    def get_handlers(self, bundle: TransactionBundle) -> List[Handler]:
        """
        Get all handlers that are going to be applied to the request in the bundle.

        :param bundle: The transaction bundle
        :return: The list of handlers to apply
        """
        handlers = []
        handlers += self.setup_handlers
        for sub_filter in self.sub_filters:
            handlers += sub_filter.get_handlers(bundle)

        handlers += self.sub_handlers
        handlers += self.cleanup_handlers
        return handlers

    def get_setup_handlers(self) -> List[Handler]:
        """
        Build a list of setup handlers and cache it

        :return: The list of handlers
        """
        handlers = []
        if self.allow_rapid_commit:
            handlers.append(RapidCommitHandler(self.rapid_commit_rejections))
        handlers.append(ServerIdHandler(duid=self.server_id))
        handlers.append(ClientIdHandler())
        handlers.append(InterfaceIdOptionHandler())
        for extension_name, extension in server_extension_registry.items():
            create_setup_handlers = getattr(extension, 'create_setup_handlers', None)
            if create_setup_handlers:
                setup_handlers = create_setup_handlers()
                for setup_handler in setup_handlers:
                    logger.log(DEBUG_HANDLING, 'Extension {} added {} to setup phase'.format(extension_name, setup_handler.__class__.__name__))

                handlers += setup_handlers
                continue

        return handlers

    @staticmethod
    def get_cleanup_handlers() -> List[Handler]:
        """
        Build a list of cleanup handlers and cache it

        :return: The list of handlers
        """
        handlers = []
        handlers.append(RejectUnwantedUnicastHandler())
        handlers.append(UnansweredIAOptionHandler())
        for extension_name, extension in server_extension_registry.items():
            create_cleanup_handlers = getattr(extension, 'create_cleanup_handlers', None)
            if create_cleanup_handlers:
                cleanup_handlers = create_cleanup_handlers()
                for cleanup_handler in cleanup_handlers:
                    logger.log(DEBUG_HANDLING, 'Extension {} added {} to cleanup phase'.format(extension_name, cleanup_handler.__class__.__name__))

                handlers += cleanup_handlers
                continue

        handlers.append(AddMissingStatusOptionHandler())
        return handlers

    @staticmethod
    def init_response(bundle: TransactionBundle):
        """
        Create the message object in bundle.response

        :param bundle: The transaction bundle
        """
        if isinstance(bundle.request, SolicitMessage):
            bundle.response = AdvertiseMessage(bundle.request.transaction_id)
        else:
            if isinstance(bundle.request, (RequestMessage, RenewMessage, RebindMessage,
             ReleaseMessage, DeclineMessage, InformationRequestMessage)):
                bundle.response = ReplyMessage(bundle.request.transaction_id)
            else:
                if isinstance(bundle.request, ConfirmMessage):
                    for option in bundle.request.get_options_of_type(IANAOption, IATAOption, IAPDOption):
                        if option.get_options_of_type((IAAddressOption, IAPrefixOption)):
                            break
                    else:
                        raise CannotRespondError('No IAs present in confirm reply')

                    bundle.response = ReplyMessage(bundle.request.transaction_id)
                else:
                    if isinstance(bundle.request, LeasequeryMessage):
                        bundle.response = LeasequeryReplyMessage(bundle.request.transaction_id)
                    else:
                        raise CannotRespondError('Do not know how to reply to {}'.format(type(bundle.request).__name__))
        bundle.create_outgoing_relay_messages()

    def construct_plain_status_reply(self, bundle: TransactionBundle, option: StatusCodeOption) -> ReplyMessage:
        """
        Construct a reply message signalling a status code to the client.

        :param bundle: The transaction bundle containing the incoming request
        :param option: The status code option to include in the reply
        :return: A reply with only the bare necessities and a status code
        """
        return ReplyMessage(bundle.request.transaction_id, options=[
         bundle.request.get_option_of_type(ClientIdOption),
         ServerIdOption(duid=self.server_id),
         option])

    def construct_leasequery_status_reply(self, bundle: TransactionBundle, option: StatusCodeOption) -> LeasequeryReplyMessage:
        """
        Construct a leasequery reply message signalling a status code to the client.

        :param bundle: The transaction bundle containing the incoming request
        :param option: The status code option to include in the reply
        :return: A leasequery reply with only the bare necessities and a status code
        """
        return LeasequeryReplyMessage(bundle.request.transaction_id, options=[
         bundle.request.get_option_of_type(ClientIdOption),
         ServerIdOption(duid=self.server_id),
         option])

    def construct_use_multicast_reply(self, bundle: TransactionBundle) -> Optional[ReplyMessage]:
        """
        Construct a message signalling to the client that they should have used multicast.

        :param bundle: The transaction bundle containing the incoming request
        :return: The proper answer to tell a client to use multicast
        """
        if bundle.received_over_multicast:
            logger.error('Not telling client to use multicast, they already did...')
            return
        return self.construct_plain_status_reply(bundle, StatusCodeOption(STATUS_USE_MULTICAST, 'You cannot send requests directly to this server, please use the proper multicast addresses'))

    def handle(self, bundle: TransactionBundle, statistics: StatisticsSet):
        """
        The main dispatcher for incoming messages.

        :param bundle: The transaction bundle
        :param statistics: Container for shared memory with statistics counters
        """
        if not bundle.request:
            return
        bundle.allow_rapid_commit = self.allow_rapid_commit
        statistics.count_message_in(bundle.request.message_type)
        logger.debug('Handling {}'.format(bundle))
        handlers = self.get_handlers(bundle)
        for handler in handlers:
            try:
                handler.analyse_pre(bundle)
            except:
                logger.exception('{} pre analysis failed'.format(handler.__class__.__name__))

        try:
            for handler in handlers:
                handler.pre(bundle)

            self.init_response(bundle)
            for handler in handlers:
                logger.log(DEBUG_HANDLING, 'Applying {}'.format(handler))
                handler.handle(bundle)

            for handler in handlers:
                handler.post(bundle)

        except ForOtherServerError as e:
            message = str(e) or 'Message is for another server'
            logger.debug('{}: ignoring'.format(message))
            statistics.count_for_other_server()
            bundle.response = None
        except CannotRespondError as e:
            message = str(e) or 'Cannot respond to this message'
            logger.warning('{}: ignoring'.format(message))
            statistics.count_do_not_respond()
            bundle.response = None
        except UseMulticastError:
            logger.debug('Unicast request received when multicast is required: informing client')
            statistics.count_use_multicast()
            bundle.response = self.construct_use_multicast_reply(bundle)
        except ReplyWithStatusError as e:
            if isinstance(e, ReplyWithLeasequeryError):
                bundle.response = self.construct_leasequery_status_reply(bundle, e.option)
            else:
                bundle.response = self.construct_plain_status_reply(bundle, e.option)
            logger.warning('Replying with {}'.format(e))
            if e.option.status_code == STATUS_UNKNOWN_QUERY_TYPE:
                statistics.count_unknown_query_type()
            else:
                if e.option.status_code == STATUS_MALFORMED_QUERY:
                    statistics.count_malformed_query()
                else:
                    if e.option.status_code == STATUS_NOT_ALLOWED:
                        statistics.count_not_allowed()
                    else:
                        statistics.count_other_error()

        for handler in handlers:
            try:
                handler.analyse_post(bundle)
            except:
                logger.exception('{} post analysis failed'.format(handler.__class__.__name__))

        if bundle.response:
            logger.log(DEBUG_HANDLING, 'Responding with {}'.format(bundle.response.__class__.__name__))
            statistics.count_message_out(bundle.response.message_type)
        else:
            logger.log(DEBUG_HANDLING, 'Not responding')