# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/delucks/.pyenv/versions/3.8.1/lib/python3.8/site-packages/todo/card.py
# Compiled at: 2020-02-22 13:33:21
# Size of source mod 2**32: 18497 bytes
"""Things which operate on or generate Trello cards"""
import re, json, shutil, itertools, webbrowser
from functools import partial
from typing import Optional
import arrow, click, trello
from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator
from prompt_toolkit.completion import WordCompleter, FuzzyWordCompleter
from todo.connection import TrelloConnection
from todo.exceptions import GTDException
from todo.input import prompt_for_confirmation, single_select
from todo.misc import get_title_of_webpage, DevNullRedirect, VALID_URL_REGEX, return_on_eof, build_name_lookup

def parse_user_date_input--- This code section failed: ---

 L.  24         0  LOAD_STR                 'MMM D YYYY'
                2  LOAD_STR                 'MM/DD/YYYY'
                4  LOAD_STR                 'DD/MM/YYYY'
                6  BUILD_LIST_3          3 
                8  STORE_FAST               'accepted_formats'

 L.  25        10  LOAD_FAST                'accepted_formats'
               12  GET_ITER         
               14  FOR_ITER             94  'to 94'
               16  STORE_FAST               'fmt'

 L.  26        18  SETUP_FINALLY        42  'to 42'

 L.  27        20  LOAD_GLOBAL              arrow
               22  LOAD_METHOD              get
               24  LOAD_FAST                'user_input'
               26  LOAD_FAST                'fmt'
               28  CALL_METHOD_2         2  ''
               30  STORE_FAST               'input_datetime'

 L.  28        32  LOAD_FAST                'input_datetime'
               34  POP_BLOCK        
               36  ROT_TWO          
               38  POP_TOP          
               40  RETURN_VALUE     
             42_0  COME_FROM_FINALLY    18  '18'

 L.  29        42  DUP_TOP          
               44  LOAD_GLOBAL              arrow
               46  LOAD_ATTR                parser
               48  LOAD_ATTR                ParserError
               50  COMPARE_OP               exception-match
               52  POP_JUMP_IF_FALSE    68  'to 68'
               54  POP_TOP          
               56  POP_TOP          
               58  POP_TOP          

 L.  30        60  POP_EXCEPT       
               62  JUMP_BACK            14  'to 14'
               64  POP_EXCEPT       
               66  JUMP_BACK            14  'to 14'
             68_0  COME_FROM            52  '52'

 L.  31        68  DUP_TOP          
               70  LOAD_GLOBAL              ValueError
               72  COMPARE_OP               exception-match
               74  POP_JUMP_IF_FALSE    90  'to 90'
               76  POP_TOP          
               78  POP_TOP          
               80  POP_TOP          

 L.  32        82  POP_EXCEPT       
               84  JUMP_BACK            14  'to 14'
               86  POP_EXCEPT       
               88  JUMP_BACK            14  'to 14'
             90_0  COME_FROM            74  '74'
               90  END_FINALLY      
               92  JUMP_BACK            14  'to 14'

