# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/aarontraas/workspace/personal/Clash-Royale-Clan-Tools/crtools/models/warparticipation.py
# Compiled at: 2019-10-16 15:53:38
# Size of source mod 2**32: 4257 bytes
from datetime import datetime, timedelta
from crtools import leagueinfo
from crtools.scorecalc import ScoreCalculator

def _get_war_date(war):
    """ returns the datetime this war was created. If it's an ongoing
    war, calculate based on the dates given when the war started.
    If it's a previous war fromt he warlog, we retrieve the creation
    date. What's returned is a timestamp. """
    war_date_raw = 0
    if hasattr(war, 'state'):
        if war.state == 'warDay':
            war_date_raw = datetime.strptime(war.war_end_time.split('.')[0], '%Y%m%dT%H%M%S')
            war_date_raw -= timedelta(days=2)
        elif war.state == 'collectionDay':
            war_date_raw = datetime.strptime(war.collection_end_time.split('.')[0], '%Y%m%dT%H%M%S')
            war_date_raw -= timedelta(days=1)
    else:
        war_date_raw = datetime.strptime(war.created_date.split('.')[0], '%Y%m%dT%H%M%S')
        war_date_raw -= timedelta(days=1)
    return datetime.timestamp(war_date_raw)


def _get_member_war_status_class(collection_day_battles, war_day_battles, war_date, join_date, current_war=False, war_day=False):
    """ returns CSS class(es) for a war log entry for a given member """
    if war_date < join_date:
        return 'not-in-clan'
        status = 'normal'
        if current_war:
            if collection_day_battles < 3:
                status = 'ok'
            elif war_day and war_day_battles > 0:
                status = 'good'
            if war_day == False or war_day_battles == 0:
                status += ' incomplete'
    elif collection_day_battles == 0:
        status = 'na'
    elif war_day_battles == 0:
        status = 'bad'
    elif collection_day_battles < 3:
        status = 'ok'
    else:
        status = 'good'
    return status


