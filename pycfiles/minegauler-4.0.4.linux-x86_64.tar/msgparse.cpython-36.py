# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/legaul/venv36/lib/python3.6/site-packages/server/bot/msgparse.py
# Compiled at: 2020-02-09 16:33:06
# Size of source mod 2**32: 25045 bytes
"""
msgparse.py - Parse bot messages

February 2020, Lewis Gaul
"""
__all__ = ('RoomType', 'parse_msg')
import argparse, enum, logging, sys
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union
from minegauler.shared import highscores as hs
from . import formatter, utils
logger = logging.getLogger(__name__)

class InvalidArgsError(Exception):
    pass


class PositionalArg:

    def __init__(self, name: str, *, parse_name: bool=False, nargs: Union[(int, str)]=1, default: Any=None, choices: Optional[Iterable[Any]]=None, type: Optional[Callable]=None, validate: Optional[Callable]=None):
        if isinstance(nargs, int):
            if nargs < 1:
                if nargs not in ('?', '*', '+'):
                    raise ValueError(f"Bad nargs value {nargs!r}")
        else:
            self.name = name
            self.parse_name = parse_name
            self.nargs = nargs
            if default is None:
                if nargs not in (1, '?'):
                    self.default = []
            self.default = default
        self._choices = choices
        self._type = type
        self._validate = validate

    def convert(self, value):
        if self._type is not None:
            return self._type(value)
        else:
            return value

    def validate(self, value):
        if self._choices is not None:
            if value not in self._choices:
                return False
        if self._validate:
            return self._validate(value)
        else:
            return True


class ArgParser(argparse.ArgumentParser):
    __doc__ = '\n    A specialised arg parser.\n\n    The list of args to be parsed can contain the following, with no overlap:\n     - Ordered positional args at the start\n     - Regular argparse args with no order\n\n    Positional args are added with \'add_positional_arg()\'. The order of calls to\n    this method determines the order the args must appear in. The following\n    options are accepted:\n     - parse_name: Whether the arg name should be parsed.\n     - nargs: The number of args to accept. Accepted values are positive\n        integers, "?" for 0 or 1, "*" for 0 or more, "+" for 1 or more.\n     - choices: As for \'add_argument()\'.\n     - type: As for \'add_argument()\'.\n\n    Positional args are greedily consumed, but if an arg does not satisfy\n    choices or if the \'type\' callable raises an exception then no more values\n    will be accepted for that arg.\n\n    Examples:\n     - If a positional arg has no type/choices restrictions and unbounded\n        \'nargs\' (i.e. set to "*" or "+") then all positional options will be\n        consumed by this arg.\n     - If a positional arg has unbounded \'nargs\' but has a \'type\' that raises an\n        exception for invalid args, subsequent args will take over the matching.\n        Note that if insufficient options are matched (e.g. nargs="+" and no\n        options are matched) then parsing ends with a standard error.\n\n    Positional argument parsing ends as soon as an option starting with a dash\n    is encountered, or when the positional args are exhausted. The remaining\n    options are passed to a standard argparse parser to match args added with\n    \'add_argument()\'.\n    '

    def __init__(self):
        super().__init__(add_help=False)
        self._name_parse_args = []
        self._positional_args = []

    def parse_known_args(self, args, namespace=None):
        """
        Override the default behaviour.
        """
        if namespace is None:
            namespace = argparse.Namespace()
        args = self._parse_positional_args(args, namespace)
        for i, arg in enumerate(args):
            if arg in self._name_parse_args:
                args[i] = f"--{arg}"

        return super().parse_known_args(args, namespace)

    def add_argument(self, name, *args, **kwargs):
        if not name.startswith('--'):
            self._name_parse_args.append(name)
            name = '--' + name.lstrip('-')
        (super().add_argument)(name, *args, **kwargs)

    def error(self, message):
        raise InvalidArgsError(message)

    def add_positional_arg(self, name: str, **kwargs) -> None:
        """
        Add a positional argument for parsing.

        :param name:
            The name of the argument - must be unique.
        :param kwargs:
            Arguments to pass to the 'PositionalArg' class.
        """
        self._positional_args.append(PositionalArg(name, **kwargs))

    def _parse_positional_args(self, kws: Iterable[str], namespace) -> Iterable[str]:
        """
        Parse the positional args.

        :param kws:
            The provided keywords.
        :param namespace:
            The namespace to set argument values in.
        :return:
            The remaining unmatched keywords.
        """
        for arg in self._positional_args:
            result, kws = self._parse_single_positional_arg(arg, kws)
            setattr(namespace, arg.name, result)

        return kws

    def _parse_single_positional_arg(self, arg: PositionalArg, kws: Iterable[str]) -> Tuple[(Any, Iterable[str])]:
        """
        Parse a single positional arg. Raise InvalidArgsError if not enough
        matching args are found.
        """
        required = arg.nargs not in ('?', '*')
        if isinstance(arg.nargs, int):
            max_matches = arg.nargs
            exp_args_string = str(arg.nargs)
        else:
            if arg.nargs == '?':
                max_matches = 1
                exp_args_string = 'optionally one'
            else:
                if arg.nargs == '*':
                    max_matches = None
                    exp_args_string = 'any number of'
                else:
                    if arg.nargs == '+':
                        max_matches = None
                        exp_args_string = 'at least one'
                    else:
                        assert False
                if kws:
                    if arg.parse_name:
                        if kws[0] == arg.name:
                            kws.pop(0)
                        else:
                            if not required:
                                return (
                                 arg.default, kws)
                            raise InvalidArgsError(f"Expected to find {arg.name!r}")
                matches = []
                while kws and (max_matches is None or len(matches) < max_matches):
                    try:
                        kw_value = arg.convert(kws[0])
                        assert arg.validate(kw_value)
                    except Exception as e:
                        logger.debug(e)
                        if arg.parse_name:
                            if not matches:
                                raise InvalidArgsError(f"Got name of positional arg {arg.name!r} but no values")
                        else:
                            break
                    else:
                        matches.append(kw_value)
                        kws.pop(0)

                if required:
                    if not matches:
                        raise InvalidArgsError(f"Expected {exp_args_string} {arg.name!r} arg")
                    else:
                        if isinstance(arg.nargs, int):
                            if len(matches) != arg.nargs:
                                assert len(matches) < arg.nargs
                                raise InvalidArgsError(f"Expected {exp_args_string} {arg.name!r} arg")
                    arg_value = arg.default
                    if matches:
                        assert arg.nargs in (1, '?') and len(matches) == 1
                        arg_value = matches[0]
                else:
                    arg_value = matches
        return (
         arg_value, kws)