Parse error at or near `ROT_TWO' instruction at offset 36


class Card:
    __doc__ = "This class is an alternative to py-trello's Card that can reuse the entire JSON structure rather than calling the\n    API for each remote attribute. The only network calls are to fetch external attributes like comments or attachments,\n    unless you call Card.fetch() to refresh the base JSON structure.\n    "

    def __init__(self, connection: TrelloConnection, card_json: dict):
        self.card_json = card_json
        self.connection = connection

    def __getitem__(self, attr):
        """Make this object subscriptable so you can treat it like the JSON structure directly"""
        return self.card_json[attr]

    def __str__(self):
        return self.card_json['name']

    @property
    def json(self):
        return self.card_json

    @property
    def id(self):
        return self.card_json['id']

    def fetch(self):
        """Refresh the base card JSON structure"""
        self.card_json = self.connection.trello.fetch_json(('/cards/' + self.id), query_params={'fields': 'all'})

    def fetch_comments(self, force: bool=False):
        """Fetch the comments on this card and return them in JSON format, adding them into self.card_json
        to cache until the next run.
        """
        if 'comments' in self.card_json:
            if not force:
                return self.card_json['comments']
        query_params = {'filter': 'commentCard'}
        comments = self.connection.trello.fetch_json(('/cards/' + self.id + '/actions'), query_params=query_params)
        sorted_comments = sorted(comments, key=(lambda comment: comment['date']))
        self.card_json['comments'] = sorted_comments
        return sorted_comments

    def fetch_attachments(self, force: bool=False):
        """Fetch the attachments on this card and return them in JSON format, after enriching the card JSON
        with the full attachment structure.
        """
        if 'attachments' in self.card_json:
            if not force:
                return self.card_json['attachments']
        attachments = self.connection.trello.fetch_json(('/cards/' + self.id + '/attachments'),
          query_params={'filter': 'false'})
        self.card_json['attachments'] = attachments
        return attachments

    def attach_url(self, url: str):
        """Attach a link from the internet"""
        return self.connection.trello.fetch_json(('/cards/' + self.id + '/attachments'),
          http_method='POST', post_args={'url': url})

    def remove_attachment(self, attachment_id: str):
        """Remove an attachment by ID"""
        return self.connection.trello.fetch_json(('/cards/' + self.id + '/attachments/' + attachment_id),
          http_method='DELETE')

    def delete(self):
        """Permanently delete the card"""
        return self.connection.trello.fetch_json(('/cards/' + self.id), http_method='DELETE')

    def set_closed(self, closed: bool=True):
        """Archive or unarchive this card"""
        return self.connection.trello.fetch_json(('/cards/' + self.id + '/closed'),
          http_method='PUT', post_args={'value': closed})

    def set_name(self, new_name: str):
        """Change this card's name"""
        self.card_json['name'] = new_name
        return self.connection.trello.fetch_json(('/cards/' + self.id + '/name'),
          http_method='PUT', post_args={'value': new_name})

    def add_label(self, label_id: str):
        """Add a label to this card by ID"""
        return self.connection.trello.fetch_json(('/cards/' + self.id + '/idLabels'),
          http_method='POST', post_args={'value': label_id})

    def remove_label(self, label_id: str):
        """Remove a label from this card by ID"""
        return self.connection.trello.fetch_json(('/cards/' + self.id + '/idLabels/' + label_id), http_method='DELETE')

    def comment(self, comment_text: str) -> dict:
        """Add a comment to a card"""
        return self.connection.trello.fetch_json(('/cards/' + self.id + '/actions/comments'),
          http_method='POST', post_args={'text': comment_text})

    def change_board(self, board_id: str, list_id: Optional[str]=None) -> None:
        """Change the board of this card, and optionally select the list the card should move to"""
        args = {'value': board_id}
        if list_id is not None:
            args['idList'] = list_id
        return self.connection.trello.fetch_json(('/cards/' + self.id + '/idBoard'), http_method='PUT', post_args=args)

    @return_on_eof
    def rename(self, default: Optional[str]=None, variables: dict={}):
        if variables:
            print('You can use the following variables in your new card title:')
            for k, v in variables.items():
                print(f"  ${k}: {v}")

        else:
            suggestion = variables.get'title0'None or self.card_json['name']
            newname = prompt(f'Input new name for this card (blank for "{default or suggestion}"): ').strip()
            if newname:
                for k, v in variables.items():
                    expansion = f"${k}"
                    if expansion in newname:
                        newname = newname.replaceexpansionv
                else:
                    self.set_name(newname)

            else:
                result = default or suggestion
                if result != self.card_json['name']:
                    self.set_name(result)

    @return_on_eof
    def add_labels(self, label_choices):
        """Give the user a way to toggle labels on this card by their
        name rather than by a numeric selection interface. Using
        prompt_toolkit, we have automatic completion which makes
        things substantially faster without having to do a visual
        lookup against numeric IDs

        Options:
            label_choices: str->trello.Label, the names and objects of labels on this board
        """
        print('Enter a tag name to toggle it, <TAB> completes. Ctrl+D to exit')
        while True:
            label_completer = FuzzyWordCompleter(label_choices.keys())
            userinput = prompt('gtd.py > tag > ', completer=label_completer).strip()
            if userinput not in label_choices.keys():
                if prompt_for_confirmation(f"Unrecognized tag name {userinput}, would you like to create it?", False):
                    label = self.connection.main_board().add_labeluserinput'green'
                    self.add_label(label.id)
                    click.echo(f"Added tag {label.name} to board {self.connection.main_board().name} and to the card {self}")
                    label_choices[userinput] = label
            else:
                label_obj = label_choices[userinput]
                try:
                    self.add_label(label_obj.id)
                    click.secho(f"Added tag {userinput}", fg='green')
                except trello.exceptions.ResourceUnavailable:
                    self.remove_label(label_obj.id)
                    click.secho(f"Removed tag {userinput}", fg='red')

    def title_to_link(self):
        sp = self.card_json['name'].split()
        links = [n for n in sp if VALID_URL_REGEX.search(n)]
        existing_attachments = [a['name'] for a in self.fetch_attachments()]
        user_parameters = {'oldname': self.card_json['name']}
        for idx, link_name in enumerate(links):
            if link_name not in existing_attachments:
                self.attach_url(link_name)
            user_parameters[f"link{idx}"] = link_name
            possible_title = get_title_of_webpage(link_name)
            if possible_title:
                user_parameters[f"title{idx}"] = possible_title
            reconstructed = ' '.join([n for n in sp if not VALID_URL_REGEX.search(n)])
            self.rename(variables=user_parameters, default=reconstructed)

    @return_on_eof
    def manipulate_attachments(self):
        """Give the user a CRUD interface for attachments on this card"""
        print('Enter a URL, "delete", "open", or "print". Ctrl+D to exit')
        attachment_completer = WordCompleter(['delete', 'print', 'open', 'http://', 'https://'], ignore_case=True)
        while True:
            user_input = prompt('gtd.py > attach > ', completer=attachment_completer).strip()
            if re.searchVALID_URL_REGEXuser_input:
                self.attach_url(user_input)
                print(f"Attached {user_input}")
            elif user_input in ('delete', 'open'):
                attachment_opts = {a:a['name'] for a in self.fetch_attachments()}
                if not attachment_opts:
                    print('This card is free of attachments')
            else:
                dest = single_select(attachment_opts.keys())
                if dest is not None:
                    target = attachment_opts[dest]
                    if user_input == 'delete':
                        self.remove_attachment(target['id'])
                        self.fetch_attachments(force=True)
                    else:
                        if user_input == 'open':
                            with DevNullRedirect():
                                webbrowser.open(target['url'])
                elif user_input == 'print':
                    existing_attachments = self.fetch_attachments(force=True)
                    if existing_attachments:
                        print('Attachments:')
                for a in existing_attachments:
                    print('  ' + a['name'])

    @return_on_eof
    def set_due_date--- This code section failed: ---

 L. 247         0  LOAD_CODE                <code_object validate_date>
                2  LOAD_STR                 'Card.set_due_date.<locals>.validate_date'
                4  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
                6  STORE_FAST               'validate_date'

 L. 250         8  LOAD_GLOBAL              Validator
               10  LOAD_ATTR                from_callable

 L. 251        12  LOAD_FAST                'validate_date'

 L. 252        14  LOAD_STR                 'Enter a date in format "Jun 15 2018", "06/15/2018" or "15/06/2018". Ctrl+D to go back'

 L. 253        16  LOAD_CONST               True

 L. 250        18  LOAD_CONST               ('error_message', 'move_cursor_to_end')
               20  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               22  STORE_FAST               'validator'

 L. 256        24  LOAD_GLOBAL              prompt
               26  LOAD_STR                 'gtd.py > duedate > '
               28  LOAD_FAST                'validator'
               30  LOAD_CONST               True
               32  LOAD_CONST               ('validator', 'validate_while_typing')
               34  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               36  STORE_FAST               'user_input'

 L. 257        38  LOAD_GLOBAL              parse_user_date_input
               40  LOAD_FAST                'user_input'
               42  CALL_FUNCTION_1       1  ''
               44  STORE_FAST               'result'

 L. 258        46  LOAD_FAST                'result'
               48  LOAD_CONST               None
               50  COMPARE_OP               is
               52  POP_JUMP_IF_FALSE    68  'to 68'

 L. 259        54  LOAD_GLOBAL              print
               56  LOAD_STR                 'Invalid date format!'
               58  CALL_FUNCTION_1       1  ''
               60  POP_TOP          
               62  JUMP_BACK            24  'to 24'

 L. 261        64  BREAK_LOOP           68  'to 68'
               66  JUMP_BACK            24  'to 24'
             68_0  COME_FROM            52  '52'

 L. 263        68  LOAD_FAST                'self'
               70  LOAD_ATTR                connection
               72  LOAD_ATTR                trello
               74  LOAD_ATTR                fetch_json

 L. 264        76  LOAD_STR                 '/cards/'
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                id
               82  BINARY_ADD       
               84  LOAD_STR                 '/due'
               86  BINARY_ADD       

 L. 264        88  LOAD_STR                 'PUT'

 L. 264        90  LOAD_STR                 'value'
               92  LOAD_FAST                'result'
               94  LOAD_METHOD              isoformat
               96  CALL_METHOD_0         0  ''
               98  BUILD_MAP_1           1 

 L. 263       100  LOAD_CONST               ('http_method', 'post_args')
              102  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              104  POP_TOP          

 L. 267       106  LOAD_FAST                'self'
              108  LOAD_METHOD              fetch
              110  CALL_METHOD_0         0  ''
              112  POP_TOP          

 L. 268       114  LOAD_GLOBAL              print
              116  LOAD_STR                 'Due date set'
              118  CALL_FUNCTION_1       1  ''
              120  POP_TOP          

 L. 269       122  LOAD_FAST                'result'
              124  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 124

    def move_to_list(self, list_choices: dict):
        """Select labels to add to this card

        Options:
            list_choices: str->trello.List, the names and objects of lists on this board
        """
        dest = single_select(sorted(list_choices.keys()))
        if dest is not None:
            destination_list = list_choices[dest]
            self.connection.trello.fetch_json(('/cards/' + self.id + '/idList'),
              http_method='PUT', post_args={'value': destination_list.id})
            print(f"Moved to {destination_list.name}")
            return destination_list

    def change_description(self):
        old_desc = self.card_json['desc']
        new_desc = click.edit(text=old_desc)
        if new_desc is not None:
            if new_desc != old_desc:
                self.connection.trello.fetch_json(('/cards/' + self.id + '/desc'),
                  http_method='PUT', post_args={'value': new_desc})
        return new_desc


def search_for_regex(card, title_regex, regex_flags):
    try:
        return re.search(title_regex, card['name'], regex_flags)
    except re.error as e:
        try:
            click.secho(f'Invalid regular expression "{title_regex}" passed: {str(e)}', fg='red')
            raise GTDException(1)
        finally:
            e = None
            del e


def check_for_label_presence(card, tags):
    """Take in a comma-sep list of tag names, and ensure that
    each is on this card"""
    if card['idLabels']:
        user_tags = set(tags.split(','))
        card_tags = set(card['_labels'])
        return user_tags.issubset(card_tags)
    return False


class CardView:
    __doc__ = "CardView presents an interface to a stateful set of cards selected by the user, allowing the user\n    to navigate back and forth between them, delete them from the list, etc.\n    CardView also translates filtering options from the CLI into parameters to request from Trello, or\n    filters to post-process the list of cards coming in.\n\n    Use this class either as an iterator ('for card in cardview') or by calling the next() and prev() methods to\n    manually step through the list of cards.\n\n    Goals:\n        Be light on resources. Store a list of IDs and only create Card objects when they are viewed for the first time.\n        Minimize network calls.\n        Simplify the API for a command to iterate over a set of selected cards\n    "

    def __init__(self, context, cards):
        self.context = context
        self.cards = cards
        self.position = 0

    def __str__(self):
        return f"CardView on {self.context.connection.main_board().name} with {len(self.cards)} items"

    def __iter__(self):
        return self

    def __next__(self):
        if self.position < len(self.cards):
            card = Card(self.context.connection, self.cards[self.position])
            self.position += 1
            return card
        raise StopIteration

    def current(self):
        return Card(self.context.connection, self.cards[self.position])

    def next(self):
        if self.position < len(self.cards) - 1:
            self.position += 1
            return self.current()

    def prev(self):
        if self.position > 0:
            self.position -= 1
            return self.current()

    def json(self):
        return json.dumps((self.cards), sort_keys=True, indent=2)

    @staticmethod
    def create(context, **kwargs):
        """Create a new CardView with the given filters on the cards to find.
        """
        query_params = {}
        regex_flags = kwargs.get'regex_flags'0
        status = kwargs.get'status''visible'
        valid_filters = ['all', 'closed', 'open', 'visible']
        if status not in valid_filters:
            click.secho(f"Card filter {status} is not valid! Use one of {','.join(valid_filters)}")
            raise GTDException(1)
        else:
            query_params['cards'] = status
            query_params['card_fields'] = 'all'
            target_cards = []
            if (list_regex := kwargs.get'list_regex'None) is not None:
                target_list_ids = []
                lists_json = context.connection.main_lists()
                pattern = re.compile(list_regex, flags=regex_flags)
                for list_object in lists_json:
                    if pattern.search(list_object['name']):
                        target_list_ids.append(list_object['id'])
                else:
                    for list_id in target_list_ids:
                        cards_json = context.connection.trello.fetch_json(f"/lists/{list_id}", query_params=query_params)
                        target_cards.extend(cards_json['cards'])

            else:
                cards_json = context.connection.trello.fetch_json(f"/boards/{context.board.id}", query_params=query_params)
            target_cards.extend(cards_json['cards'])
        filters = []
        post_processed_cards = []
        if (title_regex := kwargs.get'title_regex'None) is not None:
            filters.append(partial(search_for_regex, title_regex=title_regex, regex_flags=regex_flags))
        if (has_attachments := kwargs.get'has_attachments'None) is not None:
            filters.append(lambda c: c['badges']['attachments'] > 0)
        if (no_tags := kwargs.get'no_tags'None) is not None:
            filters.append(lambda c: not c['idLabels'])
        if (has_due_date := kwargs.get'has_due_date'None) is not None:
            filters.append(lambda c: c['due'])
        if (tags := kwargs.get'tags'None) is not None:
            filters.append(partial(check_for_label_presence, tags=tags))
        for card in target_cards:
            if all((filter_func(card) for filter_func in filters)):
                post_processed_cards.append(card)
            if not post_processed_cards:
                click.secho('No cards matched the filters provided', fg='red')
                raise GTDException(0)
            return CardView(context=context, cards=post_processed_cards)