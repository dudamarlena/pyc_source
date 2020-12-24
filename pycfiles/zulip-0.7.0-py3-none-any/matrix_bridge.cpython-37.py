# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eeshangarg/python-zulip-api/zulip/integrations/bridge_with_matrix/matrix_bridge.py
# Compiled at: 2020-04-20 21:49:10
# Size of source mod 2**32: 12478 bytes
import os, logging, signal, traceback, zulip, sys, argparse, re, configparser
from collections import OrderedDict
from types import FrameType
from typing import Any, Callable, Dict, Optional
from matrix_client.errors import MatrixRequestError
from matrix_client.client import MatrixClient
from requests.exceptions import MissingSchema
GENERAL_NETWORK_USERNAME_REGEX = '@_?[a-zA-Z0-9]+_([a-zA-Z0-9-_]+):[a-zA-Z0-9.]+'
MATRIX_USERNAME_REGEX = '@([a-zA-Z0-9-_]+):matrix.org'
ZULIP_MESSAGE_TEMPLATE = '**{username}**: {message}'
MATRIX_MESSAGE_TEMPLATE = '<{username}> {message}'

class Bridge_ConfigException(Exception):
    pass


class Bridge_FatalMatrixException(Exception):
    pass


class Bridge_ZulipFatalException(Exception):
    pass


def matrix_login(matrix_client: Any, matrix_config: Dict[(str, Any)]) -> None:
    try:
        matrix_client.login_with_password(matrix_config['username'], matrix_config['password'])
    except MatrixRequestError as exception:
        try:
            if exception.code == 403:
                raise Bridge_FatalMatrixException('Bad username or password.')
            else:
                raise Bridge_FatalMatrixException('Check if your server details are correct.')
        finally:
            exception = None
            del exception

    except MissingSchema:
        raise Bridge_FatalMatrixException('Bad URL format.')


def matrix_join_room(matrix_client: Any, matrix_config: Dict[(str, Any)]) -> Any:
    try:
        room = matrix_client.join_room(matrix_config['room_id'])
        return room
    except MatrixRequestError as exception:
        try:
            if exception.code == 403:
                raise Bridge_FatalMatrixException('Room ID/Alias in the wrong format')
            else:
                raise Bridge_FatalMatrixException("Couldn't find room.")
        finally:
            exception = None
            del exception


def die(signal: int, frame: FrameType) -> None:
    os._exit(1)


def matrix_to_zulip(zulip_client: zulip.Client, zulip_config: Dict[(str, Any)], matrix_config: Dict[(str, Any)], no_noise: bool) -> Callable[([Any, Dict[(str, Any)]], None)]:

    def _matrix_to_zulip(room, event):
        """
        Matrix -> Zulip
        """
        content = get_message_content_from_event(event, no_noise)
        zulip_bot_user = '@%s:matrix.org' % matrix_config['username']
        not_from_zulip_bot = 'body' not in event['content'] or event['sender'] != zulip_bot_user
        if not_from_zulip_bot:
            if content:
                try:
                    result = zulip_client.send_message({'type':'stream', 
                     'to':zulip_config['stream'], 
                     'subject':zulip_config['topic'], 
                     'content':content})
                except Exception as exception:
                    try:
                        raise Bridge_ZulipFatalException(exception)
                    finally:
                        exception = None
                        del exception

                if result['result'] != 'success':
                    raise Bridge_ZulipFatalException(result['msg'])

    return _matrix_to_zulip


def get_message_content_from_event(event: Dict[(str, Any)], no_noise: bool) -> Optional[str]:
    irc_nick = shorten_irc_nick(event['sender'])
    if event['type'] == 'm.room.member':
        if no_noise:
            return
            if event['membership'] == 'join':
                content = ZULIP_MESSAGE_TEMPLATE.format(username=irc_nick, message='joined')
        elif event['membership'] == 'leave':
            content = ZULIP_MESSAGE_TEMPLATE.format(username=irc_nick, message='quit')
    elif not event['type'] == 'm.room.message' or event['content']['msgtype'] == 'm.text' or event['content']['msgtype'] == 'm.emote':
        content = ZULIP_MESSAGE_TEMPLATE.format(username=irc_nick, message=(event['content']['body']))
    else:
        content = event['type']
    return content