class WarParticipation:

    def __init__--- This code section failed: ---

 L.  55         0  LOAD_CONST               False
                2  LOAD_FAST                'self'
                4  STORE_ATTR               in_war

 L.  56         6  LOAD_STR                 'na'
                8  LOAD_FAST                'self'
               10  STORE_ATTR               status

 L.  57        12  LOAD_CONST               0
               14  LOAD_FAST                'self'
               16  STORE_ATTR               score

 L.  58        18  LOAD_CONST               False
               20  LOAD_FAST                'self'
               22  STORE_ATTR               battles_played

 L.  59        24  LOAD_CONST               0
               26  LOAD_FAST                'self'
               28  STORE_ATTR               cards_earned

 L.  60        30  LOAD_CONST               0
               32  LOAD_FAST                'self'
               34  STORE_ATTR               collection_win_cards

 L.  61        36  LOAD_CONST               0
               38  LOAD_FAST                'self'
               40  STORE_ATTR               collection_day_battles_played

 L.  62        42  LOAD_CONST               0
               44  LOAD_FAST                'self'
               46  STORE_ATTR               collection_battle_wins

 L.  63        48  LOAD_CONST               0
               50  LOAD_FAST                'self'
               52  STORE_ATTR               collection_battle_losses

 L.  64        54  LOAD_CONST               0
               56  LOAD_FAST                'self'
               58  STORE_ATTR               wins

 L.  65        60  LOAD_STR                 'na'
               62  LOAD_FAST                'self'
               64  STORE_ATTR               war_league

 L.  66        66  LOAD_CONST               0
               68  LOAD_FAST                'self'
               70  STORE_ATTR               number_of_battles

 L.  70        72  LOAD_GLOBAL              hasattr
               74  LOAD_FAST                'war'
               76  LOAD_STR                 'state'
               78  CALL_FUNCTION_2       2  ''
               80  POP_JUMP_IF_FALSE    96  'to 96'
               82  LOAD_FAST                'war'
               84  LOAD_ATTR                state
               86  LOAD_STR                 'notInWar'
               88  COMPARE_OP               ==
               90  POP_JUMP_IF_FALSE    96  'to 96'

 L.  71        92  LOAD_CONST               None
               94  RETURN_VALUE     
             96_0  COME_FROM            90  '90'
             96_1  COME_FROM            80  '80'

 L.  73        96  LOAD_FAST                'member'
               98  LOAD_ATTR                tag
              100  STORE_FAST               'member_tag'

 L.  74       102  LOAD_GLOBAL              _get_war_date
              104  LOAD_FAST                'war'
              106  CALL_FUNCTION_1       1  ''
              108  STORE_FAST               'war_date'

 L.  75       110  LOAD_GLOBAL              hasattr
              112  LOAD_FAST                'member'
              114  LOAD_STR                 'join_date'
              116  CALL_FUNCTION_2       2  ''
              118  POP_JUMP_IF_FALSE   126  'to 126'
              120  LOAD_FAST                'member'
              122  LOAD_ATTR                join_date
              124  JUMP_FORWARD        128  'to 128'
            126_0  COME_FROM           118  '118'
              126  LOAD_CONST               0
            128_0  COME_FROM           124  '124'
              128  STORE_FAST               'join_date'

 L.  77       130  LOAD_GLOBAL              hasattr
              132  LOAD_FAST                'war'
              134  LOAD_STR                 'state'
              136  CALL_FUNCTION_2       2  ''
              138  POP_JUMP_IF_FALSE   148  'to 148'

 L.  78       140  LOAD_CONST               0
              142  LOAD_FAST                'self'
              144  STORE_ATTR               score
              146  JUMP_FORWARD        182  'to 182'
            148_0  COME_FROM           138  '138'

 L.  79       148  LOAD_FAST                'war_date'
              150  LOAD_FAST                'join_date'
              152  COMPARE_OP               <
              154  POP_JUMP_IF_FALSE   166  'to 166'

 L.  81       156  LOAD_STR                 'not-in-clan'
              158  LOAD_FAST                'self'
              160  STORE_ATTR               status

 L.  82       162  LOAD_CONST               None
              164  RETURN_VALUE     
            166_0  COME_FROM           154  '154'

 L.  85       166  LOAD_GLOBAL              ScoreCalculator
              168  LOAD_FAST                'config'
              170  CALL_FUNCTION_1       1  ''
              172  LOAD_METHOD              get_war_score
              174  LOAD_FAST                'self'
              176  CALL_METHOD_1         1  ''
              178  LOAD_FAST                'self'
              180  STORE_ATTR               score
            182_0  COME_FROM           146  '146'

 L.  87       182  LOAD_FAST                'war'
              184  LOAD_ATTR                participants
              186  GET_ITER         
            188_0  COME_FROM           200  '200'
              188  FOR_ITER            406  'to 406'
              190  STORE_FAST               'participant'

 L.  88       192  LOAD_FAST                'participant'
              194  LOAD_ATTR                tag
              196  LOAD_FAST                'member_tag'
              198  COMPARE_OP               ==
              200  POP_JUMP_IF_FALSE   188  'to 188'

 L.  89       202  LOAD_CONST               True
              204  LOAD_FAST                'self'
              206  STORE_ATTR               in_war

 L.  90       208  LOAD_FAST                'participant'
              210  LOAD_ATTR                cards_earned
              212  LOAD_FAST                'self'
              214  STORE_ATTR               cards_earned

 L.  91       216  LOAD_FAST                'participant'
              218  LOAD_ATTR                battles_played
              220  LOAD_FAST                'self'
              222  STORE_ATTR               battles_played

 L.  92       224  LOAD_FAST                'participant'
              226  LOAD_ATTR                collection_day_battles_played
              228  LOAD_FAST                'self'
              230  STORE_ATTR               collection_day_battles_played

 L.  93       232  LOAD_FAST                'participant'
              234  LOAD_ATTR                wins
              236  LOAD_FAST                'self'
              238  STORE_ATTR               wins

 L.  94       240  LOAD_FAST                'participant'
              242  LOAD_ATTR                number_of_battles
              244  LOAD_FAST                'self'
              246  STORE_ATTR               number_of_battles

 L.  96       248  LOAD_GLOBAL              hasattr
              250  LOAD_FAST                'war'
              252  LOAD_STR                 'state'
              254  CALL_FUNCTION_2       2  ''
          256_258  POP_JUMP_IF_FALSE   296  'to 296'

 L.  97       260  LOAD_GLOBAL              _get_member_war_status_class
              262  LOAD_FAST                'self'
              264  LOAD_ATTR                collection_day_battles_played
              266  LOAD_FAST                'self'
              268  LOAD_ATTR                battles_played
              270  LOAD_FAST                'war_date'
              272  LOAD_FAST                'join_date'
              274  LOAD_CONST               True
              276  LOAD_FAST                'war'
              278  LOAD_ATTR                state
              280  LOAD_STR                 'warDay'
              282  COMPARE_OP               ==
              284  CALL_FUNCTION_6       6  ''
              286  LOAD_FAST                'self'
              288  STORE_ATTR               status

 L.  98       290  POP_TOP          
              292  LOAD_CONST               None
              294  RETURN_VALUE     
            296_0  COME_FROM           256  '256'

 L. 100       296  LOAD_GLOBAL              _get_member_war_status_class
              298  LOAD_FAST                'self'
              300  LOAD_ATTR                collection_day_battles_played
              302  LOAD_FAST                'self'
              304  LOAD_ATTR                battles_played
              306  LOAD_FAST                'war_date'
              308  LOAD_FAST                'join_date'
              310  CALL_FUNCTION_4       4  ''
              312  LOAD_FAST                'self'
              314  STORE_ATTR               status

 L. 102       316  LOAD_GLOBAL              leagueinfo
              318  LOAD_METHOD              get_war_league_from_war
              320  LOAD_FAST                'war'
              322  LOAD_FAST                'config'
              324  LOAD_STR                 'api'
              326  BINARY_SUBSCR    
              328  LOAD_STR                 'clan_id'
              330  BINARY_SUBSCR    
              332  CALL_METHOD_2         2  ''
              334  LOAD_FAST                'self'
              336  STORE_ATTR               war_league

 L. 103       338  LOAD_GLOBAL              leagueinfo
              340  LOAD_METHOD              get_collection_win_cards
              342  LOAD_FAST                'self'
              344  LOAD_ATTR                war_league
              346  LOAD_FAST                'member'
              348  LOAD_ATTR                arena_league
              350  CALL_METHOD_2         2  ''
              352  LOAD_FAST                'self'
              354  STORE_ATTR               collection_win_cards

 L. 105       356  LOAD_GLOBAL              round
              358  LOAD_FAST                'self'
              360  LOAD_ATTR                cards_earned
              362  LOAD_FAST                'self'
              364  LOAD_ATTR                collection_win_cards
              366  BINARY_TRUE_DIVIDE
              368  CALL_FUNCTION_1       1  ''
              370  LOAD_FAST                'self'
              372  STORE_ATTR               collection_battle_wins

 L. 106       374  LOAD_FAST                'self'
              376  LOAD_ATTR                collection_day_battles_played
              378  LOAD_FAST                'self'
              380  LOAD_ATTR                collection_battle_wins
              382  BINARY_SUBTRACT  
              384  LOAD_FAST                'self'
              386  STORE_ATTR               collection_battle_losses

 L. 107       388  LOAD_GLOBAL              ScoreCalculator
              390  LOAD_FAST                'config'
              392  CALL_FUNCTION_1       1  ''
              394  LOAD_METHOD              get_war_score
              396  LOAD_FAST                'self'
              398  CALL_METHOD_1         1  ''
              400  LOAD_FAST                'self'
              402  STORE_ATTR               score
              404  JUMP_BACK           188  'to 188'

Parse error at or near `LOAD_CONST' instruction at offset 292