class BotMsgParser(ArgParser):

    def add_username_arg(self, *, nargs: Union[(int, str)]=1, allow_me=True):
        choices = list(utils.USER_NAMES)
        if allow_me:
            choices.append('me')
        self.add_positional_arg('username', nargs=nargs, choices=choices)

    def add_difficulty_arg(self):
        self.add_positional_arg('difficulty',
          nargs='?', type=(self._convert_difficulty_arg))

    def add_rank_type_arg(self):

        def convert(arg):
            try:
                return self._convert_difficulty_arg(arg)
            except InvalidArgsError:
                raise

        self.add_positional_arg('rank_type', nargs='?', type=convert)

    def add_per_cell_arg(self):
        self.add_argument('per-cell', type=int, choices=[1, 2, 3])

    def add_drag_select_arg(self):

        def _arg_type(arg):
            if arg == 'on':
                return True
            if arg == 'off':
                return False
            raise InvalidArgsError("Drag select should be one of {'on', 'off'}")

        self.add_argument('drag-select', type=_arg_type)

    @staticmethod
    def _convert_difficulty_arg(arg):
        if arg in ('b', 'beginner'):
            return 'beginner'
        else:
            if arg in ('i', 'intermediate'):
                return 'intermediate'
            if arg in ('e', 'expert'):
                return 'expert'
            if arg in ('m', 'master'):
                return 'master'
        raise InvalidArgsError(f"Invalid difficulty {arg!r}")


CommandMapping = Dict[(Optional[str], Union[(Callable, 'CommandMapping')])]

class RoomType(enum.Enum):
    GROUP = 'group'
    DIRECT = 'direct'

    def to_cmds(self) -> CommandMapping:
        if self is self.GROUP:
            return _GROUP_COMMANDS
        else:
            assert self is self.DIRECT
            return _DIRECT_COMMANDS