def shorten_irc_nick(nick: str) -> str:
    """
    Add nick shortner functions for specific IRC networks
    Eg: For freenode change '@freenode_user:matrix.org' to 'user'
    Check the list of IRC networks here:
    https://github.com/matrix-org/matrix-appservice-irc/wiki/Bridged-IRC-networks
    """
    match = re.match(GENERAL_NETWORK_USERNAME_REGEX, nick)
    if match:
        return match.group(1)
    match = re.match(MATRIX_USERNAME_REGEX, nick)
    if match:
        return match.group(1)
    return nick


def zulip_to_matrix(config: Dict[(str, Any)], room: Any) -> Callable[([Dict[(str, Any)]], None)]:

    def _zulip_to_matrix(msg):
        """
        Zulip -> Matrix
        """
        message_valid = check_zulip_message_validity(msg, config)
        if message_valid:
            matrix_username = msg['sender_full_name'].replace(' ', '')
            matrix_text = MATRIX_MESSAGE_TEMPLATE.format(username=matrix_username, message=(msg['content']))
            room.send_text(matrix_text)

    return _zulip_to_matrix


def check_zulip_message_validity(msg: Dict[(str, Any)], config: Dict[(str, Any)]) -> bool:
    is_a_stream = msg['type'] == 'stream'
    in_the_specified_stream = msg['display_recipient'] == config['stream']
    at_the_specified_subject = msg['subject'] == config['topic']
    not_from_zulip_bot = msg['sender_email'] != config['email']
    if is_a_stream:
        if not_from_zulip_bot:
            if in_the_specified_stream:
                if at_the_specified_subject:
                    return True
    return False


def generate_parser() -> argparse.ArgumentParser:
    description = "\n    Script to bridge between a topic in a Zulip stream, and a Matrix channel.\n\n    Tested connections:\n        * Zulip <-> Matrix channel\n        * Zulip <-> IRC channel (bridged via Matrix)\n\n    Example matrix 'room_id' options might be, if via matrix.org:\n        * #zulip:matrix.org (zulip channel on Matrix)\n        * #freenode_#zulip:matrix.org (zulip channel on irc.freenode.net)"
    parser = argparse.ArgumentParser(description=description, formatter_class=(argparse.RawTextHelpFormatter))
    parser.add_argument('-c', '--config', required=False, help='Path to the config file for the bridge.')
    parser.add_argument('--write-sample-config', metavar='PATH', dest='sample_config', help='Generate a configuration template at the specified location.')
    parser.add_argument('--from-zuliprc', metavar='ZULIPRC', dest='zuliprc', help='Optional path to zuliprc file for bot, when using --write-sample-config')
    parser.add_argument('--show-join-leave', dest='no_noise', default=True,
      action='store_false',
      help='Enable IRC join/leave events.')
    return parser


def read_configuration(config_file: str) -> Dict[(str, Dict[(str, str)])]:
    config = configparser.ConfigParser()
    try:
        config.read(config_file)
    except configparser.Error as exception:
        try:
            raise Bridge_ConfigException(str(exception))
        finally:
            exception = None
            del exception

    if set(config.sections()) != {'matrix', 'zulip'}:
        raise Bridge_ConfigException('Please ensure the configuration has zulip & matrix sections.')
    return {section:dict(config[section]) for section in config.sections()}


