# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/alexandria/client.py
# Compiled at: 2011-04-12 08:16:41
from alexandria.dsl.exceptions import InvalidInputException
from generator_tools.copygenerators import copy_generator
import logging

class Client(object):

    def __init__(self, id, session_manager):
        self.id = id
        self.session_manager = session_manager
        self.session_manager.restore()

    def uuid(self):
        return {'uuid': self.id, 'client_type': self.__class__.__name__}

    def get_previously_sent_item(self, menu_system):
        """
        Get the item that was previously sent to the client. It is needed to 
        be able to determine what question the incoming answer is answering.
        """
        previous_index = self.session_manager.data.get('previous_index', None)
        if previous_index >= 0:
            return copy_generator(menu_system.stack[(previous_index - 1)])
        else:
            return

    def next(self, answer, menu_system):
        """
        Step through the system, go to the next item. The answer is the incoming
        input coming from the client.
        """
        end_session = True
        try:
            try:
                item_awaiting_answer = self.get_previously_sent_item(menu_system)
                if item_awaiting_answer:
                    item_awaiting_answer.next()
                    (question, end_session) = item_awaiting_answer.send((menu_system, self.session_manager.data))
                    item_awaiting_answer.next()
                    validated_answer = item_awaiting_answer.send(answer)
                else:
                    logging.debug('client initiated contact with: %s' % answer)
                (index, item) = menu_system.next_after(self.session_manager.data.get('previous_index', 0))
                while item:
                    item.next()
                    (question, end_session) = item.send((menu_system, self.session_manager.data))
                    if question:
                        self.send(question, end_session)
                        self.session_manager.data['previous_index'] = index
                        break
                    else:
                        (index, item) = menu_system.next()

            except InvalidInputException, e:
                logging.exception(e)
                (index, repeat_item) = menu_system.repeat_current_item()
                repeat_item.next()
                (repeated_question, end_session) = repeat_item.send((menu_system, self.session_manager.data))
                self.session_manager.data['previous_index'] = index
                logging.debug('repeating current question: %s' % repeated_question)
                self.send(repeated_question, end_session)

        finally:
            self.save_state(end_session)

    def send(self, message, end_of_session):
        raise NotImplementedError, 'needs to be subclassed'

    def answer(self, message, menu_system):
        self.session_manager.restore()
        self.next(message, menu_system)

    def save_state(self, eom):
        self.session_manager.save(deactivate=eom)

    def deactivate(self):
        self.session_manager.save(deactivate=True)


class FakeUSSDClient(Client):

    def receive(self):
        return raw_input('<- ')

    def format(self, msg):
        return '-> ' + ('\n-> ').join(msg.split('\n'))

    def send(self, text, end_session):
        print self.format(text)
        if end_session:
            self.deactivate()
            import sys
            sys.exit(0)