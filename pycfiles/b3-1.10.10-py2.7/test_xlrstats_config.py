# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\xlrstats\test_xlrstats_config.py
# Compiled at: 2016-03-08 18:42:10
import logging, os
from b3.config import CfgConfigParser
from b3.plugins.xlrstats import XlrstatsPlugin
from b3 import __file__ as b3_module__file__
from tests import B3TestCase
DEFAULT_XLRSTATS_CONFIG_FILE = os.path.join(os.path.dirname(b3_module__file__), 'conf', 'plugin_xlrstats.ini')

class XlrstatsTestCase(B3TestCase):

    def setUp(self):
        """
        This method is called before each test.
        It is meant to set up the SUT (System Under Test) in a manner that will ease the testing of its features.
        """
        B3TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.p = XlrstatsPlugin(self.console, self.conf)
        logger = logging.getLogger('output')
        logger.setLevel(logging.DEBUG)


class Test_conf(XlrstatsTestCase):

    def test_empty_conf(self):
        """
        Test the behaviors expected when one starts the Xlrstats plugin with an empty config file
        """
        self.conf.loadFromString('\n        ')
        self.p.onLoadConfig()
        self.assertFalse(self.p.silent)
        self.assertTrue(self.p.hide_bots)
        self.assertTrue(self.p.exclude_bots)
        self.assertEqual(3, self.p.min_players)
        self.assertEqual('', self.p.webfront_url)
        self.assertEqual(0, self.p.webfront_config_nr)
        self.assertTrue(self.p.keep_history)
        self.assertFalse(self.p.onemaponly)
        self.assertEqual(0, self.p.minlevel)
        self.assertEqual(1000, self.p.defaultskill)
        self.assertEqual(16, self.p.Kfactor_high)
        self.assertEqual(4, self.p.Kfactor_low)
        self.assertEqual(50, self.p.Kswitch_confrontations)
        self.assertEqual(600, self.p.steepness)
        self.assertEqual(0.05, self.p.suicide_penalty_percent)
        self.assertEqual(0.1, self.p.tk_penalty_percent)
        self.assertEqual(2, self.p.assist_timespan)
        self.assertEqual(10, self.p.damage_assist_release)
        self.assertEqual(70, self.p.prematch_maxtime)
        self.assertFalse(self.p.announce)
        self.assertTrue(self.p.keep_time)
        self.assertTrue(self.p.provisional_ranking)
        self.assertTrue(self.p._defaultTableNames)
        self.assertEqual('xlr_playerstats', self.p.playerstats_table)
        self.assertEqual('xlr_weaponstats', self.p.weaponstats_table)
        self.assertEqual('xlr_weaponusage', self.p.weaponusage_table)
        self.assertEqual('xlr_bodyparts', self.p.bodyparts_table)
        self.assertEqual('xlr_playerbody', self.p.playerbody_table)
        self.assertEqual('xlr_opponents', self.p.opponents_table)
        self.assertEqual('xlr_mapstats', self.p.mapstats_table)
        self.assertEqual('xlr_playermaps', self.p.playermaps_table)
        self.assertEqual('xlr_actionstats', self.p.actionstats_table)
        self.assertEqual('xlr_playeractions', self.p.playeractions_table)
        self.assertEqual('xlr_history_monthly', self.p.history_monthly_table)
        self.assertEqual('xlr_history_weekly', self.p.history_weekly_table)
        self.assertEqual('ctime', self.p.ctime_table)

    def test_default_conf(self):
        """
        Test the behaviors expected when one starts the Xlrstats plugin with the default config file
        """
        self.conf.load(DEFAULT_XLRSTATS_CONFIG_FILE)
        self.p.onLoadConfig()
        self.assertFalse(self.p.silent)
        self.assertTrue(self.p.hide_bots)
        self.assertTrue(self.p.exclude_bots)
        self.assertEqual(3, self.p.min_players)
        self.assertEqual('', self.p.webfront_url)
        self.assertEqual(0, self.p.webfront_config_nr)
        self.assertTrue(self.p.keep_history)
        self.assertFalse(self.p.onemaponly)
        self.assertEqual(0, self.p.minlevel)
        self.assertEqual(1000, self.p.defaultskill)
        self.assertEqual(16, self.p.Kfactor_high)
        self.assertEqual(4, self.p.Kfactor_low)
        self.assertEqual(50, self.p.Kswitch_confrontations)
        self.assertEqual(600, self.p.steepness)
        self.assertEqual(0.05, self.p.suicide_penalty_percent)
        self.assertEqual(0.1, self.p.tk_penalty_percent)
        self.assertEqual(2, self.p.assist_timespan)
        self.assertEqual(10, self.p.damage_assist_release)
        self.assertEqual(70, self.p.prematch_maxtime)
        self.assertFalse(self.p.announce)
        self.assertTrue(self.p.keep_time)
        self.assertTrue(self.p.provisional_ranking)
        self.assertTrue(self.p._defaultTableNames)
        self.assertEqual('xlr_playerstats', self.p.playerstats_table)
        self.assertEqual('xlr_weaponstats', self.p.weaponstats_table)
        self.assertEqual('xlr_weaponusage', self.p.weaponusage_table)
        self.assertEqual('xlr_bodyparts', self.p.bodyparts_table)
        self.assertEqual('xlr_playerbody', self.p.playerbody_table)
        self.assertEqual('xlr_opponents', self.p.opponents_table)
        self.assertEqual('xlr_mapstats', self.p.mapstats_table)
        self.assertEqual('xlr_playermaps', self.p.playermaps_table)
        self.assertEqual('xlr_actionstats', self.p.actionstats_table)
        self.assertEqual('xlr_playeractions', self.p.playeractions_table)
        self.assertEqual('xlr_history_monthly', self.p.history_monthly_table)
        self.assertEqual('xlr_history_weekly', self.p.history_weekly_table)
        self.assertEqual('ctime', self.p.ctime_table)


