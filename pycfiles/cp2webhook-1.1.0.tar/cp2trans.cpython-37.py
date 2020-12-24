# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\cp2trans\cp2trans.py
# Compiled at: 2020-01-02 01:06:56
# Size of source mod 2**32: 26733 bytes
import os, io, re, sys, time, json, uuid, urllib, random, getpass, logging, hashlib, argparse, subprocess, configparser
from datetime import datetime
from multiprocessing import Process
import boto3, MeCab, i18n, pydub, romkan, requests, pyperclip
from Crypto.Cipher import AES
from pydub.playback import play
import google.cloud as translate
YOUDAO_API_HTTPS = 'https://openapi.youdao.com/api'
YOUDAO_TTSAPI_HTTPS = 'https://openapi.youdao.com/ttsapi'
DEFAULT_SECTION = 'default'
SOURCE_ALL = ('ja', )
TARGET_YOUDAO = ('zh-CHS', )
TARGET_AWS = ('en', )
DIVIDING_TITLE = '- - - - - - - - - - {} - - - - - - - - - - '
DIVIDING_LINE = '= = = = = = = = = = = = = = = = = = = = = = = = = '
TEST_STRING = '8月3日に放送された「中居正広の金曜日のスマイルたちへ」(TBS系)で、1日たった5分でぽっこりおなかを解消するというダイエット方法を紹介。キンタロー。のダイエットにも密着。'
CONFIG_INI = 'config.ini'
API_TOLERATED_DELAY = 1.0
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config = configparser.ConfigParser()
if not os.path.isfile(os.path.join(BASE_DIR, 'config.ini')):
    print('"config.ini" not found.')
    exit(1)
config.read((os.path.join(BASE_DIR, CONFIG_INI)), encoding='utf8')
i18n.load_path.append(os.path.join(BASE_DIR, 'lang'))
i18n.set('filename_format', '{locale}.{format}')
i18n.set('locale', config.get('global', 'language'))
i18n.set('error_on_missing_translation', True)
i18n.set('file_format', 'yml')
PROGRAM_DESCRIPTION = i18n.t('PROGRAM_DESCRIPTION')
YOUDAO_API_ERROR = i18n.t('YOUDAO_API_ERROR')
YOUDAO_TTS_ERROR = i18n.t('YOUDAO_TTS_ERROR')
AWS_API_ERROR = i18n.t('AWS_API_ERROR')
GOOGLE_API_ERROR = i18n.t('GOOGLE_API_ERROR')
CREATE_A_NOT_EXISTS_FILE = i18n.t('CREATE_A_NOT_EXISTS_FILE')
ACCESS_READONLY_PROPERTY = i18n.t('ACCESS_READONLY_PROPERTY')
WRONG_PASSWORD = i18n.t('WRONG_PASSWORD')
PASSWORD_NOT_SPECIFIED = i18n.t('PASSWORD_NOT_SPECIFIED')
FILE_NOT_FOUND = i18n.t('FILE_NOT_FOUND')
FOLDER_NOT_FOUND = i18n.t('FOLDER_NOT_FOUND')
SECTION_NOT_FOUND = i18n.t('SECTION_NOT_FOUND')
SAVING_TO_PLEASE_WAIT = i18n.t('SAVING_TO_PLEASE_WAIT')
SECTION_IS_PRESERVED = i18n.t('SECTION_IS_PRESERVED')
CHOOSE_A_TARGET = i18n.t('CHOOSE_A_TARGET')
INPUT_OLD_PASSWORD = i18n.t('INPUT_OLD_PASSWORD')
INPUT_NEW_PASSWORD = i18n.t('INPUT_NEW_PASSWORD')
INPUT_PASSWORD_TO_ENCRYPT = i18n.t('INPUT_PASSWORD_TO_ENCRYPT')
INPUT_PASSWORD_TO_DECRYPT = i18n.t('INPUT_PASSWORD_TO_DECRYPT')
START_MONITORING = i18n.t('START_MONITORING')
OVER_CHARACTERS = i18n.t('OVER_CHARACTERS')
DONE = i18n.t('DONE')
START_AGTH_FROM = i18n.t('START_AGTH_FROM')
INVALID_TARGET = i18n.t('INVALID_TARGET')
LOG_WONT_BE_SAVED = i18n.t('LOG_WONT_BE_SAVED')
TTS_PLAYING_WITH_VOICE = i18n.t('TTS_PLAYING_WITH_VOICE')
REQUEST_FINISHED_IN = i18n.t('REQUEST_FINISHED_IN')
HELP_PASSED = i18n.t('HELP_PASSED')
HELP_PROFILE = i18n.t('HELP_PROFILE')
HELP_LOG = i18n.t('HELP_LOG')
HELP_ENCRYPT = i18n.t('HELP_ENCRYPT')
HELP_TTS = i18n.t('HELP_TTS')
HELP_MATCH = i18n.t('HELP_MATCH')
HELP_NUMBER = i18n.t('HELP_NUMBER')
HELP_SOURCE = i18n.t('HELP_SOURCE')
HELP_TARGET = i18n.t('HELP_TARGET')
HELP_DISABLE = i18n.t('HELP_DISABLE')
HELP_INTERVAL = i18n.t('HELP_INTERVAL')
HELP_AGTH = i18n.t('HELP_AGTH')
HELP_OPT = i18n.t('HELP_OPT')
aws_client = boto3.client('translate')
logger = logging.getLogger(__name__)
logging.basicConfig(level=config.getint('global', 'log_level', fallback=(logging.INFO)))
if not os.path.exists(os.path.join(BASE_DIR, CONFIG_INI)):
    logger.error(FILE_NOT_FOUND.format(CONFIG_INI))
    exit(1)
