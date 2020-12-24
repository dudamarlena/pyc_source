# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/zsh_startify/__main__.py
# Compiled at: 2019-09-19 09:55:56
# Size of source mod 2**32: 7671 bytes
from os import system, getenv
from time import sleep
from shlex import quote
import libtmux
from halo import Halo
from pyfiglet import Figlet
from colorama import Fore, Style
from PyInquirer import prompt, style_from_dict, Token, Validator, ValidationError

def print_blue(text):
    print(Fore.BLUE + Style.BRIGHT + text + Style.RESET_ALL)


def print_red(text):
    print(Fore.RED + Style.BRIGHT + text + Style.RESET_ALL)


def print_yellow(text):
    print(Fore.YELLOW + Style.BRIGHT + text + Style.RESET_ALL)


def print_green(text):
    print(Fore.GREEN + Style.BRIGHT + text + Style.RESET_ALL)


def splash():
    """Print splash screen text. Uses env vars for font and header if they
    exist."""
    font = getenv('ZSH_STARTIFY_HEADER_FONT', 'univers')
    text = getenv('ZSH_STARTIFY_HEADER_TEXT', 'zsh')
    fig = Figlet(font=font)
    formatted = '\t' + fig.renderText(text).replace('\n', '\n\t')
    rainbow = True
    if rainbow:
        system('echo ' + quote(formatted) + ' | lolcat')
    else:
        print_green(formatted)


def sleep_with_spinner(secs):
    """Sleep with a nice spinner and then print a success messsage."""
    spinner = Halo(text='Loading', spinner='dots')
    spinner.start()
    sleep(secs)
    spinner.succeed('Success.')


def pretty_print_session_names(sessions, splash_flag):
    if not splash_flag:
        print('\n')
    print_blue('    === Active tmux sessions ===')
    for session in sessions:
        print_red(f"       [*] {session}")

    print()


def get_tmux_session_names(server) -> list:
    """Returns all current tmux session names"""
    return [session.name for session in server.list_sessions()]


def get_tmux_session(server, name) -> libtmux.Session:
    """Looks up a tmux session by name and returns it if it exists. Returns
    None if the session doesn't exist.
    """
    session = server.find_where({'session_name': name})
    if session is None:
        raise ValueError(f"Error: No session of name '{name}' exists.")
    return session


def attach_to_session(server, name):
    session = get_tmux_session(server, name)
    session.attach_session()


def create_new_named_session(server, name):
    session = server.new_session(name)
    session.attach_session()


def get_tmux_server() -> libtmux.Server:
    """
    Returns tmux server if it's running, and starts one if it's not.
    """
    server = libtmux.Server()
    try:
        server.list_sessions()
    except libtmux.exc.LibTmuxException:
        print_blue('Starting tmux server...')
        hack_session = 'zsh-startify-tmux-server-hack'
        start_server_hack = f"tmux has-session -t {hack_session} ||                               tmux new-session -d -s {hack_session}"
        system(start_server_hack)
        sleep_with_spinner(5)
        server = libtmux.Server()
        get_tmux_session(server, hack_session).kill_session()

    return server


def is_inside_tmux_session() -> bool:
    """Returns True if already attached to a tmux session, False otherwise"""
    return getenv('TMUX', '') != ''


MARK = {'tmux-session':'    ', 
 'non-tmux-session':'- '}
ACTIONS = {'zsh':'Launch zsh', 
 'new-tmux-session':'Create new tmux session', 
 'attach-tmux-session':'Attach to existing tmux session'}
SELECTOR_STYLE = style_from_dict({Token.QuestionMARK: '#dcbf85 bold', 
 Token.Question: '#1776A5 bold', 
 Token.Instruction: '#1776A5 bold', 
 Token.Pointer: '#FF9D00 bold', 
 Token.Selected: '#cc5454', 
 Token.Answer: '#f44336 bold'})

def prompt_for_action(tmux_sessions) -> str:
    """
    Show a prompt with all available tmux sessions, letting the user choose a
    session to attach to, the option to create a new session, or create a
    non-tmux-session session.
    """
    launch_zsh = MARK['non-tmux-session'] + ACTIONS['zsh']
    choices = [
     launch_zsh,
     MARK['non-tmux-session'] + ACTIONS['new-tmux-session'],
     {'name':ACTIONS['attach-tmux-session'], 
      'disabled':'Select from below'}]
    choices += [MARK['tmux-session'] + session for session in tmux_sessions]
    questions = [
     {'type':'list', 
      'name':'action', 
      'message':'What do you want to do?', 
      'choices':choices}]
    try:
        answers = prompt(questions, style=SELECTOR_STYLE)
    except EOFError:
        return launch_zsh
    else:
        if answers == {}:
            return launch_zsh
        return answers['action']


class TmuxSessionValidator(Validator):
    __doc__ = '\n    Tmux session names must not contain periods and must not be the empty\n    string.\n    '

    def validate(self, document):
        name = document.text
        if len(name) == 0:
            raise ValidationError(message='tmux session name must not be an empty string',
              cursor_position=0)
        else:
            if '.' in name:
                raise ValidationError(message="tmux session names may not contain '.'",
                  cursor_position=(len(name)))


def prompt_for_session_name() -> str:
    questions = [
     {'type':'input', 
      'name':'session_name', 
      'message':'Enter a session name', 
      'default':'', 
      'validate':TmuxSessionValidator}]
    answers = prompt(questions, style=SELECTOR_STYLE)
    return answers['session_name']


def action_handler(server, action):
    if action.startswith(MARK['tmux-session']):
        attach_to_session(server, action.strip())
    else:
        if ACTIONS['new-tmux-session'] in action:
            session_name = prompt_for_session_name()
            create_new_named_session(server, session_name)
        else:
            return


def main():
    if is_inside_tmux_session():
        return
    else:
        splash_flag = not getenv('ZSH_STARTIFY_NO_SPLASH', '')
        if splash_flag:
            splash()
        server = get_tmux_server()
        tmux_sessions = get_tmux_session_names(server)
        pretty_print_session_names(tmux_sessions, splash_flag)
        action = getenv('ZSH_STARTIFY_NON_INTERACTIVE', '') or prompt_for_action(tmux_sessions)
        action_handler(server, action)


if __name__ == '__main__':
    main()