def write_sample_config(target_path: str, zuliprc: Optional[str]) -> None:
    if os.path.exists(target_path):
        raise Bridge_ConfigException("Path '{}' exists; not overwriting existing file.".format(target_path))
    sample_dict = OrderedDict((
     (
      'matrix',
      OrderedDict((('host', 'https://matrix.org'), ('username', 'username'), ('password', 'password'),
             ('room_id', '#zulip:matrix.org')))),
     (
      'zulip',
      OrderedDict((('email', 'glitch-bot@chat.zulip.org'), ('api_key', 'aPiKeY'), ('site', 'https://chat.zulip.org'),
             ('stream', 'test here'), ('topic', 'matrix'))))))
    if zuliprc is not None:
        if not os.path.exists(zuliprc):
            raise Bridge_ConfigException("Zuliprc file '{}' does not exist.".format(zuliprc))
        zuliprc_config = configparser.ConfigParser()
        try:
            zuliprc_config.read(zuliprc)
        except configparser.Error as exception:
            try:
                raise Bridge_ConfigException(str(exception))
            finally:
                exception = None
                del exception

        sample_dict['zulip']['email'] = zuliprc_config['api']['email']
        sample_dict['zulip']['site'] = zuliprc_config['api']['site']
        sample_dict['zulip']['api_key'] = zuliprc_config['api']['key']
    sample = configparser.ConfigParser()
    sample.read_dict(sample_dict)
    with open(target_path, 'w') as (target):
        sample.write(target)


def main() -> None:
    signal.signal(signal.SIGINT, die)
    logging.basicConfig(level=(logging.WARNING))
    parser = generate_parser()
    options = parser.parse_args()
    if options.sample_config:
        try:
            write_sample_config(options.sample_config, options.zuliprc)
        except Bridge_ConfigException as exception:
            try:
                print('Could not write sample config: {}'.format(exception))
                sys.exit(1)
            finally:
                exception = None
                del exception

        if options.zuliprc is None:
            print("Wrote sample configuration to '{}'".format(options.sample_config))
        else:
            print("Wrote sample configuration to '{}' using zuliprc file '{}'".format(options.sample_config, options.zuliprc))
        sys.exit(0)
    else:
        if not options.config:
            print('Options required: -c or --config to run, OR --write-sample-config.')
            parser.print_usage()
            sys.exit(1)
        else:
            try:
                config = read_configuration(options.config)
            except Bridge_ConfigException as exception:
                try:
                    print('Could not parse config file: {}'.format(exception))
                    sys.exit(1)
                finally:
                    exception = None
                    del exception

        zulip_config = config['zulip']
        matrix_config = config['matrix']
        backoff = zulip.RandomExponentialBackoff(timeout_success_equivalent=300)
        while backoff.keep_going():
            print('Starting matrix mirroring bot')
            try:
                zulip_client = zulip.Client(email=(zulip_config['email']), api_key=(zulip_config['api_key']),
                  site=(zulip_config['site']))
                matrix_client = MatrixClient(matrix_config['host'])
                matrix_login(matrix_client, matrix_config)
                room = matrix_join_room(matrix_client, matrix_config)
                room.add_listener(matrix_to_zulip(zulip_client, zulip_config, matrix_config, options.no_noise))
                print('Starting listener thread on Matrix client')
                matrix_client.start_listener_thread()
                print('Starting message handler on Zulip client')
                zulip_client.call_on_each_message(zulip_to_matrix(zulip_config, room))
            except Bridge_FatalMatrixException as exception:
                try:
                    sys.exit('Matrix bridge error: {}'.format(exception))
                finally:
                    exception = None
                    del exception

            except Bridge_ZulipFatalException as exception:
                try:
                    sys.exit('Zulip bridge error: {}'.format(exception))
                finally:
                    exception = None
                    del exception

            except zulip.ZulipError as exception:
                try:
                    sys.exit('Zulip error: {}'.format(exception))
                finally:
                    exception = None
                    del exception

            except Exception:
                traceback.print_exc()

            backoff.fail()


if __name__ == '__main__':
    main()