class Conf_settings_test_case(XlrstatsTestCase):

    def init(self, option_snippet=''):
        """
        Load the XLRstats plugin with an empty config file except for the option_snippet given as a parameter which will
        be injected in the "settings" section.
        Then call the plugin onLoadConfig method.
        """
        self.conf.loadFromString('\n[settings]\n%s\n' % option_snippet)
        self.p.onLoadConfig()


class Test_conf_settings_silent(Conf_settings_test_case):

    def test_missing(self):
        self.init('')
        self.assertFalse(self.p.silent)

    def test_empty(self):
        self.init('silent:')
        self.assertFalse(self.p.silent)

    def test_junk(self):
        self.init('silent: f00')
        self.assertFalse(self.p.silent)

    def test_true(self):
        self.init('silent: true')
        self.assertTrue(self.p.silent)

    def test_on(self):
        self.init('silent: on')
        self.assertTrue(self.p.silent)

    def test_1(self):
        self.init('silent: 1')
        self.assertTrue(self.p.silent)

    def test_yes(self):
        self.init('silent: yes')
        self.assertTrue(self.p.silent)

    def test_false(self):
        self.init('silent: false')
        self.assertFalse(self.p.silent)

    def test_off(self):
        self.init('silent:off')
        self.assertFalse(self.p.silent)

    def test_0(self):
        self.init('silent: 0')
        self.assertFalse(self.p.silent)

    def test_no(self):
        self.init('silent: false')
        self.assertFalse(self.p.silent)


class Test_conf_settings_hide_bots(Conf_settings_test_case):

    def test_missing(self):
        self.init('')
        self.assertTrue(self.p.hide_bots)

    def test_empty(self):
        self.init('hide_bots: ')
        self.assertTrue(self.p.hide_bots)

    def test_junk(self):
        self.init('hide_bots: f00')
        self.assertTrue(self.p.hide_bots)

    def test_true(self):
        self.init('hide_bots: true')
        self.assertTrue(self.p.hide_bots)

    def test_on(self):
        self.init('hide_bots: on')
        self.assertTrue(self.p.hide_bots)

    def test_1(self):
        self.init('hide_bots: 1')
        self.assertTrue(self.p.hide_bots)

    def test_yes(self):
        self.init('hide_bots: yes')
        self.assertTrue(self.p.hide_bots)

    def test_false(self):
        self.init('hide_bots: false')
        self.assertFalse(self.p.hide_bots)

    def test_off(self):
        self.init('hide_bots: off')
        self.assertFalse(self.p.hide_bots)

    def test_0(self):
        self.init('hide_bots: 0')
        self.assertFalse(self.p.hide_bots)

    def test_no(self):
        self.init('hide_bots: false')
        self.assertFalse(self.p.hide_bots)


class Test_conf_settings_exclude_bots(Conf_settings_test_case):

    def test_missing(self):
        self.init('')
        self.assertTrue(self.p.exclude_bots)

    def test_empty(self):
        self.init('exclude_bots: ')
        self.assertTrue(self.p.exclude_bots)

    def test_junk(self):
        self.init('exclude_bots: f00')
        self.assertTrue(self.p.exclude_bots)

    def test_true(self):
        self.init('exclude_bots: true')
        self.assertTrue(self.p.exclude_bots)

    def test_on(self):
        self.init('exclude_bots: on')
        self.assertTrue(self.p.exclude_bots)

    def test_1(self):
        self.init('exclude_bots: 1')
        self.assertTrue(self.p.exclude_bots)

    def test_yes(self):
        self.init('exclude_bots: yes')
        self.assertTrue(self.p.exclude_bots)

    def test_false(self):
        self.init('exclude_bots: false')
        self.assertFalse(self.p.exclude_bots)

    def test_off(self):
        self.init('exclude_bots: off')
        self.assertFalse(self.p.exclude_bots)

    def test_0(self):
        self.init('exclude_bots: 0')
        self.assertFalse(self.p.exclude_bots)

    def test_no(self):
        self.init('exclude_bots: false')
        self.assertFalse(self.p.exclude_bots)


class Test_conf_settings_minPlayers(Conf_settings_test_case):
    DEFAULT_VALUE = 3

    def test_missing(self):
        self.init('')
        self.assertEqual(self.DEFAULT_VALUE, self.p.min_players)

    def test_empty(self):
        self.init('minplayers: ')
        self.assertEqual(self.DEFAULT_VALUE, self.p.min_players)

    def test_junk(self):
        self.init('minplayers: f00')
        self.assertEqual(self.DEFAULT_VALUE, self.p.min_players)

    def test_negative(self):
        self.init('minplayers: -5')
        self.assertEqual(0, self.p.min_players)

    def test_0(self):
        self.init('minplayers: 0')
        self.assertEqual(0, self.p.min_players)

    def test_1(self):
        self.init('minplayers: 1')
        self.assertEqual(1, self.p.min_players)

    def test_8(self):
        self.init('minplayers: 8')
        self.assertEqual(8, self.p.min_players)

    def test_float(self):
        self.init('minplayers: 0.5')
        self.assertEqual(self.DEFAULT_VALUE, self.p.min_players)


