# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/archipelcore/archipelAvatarControllableEntity.py
# Compiled at: 2013-03-20 13:50:16
import base64, hashlib, glob, os, xmpp
from archipelcore.utils import build_error_iq
ARCHIPEL_ERROR_CODE_AVATARS = -1
ARCHIPEL_ERROR_CODE_SET_AVATAR = -2
ARCHIPEL_NS_AVATAR = 'archipel:avatar'

class TNAvatarControllableEntity(object):
    """
    This class makes TNArchipelEntity avatar controllable.
    It allows to get and set avatars of the entity.
    """

    def __init__(self, configuration, permission_center, xmppclient, log):
        """
        Initialize the TNAvatarControllableEntity.
        @type configuration: configuration object
        @param configuration: the configuration
        @type permission_center: TNPermissionCenter
        @param permission_center: the permission center of the entity
        @type xmppclient: xmpp.Dispatcher
        @param xmppclient: the entity xmpp client
        @type log: TNArchipelLog
        @param log: the logger of the entity
        """
        self.configuration = configuration
        self.b64Avatar = None
        self.default_avatar = 'default.png'
        self.permission_center = permission_center
        self.xmppclient = xmppclient
        self.log = log
        return

    def check_acp(conn, iq):
        """
        Function that verify if the ACP is valid.
        @type conn: xmpp.Dispatcher
        @param conn: the connection
        @type iq: xmpp.Protocol.Iq
        @param iq: the IQ to check
        @raise Exception: Exception if not implemented
        """
        raise Exception('Subclass of TNAvatarControllableEntity must implement check_acp.')

    def check_perm(self, conn, stanza, action_name, error_code=-1, prefix=''):
        """
        Function that verify if the permissions are granted.
        @type conn: xmpp.Dispatcher
        @param conn: the connection
        @type stanza: xmpp.Node
        @param stanza: the stanza containing the action
        @type action_name: string
        @param action_name: the action to check
        @type error_code: int
        @param error_code: the error code to return
        @type prefix: string
        @param prefix: the prefix of the action
        @raise Exception: Exception if not implemented
        """
        raise Exception('Subclass of TNAvatarControllableEntity must implement check_perm.')

    def set_vcard(self, params={}):
        """
        Set the vcard of the entity.
        @type params: dict
        @param params: the parameters of the vCard
        @raise Exception: Exception if not implemented
        """
        raise Exception('Subclass of TNAvatarControllableEntity must implement set_vcard.')

    def init_permissions(self):
        """
        Initialize the Avatar permissions.
        """
        self.permission_center.create_permission('getavatars', 'Authorizes users to get entity avatars list', False)
        self.permission_center.create_permission('setavatar', "Authorizes users to set entity's avatar", False)

    def register_handlers(self):
        """
        Initialize the avatar handlers.
        """
        self.xmppclient.RegisterHandler('iq', self.process_avatar_iq, ns=ARCHIPEL_NS_AVATAR)

    def unregister_handlers(self):
        """
        Unregister the handlers.
        """
        self.xmppclient.UnregisterHandler('iq', self.process_avatar_iq, ns=ARCHIPEL_NS_AVATAR)

    def get_available_avatars(self, supported_file_extensions=[
 'png', 'jpg', 'jpeg', 'gif']):
        """
        Return a stanza with a list of availables avatars
        base64 encoded.
        """
        path = self.configuration.get('GLOBAL', 'machine_avatar_directory')
        resp = xmpp.Node('avatars')
        for ctype in supported_file_extensions:
            for img in glob.glob(os.path.join(path, '*.%s' % ctype)):
                f = open(img, 'r')
                data = base64.b64encode(f.read())
                image_hash = hashlib.md5(data).hexdigest()
                f.close()
                node_img = resp.addChild(name='avatar', attrs={'name': img.split('/')[(-1)], 'content-type': 'image/%s' % ctype, 'hash': image_hash})
                node_img.setData(data)

        return resp

    def set_avatar(self, name):
        """
        Change the current avatar of the entity.
        @type name: string
        @param name: the file name of avatar. base path is the configuration key "machine_avatar_directory"
        """
        name = name.replace('..', '').replace('/', '').replace('\\', '').replace(' ', '_')
        self.b64Avatar = None
        self.set_vcard(params={'filename': name})
        return

    def b64avatar_from_filename(self, image):
        """
        Create a base64 encoded avatar from filename.
        @type image: string
        @param image: relative file path of the image from conf token 'machine_avatar_directory'
        @rtype: string
        @return base64 encoded file content
        """
        avatar_dir = self.configuration.get('GLOBAL', 'machine_avatar_directory')
        f = open(os.path.join(avatar_dir, image), 'r')
        photo_data = base64.b64encode(f.read())
        f.close()
        self.b64Avatar = photo_data
        return self.b64Avatar

    def process_avatar_iq(self, conn, iq):
        """
        This method is invoked when a ARCHIPEL_NS_AVATAR IQ is received.
        It understands IQ of type:
            - alloc
            - free
        @type conn: xmpp.Dispatcher
        @param conn: ths instance of the current connection that send the stanza
        @type iq: xmpp.Protocol.Iq
        @param iq: the received IQ
        """
        reply = None
        action = self.check_acp(conn, iq)
        self.check_perm(conn, iq, action, -1)
        if action == 'getavatars':
            reply = self.iq_get_available_avatars(iq)
        elif action == 'setavatar':
            reply = self.iq_set_available_avatars(iq)
        if reply:
            conn.send(reply)
            raise xmpp.protocol.NodeProcessed
        return

    def iq_get_available_avatars(self, iq):
        """
        Return a list of availables avatars.
        @type iq: xmpp.Protocol.Iq
        @param iq: the IQ containing the request
        """
        try:
            reply = iq.buildReply('result')
            reply.setQueryPayload([self.get_available_avatars()])
        except Exception, ex:
            reply = build_error_iq(self, ex, iq, ARCHIPEL_ERROR_CODE_AVATARS)

        return reply

    def iq_set_available_avatars(self, iq):
        """
        Set the current avatar of the virtual machine.
        @type iq: xmpp.Protocol.Iq
        @param iq: the IQ containing the request
        """
        try:
            reply = iq.buildReply('result')
            avatar = iq.getTag('query').getTag('archipel').getAttr('avatar')
            self.set_avatar(avatar)
        except Exception, ex:
            reply = build_error_iq(self, ex, iq, ARCHIPEL_ERROR_CODE_SET_AVATAR)

        return reply