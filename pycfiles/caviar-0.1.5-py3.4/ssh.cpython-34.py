# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/caviar/network/ssh.py
# Compiled at: 2017-10-25 18:02:55
# Size of source mod 2**32: 5164 bytes
"""
SSH module.
"""
import importlib, time

class SSHUnavailableSessionError(BaseException):

    def __init__(self, target):
        super().__init__([
         target])
        self._SSHUnavailableSessionError__target = target

    @property
    def target(self):
        return self._SSHUnavailableSessionError__target


class SSHInvalidSessionError(BaseException):

    def __init__(self, target):
        super().__init__([
         target])
        self._SSHInvalidSessionError__target = target

    @property
    def target(self):
        return self._SSHInvalidSessionError__target


class SSHCommandError(BaseException):

    def __init__(self, target, cause_lines):
        super().__init__([
         target,
         cause_lines])
        self._SSHCommandError__target = target
        self._SSHCommandError__cause_lines = cause_lines

    @property
    def target(self):
        return self._SSHCommandError__target

    @property
    def cause_lines(self):
        return self._SSHCommandError__cause_lines


class SSHSessionFactory:
    __doc__ = '\n\tSSH session factory.\n\t'

    def __init__(self, ssh_client, private_key_path):
        self._SSHSessionFactory__pool = SSHSessionPool(ssh_client, private_key_path)

    def session(self, user, host, attempt_count=5, attempt_timeout=1):
        return SSHSession(self._SSHSessionFactory__pool, SSHUserHost(user, host), attempt_count, attempt_timeout)

    def close(self):
        self._SSHSessionFactory__pool.close()


class SSHSession:
    __doc__ = '\n\tSSH logic session.\n\t\n\t:param SSHSessionPool pool:\n\t   Session pool.\n\t:param SSHUserHost target:\n\t   Session target.\n\t:param int attempt_count:\n\t   Session availability attempt count.\n\t:param int attempt_timeout:\n\t   Session availability attempt timeout.\n\t'

    def __init__(self, pool, target, attempt_count, attempt_timeout):
        if attempt_count < 1:
            raise ValueError('Bad attempt count: {}'.format(attempt_count))
        self._SSHSession__pool = pool
        self._SSHSession__target = target
        self._SSHSession__physical_session = None
        self._SSHSession__attempt_count = attempt_count
        self._SSHSession__attempt_timeout = attempt_timeout

    def __execute(self, cmd):
        stdout, stderr = self._SSHSession__pool.get(self._SSHSession__target).execute(cmd)
        cause_lines = []
        line = stderr.readline()
        while len(line) > 0:
            cause_lines.append(line.strip())
            line = stderr.readline()

        if len(cause_lines) > 0:
            raise SSHCommandError(self._SSHSession__target, cause_lines)
        line = stdout.readline()
        while len(line) > 0:
            yield line.strip()
            line = stdout.readline()

    def __retry(self, available_attempts):
        new_available_attempts = available_attempts - 1
        if new_available_attempts < 1:
            raise SSHUnavailableSessionError(self._SSHSession__target)
        time.sleep(self._SSHSession__attempt_timeout)
        return new_available_attempts

    def execute(self, cmd):
        """
                Execute the specified command.
                
                :param str cmd:
                   Command to be executed.
                   
                :rtype:
                   iter
                :return:
                   Iterator of standard output lines.
                   
                :raise caviar.network.ssh.SSHUnavailableSessionError:
                   If it is not possible to use any physical session.
                :raise caviar.network.ssh.SSHCommandError:
                   If there was a command error.
                """
        should_continue = True
        available_attempts = self._SSHSession__attempt_count
        while should_continue:
            try:
                yield from self._SSHSession__execute(cmd)
                should_continue = False
            except SSHUnavailableSessionError:
                available_attempts = self._SSHSession__retry(available_attempts)
            except SSHInvalidSessionError:
                self._SSHSession__pool.discard(self._SSHSession__target)
                available_attempts = self._SSHSession__retry(available_attempts)


class SSHSessionPool:

    def __init__(self, ssh_client, private_key_path):
        self._SSHSessionPool__ssh_client = ssh_client
        self._SSHSessionPool__private_key_path = private_key_path
        self._SSHSessionPool__physical_sessions = {}

    def get(self, target):
        try:
            return self._SSHSessionPool__physical_sessions[target]
        except KeyError:
            physical_session = self._SSHSessionPool__ssh_client.login(target, self._SSHSessionPool__private_key_path)
            self._SSHSessionPool__physical_sessions[target] = physical_session
            return physical_session

    def discard(self, target):
        del self._SSHSessionPool__physical_sessions[target]

    def close(self):
        self._SSHSessionPool__ssh_client.close()
        for target, physical_session in self._SSHSessionPool__physical_sessions.items():
            physical_session.logout()

        self._SSHSessionPool__physical_sessions.clear()


class SSHUserHost:

    def __init__(self, user, host):
        self._SSHUserHost__user = user
        self._SSHUserHost__host = host

    @property
    def user(self):
        return self._SSHUserHost__user

    @property
    def host(self):
        return self._SSHUserHost__host

    def __hash__(self):
        return hash((self._SSHUserHost__user, self._SSHUserHost__host))

    def __eq__(self, other):
        return self._SSHUserHost__user == other.user and self._SSHUserHost__host == other.host

    def __ne__(self, other):
        return self._SSHUserHost__user != other.user or self._SSHUserHost__host != other.host

    def __repr__(self):
        return '{}@{}'.format(self._SSHUserHost__user, self._SSHUserHost__host)