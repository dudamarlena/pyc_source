# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cloud_utils/net_utils/ssh_expect_password.py
# Compiled at: 2018-01-31 14:44:08
from cloud_utils.net_utils.sshconnection import SshCbReturn
import re

def expect_password_cb(buf, password, prompt='^Password', nextcb=None, cbargs=[], retry=0, password_attempts=0, verbose=False, debug_method=None):
    """
    Sample callback to handle password prompts to be provided to ssh.cmd()
    :param buf: output from cmd()
    :param password: string password to be supplied to a detected 'password' prompt
    :param nextcb: function/method callback to be returned, this cmd() will use to
                   handle it's future output.
    :param prompt: regex string used to match prompt. case insensitive match used
    :
    """
    ret = SshCbReturn(stop=False)

    def debug(msg):
        if verbose:
            if debug_method:
                debug_method(msg)
            else:
                print msg

    def add_to_buffer(lines_to_add, newbuf):
        for line in lines_to_add:
            debug('Adding line to buf:"' + str(line) + '"')
            if newbuf is None:
                newbuf = line + '\n'
            else:
                newbuf += line + '\n'

        return newbuf

    def bufadd(line):
        return add_to_buffer(line, ret.buf)

    debug('STARTING expect_password_cb: password:' + str(password) + ', prompt:' + str(prompt))
    debug('Starting buf:"' + str(buf) + '"')
    lines = buf.splitlines()
    if password_attempts and lines[0] == '':
        debug('Removing first blank line(s) after sending password')
        lines.pop(0)
        if not lines:
            ret.buf = None
            ret.nextargs = [password, prompt, nextcb, cbargs, retry, password_attempts,
             verbose]
            return ret
    prompt_indices = [ i for i, s in enumerate(lines) if re.match(prompt, s, re.IGNORECASE) ]
    if prompt_indices:
        debug('Got password prompt, sending password...')
        if password_attempts > retry:
            raise CommandExpectPasswordException('Password dialog attempts:' + str(password_attempts) + ' exceeded retry limit:' + str(retry))
        prompt_index = prompt_indices[0]
        lines.pop(prompt_index)
        ret.buf = bufadd(lines)
        ret.sendstring = str(password).rstrip() + '\n'
        password_attempts += 1
        ret.removecb = False
        ret.nextcb = None
        ret.nextargs = [password, prompt, nextcb, cbargs, retry, password_attempts, verbose,
         debug_method]
        debug('Ending buf:"' + str(ret.buf) + '"')
        return ret
    else:
        debug('\nPassword prompt not found, continuing. password_attempts:' + str(password_attempts) + ', prompt:' + str(prompt) + ', len lines: ' + str(len(lines)))
        ret.buf = bufadd(lines)
        if nextcb is not None:
            debug('Got nextcb, calling it on our buffer now...')
            ret = nextcb(ret.buf, *cbargs)
            if ret.nextcb and not ret.removecb:
                nextcb = ret.nextcb
            else:
                nextcb = None
        ret.nextcb = None
        ret.removecb = False
        ret.nextargs = [password, prompt, nextcb, cbargs, retry, password_attempts, verbose]
        debug('Ending buf:"' + str(ret.buf) + '"')
        return ret


def expect_prompt_cb(sshconnection, buf, command=None, prompt_match='^\\w+(>|#|\\$)', verbose=None, debug_method=None):
    prompt = prompt_match + '\\s*$'
    start_match = None
    if command is not None:
        start_match = prompt + '\\s*' + command + '\\s*$'
    if verbose is None:
        verbose = sshconnection.verbose
    ret = SshCbReturn(stop=False)
    ret.buf = buf

    def debug(msg, ssh=sshconnection):
        if verbose:
            if debug_method:
                debug_method(msg)
            else:
                print msg

    debug('Starting expect_prompt_cb, prompt:' + str(prompt))
    debug('Starting buf:"' + str(buf) + '"')
    lines = buf.splitlines()
    for line in lines:
        sshconnection.debug('line:' + str(line))
        if re.search(prompt, line):
            debug(('Got prompt match in buffer. start_match:{0}, Line:"{1}"').format(start_match, line))
            if start_match:
                if re.search(start_match, line):
                    sshconnection.debug(('Found match for start_match:{0}, line:{1}').format(start_match, line))
                    command = None
                    start_match = None
            else:
                ret.removecb = True
                ret.stop = True
                debug('Ending buf:"' + str(ret.buf) + '"')
                return ret
        else:
            debug('\nPrompt not found, continuing...')

    ret.removecb = False
    ret.nextargs = [command, prompt_match, verbose, debug_method]
    return ret


class CommandExpectPasswordException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)