try:
    appid = config.get('global', 'appid')
    secretkey = config.get('global', 'secretkey')
    neologd_path = config.get('global', 'neologd')
    program_language = config.get('global', 'language')
except configparser.NoSectionError as e:
    try:
        logger.error(e.message)
        exit(1)
    finally:
        e = None
        del e

if config.has_section(DEFAULT_SECTION):
    logger.error(SECTION_IS_PRESERVED.format(DEFAULT_SECTION))
    exit(1)
if not os.path.exists(neologd_path):
    logger.error(FOLDER_NOT_FOUND.format(neologd_path))
    exit(1)
mecab_wakati = MeCab.Tagger('-Owakati -d ' + neologd_path)
mecab_chasen = MeCab.Tagger('-Ochasen -d ' + neologd_path)
client = translate.TranslationServiceClient()
parent = client.location_path('cp2trans-jp', 'global')
parser = argparse.ArgumentParser(prog='cp2trans', description=PROGRAM_DESCRIPTION)
parser.add_argument('--passwd', dest='passwd', metavar='log_file', help=HELP_PASSED)
parser.add_argument('-p', '--profile', dest='profile', metavar='section', help=HELP_PROFILE)
parser.add_argument('-l', '--log', dest='log', metavar='log_file', help=HELP_LOG)
parser.add_argument('-e', '--encrypt', dest='encrypt', metavar='password', help=HELP_ENCRYPT)
parser.add_argument('-v', '--voice', dest='voice', choices=('0', '1'), default=None, help=HELP_TTS)
parser.add_argument('-m', '--match', dest='match', metavar='pattern', default=None, help=HELP_MATCH)
parser.add_argument('-n', '--number', dest='number', metavar='number', type=int, default=256, help=HELP_NUMBER)
parser.add_argument('-s', '--source', dest='source', metavar='lang_code', default='ja', help=HELP_SOURCE)
parser.add_argument('-t', '--target', dest='target', metavar='lang_code1,lang_code2,lang_code3', default='zh-CHS,en', help=HELP_TARGET)
parser.add_argument('-d', '--disable', dest='disable', action='store_true', default=False, help=HELP_DISABLE)
parser.add_argument('-i', '--interval', dest='interval', metavar='seconds', type=float, default=1.0, help=HELP_INTERVAL)
parser.add_argument('-a', '--agth', dest='agth', metavar='agth_path', help=HELP_AGTH)
parser.add_argument('-o', '--opt', dest='opt', metavar='agth_opts', default='', help=HELP_OPT)

def youdao_encrypt(sign_str):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(sign_str.encode('utf-8'))
    return hash_algorithm.hexdigest()


