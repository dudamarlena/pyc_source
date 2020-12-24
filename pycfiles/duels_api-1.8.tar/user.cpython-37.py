# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Sources\Python\DUELS GAME\duels_api\objects\user.py
# Compiled at: 2019-03-04 16:45:41
# Size of source mod 2**32: 9644 bytes
import json, logging
from uuid import uuid4
import duels_api
from duels_api.settings import make_request

class User:

    def __init__(self, id=None, clan=None, log=None):
        if log is None:
            self.log = logging.getLogger('User')
        else:
            self.log = log
        self.id = id
        self.name = ''
        self.parts = []
        self.division = ''
        self.clan_id = ''
        self.clan = clan
        self.keys_amount = 0
        self.hp = 0
        self.attack = 0
        self.group_id = ''
        self.group_players = []
        self._get_me()

    def _get_user(self, user_id: str) -> dict:
        data = '{"playerId":"' + user_id + '","id":"' + self.id + '"}'
        j = make_request('profiles/details', data=data)
        if j:
            return j.get('player', None)
        return

    def _create_user(self) -> bool:
        data = '{"ids":["' + str(uuid4()) + '"],"appBundle":"com.deemedyainc.duels","appVersion":"0.6.6","platform":"Android"}'
        j = make_request('general/login', data=data)
        return j['profile']['_id']

    def _get_me(self) -> bool:
        if self.id is None:
            self.id = self._create_user()
            self.log.debug('Creating new user with id {}'.format(self.id))
        player = self._get_user(self.id)
        if player is not None:
            self.id = player.get('_id', None)
            self.name = player.get('name', None)
            self.division = player.get('division', None)
            self.clan_id = player.get('clanId', None)
            self.parts = player.get('character', None).get('parts', None)
            for part in self.parts:
                if part['stat']['info'] == 'Health':
                    self.hp += int(part['stat']['value'])

        return True

    def get_clan(self):
        if self.clan_id is not None:
            return duels_api.Clan(self.clan_id, self.id, self.log)
        return

    def leave_clan(self) -> bool:
        data = '{"id":"' + self.id + '"}'
        j = make_request('clan/leave', data=data)
        if j:
            self.log.debug('{} Leave clan'.format(self.name))
            return True
        self.log.debug('{} Cant leave clan'.format(self.name))
        return False

    def join_clan(self, clan_id: str) -> bool:
        data = '{"clanId":"' + str(clan_id) + '","id":"' + str(self.id) + '"}'
        j = make_request('clans/join', data=data)
        if j:
            self.log.debug('{} Join clan {}'.format(self.name, clan_id))
            return True
        self.log.debug('{} Cant join clan {}'.format(self.name, clan_id))
        return False

    def get_self_clan_members(self) -> list:
        clan = self.get_clan()
        if clan is not None:
            return clan.get_members()

    def claim_reward(self, claim_id: str) -> bool:
        data = '{"containerId":"' + str(claim_id) + '","id":"' + str(self.id) + '"}'
        j = make_request('queue/claim', data=data)
        if j:
            self.log.debug('{} Claimed reward'.format(self.id))
            return True
        self.log.debug('{} Cant claimed reward'.format(self.id))
        return False

    def get_special_crate--- This code section failed: ---

 L. 115         0  LOAD_STR                 '{"info":"SpecialCrate1","id":"'
                2  LOAD_GLOBAL              str
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                id
                8  CALL_FUNCTION_1       1  '1 positional argument'
               10  BINARY_ADD       
               12  LOAD_STR                 '"}'
               14  BINARY_ADD       
               16  STORE_FAST               'data'

 L. 116        18  LOAD_GLOBAL              make_request
               20  LOAD_STR                 'crates/buy'
               22  LOAD_FAST                'data'
               24  LOAD_CONST               ('data',)
               26  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               28  STORE_FAST               'j'

 L. 118        30  LOAD_FAST                'j'
               32  POP_JUMP_IF_FALSE   180  'to 180'

 L. 119        34  LOAD_FAST                'self'
               36  LOAD_ATTR                log
               38  LOAD_METHOD              debug
               40  LOAD_STR                 '{} Special crate'
               42  LOAD_METHOD              format
               44  LOAD_FAST                'self'
               46  LOAD_ATTR                id
               48  CALL_METHOD_1         1  '1 positional argument'
               50  CALL_METHOD_1         1  '1 positional argument'
               52  POP_TOP          

 L. 120        54  LOAD_FAST                'self'
               56  LOAD_METHOD              claim_reward
               58  LOAD_FAST                'j'
               60  LOAD_STR                 '_q'
               62  BINARY_SUBSCR    
               64  LOAD_CONST               0
               66  BINARY_SUBSCR    
               68  LOAD_STR                 '_id'
               70  BINARY_SUBSCR    
               72  CALL_METHOD_1         1  '1 positional argument'
               74  POP_JUMP_IF_FALSE   174  'to 174'

 L. 121        76  SETUP_LOOP          178  'to 178'
               78  LOAD_FAST                'j'
               80  LOAD_STR                 '_q'
               82  BINARY_SUBSCR    
               84  LOAD_CONST               0
               86  BINARY_SUBSCR    
               88  LOAD_STR                 'steps'
               90  BINARY_SUBSCR    
               92  LOAD_CONST               0
               94  BINARY_SUBSCR    
               96  LOAD_STR                 'crate'
               98  BINARY_SUBSCR    
              100  LOAD_STR                 'rewards'
              102  BINARY_SUBSCR    
              104  GET_ITER         
              106  FOR_ITER            170  'to 170'
              108  STORE_FAST               'i'

 L. 122       110  LOAD_FAST                'i'
              112  LOAD_STR                 'reward'
              114  BINARY_SUBSCR    
              116  STORE_FAST               'item'

 L. 123       118  LOAD_GLOBAL              Item
              120  LOAD_FAST                'item'
              122  LOAD_STR                 '__id'
              124  BINARY_SUBSCR    
              126  LOAD_FAST                'self'
              128  LOAD_ATTR                id
              130  LOAD_FAST                'item'
              132  LOAD_STR                 '__type'
              134  BINARY_SUBSCR    
              136  LOAD_FAST                'item'
              138  LOAD_STR                 'rarity'
              140  BINARY_SUBSCR    
              142  LOAD_FAST                'item'
              144  LOAD_STR                 'stat'
              146  BINARY_SUBSCR    
              148  LOAD_STR                 'info'
              150  BINARY_SUBSCR    
              152  LOAD_FAST                'item'
              154  LOAD_STR                 'stat'
              156  BINARY_SUBSCR    
              158  LOAD_STR                 'value'
              160  BINARY_SUBSCR    
              162  CALL_FUNCTION_6       6  '6 positional arguments'
              164  YIELD_VALUE      
              166  POP_TOP          
              168  JUMP_BACK           106  'to 106'
              170  POP_BLOCK        
              172  JUMP_ABSOLUTE       184  'to 184'
            174_0  COME_FROM            74  '74'

 L. 125       174  BUILD_LIST_0          0 
              176  RETURN_VALUE     
            178_0  COME_FROM_LOOP       76  '76'
              178  JUMP_FORWARD        184  'to 184'
            180_0  COME_FROM            32  '32'

 L. 127       180  BUILD_LIST_0          0 
              182  RETURN_VALUE     
            184_0  COME_FROM           178  '178'

