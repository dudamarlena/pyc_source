# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pywurfl/algorithms/wurfl/handlers.py
# Compiled at: 2011-01-06 15:20:21
"""
This module contains the supporting classes for the Two Step Analysis user agent
algorithm that is used as the primary way to match user agents with the Java API
for the WURFL.

A description of the way the following source is intended to work can be found
within the source for the original Java API implementation here:
http://sourceforge.net/projects/wurfl/files/WURFL Java API/

The original Java code is GPLd and Copyright (c) WURFL-Pro srl
"""
__author__ = 'Armand Lynch <lyncha@users.sourceforge.net>'
__copyright__ = 'Copyright 2011, Armand Lynch'
__license__ = 'LGPL'
__url__ = 'http://celljam.net/'
__version__ = '1.2.1'
import re
from pywurfl.algorithms.wurfl.utils import first_semi_colon, first_slash, first_space, is_mobile_browser, second_slash, third_space
from pywurfl.algorithms.wurfl.utils import indexof_or_length as iol
from pywurfl.algorithms.wurfl import normalizers
from pywurfl.algorithms.wurfl.strategies import ld_match, ris_match

class AbstractMatcher(object):
    user_agent_map = {}

    def __init__(self, normalizer=normalizers.generic):
        self.normalizer = normalizer
        self.known_user_agents = set()

    def add(self, user_agent, wurfl_id):
        self.known_user_agents.add(user_agent)
        self.user_agent_map[user_agent] = wurfl_id

    @property
    def user_agents(self):
        return sorted(self.known_user_agents)

    def can_handle(self, user_agent):
        raise NotImplementedError

    def __call__(self, user_agent):
        normalized_user_agent = self.normalizer(user_agent)
        devid = self.conclusive_match(normalized_user_agent)
        if not devid or devid == 'generic':
            devid = self.recovery_match(normalized_user_agent)
        if not devid or devid == 'generic':
            devid = self.catch_all_recovery_match(user_agent)
        return devid

    def conclusive_match(self, user_agent):
        match = self.find_matching_ua(user_agent)
        devid = self.user_agent_map.get(match, 'generic')
        return devid

    def find_matching_ua(self, user_agent):
        tolerance = first_slash(user_agent)
        match = self.ris_matcher(user_agent, tolerance)
        return match

    def recovery_match(self, user_agent):
        return 'generic'

    recovery_map = (
     ('UP.Browser/7.2', 'opwv_v72_generic'),
     ('UP.Browser/7', 'opwv_v7_generic'),
     ('UP.Browser/6.2', 'opwv_v62_generic'),
     ('UP.Browser/6', 'opwv_v6_generic'),
     ('UP.Browser/5', 'upgui_generic'),
     ('UP.Browser/4', 'uptext_generic'),
     ('UP.Browser/3', 'uptext_generic'),
     ('Series60', 'nokia_generic_series60'),
     ('NetFront/3.0', 'generic_netfront_ver3'),
     ('ACS-NF/3.0', 'generic_netfront_ver3'),
     ('NetFront/3.1', 'generic_netfront_ver3_1'),
     ('ACS-NF/3.1', 'generic_netfront_ver3_1'),
     ('NetFront/3.2', 'generic_netfront_ver3_2'),
     ('ACS-NF/3.2', 'generic_netfront_ver3_2'),
     ('NetFront/3.3', 'generic_netfront_ver3_3'),
     ('ACS-NF/3.3', 'generic_netfront_ver3_3'),
     ('NetFront/3.4', 'generic_netfront_ver3_4'),
     ('NetFront/3.5', 'generic_netfront_ver3_5'),
     ('NetFront/4.0', 'generic_netfront_ver4'),
     ('NetFront/4.1', 'generic_netfront_ver4_1'),
     ('Windows CE', 'generic_ms_mobile_browser_ver1'),
     ('Mozilla/4.0', 'generic_web_browser'),
     ('Mozilla/5.0', 'generic_web_browser'),
     ('Mozilla/6.0', 'generic_web_browser'),
     ('Mozilla/', 'generic_xhtml'),
     ('ObigoInternetBrowser/Q03C', 'generic_xhtml'),
     ('AU-MIC/2', 'generic_xhtml'),
     ('AU-MIC-', 'generic_xhtml'),
     ('AU-OBIGO/', 'generic_xhtml'),
     ('Obigo/Q03', 'generic_xhtml'),
     ('Obigo/Q04', 'generic_xhtml'),
     ('ObigoInternetBrowser/2', 'generic_xhtml'),
     ('Teleca Q03B1', 'generic_xhtml'),
     ('Opera Mini/1', 'browser_opera_mini_release1'),
     ('Opera Mini/2', 'browser_opera_mini_release2'),
     ('Opera Mini/3', 'browser_opera_mini_release3'),
     ('Opera Mini/4', 'browser_opera_mini_release4'),
     ('Opera Mini/5', 'browser_opera_mini_release5'),
     ('DoCoMo', 'docomo_generic_jap_ver1'),
     ('KDDI', 'docomo_generic_jap_ver1'))

    def catch_all_recovery_match(self, user_agent):
        match = 'generic'
        for (partial_agent, wdevice) in self.recovery_map:
            if partial_agent in user_agent:
                match = wdevice
                break

        return match

    def ris_matcher(self, user_agent, tolerance):
        return ris_match(self.user_agents, user_agent, tolerance)

    def ld_matcher(self, user_agent, tolerance):
        return ld_match(self.user_agents, user_agent, tolerance)


class AlcatelMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return user_agent.startswith('Alcatel') or user_agent.startswith('ALCATEL')


class AndroidMatcher(AbstractMatcher):
    androids = {}
    androids[''] = 'generic_android'
    androids['1_5'] = 'generic_android_ver1_5'
    androids['1_6'] = 'generic_android_ver1_6'
    androids['2_0'] = 'generic_android_ver2'
    androids['2_1'] = 'generic_android_ver2_1'
    androids['2_2'] = 'generic_android_ver2_2'
    android_os_re = re.compile('.*Android[\\s/](\\d)\\.(\\d)')

    def can_handle(self, user_agent):
        return user_agent.startswith('Mozilla') and 'Android' in user_agent

    def find_matching_ua(self, user_agent):
        tolerance = iol(user_agent, ' ', start_index=iol(user_agent, 'Android'))
        match = self.ris_matcher(user_agent, tolerance)
        return match

    def recovery_match(self, user_agent):
        if 'Froyo' in user_agent:
            return 'generic_android_ver2_2'
        return self.androids.get(self.android_os_version(user_agent), 'generic_android')

    def android_os_version(self, user_agent):
        match = self.android_os_re.match(user_agent)
        if match:
            return '%s_%s' % (match.group(1), match.group(2))


class AOLMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return not is_mobile_browser(user_agent) and 'AOL' in user_agent


class AppleMatcher(AbstractMatcher):
    APPLE_LD_TOLERANCE = 5

    def can_handle(self, user_agent):
        return 'iPhone' in user_agent or 'iPod' in user_agent or 'iPad' in user_agent

    def find_matching_ua(self, user_agent):
        if user_agent.startswith('Apple'):
            tolerance = third_space(user_agent)
        else:
            tolerance = first_semi_colon(user_agent)
        match = self.ris_matcher(user_agent, tolerance)
        return match

    def recovery_match(self, user_agent):
        if 'iPad' in user_agent:
            return 'apple_ipad_ver1'
        if 'iPod' in user_agent:
            return 'apple_ipod_touch_ver1'
        return 'apple_iphone_ver1'


class BenQMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return user_agent.startswith('BENQ') or user_agent.startswith('BenQ')