def youdao_truncate(q):
    if q is None:
        return
    size = len(q)
    if size <= 20:
        return q
    return q[0:10] + str(size) + q[size - 10:size]


def youdao_translate(text, target='zh-CHS', source='ja'):
    curtime = str(int(time.time()))
    salt = str(uuid.uuid1())
    sign_str = appid + youdao_truncate(text) + salt + curtime + secretkey
    sign = youdao_encrypt(sign_str)
    data = {'from':source, 
     'to':target, 
     'signType':'v3', 
     'curtime':curtime, 
     'appKey':appid, 
     'q':text, 
     'salt':salt, 
     'sign':sign}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(YOUDAO_API_HTTPS, data=data, headers=headers)
    start_time = datetime.now()
    period = (datetime.now() - start_time).seconds
    logger.debug('Youdao API finished API request in {} seconds'.format(period))
    if period > API_TOLERATED_DELAY:
        logger.info(REQUEST_FINISHED_IN.format('Youdao API', period))
    if r.ok and 'application/json' in r.headers['Content-type']:
        j = json.loads(r.text)
        if 'translation' in j.keys():
            if len(j['translation']) > 0:
                return json.loads(r.text)['translation'][0]
        logger.error(YOUDAO_API_ERROR.format(r.text))
    else:
        logger.error(YOUDAO_API_ERROR.format(r.status_code))
        return


def youdao_tts(text, voice='1', lang_type='ja'):
    if text == '':
        return
    salt = str(uuid.uuid1())
    sign_str = appid + text + salt + secretkey
    sign = youdao_encrypt(sign_str)
    data = {'langType':lang_type, 
     'appKey':appid, 
     'q':text, 
     'salt':salt, 
     'sign':sign}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    start_time = datetime.now()
    r = requests.post(YOUDAO_API_HTTPS, data=data, headers=headers)
    period = (datetime.now() - start_time).seconds
    logger.debug('Youdao TTS finished API request in {} seconds'.format(period))
    if period > API_TOLERATED_DELAY:
        logger.info(REQUEST_FINISHED_IN.format('Youdao TTS', period))
    if r.ok and 'audio/mp3' in r.headers['Content-Type']:
        data = io.BytesIO(r.content)
        tts = pydub.AudioSegment.from_file(data, format='mp3')
        logger.info(TTS_PLAYING_WITH_VOICE.format(voice))
        play(tts)
        logger.debug('TTS playing finished normally.')
    elif 'application/json' in r.headers['Content-Type']:
        logger.error(YOUDAO_TTS_ERROR.format(json.loads(r.text)['errorCode']))
    else:
        logger.error(YOUDAO_TTS_ERROR.format(r.status_code))


def aws_translate(text, target='en', source='ja'):
    start_time = datetime.now()
    result_dict = aws_client.translate_text(Text=text, SourceLanguageCode=source,
      TargetLanguageCode=target)
    period = (datetime.now() - start_time).seconds
    logger.debug('AWS finished API request in {} seconds'.format(period))
    if period > API_TOLERATED_DELAY:
        logger.info(REQUEST_FINISHED_IN.format('AWS', period))
    r = result_dict.get('TranslatedText', None)
    if r == None:
        logger.error(AWS_API_ERROR.format(str(result_dict)))
        return
    return r


def google_translate(text, target='zh-CN', source='ja'):
    response = client.translate_text(parent=parent, contents=[text], mime_type='text/plain', source_language_code=source, target_language_code=target)
    try:
        r = response.translations[0].translated_text
    except Exception:
        logger.log(GOOGLE_API_ERROR.format(str(response)))
        return
    else:
        return r


def align(value):
    if isinstance(value, str):
        value = value.encode('ascii')
    elif isinstance(value, bytes):
        pass
    else:
        logger.critical('align() only accept str and bytes.')
        exit(1)
    while len(value) % 16 != 0:
        value += ' '

    return value


def encrypt(ascii_safe_text, key):
    assert isinstance(ascii_safe_text, str)
    aes = AES.new(align(key), AES.MODE_ECB)
    return aes.encrypt(align(ascii_safe_text))


def decrypt(cipher, key):
    assert isinstance(cipher, bytes)
    aes = AES.new(align(key), AES.MODE_ECB)
    return aes.decrypt(align(cipher)).decode('ascii').rstrip()