Parse error at or near `COME_FROM_LOOP' instruction at offset 178_0

    def write_to_clan_chat(self, text: str) -> bool:
        data = '{"msg":"' + str(text) + '","id":"' + str(self.id) + '"}'
        j = make_request('clan/write', data=data)
        if j:
            return True
        return False

    def get_self_opponent_clan(self) -> str:
        clan = self.get_clan()
        if clan is not None:
            return clan.get_opponent_clan(self.clan_id, self.id)

    def search_clans(self) -> list:
        data = '{"id":"' + str(self.id) + '"}'
        j = make_request('clans/search', data=data)
        if j:
            for i in j['clans']:
                yield duels_api.Clan(i['_id'], self.id, self.log)

        else:
            return []

    def set_ranked_group_info(self) -> bool:
        data = '{"id":"' + self.id + '"}'
        j = make_request('ranking/group', data=data)
        if j:
            try:
                self.group_id = j['group']['_id']
                self.group_players = [i['pid'] for i in j['group']['members'] if i.get('pid') is not None]
                self.group_players.remove(self.id)
            except Exception as e:
                try:
                    print(self)
                    print(j)
                    print(e)
                finally:
                    e = None
                    del e

            return True
        return False

    def get_ranked_claim_id(self) -> str:
        data = '{"id":"' + str(self.id) + '"}'
        j = make_request('ranking/group', data=data)
        if j:
            j = j.get('_q')
            if j is not None:
                return j[0]['_id']
            return
        else:
            return

    def ranked_battle(self, enemy_id: str) -> bool:
        data = '{"enemyId":"' + str(enemy_id) + '","groupId":"' + str(self.group_id) + '","id":"' + str(self.id) + '"}'
        j = make_request('battle/ranked', data=data)
        if j:
            return True
        return False

    def clan_battle(self) -> int:
        if self.get_defeated_clan_opponent() < 10:
            self.log.debug('clan battle {}'.format(self.name))
            data = '{"id":"' + str(self.id) + '"}'
            j = make_request('clan/war/battle', data=data)
            if j:
                return j['battle']['result']
            return -1
        else:
            return -2

    def claim_reward_group(self) -> int:
        claim_id = self.get_ranked_claim_id()
        if claim_id is not None:
            data = '{"containerId":"' + str(claim_id) + '","id":"' + str(self.id) + '"}'
            j = make_request('queue/claim', data=data)
            if j:
                self.log.debug('Claim reward {} - keys: {}'.format(self.name, j['_u']['Key@Value']))
                return j['_u']['Key@Value']
            return -1
        else:
            self.log.debug('Cant get reward for ranked battle {}'.format(self.name))
            return -2

    def get_defeated_clan_opponent(self) -> int:
        data = '{"chat":false,"id":"' + self.id + '"}'
        j = make_request('clan', data=data)
        if j:
            j = j['clan']['war'].get('war', None)
            if j is not None:
                return j['defeatedOpponents']
            return 10
        else:
            return -1

    def defeat_ranked_group(self) -> int:
        self.set_ranked_group_info()
        if len(self.group_players) >= 15:
            for i in self.group_players:
                count = 0
                result = self.ranked_battle(i)
                while result != True and count <= 50:
                    result = self.ranked_battle(i)
                    count += 1

                if result != True:
                    player = User(i)
                    self.log.debug('Start working as {}'.format(player.name))
                    player.defeat_ranked_group()
                else:
                    self.log.debug('{} beated {}'.format(self.name, i))

            return self.claim_reward_group()
        self.log.debug('Not enough player in group {}'.format(self.name))
        return -1

    def get_stats(self) -> tuple:
        return (self.hp, self.attack)

    def save(self, file='users.json') -> bool:
        l = []
        try:
            with open(file, 'r', encoding='utf8') as (f):
                l = json.loads(f.read())
        except FileNotFoundError:
            pass

        l.append(self.id)
        with open(file, 'w', encoding='utf8') as (f):
            f.write(json.dumps(l) + '\n')
        return True

    def __eq__(self, other) -> bool:
        if isinstance(other, User):
            if other.id == self.id:
                return True
            return False
        else:
            if isinstance(other, str):
                if other == self.id:
                    return True
                return False
            else:
                return False

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return 'User ID: {} Name: {} Division: {} Clan ID: {} HP: {} Attack: {}'.format(self.id, self.name, self.division, self.clan_id, self.hp, self.attack)