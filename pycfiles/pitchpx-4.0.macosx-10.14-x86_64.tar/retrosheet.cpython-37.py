# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shinyorke/python_venv/pitchpx/lib/python3.7/site-packages/pitchpx/baseball/retrosheet.py
# Compiled at: 2018-12-12 04:43:08
# Size of source mod 2**32: 6546 bytes
__author__ = 'Shinichi Nakagawa'

class RetroSheet(object):
    EVENT_02_GENERIC_OUT_FLYBALL = ('flyout', 'fly out', 'sac fly', 'sac fly dp')
    EVENT_02_GENERIC_OUT_LINEDRIVE = ('lineout', 'line out', 'bunt lineout')
    EVENT_02_GENERIC_OUT_POPUP = ('pop out', 'bunt pop out')
    EVENT_02_GENERIC_OUT_GROUNDBALL = ('groundout', 'ground out', 'sac bunt', 'bunt groundout',
                                       'grounded into dp')
    EVENT_02_GENERIC_OUT_OTHER = ('forceout', 'double play', 'triple play', 'sacrifice bunt d')
    EVENT_03_STRIKE_OUT = ('strikeout', 'strikeout - dp')
    EVENT_14_WALK = ('walk', )
    EVENT_15_INTENT_WALK = ('intent walk', )
    EVENT_16_HIT_BY_PITCH = ('hit by pitch', )
    EVENT_19_FIELDERS_CHOICE = ('fielders choice out', 'fielders choice')
    EVENT_20_SINGLE = ('single', )
    EVENT_21_DOUBLE = ('double', )
    EVENT_22_TRIPLE = ('triple', )
    EVENT_23_HOME_RUN = ('home run', )
    EVENT_CD_HITS = (20, 21, 22, 23)

    @classmethod
    def event_cd(cls, event_tx, ab_des):
        """
        Event Code for Retrosheet
        :param event_tx: Event text
        :param ab_des: at bat description
        :return: event_cd(int)
        """
        _event_tx = event_tx.lower()
        _ab_des = ab_des.lower()
        if _event_tx in cls.EVENT_02_GENERIC_OUT_FLYBALL:
            return 2
            if _event_tx in cls.EVENT_02_GENERIC_OUT_LINEDRIVE:
                return 2
            if _event_tx in cls.EVENT_02_GENERIC_OUT_POPUP:
                return 2
            if _event_tx in cls.EVENT_02_GENERIC_OUT_GROUNDBALL:
                return 2
            if _event_tx in cls.EVENT_02_GENERIC_OUT_OTHER:
                return 2
            if _event_tx in cls.EVENT_03_STRIKE_OUT:
                return 3
            if _event_tx in cls.EVENT_14_WALK:
                return 14
            if _event_tx in cls.EVENT_15_INTENT_WALK:
                return 15
            if _event_tx in cls.EVENT_16_HIT_BY_PITCH:
                return 16
            if _event_tx.lower().count('interference') > 0:
                return 17
            if _event_tx[-5:] == 'error':
                return 18
            if _event_tx in cls.EVENT_19_FIELDERS_CHOICE:
                return 19
            if _event_tx in cls.EVENT_20_SINGLE:
                return 20
            if _event_tx in cls.EVENT_21_DOUBLE:
                return 21
            if _event_tx in cls.EVENT_22_TRIPLE:
                return 22
            if _event_tx in cls.EVENT_23_HOME_RUN:
                return 23
            if _event_tx == 'runner out':
                if _ab_des.count('caught stealing') > 0:
                    return 6
                if _ab_des.count('picks off') > 0:
                    return 8
                return 0
        else:
            return 0

    @classmethod
    def battedball_cd(cls, event_cd, event_tx, ab_des):
        """
        Batted ball Code for Retrosheet
        :param event_cd: Event code
        :param event_tx: Event text
        :param ab_des: at bat description
        :return: battedball_cd(str)
        """
        _event_tx = event_tx.lower()
        if _event_tx in cls.EVENT_02_GENERIC_OUT_FLYBALL:
            return 'F'
        if _event_tx in cls.EVENT_02_GENERIC_OUT_LINEDRIVE:
            return 'L'
        if _event_tx in cls.EVENT_02_GENERIC_OUT_POPUP:
            return 'P'
        if _event_tx in cls.EVENT_02_GENERIC_OUT_GROUNDBALL:
            return 'G'
        if _event_tx in cls.EVENT_02_GENERIC_OUT_OTHER:
            return cls._battedball_cd(ab_des)
        if event_cd in cls.EVENT_CD_HITS:
            return cls._battedball_cd(ab_des)
        return ''

    @classmethod
    def _battedball_cd(cls, ab_des):
        """
        Batted ball Code for at bat description
        :param ab_des: at bat description
        :return: battedball_cd(str)
        """
        _ab_des = ab_des.lower()
        if ab_des.count('ground') > 0:
            return 'G'
        if _ab_des.count('lines') > 0:
            return 'L'
        if _ab_des.count('flies') > 0:
            return 'F'
        if _ab_des.count('pops') > 0:
            return 'P'
        if _ab_des.count('on a line drive') > 0:
            return 'L'
        if _ab_des.count('fly ball') > 0:
            return 'F'
        if _ab_des.count('ground ball') > 0:
            return 'G'
        if _ab_des.count('pop up') > 0:
            return 'P'
        return ''

    @classmethod
    def ball_count--- This code section failed: ---

 L. 162         0  LOAD_FAST                'ball_tally'
                2  LOAD_FAST                'strike_tally'
                4  ROT_TWO          
                6  STORE_FAST               'b'
                8  STORE_FAST               's'

 L. 163        10  LOAD_FAST                'pitch_res'
               12  LOAD_STR                 'B'
               14  COMPARE_OP               ==
               16  POP_JUMP_IF_FALSE    36  'to 36'

 L. 164        18  LOAD_FAST                'ball_tally'
               20  LOAD_CONST               4
               22  COMPARE_OP               <
               24  POP_JUMP_IF_FALSE   102  'to 102'

 L. 165        26  LOAD_FAST                'b'
               28  LOAD_CONST               1
               30  INPLACE_ADD      
               32  STORE_FAST               'b'
               34  JUMP_FORWARD        102  'to 102'
             36_0  COME_FROM            16  '16'

 L. 166        36  LOAD_FAST                'pitch_res'
               38  LOAD_STR                 'S'
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_TRUE     60  'to 60'
               44  LOAD_FAST                'pitch_res'
               46  LOAD_STR                 'C'
               48  COMPARE_OP               ==
               50  POP_JUMP_IF_TRUE     60  'to 60'
               52  LOAD_FAST                'pitch_res'
               54  LOAD_STR                 'X'
               56  COMPARE_OP               ==
               58  POP_JUMP_IF_FALSE    78  'to 78'
             60_0  COME_FROM            50  '50'
             60_1  COME_FROM            42  '42'

 L. 167        60  LOAD_FAST                'strike_tally'
               62  LOAD_CONST               3
               64  COMPARE_OP               <
               66  POP_JUMP_IF_FALSE   102  'to 102'

 L. 168        68  LOAD_FAST                's'
               70  LOAD_CONST               1
               72  INPLACE_ADD      
               74  STORE_FAST               's'
               76  JUMP_FORWARD        102  'to 102'
             78_0  COME_FROM            58  '58'

 L. 169        78  LOAD_FAST                'pitch_res'
               80  LOAD_STR                 'F'
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE   102  'to 102'

 L. 170        86  LOAD_FAST                'strike_tally'
               88  LOAD_CONST               2
               90  COMPARE_OP               <
               92  POP_JUMP_IF_FALSE   102  'to 102'

 L. 171        94  LOAD_FAST                's'
               96  LOAD_CONST               1
               98  INPLACE_ADD      
              100  STORE_FAST               's'
            102_0  COME_FROM            92  '92'
            102_1  COME_FROM            84  '84'
            102_2  COME_FROM            76  '76'
            102_3  COME_FROM            66  '66'
            102_4  COME_FROM            34  '34'
            102_5  COME_FROM            24  '24'

 L. 172       102  LOAD_FAST                'b'
              104  LOAD_FAST                's'
              106  BUILD_TUPLE_2         2 
              108  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 108

    @classmethod
    def is_pa_terminal(cls, ball_tally, strike_tally, pitch_res, event_cd):
        """
        Is PA terminal
        :param ball_tally: Ball telly
        :param strike_tally: Strike telly
        :param pitch_res: pitching result(Retrosheet format)
        :param event_cd: Event code
        :return: True or False
        """
        if pitch_res == 'X':
            return True
            if pitch_res == 'S' or pitch_res == 'C':
                if event_cd == 3:
                    if strike_tally == 2:
                        return True
        elif pitch_res == 'B' and not event_cd == 14:
            if event_cd == 15:
                if ball_tally == 3:
                    return True
        return False