def rename(filepath, insert_text):
    path, ext = os.path.splitext(filepath)
    return path + insert_text + ext


def passwd(filepath):
    if not os.path.isfile(filepath):
        logger.error(FILE_NOT_FOUND.format(filepath))
        exit(1)
    else:
        target = input(CHOOSE_A_TARGET)
        if target == 'C':
            old_password = getpass.getpass(INPUT_OLD_PASSWORD)
            with open(filepath, 'rb') as (f):
                try:
                    log = json.loads(decrypt(f.read(), old_password))
                except (UnicodeDecodeError, json.decoder.JSONDecodeError):
                    logger.error(WRONG_PASSWORD.format(filepath))
                    exit(1)

            new_password = getpass.getpass(INPUT_NEW_PASSWORD)
            new_filepath = rename(filepath, '(encrypted)')
            logger.info(SAVING_TO_PLEASE_WAIT.format(new_filepath))
            with open(new_filepath, 'wb') as (f):
                f.write(encrypt(json.dumps(log), new_password))
            logger.info(DONE)
        elif target == 'E':
            with open(filepath, 'r') as (f):
                try:
                    log = json.loads(f.read())
                except (UnicodeDecodeError, json.decoder.JSONDecodeError):
                    logger.error(PASSWORD_NOT_SPECIFIED.format(filepath))
                    exit(1)

            new_filepath = rename(filepath, '(encrypted)')
            password = getpass.getpass(INPUT_PASSWORD_TO_ENCRYPT.format(filepath))
            logger.info(SAVING_TO_PLEASE_WAIT.format(new_filepath))
            with open(new_filepath, 'wb') as (f):
                f.write(encrypt(json.dumps(log), password))
            logger.info(DONE)
        elif target == 'D':
            password = getpass.getpass(INPUT_PASSWORD_TO_DECRYPT.format(filepath))
            with open(filepath, 'rb') as (f):
                try:
                    log = json.loads(decrypt(f.read(), password))
                except (UnicodeDecodeError, json.decoder.JSONDecodeError):
                    logger.error(WRONG_PASSWORD.format(filepath))
                    exit(1)

            new_filepath = rename(filepath, '(decrypted)')
            logger.info(SAVING_TO_PLEASE_WAIT.format(new_filepath))
            with open(new_filepath, 'w') as (f):
                f.write(json.dumps(log))
            logger.info(DONE)
        else:
            logger.error(INVALID_TARGET.format(target))
            exit(1)