class BlackberryMatcher(AbstractMatcher):
    blackberries = {}
    blackberries['2.'] = 'blackberry_generic_ver2'
    blackberries['3.2'] = 'blackberry_generic_ver3_sub2'
    blackberries['3.3'] = 'blackberry_generic_ver3_sub30'
    blackberries['3.5'] = 'blackberry_generic_ver3_sub50'
    blackberries['3.6'] = 'blackberry_generic_ver3_sub60'
    blackberries['3.7'] = 'blackberry_generic_ver3_sub70'
    blackberries['4.1'] = 'blackberry_generic_ver4_sub10'
    blackberries['4.2'] = 'blackberry_generic_ver4_sub20'
    blackberries['4.3'] = 'blackberry_generic_ver4_sub30'
    blackberries['4.5'] = 'blackberry_generic_ver4_sub50'
    blackberries['4.6'] = 'blackberry_generic_ver4_sub60'
    blackberries['4.7'] = 'blackberry_generic_ver4_sub70'
    blackberries['4.'] = 'blackberry_generic_ver4'
    blackberries['5.'] = 'blackberry_generic_ver5'
    blackberries['6.'] = 'blackberry_generic_ver6'
    blackberry_os_re = re.compile('.*Black[Bb]erry[^/\\s]+/(\\d\\.\\d)')

    def can_handle(self, user_agent):
        return 'BlackBerry' in user_agent or 'Blackberry' in user_agent

    def recovery_match(self, user_agent):
        match = 'generic'
        version = self.blackberry_os_version(user_agent)
        if version:
            match = self.blackberries.get(version, 'generic')
            if match == 'generic':
                match = self.blackberries.get(version[:-1], 'generic')
        return match

    def blackberry_os_version(self, user_agent):
        match = self.blackberry_os_re.match(user_agent)
        if match:
            return match.group(1)


class BotMatcher(AbstractMatcher):
    bots = ('bot', 'crawler', 'spider', 'novarra', 'transcoder', 'yahoo! searchmonkey',
            'yahoo! slurp', 'feedfetcher-google', 'toolbar', 'mowser', 'mediapartners-google',
            'azureus', 'inquisitor', 'baiduspider', 'baidumobaider', 'indy library',
            'slurp', 'crawl', 'wget', 'ucweblient', 'snoopy', 'mozfdsilla', 'ask jeeves',
            'jeeves/teoma', 'mechanize', 'http client', 'servicemonitor', 'httpunit',
            'hatena', 'ichiro')
    BOT_TOLERANCE = 4

    def can_handle(self, user_agent):
        user_agent = user_agent.lower()
        for bot in self.bots:
            if bot in user_agent:
                return True

        return False

    def find_matching_ua(self, user_agent):
        match = self.ld_matcher(user_agent, self.BOT_TOLERANCE)
        return match

    def recovery_match(self, user_agent):
        return 'generic_web_crawler'


class CatchAllMatcher(AbstractMatcher):
    MOZILLA_LD_TOLERANCE = 4

    def can_handle(self, user_agent):
        return True

    def find_matching_ua(self, user_agent):
        if user_agent.startswith('Mozilla'):
            if user_agent.startswith('Mozilla/4'):
                match = ld_match(self.extract_uas('Mozilla/4'), user_agent, self.MOZILLA_LD_TOLERANCE)
            elif user_agent.startswith('Mozilla/5'):
                match = ld_match(self.extract_uas('Mozilla/5'), user_agent, self.MOZILLA_LD_TOLERANCE)
            else:
                match = ld_match(self.extract_uas('Mozilla'), user_agent, self.MOZILLA_LD_TOLERANCE)
        else:
            match = super(CatchAllMatcher, self).find_matching_ua(user_agent)
        return match

    def extract_uas(self, start):
        return (x for x in self.user_agents if x.startswith(start))


class ChromeMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return not is_mobile_browser(user_agent) and 'Chrome' in user_agent


class DoCoMoMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return user_agent.startswith('DoCoMo')

    def find_matching_ua(self, user_agent):
        return ''

    def recovery_match(self, user_agent):
        if user_agent.startswith('DoCoMo/2'):
            return 'docomo_generic_jap_ver2'
        return 'docomo_generic_jap_ver1'


class FirefoxMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return not is_mobile_browser(user_agent) and 'Firefox' in user_agent


class GrundigMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return user_agent.startswith('Grundig') or user_agent.startswith('GRUNDIG')


class HTCMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return user_agent.startswith('HTC') or 'XV6875.1' in user_agent


class KDDIMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return 'KDDI' in user_agent

    def find_matching_ua(self, user_agent):
        if user_agent.startswith('KDDI/'):
            tolerance = second_slash(user_agent)
        elif user_agent.startswith('KDDI'):
            tolerance = first_slash(user_agent)
        else:
            tolerance = iol(user_agent, ')')
        match = self.ris_matcher(user_agent, tolerance)
        return match

    def recovery_match(self, user_agent):
        if 'Opera' in user_agent:
            return 'opera'
        return 'opwv_v62_generic'


class KonquerorMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return not is_mobile_browser(user_agent) and 'Konqueror' in user_agent


class KyoceraMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return user_agent.startswith('kyocera') or user_agent.startswith('QC-') or user_agent.startswith('KWC-')


class LGMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return user_agent.startswith('lg') or 'LG-' in user_agent or 'LGE' in user_agent

    def find_matching_ua(self, user_agent):
        tolerance = iol(user_agent, '/', start_index=user_agent.upper().index('LG'))
        match = self.ris_matcher(user_agent, tolerance)
        return match


class LGUPLUSMatcher(AbstractMatcher):
    lgpluses = (
     (
      'generic_lguplus_rexos_facebook_browser',
      ('Windows NT 5', 'POLARIS')),
     (
      'generic_lguplus_rexos_webviewer_browser',
      ('Windows NT 5', )),
     (
      'generic_lguplus_winmo_facebook_browser',
      ('Windows CE', 'POLARIS')),
     (
      'generic_lguplus_android_webkit_browser',
      ('Android', 'AppleWebKit')))

    def can_handle(self, user_agent):
        return 'lgtelecom' in user_agent or 'LGUPLUS' in user_agent

    def conclusive_match(self, user_agent):
        return 'generic'

    def recovery_match(self, user_agent):
        for (wid, searches) in self.lgpluses:
            for search in searches:
                if search not in user_agent:
                    break
            else:
                return wid

        return 'generic_lguplus'


class MaemoMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return 'Maemo ' in user_agent

    def find_matching_ua(self, user_agent):
        tolerance = first_space(user_agent)
        match = self.ris_matcher(user_agent, tolerance)
        return match


class MitsubishiMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return user_agent.startswith('Mitsu')


class MotorolaMatcher(AbstractMatcher):
    MOTOROLA_TOLERANCE = 5

    def can_handle(self, user_agent):
        return user_agent.startswith('Mot-') or 'MOT-' in user_agent or 'Motorola' in user_agent

    def find_matching_ua(self, user_agent):
        if user_agent.startswith('Mot-') or user_agent.startswith('MOT-') or user_agent.startswith('Motorola'):
            match = super(MotorolaMatcher, self).find_matching_ua(user_agent)
        else:
            match = self.ld_matcher(user_agent, self.MOTOROLA_TOLERANCE)
        return match

    def recovery_match(self, user_agent):
        match = 'generic'
        if 'MIB/2.2' in user_agent or 'MIB/BER2.2' in user_agent:
            match = 'mot_mib22_generic'
        return match


class MSIEMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return not is_mobile_browser(user_agent) and user_agent.startswith('Mozilla') and 'MSIE' in user_agent