_GENERAL_INFO = "Welcome to the Minegauler bot!\n\nDownload Minegauler from https://github.com/LewisGaul/minegauler.\n\nThe bot provides the ability to check highscores and matchups for games of Minegauler, and also gives notifications whenever anyone in the group sets a new highscore.\n\nThere are a few settings to filter Minegauler games with:\n - difficulty: One of 'beginner', 'intermediate', 'expert' or 'master'.  \n   By default the combination of beginner, intermediate and expert is used,    with 1000 used for any difficulties not completed.\n - drag-select: One of 'on' or 'off'.  \n   By default no filter is applied (the best time of either mode is used).\n - per-cell: One of 1, 2 or 3.  \n   By default no filter is applied (the best time of any mode is used).\n\nAll highscores are independent of each of the above modes, and all commands accept these filters to view specific times. E.g. 'ranks beginner per-cell 1'.\n\nCommands can be issued in group chat and direct chat. Most of the commands are the same, however some are only available in one of the other (e.g. 'set nickname'). Type 'help' or '?' to check the available commands.\n\nTo interact with a bot in Webex Teams group chats, the bot must be tagged. To do this, type @ followed by the bot's name. The client should auto-suggest a completion, at which point you'll need to press enter or tab to select the completion and turn it into a tag.\n\nSome useful common commands:  \n'ranks' - display rankings  \n'matchups <name> <name> ...' - display comparison of times between users\n\nSome useful group-chat commands:  \n'challenge <name> ...' - challenge other users to a game\n\nSome useful direct-chat commands:  \n'set nickname' - set your nickname that you use in the Minegauler app\n"

def helpstring(text):

    def decorator(func):
        func.__helpstring__ = text
        return func

    return decorator


def schema(text):

    def decorator(func):
        func.__schema__ = text
        return func

    return decorator


def cmd_help(func: Callable, *, only_schema: bool=False, allow_markdown: bool=False) -> str:
    lines = []
    if not only_schema:
        try:
            lines.append(func.__helpstring__)
        except AttributeError:
            logger.warning('No helpstring found on message handling function %r', func.__name__)

    try:
        schema = func.__schema__
    except AttributeError:
        logger.warning('No schema found on message handling function %r', func.__name__)
    else:
        if allow_markdown:
            lines.append(f"`{schema}`")
        else:
            lines.append(schema)
        if not lines:
            return 'Unexpected error: unable to get help message\n\n'
        else:
            return '\n\n'.join(lines)


@helpstring('Get help for a command')
@schema('help [<command>]')
def group_help(args, **kwargs):
    allow_markdown = kwargs.get('allow_markdown', False)
    linebreak = '\n\n' if allow_markdown else '\n'
    commands = _flatten_cmds(_GROUP_COMMANDS)
    if allow_markdown:
        commands = f"`{commands}`"
    else:
        if not args:
            return commands
        func, _ = _map_to_cmd(' '.join(args), _GROUP_COMMANDS)
        if func is None:
            raise InvalidArgsError(linebreak.join(['Unrecognised command', commands]))
        else:
            return cmd_help(func, allow_markdown=allow_markdown)


@helpstring('Get help for a command')
@schema('help [<command>]')
def direct_help(args, **kwargs):
    allow_markdown = kwargs.get('allow_markdown', False)
    linebreak = '\n\n' if allow_markdown else '\n'
    commands = _flatten_cmds(_DIRECT_COMMANDS)
    if allow_markdown:
        commands = f"`{commands}`"
    else:
        if not args:
            return commands
        func, _ = _map_to_cmd(' '.join(args), _DIRECT_COMMANDS)
        if func is None:
            raise InvalidArgsError(linebreak.join(['Unrecognised command', commands]))
        else:
            return cmd_help(func, allow_markdown=allow_markdown)


@helpstring('Get information about the game')
@schema('info')
def info(args, **kwargs):
    BotMsgParser().parse_args(args)
    return _GENERAL_INFO


@helpstring('Get player info')
@schema('player <name> [b[eginner] | i[ntermediate] | e[xpert] | m[aster]] [drag-select {on | off}] [per-cell {1 | 2 | 3}]')
def player(args, username: str, allow_markdown=False, **kwargs):
    parser = BotMsgParser()
    parser.add_username_arg()
    parser.add_difficulty_arg()
    parser.add_per_cell_arg()
    parser.add_drag_select_arg()
    args = parser.parse_args(args)
    if args.username == 'me':
        args.username = username
    diff = args.difficulty[0] if args.difficulty else None
    highscores = hs.get_highscores((hs.HighscoresDatabases.REMOTE),
      name=(utils.USER_NAMES[args.username]),
      difficulty=diff,
      drag_select=(args.drag_select),
      per_cell=(args.per_cell))
    filters_str = formatter.format_filters(None,
      (args.drag_select), (args.per_cell), no_difficulty=True)
    if filters_str:
        filters_str = ' with ' + filters_str
    lines = [
     'Player info for {}{}:'.format(args.username, filters_str)]
    lines.extend(formatter.format_player_highscores(highscores, difficulty=(args.difficulty)))
    linebreak = '  \n' if allow_markdown else '\n'
    return linebreak.join(lines)