class Test_conf_settings_webfronturl(Conf_settings_test_case):

    def test_missing(self):
        self.init('')
        self.assertEqual('', self.p.webfront_url)

    def test_empty(self):
        self.init('webfronturl: ')
        self.assertEqual('', self.p.webfront_url)

    def test_junk(self):
        self.init('webfronturl: f00')
        self.assertEqual('f00', self.p.webfront_url)

    def test_nominal(self):
        self.init('webfronturl: http://somewhere.com')
        self.assertEqual('http://somewhere.com', self.p.webfront_url)


class Test_conf_settings_servernumber(Conf_settings_test_case):
    DEFAULT_VALUE = 0

    def test_missing(self):
        self.init('')
        self.assertEqual(self.DEFAULT_VALUE, self.p.webfront_config_nr)

    def test_empty(self):
        self.init('servernumber: ')
        self.assertEqual(self.DEFAULT_VALUE, self.p.webfront_config_nr)

    def test_junk(self):
        self.init('servernumber: f00')
        self.assertEqual(self.DEFAULT_VALUE, self.p.webfront_config_nr)

    def test_negative(self):
        self.init('servernumber: -5')
        self.assertEqual(self.DEFAULT_VALUE, self.p.webfront_config_nr)

    def test_0(self):
        self.init('servernumber: 0')
        self.assertEqual(0, self.p.webfront_config_nr)

    def test_1(self):
        self.init('servernumber: 1')
        self.assertEqual(1, self.p.webfront_config_nr)

    def test_8(self):
        self.init('servernumber: 8')
        self.assertEqual(8, self.p.webfront_config_nr)

    def test_float(self):
        self.init('servernumber: 0.5')
        self.assertEqual(self.DEFAULT_VALUE, self.p.webfront_config_nr)


class Test_conf_settings_keep_history(Conf_settings_test_case):

    def test_missing(self):
        self.init('')
        self.assertTrue(self.p.keep_history)

    def test_empty(self):
        self.init('keep_history: ')
        self.assertTrue(self.p.keep_history)

    def test_junk(self):
        self.init('keep_history: f00')
        self.assertTrue(self.p.keep_history)

    def test_true(self):
        self.init('keep_history: true')
        self.assertTrue(self.p.keep_history)

    def test_on(self):
        self.init('keep_history: on')
        self.assertTrue(self.p.keep_history)

    def test_1(self):
        self.init('keep_history: 1')
        self.assertTrue(self.p.keep_history)

    def test_yes(self):
        self.init('keep_history: yes')
        self.assertTrue(self.p.keep_history)

    def test_false(self):
        self.init('keep_history: false')
        self.assertFalse(self.p.keep_history)

    def test_off(self):
        self.init('keep_history: off')
        self.assertFalse(self.p.keep_history)

    def test_0(self):
        self.init('keep_history: 0')
        self.assertFalse(self.p.keep_history)

    def test_no(self):
        self.init('keep_history: false')
        self.assertFalse(self.p.keep_history)


class Test_conf_settings_onemaponly(Conf_settings_test_case):

    def test_missing(self):
        self.init('')
        self.assertFalse(self.p.onemaponly)

    def test_empty(self):
        self.init('onemaponly: ')
        self.assertFalse(self.p.onemaponly)

    def test_junk(self):
        self.init('onemaponly: f00')
        self.assertFalse(self.p.onemaponly)

    def test_true(self):
        self.init('onemaponly: true')
        self.assertTrue(self.p.onemaponly)

    def test_on(self):
        self.init('onemaponly: on')
        self.assertTrue(self.p.onemaponly)

    def test_1(self):
        self.init('onemaponly: 1')
        self.assertTrue(self.p.onemaponly)

    def test_yes(self):
        self.init('onemaponly: yes')
        self.assertTrue(self.p.onemaponly)

    def test_false(self):
        self.init('onemaponly: false')
        self.assertFalse(self.p.onemaponly)

    def test_off(self):
        self.init('onemaponly: off')
        self.assertFalse(self.p.onemaponly)

    def test_0(self):
        self.init('onemaponly: 0')
        self.assertFalse(self.p.onemaponly)

    def test_no(self):
        self.init('onemaponly: false')
        self.assertFalse(self.p.onemaponly)


class Test_conf_settings_minlevel(Conf_settings_test_case):
    DEFAULT_VALUE = 0

    def test_missing(self):
        self.init('')
        self.assertEqual(self.DEFAULT_VALUE, self.p.minlevel)

    def test_empty(self):
        self.init('minlevel: ')
        self.assertEqual(self.DEFAULT_VALUE, self.p.minlevel)

    def test_junk(self):
        self.init('minlevel: f00')
        self.assertEqual(self.DEFAULT_VALUE, self.p.minlevel)

    def test_negative(self):
        self.init('minlevel: -5')
        self.assertEqual(self.DEFAULT_VALUE, self.p.minlevel)

    def test_0(self):
        self.init('minlevel: 0')
        self.assertEqual(0, self.p.minlevel)

    def test_1(self):
        self.init('minlevel: 1')
        self.assertEqual(1, self.p.minlevel)

    def test_8(self):
        self.init('minlevel: 8')
        self.assertEqual(0, self.p.minlevel)

    def test_float(self):
        self.init('minlevel: 0.5')
        self.assertEqual(self.DEFAULT_VALUE, self.p.minlevel)