class NecMatcher(AbstractMatcher):
    NEC_LD_TOLERANCE = 2

    def can_handle(self, user_agent):
        return user_agent.startswith('NEC') or user_agent.startswith('KGT')

    def find_matching_ua(self, user_agent):
        if user_agent.startswith('NEC'):
            match = super(NecMatcher, self).find_matching_ua(user_agent)
        else:
            match = self.ld_matcher(user_agent, self.NEC_LD_TOLERANCE)
        return match


class NokiaMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return 'Nokia' in user_agent

    def find_matching_ua(self, user_agent):
        tol1 = iol(user_agent, '/', start_index=user_agent.index('Nokia'))
        tol2 = iol(user_agent, ' ', start_index=user_agent.index('Nokia'))
        tolerance = tol1 if tol1 < tol2 else tol2
        match = self.ris_matcher(user_agent, tolerance)
        return match

    def recovery_match(self, user_agent):
        match = 'generic'
        if 'Series60' in user_agent:
            match = 'nokia_generic_series60'
        elif 'Series80' in user_agent:
            match = 'nokia_generic_series80'
        return match


class OperaMatcher(AbstractMatcher):
    OPERA_TOLERANCE = 1
    operas = {}
    operas['7'] = 'opera_7'
    operas['8'] = 'opera_8'
    operas['9'] = 'opera_9'
    operas['10'] = 'opera_10'
    opera_re = re.compile('.*Opera[\\s/](\\d+).*')

    def can_handle(self, user_agent):
        return not is_mobile_browser(user_agent) and 'Opera' in user_agent

    def find_matching_ua(self, user_agent):
        match = self.ld_matcher(user_agent, self.OPERA_TOLERANCE)
        return match

    def recovery_match(self, user_agent):
        match = self.opera_re.match(user_agent)
        if match:
            return self.operas.get(match.group(1), 'opera')
        return 'opera'


class OperaMiniMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return 'Opera Mini' in user_agent

    def recovery_match(self, user_agent):
        match = ''
        if 'Opera Mini/1' in user_agent:
            match = 'browser_opera_mini_release1'
        elif 'Opera Mini/2' in user_agent:
            match = 'browser_opera_mini_release2'
        elif 'Opera Mini/3' in user_agent:
            match = 'browser_opera_mini_release3'
        elif 'Opera Mini/4' in user_agent:
            match = 'browser_opera_mini_release4'
        elif 'Opera Mini/5' in user_agent:
            match = 'browser_opera_mini_release5'
        return match


class PanasonicMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return user_agent.startswith('Panasonic')


class PantechMatcher(AbstractMatcher):
    PANTECH_LD_TOLERANCE = 4

    def can_handle(self, user_agent):
        return user_agent.startswith('Pantech') or user_agent.startswith('PT-') or user_agent.startswith('PANTECH') or user_agent.startswith('PG-')

    def find_matching_ua(self, user_agent):
        if user_agent.startswith('Pantech'):
            match = self.ld_matcher(user_agent, self.PANTECH_LD_TOLERANCE)
        else:
            match = super(PantechMatcher, self).find_matching_ua(user_agent)
        return match


class PhilipsMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return user_agent.startswith('Philips') or user_agent.startswith('PHILIPS')


class PortalmmmMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return user_agent.startswith('portalmmm')

    def find_matching_ua(self, user_agent):
        return ''


class QtekMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return user_agent.startswith('Qtek')


class SafariMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return not is_mobile_browser(user_agent) and user_agent.startswith('Mozilla') and 'Safari' in user_agent

    def recovery_match(self, user_agent):
        if 'Macintosh' in user_agent or 'Windows' in user_agent:
            match = 'generic_web_browser'
        else:
            match = 'generic'
        return match


class SagemMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return user_agent.startswith('Sagem') or user_agent.startswith('SAGEM')