@helpstring('Get rankings')
@schema('ranks [b[eginner] | i[ntermediate] | e[xpert] | m[aster]] [drag-select {on | off}] [per-cell {1 | 2 | 3}]')
def ranks(args, **kwargs) -> str:
    allow_markdown = kwargs.get('allow_markdown', False)
    parser = BotMsgParser()
    parser.add_rank_type_arg()
    parser.add_per_cell_arg()
    parser.add_drag_select_arg()
    args = parser.parse_args(args)
    times = utils.get_highscore_times(args.rank_type, args.drag_select, args.per_cell)
    lines = []
    lines.append('Rankings for {}'.format(formatter.format_filters(args.rank_type, args.drag_select, args.per_cell)))
    ranks = formatter.format_highscore_times(times)
    if allow_markdown:
        ranks = f"```\n{ranks}\n```"
    lines.append(ranks)
    return '\n'.join(lines)


@helpstring('Get stats for played games')
@schema('stats [players ...] [b[eginner] | i[ntermediate] | e[xpert] | m[aster]] [drag-select {on | off}] [per-cell {1 | 2 | 3}]')
def stats(args, **kwargs):
    parser = BotMsgParser()
    parser.add_difficulty_arg()
    parser.add_per_cell_arg()
    parser.add_drag_select_arg()
    args = parser.parse_args(args)
    return 'Stats'


@helpstring('Get player stats')
@schema('stats players {all | <name> [<name> ...]} [b[eginner] | i[ntermediate] | e[xpert] | m[aster]] [drag-select {on | off}] [per-cell {1 | 2 | 3}]')
def stats_players(args, **kwargs):
    parser = BotMsgParser()
    parser.add_username_arg(nargs='+')
    parser.add_difficulty_arg()
    parser.add_per_cell_arg()
    parser.add_drag_select_arg()
    args = parser.parse_args(args)
    return 'Player stats {}'.format(', '.join(args.username))


@helpstring('Get matchups for given players')
@schema('matchups <name> <name> [<name> ...] [b[eginner] | i[ntermediate] | e[xpert] | m[aster]] [drag-select {on | off}] [per-cell {1 | 2 | 3}]')
def matchups(args, username: str, allow_markdown: bool=False, room_type=RoomType.DIRECT, **kwargs):
    parser = BotMsgParser()
    parser.add_username_arg(nargs='+')
    parser.add_difficulty_arg()
    parser.add_per_cell_arg()
    parser.add_drag_select_arg()
    args = parser.parse_args(args)
    users = {(u if u != 'me' else username) for u in args.username}
    if len(users) < 2 or len(users) > 5:
        raise InvalidArgsError('Require between 2 and 5 username args')
    else:
        names = {utils.USER_NAMES[u] for u in users}
        times = utils.get_highscore_times(args.difficulty, args.drag_select, args.per_cell, names)
        matchups = utils.get_matchups(times)
        if allow_markdown:
            if room_type is RoomType.GROUP:
                users_str = ', '.join(utils.tag_user(u) for u in users)
        users_str = ', '.join(users)
    lines = [
     'Matchups between {} for {}:'.format(users_str, formatter.format_filters(args.difficulty, args.drag_select, args.per_cell))]
    lines.extend(formatter.format_matchups(matchups))
    linebreak = '  \n' if allow_markdown else '\n'
    return linebreak.join(lines)


@helpstring('Get best matchups including at least one of specified players')
@schema('best-matchups [<name> ...] [b[eginner] | i[ntermediate] | e[xpert] | m[aster]] [drag-select {on | off}] [per-cell {1 | 2 | 3}]')
def best_matchups(args, username: str, allow_markdown=False, room_type=RoomType.DIRECT, **kwargs):
    parser = BotMsgParser()
    parser.add_username_arg(nargs='*')
    parser.add_difficulty_arg()
    parser.add_per_cell_arg()
    parser.add_drag_select_arg()
    args = parser.parse_args(args)
    users = {(u if u != 'me' else username) for u in args.username}
    names = {utils.USER_NAMES[u] for u in users}
    times = utils.get_highscore_times(args.difficulty, args.drag_select, args.per_cell, utils.USER_NAMES.values())
    matchups = utils.get_matchups(times, include_users=names)[:10]
    if allow_markdown:
        if room_type is RoomType.GROUP:
            users_str = ', '.join(utils.tag_user(u) for u in users)
    else:
        users_str = ', '.join(users)
    if users_str:
        users_str = ' including ' + users_str
    lines = [
     'Best matchups{} for {}:'.format(users_str, formatter.format_filters(args.difficulty, args.drag_select, args.per_cell))]
    lines.extend(formatter.format_matchups(matchups))
    linebreak = '  \n' if allow_markdown else '\n'
    return linebreak.join(lines)