class Test_conf_settings_defaultskill(Conf_settings_test_case):
    DEFAULT_VALUE = 1000

    def test_missing(self):
        self.init('')
        self.assertEqual(self.DEFAULT_VALUE, self.p.defaultskill)

    def test_empty(self):
        self.init('defaultskill: ')
        self.assertEqual(self.DEFAULT_VALUE, self.p.defaultskill)

    def test_junk(self):
        self.init('defaultskill: f00')
        self.assertEqual(self.DEFAULT_VALUE, self.p.defaultskill)

    def test_negative(self):
        self.init('defaultskill: -5')
        self.assertEqual(-5, self.p.defaultskill)

    def test_0(self):
        self.init('defaultskill: 0')
        self.assertEqual(0, self.p.defaultskill)

    def test_1(self):
        self.init('defaultskill: 1')
        self.assertEqual(1, self.p.defaultskill)

    def test_8(self):
        self.init('defaultskill: 8')
        self.assertEqual(8, self.p.defaultskill)

    def test_float(self):
        self.init('defaultskill: 0.5')
        self.assertEqual(self.DEFAULT_VALUE, self.p.defaultskill)


class Test_conf_settings_Kfactor_high(Conf_settings_test_case):
    DEFAULT_VALUE = 16

    def test_missing(self):
        self.init('')
        self.assertEqual(self.DEFAULT_VALUE, self.p.Kfactor_high)

    def test_empty(self):
        self.init('Kfactor_high: ')
        self.assertEqual(self.DEFAULT_VALUE, self.p.Kfactor_high)

    def test_junk(self):
        self.init('Kfactor_high: f00')
        self.assertEqual(self.DEFAULT_VALUE, self.p.Kfactor_high)

    def test_negative(self):
        self.init('Kfactor_high: -5')
        self.assertEqual(-5, self.p.Kfactor_high)

    def test_0(self):
        self.init('Kfactor_high: 0')
        self.assertEqual(0, self.p.Kfactor_high)

    def test_1(self):
        self.init('Kfactor_high: 1')
        self.assertEqual(1, self.p.Kfactor_high)

    def test_8(self):
        self.init('Kfactor_high: 8')
        self.assertEqual(8, self.p.Kfactor_high)

    def test_float(self):
        self.init('Kfactor_high: 0.5')
        self.assertEqual(self.DEFAULT_VALUE, self.p.Kfactor_high)


class Test_conf_settings_Kfactor_low(Conf_settings_test_case):
    DEFAULT_VALUE = 4

    def test_missing(self):
        self.init('')
        self.assertEqual(self.DEFAULT_VALUE, self.p.Kfactor_low)

    def test_empty(self):
        self.init('Kfactor_low: ')
        self.assertEqual(self.DEFAULT_VALUE, self.p.Kfactor_low)

    def test_junk(self):
        self.init('Kfactor_low: f00')
        self.assertEqual(self.DEFAULT_VALUE, self.p.Kfactor_low)

    def test_negative(self):
        self.init('Kfactor_low: -5')
        self.assertEqual(-5, self.p.Kfactor_low)

    def test_0(self):
        self.init('Kfactor_low: 0')
        self.assertEqual(0, self.p.Kfactor_low)

    def test_1(self):
        self.init('Kfactor_low: 1')
        self.assertEqual(1, self.p.Kfactor_low)

    def test_8(self):
        self.init('Kfactor_low: 8')
        self.assertEqual(8, self.p.Kfactor_low)

    def test_float(self):
        self.init('Kfactor_low: 0.5')
        self.assertEqual(self.DEFAULT_VALUE, self.p.Kfactor_low)


class Test_conf_settings_Kswitch_confrontations(Conf_settings_test_case):
    DEFAULT_VALUE = 50

    def test_missing(self):
        self.init('')
        self.assertEqual(self.DEFAULT_VALUE, self.p.Kswitch_confrontations)

    def test_empty(self):
        self.init('Kswitch_confrontations: ')
        self.assertEqual(self.DEFAULT_VALUE, self.p.Kswitch_confrontations)

    def test_junk(self):
        self.init('Kswitch_confrontations: f00')
        self.assertEqual(self.DEFAULT_VALUE, self.p.Kswitch_confrontations)

    def test_negative(self):
        self.init('Kswitch_confrontations: -5')
        self.assertEqual(-5, self.p.Kswitch_confrontations)

    def test_0(self):
        self.init('Kswitch_confrontations: 0')
        self.assertEqual(0, self.p.Kswitch_confrontations)

    def test_1(self):
        self.init('Kswitch_confrontations: 1')
        self.assertEqual(1, self.p.Kswitch_confrontations)

    def test_8(self):
        self.init('Kswitch_confrontations: 8')
        self.assertEqual(8, self.p.Kswitch_confrontations)

    def test_float(self):
        self.init('Kswitch_confrontations: 0.5')
        self.assertEqual(self.DEFAULT_VALUE, self.p.Kswitch_confrontations)


class Test_conf_settings_steepness(Conf_settings_test_case):
    DEFAULT_VALUE = 600

    def test_missing(self):
        self.init('')
        self.assertEqual(self.DEFAULT_VALUE, self.p.steepness)

    def test_empty(self):
        self.init('steepness: ')
        self.assertEqual(self.DEFAULT_VALUE, self.p.steepness)

    def test_junk(self):
        self.init('steepness: f00')
        self.assertEqual(self.DEFAULT_VALUE, self.p.steepness)

    def test_negative(self):
        self.init('steepness: -5')
        self.assertEqual(-5, self.p.steepness)

    def test_0(self):
        self.init('steepness: 0')
        self.assertEqual(0, self.p.steepness)

    def test_1(self):
        self.init('steepness: 1')
        self.assertEqual(1, self.p.steepness)

    def test_8(self):
        self.init('steepness: 8')
        self.assertEqual(8, self.p.steepness)

    def test_float(self):
        self.init('steepness: 0.5')
        self.assertEqual(self.DEFAULT_VALUE, self.p.steepness)


