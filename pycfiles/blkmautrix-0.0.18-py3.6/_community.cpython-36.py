# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/bridge/_community.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 3321 bytes
from typing import Optional, NewType, Tuple
from mautrix.api import Path, Method
from mautrix.appservice import AppService, IntentAPI
from mautrix.types import UserID, RoomID, ContentURI
from mautrix.errors import MatrixStandardRequestError
CommunityID = NewType('CommunityID', str)

class CommunityHelper:
    az: AppService

    def __init__(self, az: AppService) -> None:
        self.az = az

    async def create(self, localpart: str) -> Tuple[(CommunityID, bool)]:
        try:
            resp = await self.az.intent.api.request(Method.POST, Path.create_group, {'localpart': localpart})
            return (
             CommunityID(resp['group_id']), True)
        except MatrixStandardRequestError as e:
            if e.message == 'Group already exists':
                return (
                 CommunityID(f"+{localpart}:{self.az.domain}"), False)
            raise

    async def update(self, community_id: CommunityID, name: Optional[str]=None, avatar_url: Optional[ContentURI]=None, short_desc: Optional[str]=None, long_desc: Optional[str]=None) -> None:
        if not community_id:
            return
        await self.az.intent.api.request(Method.POST, Path.groups[community_id].profile, {k:v for k, v in {'name':name, 
         'avatar_url':avatar_url, 
         'short_description':short_desc, 
         'long_description':long_desc}.items() if v is not None if v is not None})

    async def invite(self, community_id: CommunityID, user_id: UserID) -> None:
        if not community_id or not user_id:
            return
        try:
            await self.az.intent.api.request(Method.PUT, Path.groups[community_id].admin.users.invite[user_id])
        except MatrixStandardRequestError as e:
            self.az.intent.log.warning(f"Failed to invite {user_id} to {community_id}: {e}")

    async def join(self, community_id: CommunityID, intent: IntentAPI) -> bool:
        if not community_id or not intent:
            return False
        else:
            await intent.ensure_registered()
            await self.invite(community_id, intent.mxid)
            try:
                await intent.api.request(Method.PUT, Path.groups[community_id].self.accept_invite)
            except MatrixStandardRequestError as e:
                intent.log.warning(f"Failed to join {community_id}: {e}")

            return True

    async def add_room(self, community_id: CommunityID, room_id: RoomID) -> bool:
        if not community_id or not room_id:
            return False
        else:
            try:
                await self.az.intent.api.request(Method.PUT, Path.groups[community_id].admin.rooms[room_id])
            except MatrixStandardRequestError as e:
                self.az.intent.log.warning(f"Failed to add {room_id} to {community_id}: {e}")

            return True