@helpstring('Challenge other players to a game')
@schema('challenge <name> [<name> ...] [b[eginner] | i[ntermediate] | e[xpert] | m[aster]] [drag-select {on | off}] [per-cell {1 | 2 | 3}]')
def challenge(args, username: str, **kwargs):
    parser = BotMsgParser()
    parser.add_username_arg(nargs='+', allow_me=False)
    parser.add_difficulty_arg()
    parser.add_per_cell_arg()
    parser.add_drag_select_arg()
    args = parser.parse_args(args)
    names = {u for u in args.username if u != username}
    if len(names) < 1:
        raise InvalidArgsError("Need at least one other player's name")
    else:
        users_str = ', '.join(utils.tag_user(u) for u in names)
        diff_str = args.difficulty + ' ' if args.difficulty else ''
        opts = dict()
        if args.drag_select:
            opts['drag-select'] = 'on' if args.drag_select else 'off'
        if args.per_cell:
            opts['per-cell'] = args.per_cell
        if opts:
            opts_str = ' with {}'.format(formatter.format_kwargs(opts))
        else:
            opts_str = ''
    return '{} has challenged {} to a {}game of Minegauler{}'.format(username, users_str, diff_str, opts_str)


@helpstring('Set your nickname')
@schema('set nickname <name>')
def set_nickname(args, username: str, **kwargs):
    new = ' '.join(args)
    old = utils.USER_NAMES[username]
    logger.debug('Changing nickname of %s from %r to %r', username, old, new)
    utils.set_user_nickname(username, new)
    return f"Nickname changed from '{old}' to '{new}'"


_COMMON_COMMANDS = {'help':info, 
 'info':info, 
 'player':player, 
 'ranks':ranks, 
 'matchups':matchups, 
 'best-matchups':best_matchups}
_GROUP_COMMANDS = {**_COMMON_COMMANDS, **{'help':group_help, 
 'challenge':challenge}}
_DIRECT_COMMANDS = {**_COMMON_COMMANDS, **{'help':direct_help, 
 'set':{'nickname': set_nickname}}}

def _map_to_cmd(msg: str, cmds: CommandMapping) -> Tuple[(Callable, List[str])]:
    func = None
    words = msg.split()
    while words:
        next_word = words[0]
        if next_word in cmds:
            words.pop(0)
            if callable(cmds[next_word]):
                func = cmds[next_word]
                break
            else:
                cmds = cmds[next_word]
        else:
            break
        if None in cmds:
            func = cmds[None]

    return (
     func, words)


def _flatten_cmds(cmds: CommandMapping, root: bool=True) -> str:
    to_join = []
    for k, v in cmds.items():
        item = k
        if isinstance(v, dict):
            item += ' ' + _flatten_cmds(v, root=False)
        if item:
            to_join.append(item)

    ret = ' | '.join(to_join)
    if None in cmds:
        ret = f"[{ret}]"
    else:
        if len(cmds) > 1:
            if not root:
                ret = f"{{{ret}}}"
    return ret


def parse_msg(msg: str, room_type: RoomType, *, allow_markdown: bool=False, **kwargs) -> str:
    """
    Parse a message and perform the corresponding action.

    :param msg:
        The message to parse.
    :param room_type:
        The room type the message was received in.
    :param allow_markdown:
        Whether to allow markdown in the response.
    :param kwargs:
        Other arguments to pass on to sub-command functions.
    :return:
        Response text.
    :raise InvalidArgsError:
        Unrecognised command. The text of the error is a suitable error/help
        message.
    """
    msg = msg.strip()
    if msg.endswith('?'):
        if not (msg.startswith('help ') and msg.split()[1] != '?'):
            msg = 'help ' + msg[:-1]
    cmds = room_type.to_cmds()
    func = None
    try:
        func, args = _map_to_cmd(msg, cmds)
        if func is None:
            raise InvalidArgsError('Base command not found')
        return func(args, allow_markdown=allow_markdown, room_type=room_type, **kwargs)
    except InvalidArgsError as e:
        logger.debug('Invalid message: %r', msg)
        if func is None:
            return "Unrecognised command - try 'help' or 'info'"
        linebreak = '\n\n' if allow_markdown else '\n'
        resp_msg = cmd_help(func, only_schema=True, allow_markdown=allow_markdown)
        resp_msg = linebreak.join(['Unrecognised command', resp_msg])
        raise InvalidArgsError(resp_msg) from e


def main(argv):
    try:
        resp = parse_msg((' '.join(argv)), (RoomType.GROUP), username='dummy-user')
    except InvalidArgsError as e:
        resp = str(e)

    print(resp)


if __name__ == '__main__':
    main(sys.argv[1:])