class Test_conf_settings_suicide_penalty_percent(Conf_settings_test_case):
    DEFAULT_VALUE = 0.05

    def test_missing(self):
        self.init('')
        self.assertEqual(self.DEFAULT_VALUE, self.p.suicide_penalty_percent)

    def test_empty(self):
        self.init('suicide_penalty_percent: ')
        self.assertEqual(self.DEFAULT_VALUE, self.p.suicide_penalty_percent)

    def test_junk(self):
        self.init('suicide_penalty_percent: f00')
        self.assertEqual(self.DEFAULT_VALUE, self.p.suicide_penalty_percent)

    def test_negative(self):
        self.init('suicide_penalty_percent: -5')
        self.assertEqual(-5.0, self.p.suicide_penalty_percent)

    def test_0(self):
        self.init('suicide_penalty_percent: 0')
        self.assertEqual(0.0, self.p.suicide_penalty_percent)

    def test_1(self):
        self.init('suicide_penalty_percent: 1')
        self.assertEqual(1.0, self.p.suicide_penalty_percent)

    def test_8(self):
        self.init('suicide_penalty_percent: 8')
        self.assertEqual(8.0, self.p.suicide_penalty_percent)

    def test_float(self):
        self.init('suicide_penalty_percent: 0.5')
        self.assertEqual(0.5, self.p.suicide_penalty_percent)


class Test_conf_settings_tk_penalty_percent(Conf_settings_test_case):
    DEFAULT_VALUE = 0.1

    def test_missing(self):
        self.init('')
        self.assertEqual(self.DEFAULT_VALUE, self.p.tk_penalty_percent)

    def test_empty(self):
        self.init('tk_penalty_percent: ')
        self.assertEqual(self.DEFAULT_VALUE, self.p.tk_penalty_percent)

    def test_junk(self):
        self.init('tk_penalty_percent: f00')
        self.assertEqual(self.DEFAULT_VALUE, self.p.tk_penalty_percent)

    def test_negative(self):
        self.init('tk_penalty_percent: -5')
        self.assertEqual(-5.0, self.p.tk_penalty_percent)

    def test_0(self):
        self.init('tk_penalty_percent: 0')
        self.assertEqual(0.0, self.p.tk_penalty_percent)

    def test_1(self):
        self.init('tk_penalty_percent: 1')
        self.assertEqual(1.0, self.p.tk_penalty_percent)

    def test_8(self):
        self.init('tk_penalty_percent: 8')
        self.assertEqual(8.0, self.p.tk_penalty_percent)

    def test_float(self):
        self.init('tk_penalty_percent: 0.5')
        self.assertEqual(0.5, self.p.tk_penalty_percent)


class Test_conf_settings_assist_timespan(Conf_settings_test_case):
    DEFAULT_VALUE = 2

    def test_missing(self):
        self.init('')
        self.assertEqual(self.DEFAULT_VALUE, self.p.assist_timespan)

    def test_empty(self):
        self.init('assist_timespan: ')
        self.assertEqual(self.DEFAULT_VALUE, self.p.assist_timespan)

    def test_junk(self):
        self.init('assist_timespan: f00')
        self.assertEqual(self.DEFAULT_VALUE, self.p.assist_timespan)

    def test_negative(self):
        self.init('assist_timespan: -5')
        self.assertEqual(-5, self.p.assist_timespan)

    def test_0(self):
        self.init('assist_timespan: 0')
        self.assertEqual(0, self.p.assist_timespan)

    def test_1(self):
        self.init('assist_timespan: 1')
        self.assertEqual(1, self.p.assist_timespan)

    def test_8(self):
        self.init('assist_timespan: 8')
        self.assertEqual(8, self.p.assist_timespan)

    def test_float(self):
        self.init('assist_timespan: 0.5')
        self.assertEqual(self.DEFAULT_VALUE, self.p.assist_timespan)


class Test_conf_settings_damage_assist_release(Conf_settings_test_case):
    DEFAULT_VALUE = 10

    def test_missing(self):
        self.init('')
        self.assertEqual(self.DEFAULT_VALUE, self.p.damage_assist_release)

    def test_empty(self):
        self.init('damage_assist_release: ')
        self.assertEqual(self.DEFAULT_VALUE, self.p.damage_assist_release)

    def test_junk(self):
        self.init('damage_assist_release: f00')
        self.assertEqual(self.DEFAULT_VALUE, self.p.damage_assist_release)

    def test_negative(self):
        self.init('damage_assist_release: -5')
        self.assertEqual(-5, self.p.damage_assist_release)

    def test_0(self):
        self.init('damage_assist_release: 0')
        self.assertEqual(0, self.p.damage_assist_release)

    def test_1(self):
        self.init('damage_assist_release: 1')
        self.assertEqual(1, self.p.damage_assist_release)

    def test_8(self):
        self.init('damage_assist_release: 8')
        self.assertEqual(8, self.p.damage_assist_release)

    def test_float(self):
        self.init('damage_assist_release: 0.5')
        self.assertEqual(self.DEFAULT_VALUE, self.p.damage_assist_release)


