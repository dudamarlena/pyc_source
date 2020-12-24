# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib64/python3.4/site-packages/PyIRC/extensions/basicapi.py
# Compiled at: 2015-10-08 05:15:23
# Size of source mod 2**32: 20750 bytes
__doc__ = 'A basic easy-to-use API\n\nThis provides simple interfaces to messaging, responses, topic setting, and\nbasic channel access control.\n'
from logging import getLogger
from PyIRC.extensions import BaseExtension
_logger = getLogger(__name__)

class BasicAPI(BaseExtension):
    """BasicAPI"""
    requires = [
     'ISupport']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base.basicapi = self

    def message(self, target, message, notice=False):
        """Send a message to a target.

        :param target:
            Where to send the message, This may be a
            :py:class:`~PyIRC.extensions.channeltrack.Channel` instance,
            :py:class:`~PyIRC.extensions.usertrack.User` instance, or a
            string.

        :param message:
            Message to send.

        :param notice:
            Whether to send the message as a notice.

        .. warning::
            Use notice judiciously, as many users find them irritating!

        """
        if hasattr(target, 'name'):
            target = target.name
        elif hasattr(target, 'nick'):
            target = target.nick
        self.send('NOTICE' if notice else 'PRIVMSG', [target, message])

    def reply_target(self, line):
        """Get the appropriate target to reply to a given line.

        :param line:
            :py:class:`~PyIRC.base.line.Line` instance of the message to get
            the reply target of. This is needed due to the limitations of the
            IRC framing format.

        :returns:
            Target to reply to

        """
        isupport = self.base.isupport
        statusmsg = tuple(isupport.get('STATUSMSG'))
        if statusmsg and line.params[0].startswith(statusmsg):
            return line.params[0]
        channels = tuple(isupport.get('CHANTYPES'))
        if line.params[0].startswith(channels):
            return line.params[0]
        if line.hostmask.nick:
            return line.hostmask.nick

    def topic(self, channel, topic):
        """Set the topic in a channel.

        .. note::
            You usually must be opped to set the topic in a channel. This
            command may fail, and this function cannot tell you due to IRC's
            asynchronous nature.

        :param channel:
            Channel to set the topic in. This can be either a
            :py:class:`~PyIRC.extensions.channeltrack.Channel` instance or a
            string.

        :param topic:
            Topic to set in channel. Will unset the topic if set to None or
            the empty string.

        """
        if hasattr(channel, 'name'):
            channel = channel.name
        if topic is None:
            topic = ''
        self.send('TOPIC', [channel, topic])

    def mode_params(self, add, mode, target, *args):
        r"""Set modes on a channel with a given target list.

        This is suitable for mass bans/unbans, special status modes, and more.

        :param add:
            Whether or not mode is being added or removed

        :param mode:
            Mode to apply to channel.

        :param target:
            Channel to apply the modes in. This can be a
            :py:class:`~PyIRC.extensions.channeltrack.Channel` instance,
            :py:class:`~PyIRC.extensions.usertrack.User` instance, or a
            string.

        :param \*args:
            Targets or params for modes. Can be either
            :py:class:`~PyIRC.extensions.usertrack.User` instances or strings.

        """
        if not args:
            raise ValueError('args are needed for this function')
        if len(mode) > 1:
            raise ValueError('Only one mode may be set by this function')
        if hasattr(target, 'name'):
            target = target.name
        else:
            if hasattr(target, 'nick'):
                target = target.nick
            params = []
            for param in args:
                if hasattr(target, 'nick'):
                    param = param.nick
                params.append(param)

            isupport = self.base.isupport
            modes = isupport.get('MODES')
            if modes:
                modes = int(modes)
            else:
                modes = 4
        if modes > 8:
            modes = 8
        groups = (params[n:n + modes] for n in range(0, len(params), modes))
        flag = '+' if add else '-'
        for group in groups:
            modes = flag + mode * len(group)
            params = [target, flag + mode * len(group)]
            params.extend(group)
            self.send('MODE', params)

    def op(self, channel, *args):
        r"""Op a user (or users) on a given channel.

        :param channel:
            Channel to op the user or users in. This can be a
            :py:class:`~PyIRC.extensions.channeltrack.Channel` instance, or a
            string.

        :param \*args:
            Users to op. Can be
            :py:class:`~PyIRC.extensions.usertrack.User` instances or strings.

        """
        if not args:
            raise ValueError('args are needed for this function')
        self.mode_params(True, 'o', channel, *args)

    def oper(self, password, username=None):
        """Attempt to oper up.

        :param password:
            Password to oper up with.

        :param username:
            Username to oper up with. If blank, attempt to use the nick we
            connected with (or attempted to).
        """
        if username is None:
            username = self.base.nick
        self.send('OPER', [username, password])

    def deop(self, channel, *args):
        r"""Deop a user (or users) on a given channel.

        :param channel:
            Channel to deopop the user or users in. This can be a
            :py:class:`~PyIRC.extensions.channeltrack.Channel` instance, or a
            string.

        :param \*args:
            Users to deop. Can be
            :py:class:`~PyIRC.extensions.usertrack.User` instances or strings.

        """
        if not args:
            raise ValueError('args are needed for this function')
        self.mode_params(False, 'o', channel, *args)

    def voice(self, channel, *args):
        r"""Voice a user (or users) on a given channel.

        :param channel:
            Channel to voice the user or users in. This can be a
            :py:class:`~PyIRC.extensions.channeltrack.Channel` instance, or a
            string.

        :param \*args:
            Users to voice. Can be
            :py:class:`~PyIRC.extensions.usertrack.User` instances or strings.

        """
        if not args:
            raise ValueError('args are needed for this function')
        self.mode_params(True, 'v', channel, *args)

    def devoice(self, channel, *args):
        r"""Devoice a user (or users) on a given channel.

        :param channel:
            Channel to devoice the user or users in. This can be a
            :py:class:`~PyIRC.extensions.channeltrack.Channel` instance, or a
            string.

        :param \*args:
            Users to devoice. Can be
            :py:class:`~PyIRC.extensions.usertrack.User` instances or strings.

        """
        if not args:
            raise ValueError('args are needed for this function')
        self.mode_params(False, 'v', channel, *args)

    def halfop(self, channel, *args):
        r"""Halfop a user (or users) on a given channel.

        This may not be supported by your IRC server. Notably, FreeNode,
        EfNet, and IRCNet do not support this.

        :param channel:
            Channel to halfop the user or users in. This can be a
            :py:class:`~PyIRC.extensions.channeltrack.Channel` instance, or a
            string.

        :param \*args:
            Users to halfop. Can be
            :py:class:`~PyIRC.extensions.usertrack.User` instances or strings.

        """
        if not args:
            raise ValueError('args are needed for this function')
        self.mode_params(True, 'h', channel, *args)

    def dehalfop(self, channel, *args):
        r"""Dehalfop a user (or users) on a given channel.

        This may not be supported by your IRC server. Notably, FreeNode,
        EfNet, and IRCNet do not support this.

        :param channel:
            Channel to dehalfop the user or users in. This can be a
            :py:class:`~PyIRC.extensions.channeltrack.Channel` instance, or a
            string.

        :param \*args:
            Users to dehalfop. Can be
            :py:class:`~PyIRC.extensions.usertrack.User` instances or strings.

        """
        if not args:
            raise ValueError('args are needed for this function')
        self.mode_params(False, 'h', channel, *args)

    def process_bantargs(self, *args):
        """Process ban targets (as used by ban modes).

        .. note::
            The default mask format is $a:account if an account is available
            for the user. This only works on servers that support extended
            bans. The fallback is ``*!*@host``. This may not be suitable for
            all uses. It is recommended more advanced users use strings
            instead of User instances.

        """
        if not args:
            raise ValueError('args are needed for this function')
        isupport = self.base.isupport
        if not isupport:
            extbans = False
        else:
            extban = isupport.get('EXTBAN')
            if extban[0] != '$' or 'a' not in extban[1]:
                extbans = False
            else:
                extbans = True
        params = []
        for param in args:
            if not hasattr(param, 'nick'):
                params.append(param)
                continue
            if extbans and param.account:
                param = '$a:{}'.format(param.account)
            else:
                param = '*!*@{}'.format(param.host)
            params.append(param)

        return params

    def ban(self, channel, *args):
        r"""Ban a user (or users) on a given channel.

        :param channel:
            Channel to ban the user or users in. This can be a
            :py:class:`~PyIRC.extensions.channeltrack.Channel` instance, or a
            string.

        :param \*args:
            Users to ban. Can be
            :py:class:`~PyIRC.extensions.usertrack.User` instances or strings.

        .. note::
            All items are passed through :meth:`process_bantargs`.

        """
        self.mode_params(True, 'b', channel, *self.process_bantargs(*args))

    def unban(self, channel, *args):
        r"""Unban a user (or users) on a given channel.

        Note at present this is not reliable if User instances are passed in.
        This is an unfortunate side effect of the way IRC works (ban masks may
        be freeform). Another extension may provide enhanced capability to
        do this in the future.

        :param channel:
            Channel to unban the user or users in. This can be a
            :py:class:`~PyIRC.extensions.channeltrack.Channel` instance, or a
            string.

        :param \*args:
            Users to unban. Can be
            :py:class:`~PyIRC.extensions.usertrack.User` instances or strings.

        .. note::
            All items are passed through :meth:`process_bantargs`.

        """
        self.mode_params(False, 'b', channel, *self.process_bantargs(*args))

    def banexempt(self, channel, *args):
        r"""Exempt a user (or users) from being banned on a given channel.

        Most (but not all) servers support this. IRCNet notably does not.

        :param channel:
            Channel to ban exempt the user or users in. This can be a
            :py:class:`~PyIRC.extensions.channeltrack.Channel` instance, or a
            string.

        :param \*args:
            Users to ban exempt. Can be
            :py:class:`~PyIRC.extensions.usertrack.User` instances or strings.

        .. note::
            All items are passed through :meth:`process_bantargs`.

        """
        isupport = self.base.isupport
        if isupport and not (isupport.get('EXCEPTS') or 'e' in isupport.get('CHANMODES')[0]):
            return False
        self.mode_params(True, 'e', channel, *self.process_bantargs(*args))

    def unbanexempt(self, channel, *args):
        r"""Un-exempt a user (or users) from being banned on a given channel.

        Most (but not all) servers support this. IRCNet notably does not.

        Note at present this is not reliable if User instances are passed in.
        This is an unfortunate side effect of the way IRC works (ban masks may
        be freeform). Another extension may provide enhanced capability to
        do this in the future.

        :param channel:
            Channel to un-ban exempt the user or users in. This can be a
            :py:class:`~PyIRC.extensions.channeltrack.Channel` instance, or a
            string.

        :param \*args:
            Users to un-ban exempt. Can be
            :py:class:`~PyIRC.extensions.usertrack.User` instances or strings.

        .. note::
            All items are passed through :meth:`process_bantargs`.
        """
        isupport = self.base.isupport
        if isupport and not (isupport.get('EXCEPTS') or 'e' in isupport.get('CHANMODES')[0]):
            return False
        self.mode_params(False, 'e', channel, *self.process_bantargs(*args))

    def inviteexempt(self, channel, *args):
        r"""Invite exempt a user (or users) on a given channel.

        Most (but not all) servers support this. IRCNet notably does not.

        :param channel:
            Channel to ban exempt the user or users in. This can be a
            :py:class:`~PyIRC.extensions.channeltrack.Channel` instance, or a
            string.

        :param \*args:
            Users to invite exempt. Can be
            :py:class:`~PyIRC.extensions.usertrack.User` instances or strings.

        .. note::
            All items are passed through :meth:`process_bantargs`.

        """
        isupport = self.base.isupport
        if isupport and not (isupport.get('EXCEPTS') or 'I' in isupport.get('CHANMODES')[0]):
            return False
        self.mode_params(True, 'I', channel, *self.process_bantargs(*args))

    def uninviteexempt(self, channel, *args):
        r"""Un-invite exempt a user (or users) on a given channel.

        Most (but not all) servers support this. IRCNet notably does not.

        Note at present this is not reliable if User instances are passed in.
        This is an unfortunate side effect of the way IRC works (masks may be
        freeform). Another extension may provide enhanced capability to do this
        in the future.

        :param channel:
            Channel to un-invite exempt the user or users in. This can be a
            :py:class:`~PyIRC.extensions.channeltrack.Channel` instance, or a
            string.

        :param \*args:
            Users to un-invite exempt. Can be
            :py:class:`~PyIRC.extensions.usertrack.User` instances or strings.

        .. note::
            All items are passed through :meth:`process_bantargs`.
        """
        isupport = self.base.isupport
        if isupport and not (isupport.get('EXCEPTS') or 'I' in isupport.get('CHANMODES')[0]):
            return False
        self.mode_params(False, 'I', channel, *self.process_bantargs(*args))

    def quiet(self, channel, *args):
        r"""Quiet a user (or users) on a given channel.

        Many servers do not support this. This supports the charybdis-derived
        variant. This means it will work on Charybdis and ircd-seven networks
        (notably FreeNode) but few others.

        InspIRCd and (UnrealIRCd) support will come eventually.

        This **requires** :py:class:`~PyIRC.extensions.isupport.ISupport` be
        enabled, to disambiguate quiet from owner on UnrealIRCd and InspIRCd.

        :param channel:
            Channel to quiet the user or users in. This can be a
            :py:class:`~PyIRC.extensions.channeltrack.Channel` instance, or a
            string.

        :param \*args:
            Users to quiet. Can be
            :py:class:`~PyIRC.extensions.usertrack.User` instances or strings.

        .. note::
            All items are passed through :meth:`process_bantargs`.

        """
        isupport = self.base.isupport
        if not isupport:
            return False
        if 'q' not in isupport.get('CHANMODES')[0]:
            return False
        if 'q' in isupport.get('PREFIX'):
            return False
        self.mode_params(True, 'q', channel, *self.process_bantargs(*args))

    def unquiet(self, channel, *args):
        r"""Unquiet a user (or users) on a given channel.

        Many servers do not support this. This supports the charybdis-derived
        variant. This means it will work on Charybdis and ircd-seven networks
        (notably FreeNode) but few others.

        InspIRCd and (UnrealIRCd) support will come eventually.

        This **requires** :py:class:`~PyIRC.extensions.isupport.ISupport` be
        enabled, to disambiguate quiet from owner on UnrealIRCd and InspIRCd.

        Note at present this is not reliable if
        :py:class:`~PyIRC.extensions.usertrack.User` instances are passed in.
        This is an unfortunate side effect of the way IRC works (masks may be
        freeform). Another extension may provide enhanced capability to do this
        in the future.

        :param channel:
            Channel to unquiet the user or users in. This can be a
            :py:class:`~PyIRC.extensions.channeltrack.Channel` instance, or a
            string.

        :param \*args:
            Users to unquiet. Can be
            :py:class:`~PyIRC.extensions.usertrack.User` instances or strings.

        .. note::
            All items are passed through :meth:`process_bantargs`.

        """
        isupport = self.base.isupport
        if not isupport:
            return False
        if 'q' not in isupport.get('CHANMODES')[0]:
            return False
        if 'q' in isupport.get('PREFIX'):
            return False
        self.mode_params(False, 'q', channel, *self.process_bantargs(*args))

    def join(self, channel, key=None):
        """Attempt to join a channel.

        :param channel:
            Name of the Channel to join.

        :param key:
            Channel key to use, if needed.

        """
        params = [
         channel]
        if key is not None:
            params.append(key)
        self.send('JOIN', params)

    def part(self, channel, reason=None):
        """Part a channel.

        :param channel:
            Channel to part from. This can be a
            :py:class:`~PyIRC.extensions.channeltrack.Channel` instance, or a
            string.

        :param reason:
            Freeform reason to leave the channel.

        """
        if hasattr(channel, 'name'):
            channel = channel.name
        params = [channel]
        if reason is not None:
            params.append(reason)
        self.send('PART', params)

    def kick(self, channel, user, reason=None):
        """Kick a user from a channel.

        ..note:: This command usually requires channel operator privileges.

        :param channel:
            Where to kick the user from. This may be a
            :py:class:`~PyIRC.extensions.channeltrack.Channel` instance, or a
            string.

        :param user:
            User to kick from the channel. This may be a
            :py:class:`~PyIRC.extensions.usertrack.User` instance, or a
            string.

        :param reason:
            Freeform reason to kick the user.

        """
        if hasattr(channel, 'name'):
            channel = channel.name
        if hasattr(user, 'nick'):
            user = user.nick
        params = [channel, user]
        if reason is not None:
            params.append(reason)
        self.send('KICK', params)