# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/typtop/config.py
# Compiled at: 2017-03-23 17:31:44
import sys, os
VERSION = '0.2.11'
DB_NAME = 'typtop'
SEC_DB_PATH = '/etc/typtop.d'
LOG_DIR = '/var/log/'
BINDIR = '/usr/local/bin'
SYSTEM = ''
TEST = False
if os.environ.get('RUN_TYPTOP_TEST'):
    TEST = True

def set_distro():
    os = sys.platform
    if os == 'darwin':
        return 'darwin'
    if os.startswith('linux'):
        try:
            import distro
            dist = distro.id()
            name = distro.name()
        except ImportError:
            dist = 'ubuntu'
            name = 'Ubuntu'

        if dist in ('ubuntu', 'debian'):
            return 'debian'
        if dist in ('fedora', 'rhel', 'centos'):
            return 'fedora'
        if dist == 'arch':
            return 'arch'
        raise ValueError(('Not supported for your Linux distribution: {}').format(name))
    else:
        raise ValueError(('Not supported for your OS: {}').format(os))


DISTRO = set_distro()

def warm_up_with(pw):
    return [
     pw.swapcase(), pw[0].swapcase() + pw[1:],
     pw + '1', '1' + pw,
     '`' + pw, pw + '`',
     pw + '0', '0' + pw,
     pw[:-1] + pw[(-1)] + pw[(-1)]]


GROUP = 'shadow' if DISTRO in 'debian' else 'root' if DISTRO in ('fedora', 'arch') else 'wheel' if DISTRO in 'darwin' else ''
if sys.platform == 'darwin':
    SYSTEM = 'OSX'
elif sys.platform.startswith('linux'):
    SYSTEM = 'LINUX'
else:
    raise ValueError('Not yet suporrted. Report in @github/rchatterjee/pam_typopw')
if SYSTEM == 'OSX':
    SEC_DB_PATH = '/usr/local/etc/typtop.d/'
elif SYSTEM == 'LINUX':
    SEC_DB_PATH = '/usr/local/etc/typtop.d/'
CACHE_SIZE = 5
WAITLIST_SIZE = 10
PADDED_PW_SIZE = 64
EDIT_DIST_CUTOFF = 1.0 / 10
REL_ENT_CUTOFF = 3
LOWER_ENT_CUTOFF = 0
NUMBER_OF_ENTRIES_TO_ALLOW_TYPO_LOGIN = 0
NUMBER_OF_DAYS_TO_ALLOW_TYPO_LOGIN = 15
UPDATE_GAPS = 21600
WARM_UP_CACHE = 1
auxT = 'Header'
HEADER_CTX = 'HeaderCtx'
HMAC_SALT = 'HMACSalt'
FREQ_COUNTS = 'FreqCounts'
REAL_PW = 'RealPassword'
ENC_PK = 'EncPublicKey'
INDEX_J = 'IndexJ'
ALLOWED_TYPO_LOGIN = 'AllowedTypoLogin'
LOGIN_COUNT = 'LoginCount'
INSTALLATION_ID = 'InstallationId'
INSTALLATION_DATE = 'InstallationDate'
ALLOWED_LOGGING = 'AllowLogging'
ALLOWED_UPLOAD = 'AllowUpload'
LOG_LAST_SENTTIME = 'LastLogSetntTime'
LOG_SENT_PERIOD = 'PeriodForSendingLog'
SYSTEM_STATUS = 'SystemStatus'
SYSTEM_STATUS_PW_CHANGED = 'PasswordChanged'
SYSTEM_STATUS_ALL_GOOD = 'StatusAllGood'
SYSTEM_STATUS_CORRUPTED_DB = 'StatusCorruptedDB'
SYSTEM_STATUS_NOT_INITIALIZED = 'NotInitialized'
TYPO_CACHE = 'TypoCache'
WAIT_LIST = 'WaitList'
logT = 'Log'
logT_cols = [
 'tid', 'edit_dist', 'rel_entropy', 'ts',
 'istop5fixable', 'in_cache', 'localtime']
GITHUB_URL = 'https://github.com/rchatterjee/pam-typopw'
first_msg = ('\n\n\n  /  |                          /  |\n _$$ |_    __    __   ______   _$$ |_     ______    ______\n/ $$   |  /  |  /  | /      \\ / $$   |   /      \\  /      \\\n$$$$$$/   $$ |  $$ |/$$$$$$  |$$$$$$/   /$$$$$$  |/$$$$$$  |\n  $$ | __ $$ |  $$ |$$ |  $$ |  $$ | __ $$ |  $$ |$$ |  $$ |\n  $$ |/  |$$ \\__$$ |$$ |__$$ |  $$ |/  |$$ \\__$$ |$$ |__$$ |\n  $$  $$/ $$    $$ |$$    $$/   $$  $$/ $$    $$/ $$    $$/\n   $$$$/   $$$$$$$ |$$$$$$$/     $$$$/   $$$$$$/  $$$$$$$/\n          /  \\__$$ |$$ |                          $$ |\n          $$    $$/ $$ |                          $$ |\n           $$$$$$/  $$/                           $$/\nHello!\n\nThanks for installing TypToP (version: {version}).  This software\nattaches a new pluggable authentication module (PAM) to some of your\ncommon authentication processes, such as su, login, screensaver etc.,\nand observes for password typing mistakes. It records your frequent\ntyping mistakes, and enable logging in with slight vairations of your\nactual login password that are frequent and safe to do so.\n\nThis is a research prototype, and we are collecting some anonymous\nnon-sensitive data about your password typing patterns to verify our\ndesign. The details of what we collect, how we collect and store, and\nthe security blueprint of this software can be found in the GitHub\npage: {url}.  The participation in the study is completely voluntary,\nand you can opt out at any time while still keep using the software.\n\nCheckout other options (such as opting out of the study) of the\nutility script typtop by running:\n\n$ typtops.py --help\n\nNote, You have to initiate this for each user who intend to use the\nbenefit of adaptive typo-tolerant password login.\n').format(url=GITHUB_URL, version=VERSION)