class Test_conf_settings_prematch_maxtime(Conf_settings_test_case):
    DEFAULT_VALUE = 70

    def test_missing(self):
        self.init('')
        self.assertEqual(self.DEFAULT_VALUE, self.p.prematch_maxtime)

    def test_empty(self):
        self.init('prematch_maxtime: ')
        self.assertEqual(self.DEFAULT_VALUE, self.p.prematch_maxtime)

    def test_junk(self):
        self.init('prematch_maxtime: f00')
        self.assertEqual(self.DEFAULT_VALUE, self.p.prematch_maxtime)

    def test_negative(self):
        self.init('prematch_maxtime: -5')
        self.assertEqual(-5, self.p.prematch_maxtime)

    def test_0(self):
        self.init('prematch_maxtime: 0')
        self.assertEqual(0, self.p.prematch_maxtime)

    def test_1(self):
        self.init('prematch_maxtime: 1')
        self.assertEqual(1, self.p.prematch_maxtime)

    def test_8(self):
        self.init('prematch_maxtime:8')
        self.assertEqual(8, self.p.prematch_maxtime)

    def test_float(self):
        self.init('prematch_maxtime: 0.5')
        self.assertEqual(self.DEFAULT_VALUE, self.p.prematch_maxtime)


class Test_conf_settings_announce(Conf_settings_test_case):

    def test_missing(self):
        self.init('')
        self.assertFalse(self.p.announce)

    def test_empty(self):
        self.init('announce: ')
        self.assertFalse(self.p.announce)

    def test_junk(self):
        self.init('announce: f00')
        self.assertFalse(self.p.announce)

    def test_true(self):
        self.init('announce: true')
        self.assertTrue(self.p.announce)

    def test_on(self):
        self.init('announce: on')
        self.assertTrue(self.p.announce)

    def test_1(self):
        self.init('announce: 1')
        self.assertTrue(self.p.announce)

    def test_yes(self):
        self.init('announce: yes')
        self.assertTrue(self.p.announce)

    def test_false(self):
        self.init('announce: false')
        self.assertFalse(self.p.announce)

    def test_off(self):
        self.init('announce: off')
        self.assertFalse(self.p.announce)

    def test_0(self):
        self.init('announce: 0')
        self.assertFalse(self.p.announce)

    def test_no(self):
        self.init('announce: false')
        self.assertFalse(self.p.announce)


class Test_conf_settings_keep_time(Conf_settings_test_case):

    def test_missing(self):
        self.init('')
        self.assertTrue(self.p.keep_time)

    def test_empty(self):
        self.init('keep_time: ')
        self.assertTrue(self.p.keep_time)

    def test_junk(self):
        self.init('keep_time: f00')
        self.assertTrue(self.p.keep_time)

    def test_true(self):
        self.init('keep_time: true')
        self.assertTrue(self.p.keep_time)

    def test_on(self):
        self.init('keep_time: on')
        self.assertTrue(self.p.keep_time)

    def test_1(self):
        self.init('keep_time: 1')
        self.assertTrue(self.p.keep_time)

    def test_yes(self):
        self.init('keep_time: yes')
        self.assertTrue(self.p.keep_time)

    def test_false(self):
        self.init('keep_time: false')
        self.assertFalse(self.p.keep_time)

    def test_off(self):
        self.init('keep_time: off')
        self.assertFalse(self.p.keep_time)

    def test_0(self):
        self.init('keep_time: 0')
        self.assertFalse(self.p.keep_time)

    def test_no(self):
        self.init('keep_time: false')
        self.assertFalse(self.p.keep_time)


class Test_conf_settings_provisional_ranking(Conf_settings_test_case):

    def test_missing(self):
        self.init('')
        self.assertTrue(self.p.provisional_ranking)

    def test_empty(self):
        self.init('provisional_ranking: ')
        self.assertTrue(self.p.provisional_ranking)

    def test_junk(self):
        self.init('provisional_ranking: f00')
        self.assertTrue(self.p.provisional_ranking)

    def test_true(self):
        self.init('provisional_ranking: true')
        self.assertTrue(self.p.provisional_ranking)

    def test_on(self):
        self.init('provisional_ranking: on')
        self.assertTrue(self.p.provisional_ranking)

    def test_1(self):
        self.init('provisional_ranking: 1')
        self.assertTrue(self.p.provisional_ranking)

    def test_yes(self):
        self.init('provisional_ranking: yes')
        self.assertTrue(self.p.provisional_ranking)

    def test_false(self):
        self.init('provisional_ranking: false')
        self.assertFalse(self.p.provisional_ranking)

    def test_off(self):
        self.init('provisional_ranking: off')
        self.assertFalse(self.p.provisional_ranking)

    def test_0(self):
        self.init('provisional_ranking: 0')
        self.assertFalse(self.p.provisional_ranking)

    def test_no(self):
        self.init('provisional_ranking: false')
        self.assertFalse(self.p.provisional_ranking)


class Test_conf_settings_auto_correct(Conf_settings_test_case):

    def test_missing(self):
        self.init('')
        self.assertTrue(self.p.auto_correct)

    def test_empty(self):
        self.init('auto_correct: ')
        self.assertTrue(self.p.auto_correct)

    def test_junk(self):
        self.init('auto_correct: f00')
        self.assertTrue(self.p.auto_correct)

    def test_true(self):
        self.init('auto_correct: true')
        self.assertTrue(self.p.auto_correct)

    def test_on(self):
        self.init('auto_correct: on')
        self.assertTrue(self.p.auto_correct)

    def test_1(self):
        self.init('auto_correct: 1')
        self.assertTrue(self.p.auto_correct)

    def test_yes(self):
        self.init('auto_correct: yes')
        self.assertTrue(self.p.auto_correct)

    def test_false(self):
        self.init('auto_correct: false')
        self.assertFalse(self.p.auto_correct)

    def test_off(self):
        self.init('auto_correct: off')
        self.assertFalse(self.p.auto_correct)

    def test_0(self):
        self.init('auto_correct: 0')
        self.assertFalse(self.p.auto_correct)

    def test_no(self):
        self.init('auto_correct: false')
        self.assertFalse(self.p.auto_correct)