def main_loop(profile):
    paste = pyperclip.paste()
    tts_thread = None
    count = 0
    logger.debug(profile.print_config())
    logger.info(START_MONITORING)
    while True:
        if paste == pyperclip.paste():
            count += 1
            logger.debug('[{}] Same paste, continue...'.format(count))
            time.sleep(profile.interval)
            continue
        else:
            paste = pyperclip.paste()
            if len(paste) > profile.number:
                count = 0
                logger.info(OVER_CHARACTERS.format(profile.number))
                time.sleep(profile.interval)
                continue
            else:
                count = 0
                logger.debug('A different detected.')
                print((DIVIDING_TITLE.format('SOURCE')), flush=True)
                if profile.source == 'ja':
                    source = mecab_wakati.parse(paste).rstrip()
                    print(source, flush=True)
                else:
                    source = paste
                    print(source, flush=True)
                if profile.voice:
                    if profile.match:
                        if re.search(profile.match, paste) or :
                            logger.debug('"{}" matches in paste. Continue...'.format(profile.match))
                            if tts_thread:
                                tts_thread.kill()
                                logger.debug('Previous TTS process killed.')
                            tts_thread = Process(target=youdao_tts, args=(paste, profile.voice, profile.source))
                            tts_thread.start()
                            logger.debug('TTS process starts.')
                    else:
                        logger.debug('"{}" does not match in paste. Pass...'.format(profile.match))
                elif paste in profile.log:
                    print((DIVIDING_TITLE.format('ROMKAN (from log)')), flush=True)
                    print((profile.log[paste]['romkan']), flush=True)
                elif profile.source == 'ja':
                    print((DIVIDING_TITLE.format('ROMKAN')), flush=True)
                    chasen_list, roma_text = mecab_chasen.parse(paste), ''
                    for line in chasen_list.split('\n'):
                        if line != '' and line != 'EOS':
                            items = line.split('\t')
                            roma_text += romkan.to_roma(items[1]) + ' '

                    print(roma_text, flush=True)
                else:
                    roma_text = None
            if paste in profile.log and profile.log[paste]['youdao'] is not None:
                print((DIVIDING_TITLE.format('YOUDAO (from log)')), flush=True)
                youdao = profile.log[paste]['youdao']
                print(youdao, flush=True)
            elif 'youdao' in profile.disable:
                logger.info('The "--disable" option is set. Pass youdao translate.')
                youdao = None
            else:
                print((DIVIDING_TITLE.format('YOUDAO')), flush=True)
                youdao = youdao_translate(paste, target=(profile.target[0]), source=(profile.source))
                print(youdao, flush=True)
            if paste in profile.log and profile.log[paste]['aws'] is not None:
                print((DIVIDING_TITLE.format('AWS (from log)')), flush=True)
                aws = profile.log[paste]['aws']
                print(aws, flush=True)
            elif 'aws' in profile.disable:
                logger.info('The "--disable" option is set. Pass aws translate.')
                aws = None
            else:
                print((DIVIDING_TITLE.format('AWS')), flush=True)
                aws = aws_translate(paste, target=(profile.target[1]), source=(profile.source))
                print(aws, flush=True)
            if paste in profile.log and profile.log[paste]['aws'] is not None:
                print((DIVIDING_TITLE.format('GOOGLE (from log)')), flush=True)
                google = profile.log[paste]['google']
                print(google, flush=True)
            elif 'google' in profile.disable:
                logger.info('The "--disable" option is set. Pass google translate.')
                google = None
            else:
                print((DIVIDING_TITLE.format('GOOGLE')), flush=True)
                google = google_translate(paste)
                print(google, flush=True)
        profile.log[paste] = {}
        profile.log[paste]['source'] = source
        profile.log[paste]['romkan'] = roma_text
        profile.log[paste]['youdao'] = youdao
        profile.log[paste]['aws'] = aws
        profile.log[paste]['google'] = google
        print(DIVIDING_LINE, flush=True)