class SamsungMatcher(AbstractMatcher):
    SAMSUNGS = [
     'SEC-', 'SAMSUNG-', 'SCH', 'Samsung', 'SPH', 'SGH',
     'SAMSUNG/']

    def can_handle(self, user_agent):
        return 'Samsung/SGH' in user_agent or 'Samsung' in user_agent or user_agent.startswith('SEC-') or user_agent.startswith('SAMSUNG') or user_agent.startswith('SPH') or user_agent.startswith('SGH') or user_agent.startswith('SCH')

    def find_matching_ua(self, user_agent):
        for sams in self.SAMSUNGS:
            if sams in user_agent:
                tol1 = iol(user_agent, '/', start_index=user_agent.index(sams))
                tol2 = iol(user_agent, ' ', start_index=user_agent.index(sams))
                tolerance = tol1 if tol1 < tol2 else tol2
                break
        else:
            tolerance = len(user_agent)

        match = self.ris_matcher(user_agent, tolerance)
        return match


class SanyoMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return user_agent.startswith('Sanyo') or user_agent.startswith('SANYO')


class SharpMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return user_agent.startswith('Sharp') or user_agent.startswith('SHARP')


class SiemensMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return user_agent.startswith('SIE-')


class SonyEricssonMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return 'SonyEricsson' in user_agent

    def find_matching_ua(self, user_agent):
        if user_agent.startswith('SonyEricsson'):
            match = super(SonyEricssonMatcher, self).find_matching_ua(user_agent)
        else:
            tolerance = second_slash(user_agent)
            match = self.ris_matcher(user_agent, tolerance)
        return match


class SPVMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return 'SPV' in user_agent

    def find_matching_ua(self, user_agent):
        tolerance = iol(user_agent, ';', start_index=iol(user_agent, 'SPV'))
        match = self.ris_matcher(user_agent, tolerance)
        return match


class ToshibaMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return user_agent.startswith('Toshiba')


class VodafoneMatcher(AbstractMatcher):

    def can_handle(self, user_agent):
        return user_agent.startswith('Vodafone')

    def find_matching_ua(self, user_agent):
        tolerance = iol(user_agent, '/', 3)
        match = self.ris_matcher(user_agent, tolerance)
        return match


class WindowsCEMatcher(AbstractMatcher):
    WINDOWS_CE_TOLERANCE = 3

    def can_handle(self, user_agent):
        return 'Mozilla/' in user_agent and ('Windows CE' in user_agent or 'WindowsCE' in user_agent or 'ZuneWP7' in user_agent)

    def find_matching_ua(self, user_agent):
        match = self.ld_matcher(user_agent, self.WINDOWS_CE_TOLERANCE)
        return match

    def recovery_match(self, user_agent):
        return 'generic_ms_mobile_browser_ver1'


handlers = [
 NokiaMatcher(),
 LGUPLUSMatcher(),
 AndroidMatcher(normalizers.android),
 SonyEricssonMatcher(),
 MotorolaMatcher(),
 BlackberryMatcher(),
 SiemensMatcher(),
 SagemMatcher(),
 SamsungMatcher(),
 PanasonicMatcher(),
 NecMatcher(),
 QtekMatcher(),
 MitsubishiMatcher(),
 PhilipsMatcher(),
 LGMatcher(normalizers.lg),
 AppleMatcher(),
 KyoceraMatcher(),
 AlcatelMatcher(),
 SharpMatcher(),
 SanyoMatcher(),
 BenQMatcher(),
 PantechMatcher(),
 ToshibaMatcher(),
 GrundigMatcher(),
 HTCMatcher(),
 BotMatcher(),
 SPVMatcher(),
 WindowsCEMatcher(),
 PortalmmmMatcher(),
 DoCoMoMatcher(),
 KDDIMatcher(),
 VodafoneMatcher(),
 OperaMiniMatcher(),
 MaemoMatcher(normalizers.maemo),
 ChromeMatcher(normalizers.chrome),
 AOLMatcher(),
 OperaMatcher(),
 KonquerorMatcher(normalizers.konqueror),
 SafariMatcher(normalizers.safari),
 FirefoxMatcher(normalizers.firefox),
 MSIEMatcher(normalizers.msie),
 CatchAllMatcher()]