class Test_conf_settings_auto_purge(Conf_settings_test_case):

    def test_missing(self):
        self.init('')
        self.assertFalse(self.p.auto_purge)

    def test_empty(self):
        self.init('auto_purge: ')
        self.assertFalse(self.p.auto_purge)

    def test_junk(self):
        self.init('auto_purge: f00')
        self.assertFalse(self.p.auto_purge)

    def test_true(self):
        self.init('auto_purge: true')
        self.assertTrue(self.p.auto_purge)

    def test_on(self):
        self.init('auto_purge: on')
        self.assertTrue(self.p.auto_purge)

    def test_1(self):
        self.init('auto_purge: 1')
        self.assertTrue(self.p.auto_purge)

    def test_yes(self):
        self.init('auto_purge: yes')
        self.assertTrue(self.p.auto_purge)

    def test_false(self):
        self.init('auto_purge: false')
        self.assertFalse(self.p.auto_purge)

    def test_off(self):
        self.init('auto_purge: off')
        self.assertFalse(self.p.auto_purge)

    def test_0(self):
        self.init('auto_purge: 0')
        self.assertFalse(self.p.auto_purge)

    def test_no(self):
        self.init('auto_purge: false')
        self.assertFalse(self.p.auto_purge)


class Conf_tables_test_case(XlrstatsTestCase):

    def init(self, option_snippet=''):
        """
        Load the XLRstats plugin with an empty config file except for the option_snippet given as a parameter which will
        be injected in the "tables" section.
        Then call the plugin onLoadConfig method.
        """
        self.conf.loadFromString('\n[tables]\n%s\n' % option_snippet)
        self.p.onLoadConfig()


class Test_conf_tables_playerstats(Conf_tables_test_case):
    DEFAULT_VALUE = 'xlr_playerstats'

    def test_missing(self):
        self.init('')
        self.assertEqual(self.DEFAULT_VALUE, self.p.playerstats_table)
        self.assertTrue(self.p._defaultTableNames)

    def test_empty(self):
        self.init('playerstats: ')
        self.assertEqual(self.DEFAULT_VALUE, self.p.playerstats_table)
        self.assertTrue(self.p._defaultTableNames)

    def test_nominal(self):
        self.init('playerstats: f00')
        self.assertEqual('f00', self.p.playerstats_table)
        self.assertFalse(self.p._defaultTableNames)


class Test_conf_tables_weaponstats(Conf_tables_test_case):
    DEFAULT_VALUE = 'xlr_weaponstats'

    def test_missing(self):
        self.init('')
        self.assertEqual(self.DEFAULT_VALUE, self.p.weaponstats_table)
        self.assertTrue(self.p._defaultTableNames)

    def test_empty(self):
        self.init('weaponstats: ')
        self.assertEqual(self.DEFAULT_VALUE, self.p.weaponstats_table)
        self.assertTrue(self.p._defaultTableNames)

    def test_nominal(self):
        self.init('weaponstats: f00')
        self.assertEqual('f00', self.p.weaponstats_table)
        self.assertFalse(self.p._defaultTableNames)


class Test_conf_tables_weaponusage(Conf_tables_test_case):
    DEFAULT_VALUE = 'xlr_weaponusage'

    def test_missing(self):
        self.init('')
        self.assertEqual(self.DEFAULT_VALUE, self.p.weaponusage_table)
        self.assertTrue(self.p._defaultTableNames)

    def test_empty(self):
        self.init('weaponusage: ')
        self.assertEqual(self.DEFAULT_VALUE, self.p.weaponusage_table)
        self.assertTrue(self.p._defaultTableNames)

    def test_nominal(self):
        self.init('weaponusage: f00')
        self.assertEqual('f00', self.p.weaponusage_table)
        self.assertFalse(self.p._defaultTableNames)


class Test_conf_tables_bodyparts(Conf_tables_test_case):
    DEFAULT_VALUE = 'xlr_bodyparts'

    def test_missing(self):
        self.init('')
        self.assertEqual(self.DEFAULT_VALUE, self.p.bodyparts_table)
        self.assertTrue(self.p._defaultTableNames)

    def test_empty(self):
        self.init('bodyparts: ')
        self.assertEqual(self.DEFAULT_VALUE, self.p.bodyparts_table)
        self.assertTrue(self.p._defaultTableNames)

    def test_nominal(self):
        self.init('bodyparts: f00')
        self.assertEqual('f00', self.p.bodyparts_table)
        self.assertFalse(self.p._defaultTableNames)


class Test_conf_tables_playerbody(Conf_tables_test_case):
    DEFAULT_VALUE = 'xlr_playerbody'

    def test_missing(self):
        self.init('')
        self.assertEqual(self.DEFAULT_VALUE, self.p.playerbody_table)
        self.assertTrue(self.p._defaultTableNames)

    def test_empty(self):
        self.init('playerbody: ')
        self.assertEqual(self.DEFAULT_VALUE, self.p.playerbody_table)
        self.assertTrue(self.p._defaultTableNames)

    def test_nominal(self):
        self.init('playerbody: f00')
        self.assertEqual('f00', self.p.playerbody_table)
        self.assertFalse(self.p._defaultTableNames)