class Profile:
    _log: dict
    _log_filename: str

    def __init__(self, section, log, encrypt, voice, match, disable, source, target, interval, agth, opt):
        if section:
            if not config.has_section(section):
                logger.error(SECTION_NOT_FOUND.format(section))
                exit(1)
            log = config.get(section, 'log', fallback=(section + '.json'))
            encrypt = config.get(section, 'encrypt', fallback=None)
            voice = config.get(section, 'voice', fallback=None)
            match = config.get(section, 'match', fallback=None)
            disable = config.get(section, 'disable', fallback='')
            number = config.getint(section, 'number', fallback=256)
            source = config.get(section, 'source', fallback='ja')
            target = config.get(section, 'target', fallback='zh-CHS,en,zh-CN')
            interval = config.getfloat(section, 'interval', fallback=1.0)
            agth = config.get(section, 'agth', fallback=None)
            opt = config.get(section, 'opt', fallback='')
        else:
            self._section = DEFAULT_SECTION
        self._encrypt = encrypt
        if log:
            os.path.isfile(log) or logger.info(CREATE_A_NOT_EXISTS_FILE.format(log))
            self._log_filename = log
            self._log = {}
        elif log:
            self._log_filename = log
            if encrypt:
                with open(log, 'rb') as (f):
                    try:
                        self._log = json.loads(decrypt(f.read(), encrypt))
                    except (UnicodeDecodeError, json.decoder.JSONDecodeError):
                        logger.error(WRONG_PASSWORD.format(log))
                        exit(1)

            else:
                with open(log, 'r') as (f):
                    try:
                        self._log = json.loads(f.read())
                    except (UnicodeDecodeError, json.decoder.JSONDecodeError):
                        logger.error(PASSWORD_NOT_SPECIFIED.format(log))
                        exit(1)

        else:
            self._log_filename = DEFAULT_SECTION + '.json'
            if os.path.exists(self._log_filename):
                with open(self._log_filename, 'r+') as (f):
                    self._log = json.loads(f.read())
            else:
                self._log = {}
        if voice:
            if voice not in ('0', '1'):
                logger.warning('--voice option "{}" might be invalid.'.format(voice))
        self._voice = voice
        self._match = match
        self._disable = disable
        self._number = number
        if source not in SOURCE_ALL:
            logger.error('--source option "{}" is not supported.'.format(source))
            exit(1)
        targets = target.split(',')
        if len(targets) != 3:
            logger.error('--target option "{}" format error.'.format(target))
            exit(1)
        if targets[0] not in TARGET_YOUDAO:
            logger.error('--target option "{}" not supported by youdao.'.format(targets[0]))
            exit(1)
        if targets[1] not in TARGET_AWS:
            logger.error('--target option "{}" not supported by aws.'.format(targets[1]))
            exit(1)
        self._source = source
        self._target = (targets[0], targets[1])
        self._interval = interval
        self._agth = agth
        self._opt = opt if opt else ''
        if self._agth:
            cmd = agth + opt
            logger.info(START_AGTH_FROM.format(agth, opt))
            subprocess.Popen([agth] + opt.split(' '))

    @property
    def section(self):
        if self._section == DEFAULT_SECTION:
            logger.warning('Cannot call default section. Continue...')
            return
        return self._section

    @section.setter
    def section(self, value):
        logger.warning(ACCESS_READONLY_PROPERTY.format('section'))

    @property
    def log_filename(self):
        return self._log_filename

    @log_filename.setter
    def log_filename(self, value):
        logger.warning(ACCESS_READONLY_PROPERTY.format('log_filename'))

    @property
    def log(self):
        return self._log

    @log.setter
    def log(self, value):
        self._log = value

    @property
    def encrypt(self):
        return self._encrypt

    @encrypt.setter
    def encrypt(self, value):
        logger.warning(ACCESS_READONLY_PROPERTY.format('encrypt'))

    @property
    def voice(self):
        return self._voice

    @voice.setter
    def voice(self, value):
        logger.warning(ACCESS_READONLY_PROPERTY.format('voice'))

    @property
    def match(self):
        return self._match

    @match.setter
    def match(self, value):
        logger.warning(ACCESS_READONLY_PROPERTY.format('match'))

    @property
    def disable(self):
        return self._disable

    @disable.setter
    def disable(self, value):
        logger.warning(ACCESS_READONLY_PROPERTY.format('disable'))

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        logger.warning(ACCESS_READONLY_PROPERTY.format('number'))

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        logger.warning(ACCESS_READONLY_PROPERTY.format('source'))

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        logger.warning(ACCESS_READONLY_PROPERTY.format('target'))

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, value):
        logger.warning(ACCESS_READONLY_PROPERTY.format('interval'))

    @property
    def agth(self):
        return self._agth

    @agth.setter
    def agth(self, value):
        logger.warning(ACCESS_READONLY_PROPERTY.format('agth'))

    @property
    def opt(self):
        return self._opt

    @opt.setter
    def opt(self, value):
        logger.warning(ACCESS_READONLY_PROPERTY.format('opt'))

    def save_log(self):
        if self._encrypt:
            with open(self._log_filename, 'wb') as (f):
                f.write(encrypt(json.dumps(self._log), self.encrypt))
        else:
            with open(self._log_filename, 'w') as (f):
                f.write(json.dumps(self._log))

    def print_config(self):
        return '\n        log = {}\n        encrypt = {}\n        voice = {}\n        match = {}\n        disable = {}\n        number = {}\n        source = {}\n        target = {}\n        interval = {}\n        agth = {}\n        opt = {}\n        '.format(self.log, self.encrypt, self.voice, self.match, self.disable, self.number, self.source, self.target, self.interval, self.agth, self.opt)


def main():
    args = parser.parse_args(sys.argv[1:])
    if args.passwd:
        passwd(args.passwd)
        exit(0)
    profile = Profile(args.profile, args.log, args.encrypt, args.voice, args.match, args.disable, args.source, args.target, args.interval, args.agth, args.opt)
    try:
        main_loop(profile)
    except KeyboardInterrupt:
        logger.info(SAVING_TO_PLEASE_WAIT.format(profile.log_filename))
        profile.save_log()
        logger.info(DONE)


if __name__ == '__main__':
    main()