class Test_conf_tables_opponents(Conf_tables_test_case):
    DEFAULT_VALUE = 'xlr_opponents'

    def test_missing(self):
        self.init('')
        self.assertEqual(self.DEFAULT_VALUE, self.p.opponents_table)
        self.assertTrue(self.p._defaultTableNames)

    def test_empty(self):
        self.init('opponents: ')
        self.assertEqual(self.DEFAULT_VALUE, self.p.opponents_table)
        self.assertTrue(self.p._defaultTableNames)

    def test_nominal(self):
        self.init('opponents: f00')
        self.assertEqual('f00', self.p.opponents_table)
        self.assertFalse(self.p._defaultTableNames)


class Test_conf_tables_mapstats(Conf_tables_test_case):
    DEFAULT_VALUE = 'xlr_mapstats'

    def test_missing(self):
        self.init('')
        self.assertEqual(self.DEFAULT_VALUE, self.p.mapstats_table)
        self.assertTrue(self.p._defaultTableNames)

    def test_empty(self):
        self.init('mapstats: ')
        self.assertEqual(self.DEFAULT_VALUE, self.p.mapstats_table)
        self.assertTrue(self.p._defaultTableNames)

    def test_nominal(self):
        self.init('mapstats: f00')
        self.assertEqual('f00', self.p.mapstats_table)
        self.assertFalse(self.p._defaultTableNames)


class Test_conf_tables_playermaps(Conf_tables_test_case):
    DEFAULT_VALUE = 'xlr_playermaps'

    def test_missing(self):
        self.init('')
        self.assertEqual(self.DEFAULT_VALUE, self.p.playermaps_table)
        self.assertTrue(self.p._defaultTableNames)

    def test_empty(self):
        self.init('playermaps: ')
        self.assertEqual(self.DEFAULT_VALUE, self.p.playermaps_table)
        self.assertTrue(self.p._defaultTableNames)

    def test_nominal(self):
        self.init('playermaps: f00')
        self.assertEqual('f00', self.p.playermaps_table)
        self.assertFalse(self.p._defaultTableNames)


class Test_conf_tables_actionstats(Conf_tables_test_case):
    DEFAULT_VALUE = 'xlr_actionstats'

    def test_missing(self):
        self.init('')
        self.assertEqual(self.DEFAULT_VALUE, self.p.actionstats_table)
        self.assertTrue(self.p._defaultTableNames)

    def test_empty(self):
        self.init('actionstats: ')
        self.assertEqual(self.DEFAULT_VALUE, self.p.actionstats_table)
        self.assertTrue(self.p._defaultTableNames)

    def test_nominal(self):
        self.init('actionstats: f00')
        self.assertEqual('f00', self.p.actionstats_table)
        self.assertFalse(self.p._defaultTableNames)


class Test_conf_tables_playeractions(Conf_tables_test_case):
    DEFAULT_VALUE = 'xlr_playeractions'

    def test_missing(self):
        self.init('')
        self.assertEqual(self.DEFAULT_VALUE, self.p.playeractions_table)
        self.assertTrue(self.p._defaultTableNames)

    def test_empty(self):
        self.init('playeractions: ')
        self.assertEqual(self.DEFAULT_VALUE, self.p.playeractions_table)
        self.assertTrue(self.p._defaultTableNames)

    def test_nominal(self):
        self.init('playeractions: f00')
        self.assertEqual('f00', self.p.playeractions_table)
        self.assertFalse(self.p._defaultTableNames)


class Test_conf_tables_history_monthly(Conf_tables_test_case):
    DEFAULT_VALUE = 'xlr_history_monthly'

    def test_missing(self):
        self.init('')
        self.assertEqual(self.DEFAULT_VALUE, self.p.history_monthly_table)
        self.assertTrue(self.p._defaultTableNames)

    def test_empty(self):
        self.init('history_monthly: ')
        self.assertEqual(self.DEFAULT_VALUE, self.p.history_monthly_table)
        self.assertTrue(self.p._defaultTableNames)

    def test_nominal(self):
        self.init('history_monthly: f00')
        self.assertEqual('f00', self.p.history_monthly_table)
        self.assertFalse(self.p._defaultTableNames)


class Test_conf_tables_history_weekly(Conf_tables_test_case):
    DEFAULT_VALUE = 'xlr_history_weekly'

    def test_missing(self):
        self.init('')
        self.assertEqual(self.DEFAULT_VALUE, self.p.history_weekly_table)
        self.assertTrue(self.p._defaultTableNames)

    def test_empty(self):
        self.init('history_weekly: ')
        self.assertEqual(self.DEFAULT_VALUE, self.p.history_weekly_table)
        self.assertTrue(self.p._defaultTableNames)

    def test_nominal(self):
        self.init('history_weekly: f00')
        self.assertEqual('f00', self.p.history_weekly_table)
        self.assertFalse(self.p._defaultTableNames)


class Test_conf_tables_ctime(Conf_tables_test_case):
    DEFAULT_VALUE = 'ctime'

    def test_missing(self):
        self.init('')
        self.assertEqual(self.DEFAULT_VALUE, self.p.ctime_table)
        self.assertTrue(self.p._defaultTableNames)

    def test_empty(self):
        self.init('ctime: ')
        self.assertEqual(self.DEFAULT_VALUE, self.p.ctime_table)
        self.assertTrue(self.p._defaultTableNames)

    def test_nominal(self):
        self.init('ctime: f00')
        self.assertEqual('f00', self.p.ctime_table)
        self.assertFalse(self.p._defaultTableNames)