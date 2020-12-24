# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/lib/core/settings.py
# Compiled at: 2013-12-09 06:41:17
"""
Copyright (c) 2006-2013 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""
import os, re, subprocess, string, sys
from lib.core.enums import DBMS
from lib.core.enums import DBMS_DIRECTORY_NAME
from lib.core.enums import OS
from lib.core.revision import getRevisionNumber
VERSION = '1.0-dev'
REVISION = getRevisionNumber()
VERSION_STRING = 'sqlmap/%s%s' % (VERSION, '-%s' % REVISION if REVISION else '')
DESCRIPTION = 'automatic SQL injection and database takeover tool'
SITE = 'http://sqlmap.org'
ISSUES_PAGE = 'https://github.com/sqlmapproject/sqlmap/issues/new'
GIT_REPOSITORY = 'git://github.com/sqlmapproject/sqlmap.git'
ML = 'sqlmap-users@lists.sourceforge.net'
DIFF_TOLERANCE = 0.05
CONSTANT_RATIO = 0.9
LOWER_RATIO_BOUND = 0.02
UPPER_RATIO_BOUND = 0.98
PARAMETER_AMP_MARKER = '__AMP__'
PARAMETER_SEMICOLON_MARKER = '__SEMICOLON__'
PARTIAL_VALUE_MARKER = '__PARTIAL_VALUE__'
PARTIAL_HEX_VALUE_MARKER = '__PARTIAL_HEX_VALUE__'
URI_QUESTION_MARKER = '__QUESTION_MARK__'
ASTERISK_MARKER = '__ASTERISK_MARK__'
REPLACEMENT_MARKER = '__REPLACEMENT_MARK__'
PAYLOAD_DELIMITER = '__PAYLOAD_DELIMITER__'
CHAR_INFERENCE_MARK = '%c'
PRINTABLE_CHAR_REGEX = '[^\\x00-\\x1f\\x7f-\\xff]'
PERMISSION_DENIED_REGEX = '(command|permission|access)\\s*(was|is)?\\s*denied'
MAX_CONNECTIONS_REGEX = 'max.+connections'
GOOGLE_REGEX = 'url\\?\\w+=((?![^>]+webcache\\.googleusercontent\\.com)http[^>]+)&(sa=U|rct=j)'
TEXT_TAG_REGEX = '(?si)<(abbr|acronym|b|blockquote|br|center|cite|code|dt|em|font|h\\d|i|li|p|pre|q|strong|sub|sup|td|th|title|tt|u)(?!\\w).*?>(?P<result>[^<]+)'
IP_ADDRESS_REGEX = '\\b\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\b'
CONCAT_ROW_DELIMITER = ','
CONCAT_VALUE_DELIMITER = '|'
TIME_STDEV_COEFF = 7
MIN_VALID_DELAYED_RESPONSE = 0.5
WARN_TIME_STDEV = 0.5
UNION_MIN_RESPONSE_CHARS = 10
UNION_STDEV_COEFF = 7
TIME_DELAY_CANDIDATES = 3
HTTP_ACCEPT_HEADER_VALUE = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
HTTP_ACCEPT_ENCODING_HEADER_VALUE = 'gzip,deflate'
BACKDOOR_RUN_CMD_TIMEOUT = 5
MAX_TECHNIQUES_PER_VALUE = 2
METADB_SUFFIX = '_masterdb'
MIN_TIME_RESPONSES = 15
MIN_UNION_RESPONSES = 5
INFERENCE_BLANK_BREAK = 10
INFERENCE_UNKNOWN_CHAR = '?'
INFERENCE_GREATER_CHAR = '>'
INFERENCE_EQUALS_CHAR = '='
INFERENCE_NOT_EQUALS_CHAR = '!='
UNKNOWN_DBMS = 'Unknown'
UNKNOWN_DBMS_VERSION = 'Unknown'
DYNAMICITY_MARK_LENGTH = 32
DUMMY_USER_PREFIX = '__dummy__'
DEFAULT_PAGE_ENCODING = 'iso-8859-1'
DUMMY_URL = 'http://foo/bar?id=1'
IS_WIN = subprocess.mswindows
PLATFORM = os.name
PYVERSION = sys.version.split()[0]
MSSQL_SYSTEM_DBS = ('Northwind', 'master', 'model', 'msdb', 'pubs', 'tempdb')
MYSQL_SYSTEM_DBS = ('information_schema', 'mysql')
PGSQL_SYSTEM_DBS = ('information_schema', 'pg_catalog', 'pg_toast')
ORACLE_SYSTEM_DBS = ('CTXSYS', 'DBSNMP', 'DMSYS', 'EXFSYS', 'MDSYS', 'OLAPSYS', 'ORDSYS',
                     'OUTLN', 'SYS', 'SYSAUX', 'SYSMAN', 'SYSTEM', 'TSMSYS', 'WMSYS',
                     'XDB')
SQLITE_SYSTEM_DBS = ('sqlite_master', 'sqlite_temp_master')
ACCESS_SYSTEM_DBS = ('MSysAccessObjects', 'MSysACEs', 'MSysObjects', 'MSysQueries',
                     'MSysRelationships', 'MSysAccessStorage', 'MSysAccessXML', 'MSysModules',
                     'MSysModules2')
FIREBIRD_SYSTEM_DBS = ('RDB$BACKUP_HISTORY', 'RDB$CHARACTER_SETS', 'RDB$CHECK_CONSTRAINTS',
                       'RDB$COLLATIONS', 'RDB$DATABASE', 'RDB$DEPENDENCIES', 'RDB$EXCEPTIONS',
                       'RDB$FIELDS', 'RDB$FIELD_DIMENSIONS', ' RDB$FILES', 'RDB$FILTERS',
                       'RDB$FORMATS', 'RDB$FUNCTIONS', 'RDB$FUNCTION_ARGUMENTS',
                       'RDB$GENERATORS', 'RDB$INDEX_SEGMENTS', 'RDB$INDICES', 'RDB$LOG_FILES',
                       'RDB$PAGES', 'RDB$PROCEDURES', 'RDB$PROCEDURE_PARAMETERS',
                       'RDB$REF_CONSTRAINTS', 'RDB$RELATIONS', 'RDB$RELATION_CONSTRAINTS',
                       'RDB$RELATION_FIELDS', 'RDB$ROLES', 'RDB$SECURITY_CLASSES',
                       'RDB$TRANSACTIONS', 'RDB$TRIGGERS', 'RDB$TRIGGER_MESSAGES',
                       'RDB$TYPES', 'RDB$USER_PRIVILEGES', 'RDB$VIEW_RELATIONS')
MAXDB_SYSTEM_DBS = ('SYSINFO', 'DOMAIN')
SYBASE_SYSTEM_DBS = ('master', 'model', 'sybsystemdb', 'sybsystemprocs')
DB2_SYSTEM_DBS = ('NULLID', 'SQLJ', 'SYSCAT', 'SYSFUN', 'SYSIBM', 'SYSIBMADM', 'SYSIBMINTERNAL',
                  'SYSIBMTS', 'SYSPROC', 'SYSPUBLIC', 'SYSSTAT', 'SYSTOOLS')
HSQLDB_SYSTEM_DBS = ('INFORMATION_SCHEMA', 'SYSTEM_LOB')
MSSQL_ALIASES = ('microsoft sql server', 'mssqlserver', 'mssql', 'ms')
MYSQL_ALIASES = ('mysql', 'my')
PGSQL_ALIASES = ('postgresql', 'postgres', 'pgsql', 'psql', 'pg')
ORACLE_ALIASES = ('oracle', 'orcl', 'ora', 'or')
SQLITE_ALIASES = ('sqlite', 'sqlite3')
ACCESS_ALIASES = ('msaccess', 'access', 'jet', 'microsoft access')
FIREBIRD_ALIASES = ('firebird', 'mozilla firebird', 'interbase', 'ibase', 'fb')
MAXDB_ALIASES = ('maxdb', 'sap maxdb', 'sap db')
SYBASE_ALIASES = ('sybase', 'sybase sql server')
DB2_ALIASES = ('db2', 'ibm db2', 'ibmdb2')
HSQLDB_ALIASES = ('hsql', 'hsqldb', 'hs', 'hypersql')
DBMS_DIRECTORY_DICT = dict((getattr(DBMS, _), getattr(DBMS_DIRECTORY_NAME, _)) for _ in dir(DBMS) if not _.startswith('_'))
SUPPORTED_DBMS = MSSQL_ALIASES + MYSQL_ALIASES + PGSQL_ALIASES + ORACLE_ALIASES + SQLITE_ALIASES + ACCESS_ALIASES + FIREBIRD_ALIASES + MAXDB_ALIASES + SYBASE_ALIASES + DB2_ALIASES + HSQLDB_ALIASES
SUPPORTED_OS = ('linux', 'windows')
USER_AGENT_ALIASES = ('ua', 'useragent', 'user-agent')
REFERER_ALIASES = ('ref', 'referer', 'referrer')
HOST_ALIASES = ('host', )
BASIC_HELP_ITEMS = ('url', 'googleDork', 'data', 'cookie', 'randomAgent', 'proxy',
                    'testParameter', 'dbms', 'level', 'risk', 'tech', 'getAll', 'getBanner',
                    'getCurrentUser', 'getCurrentDb', 'getPasswordHashes', 'getTables',
                    'getColumns', 'getSchema', 'dumpTable', 'dumpAll', 'db', 'tbl',
                    'col', 'osShell', 'osPwn', 'batch', 'checkTor', 'flushSession',
                    'tor', 'wizard')
NULL = 'NULL'
BLANK = '<blank>'
CURRENT_DB = 'CD'
ERROR_PARSING_REGEXES = ('<b>[^<]*(fatal|error|warning|exception)[^<]*</b>:?\\s*(?P<result>.+?)<br\\s*/?\\s*>',
                         '(?m)^(fatal|error|warning|exception):?\\s*(?P<result>.+?)$',
                         '<li>Error Type:<br>(?P<result>.+?)</li>', "error '[0-9a-f]{8}'((<[^>]+>)|\\s)+(?P<result>[^<>]+)")
META_CHARSET_REGEX = '(?si)<head>.*<meta http-equiv="?content-type"?[^>]+charset=(?P<result>[^">]+).*</head>'
META_REFRESH_REGEX = '(?si)<head>.*<meta http-equiv="?refresh"?[^>]+content="?[^">]+url=(?P<result>[^">]+).*</head>'
EMPTY_FORM_FIELDS_REGEX = '(&|\\A)(?P<result>[^=]+=(&|\\Z))'
COMMON_PASSWORD_SUFFIXES = ('1', '123', '2', '12', '3', '13', '7', '11', '5', '22',
                            '23', '01', '4', '07', '21', '14', '10', '06', '08',
                            '8', '15', '69', '16', '6', '18')
COMMON_PASSWORD_SUFFIXES += ('!', '.', '*', '!!', '?', ';', '..', '!!!', ', ', '@')
WEBSCARAB_SPLITTER = '### Conversation'
BURP_REQUEST_REGEX = '={10,}\\s+[^=]+={10,}\\s(.+?)\\s={10,}'
BURP_XML_HISTORY_REGEX = '<request base64="true"><!\\[CDATA\\[([^]]+)'
UNICODE_ENCODING = 'utf8'
URI_HTTP_HEADER = 'URI'
URI_INJECTABLE_REGEX = '//[^/]*/([^\\.*?]+)\\Z'
SENSITIVE_DATA_REGEX = '(\\s|=)(?P<result>[^\\s=]*%s[^\\s]*)\\s'
MAX_NUMBER_OF_THREADS = 10
MIN_STATISTICAL_RANGE = 0.01
MIN_RATIO = 0.0
MAX_RATIO = 1.0
CUSTOM_INJECTION_MARK_CHAR = '*'
INJECT_HERE_MARK = '%INJECT HERE%'
MYSQL_ERROR_CHUNK_LENGTH = 50
MSSQL_ERROR_CHUNK_LENGTH = 100
EXCLUDE_UNESCAPE = (
 'WAITFOR DELAY ', ' INTO DUMPFILE ', ' INTO OUTFILE ', 'CREATE ', 'BULK ', 'EXEC ', 'RECONFIGURE ', 'DECLARE ', "'%s'" % CHAR_INFERENCE_MARK)
REFLECTED_VALUE_MARKER = '__REFLECTED_VALUE__'
REFLECTED_BORDER_REGEX = '[^A-Za-z]+'
REFLECTED_REPLACEMENT_REGEX = '.+?'
REFLECTED_MAX_REGEX_PARTS = 10
URLENCODE_FAILSAFE_CHARS = '()|,'
URLENCODE_CHAR_LIMIT = 2000
DEFAULT_MSSQL_SCHEMA = 'dbo'
HASH_MOD_ITEM_DISPLAY = 11
MAX_INT = sys.maxint
RESTORE_MERGED_OPTIONS = ('col', 'db', 'dnsName', 'privEsc', 'tbl', 'regexp', 'string',
                          'textOnly', 'threads', 'timeSec', 'tmpPath', 'uChar', 'user')
IGNORE_PARAMETERS = ('__VIEWSTATE', '__VIEWSTATEENCRYPTED', '__EVENTARGUMENT', '__EVENTTARGET',
                     '__EVENTVALIDATION', 'ASPSESSIONID', 'ASP.NET_SESSIONID', 'JSESSIONID',
                     'CFID', 'CFTOKEN')
ASP_NET_CONTROL_REGEX = '(?i)\\Actl\\d+\\$'
TURN_OFF_RESUME_INFO_LIMIT = 20
RESULTS_FILE_FORMAT = 'results-%m%d%Y_%I%M%p.csv'
CODECS_LIST_PAGE = 'http://docs.python.org/library/codecs.html#standard-encodings'
SQL_SCALAR_REGEX = '\\A(SELECT(?!\\s+DISTINCT\\(?))?\\s*\\w*\\('
LOCALHOST = '127.0.0.1'
DEFAULT_TOR_SOCKS_PORT = 9050
DEFAULT_TOR_HTTP_PORTS = (8123, 8118)
LOW_TEXT_PERCENT = 20
IGNORE_SPACE_AFFECTED_KEYWORDS = ('CAST', 'COUNT', 'EXTRACT', 'GROUP_CONCAT', 'MAX',
                                  'MID', 'MIN', 'SESSION_USER', 'SUBSTR', 'SUBSTRING',
                                  'SUM', 'SYSTEM_USER', 'TRIM')
LEGAL_DISCLAIMER = "Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program"
REFLECTIVE_MISS_THRESHOLD = 20
HTML_TITLE_REGEX = '<title>(?P<result>[^<]+)</title>'
ITOA64 = './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
DUMMY_SQL_INJECTION_CHARS = ";()'"
DUMMY_USER_INJECTION = '(?i)[^\\w](AND|OR)\\s+[^\\s]+[=><]|\\bUNION\\b.+\\bSELECT\\b'
CRAWL_EXCLUDE_EXTENSIONS = ('gif', 'jpg', 'jpeg', 'image', 'jar', 'tif', 'bmp', 'war',
                            'ear', 'mpg', 'mpeg', 'wmv', 'mpeg', 'scm', 'iso', 'dmp',
                            'dll', 'cab', 'so', 'avi', 'mkv', 'bin', 'iso', 'tar',
                            'png', 'pdf', 'ps', 'wav', 'mp3', 'mp4', 'au', 'aiff',
                            'aac', 'zip', 'rar', '7z', 'gz', 'flv', 'mov')
PROBLEMATIC_CUSTOM_INJECTION_PATTERNS = "(\\bq=[^;']+)|(\\*/\\*)"
BRUTE_TABLE_EXISTS_TEMPLATE = 'EXISTS(SELECT %d FROM %s)'
BRUTE_COLUMN_EXISTS_TEMPLATE = 'EXISTS(SELECT %s FROM %s)'
IDS_WAF_CHECK_PAYLOAD = 'AND 1=1 UNION ALL SELECT 1,2,3,table_name FROM information_schema.tables WHERE 2>1'
WAF_ATTACK_VECTORS = (
 '',
 'search=<script>alert(1)</script>',
 'file=../../../../etc/passwd',
 'q=<invalid>foobar',
 'id=1 %s' % IDS_WAF_CHECK_PAYLOAD)
ROTATING_CHARS = ('\\', '|', '|', '/', '-')
BIGARRAY_CHUNK_LENGTH = 4096
TRIM_STDOUT_DUMP_SIZE = 256
PARSE_HEADERS_LIMIT = 3
ORDER_BY_STEP = 10
MAX_TIME_REVALIDATION_STEPS = 5
PARAMETER_SPLITTING_REGEX = '[,|;]'
UNION_CHAR_REGEX = '\\A\\w+\\Z'
UNENCODED_ORIGINAL_VALUE = 'original'
COMMON_USER_COLUMNS = ('user', 'username', 'user_name', 'benutzername', 'benutzer',
                       'utilisateur', 'usager', 'consommateur', 'utente', 'utilizzatore',
                       'usufrutuario', 'korisnik', 'usuario', 'consumidor')
DEFAULT_GET_POST_DELIMITER = '&'
DEFAULT_COOKIE_DELIMITER = ';'
FORCE_COOKIE_EXPIRATION_TIME = '9999999999'
HASHDB_FLUSH_THRESHOLD = 32
HASHDB_FLUSH_RETRIES = 3
HASHDB_MILESTONE_VALUE = 'cAWxkLYCQT'
LARGE_OUTPUT_THRESHOLD = 1048576
SLOW_ORDER_COUNT_THRESHOLD = 10000
HASH_RECOGNITION_QUIT_THRESHOLD = 10000
MAX_SINGLE_URL_REDIRECTIONS = 4
MAX_TOTAL_REDIRECTIONS = 10
MAX_DNS_LABEL = 63
DNS_BOUNDARIES_ALPHABET = re.sub('[a-fA-F]', '', string.ascii_letters)
HEURISTIC_CHECK_ALPHABET = ('"', "'", ')', '(', '[', ']', ',', '.')
MAX_CONNECTION_CHUNK_SIZE = 10485760
MAX_CONNECTION_TOTAL_SIZE = 104857600
MAX_BISECTION_LENGTH = 52428800
LARGE_CHUNK_TRIM_MARKER = '__TRIMMED_CONTENT__'
GENERIC_SQL_COMMENT = '-- '
VALID_TIME_CHARS_RUN_THRESHOLD = 100
CHECK_ZERO_COLUMNS_THRESHOLD = 10
BOLD_PATTERNS = ("' injectable", 'might be injectable', "' is vulnerable", 'is not injectable',
                 'test failed', 'test passed', 'live test final result', 'test shows that')
GENERIC_DOC_ROOT_DIRECTORY_NAMES = ('htdocs', 'httpdocs', 'public', 'wwwroot', 'www')
MAX_HELP_OPTION_LENGTH = 18
MAX_CONNECT_RETRIES = 100
FORMAT_EXCEPTION_STRINGS = ('Type mismatch', 'Error converting', 'Failed to convert',
                            'System.FormatException', 'java.lang.NumberFormatException')
VIEWSTATE_REGEX = '(?i)(?P<name>__VIEWSTATE[^"]*)[^>]+value="(?P<result>[^"]+)'
EVENTVALIDATION_REGEX = '(?i)(?P<name>__EVENTVALIDATION[^"]*)[^>]+value="(?P<result>[^"]+)'
LIMITED_ROWS_TEST_NUMBER = 15
INVALID_UNICODE_CHAR_FORMAT = '\\?%02x'
SOAP_RECOGNITION_REGEX = '(?s)\\A(<\\?xml[^>]+>)?\\s*<([^> ]+)( [^>]+)?>.+</\\2.*>\\s*\\Z'
JSON_RECOGNITION_REGEX = '(?s)\\A(\\s*\\[)*\\s*\\{.*"[^"]+"\\s*:\\s*("[^"]+"|\\d+).*\\}\\s*(\\]\\s*)*\\Z'
MULTIPART_RECOGNITION_REGEX = '(?i)Content-Disposition:[^;]+;\\s*name='
DEFAULT_CONTENT_TYPE = 'application/x-www-form-urlencoded; charset=utf-8'
PLAIN_TEXT_CONTENT_TYPE = 'text/plain; charset=utf-8'
SUHOSIN_MAX_VALUE_LENGTH = 512
MIN_BINARY_DISK_DUMP_SIZE = 100
FORM_SEARCH_REGEX = '(?si)<form(?!.+<form).+?</form>'
MIN_ENCODED_LEN_CHECK = 5
METASPLOIT_SESSION_TIMEOUT = 180
NETSCAPE_FORMAT_HEADER_COOKIES = '# Netscape HTTP Cookie File.'
BRUTE_DOC_ROOT_PREFIXES = {OS.LINUX: ('/var/www', '/var/www/%TARGET%', '/var/www/vhosts/%TARGET%', '/var/www/virtual/%TARGET%',
 '/var/www/clients/vhosts/%TARGET%', '/var/www/clients/virtual/%TARGET%'), 
   OS.WINDOWS: ('/xampp', '/Program Files/xampp/', '/wamp', '/Program Files/wampp/', '/Inetpub/wwwroot',
 '/Inetpub/wwwroot/%TARGET%', '/Inetpub/vhosts/%TARGET%')}
BRUTE_DOC_ROOT_SUFFIXES = ('', 'html', 'htdocs', 'httpdocs', 'php', 'public', 'src',
                           'site', 'build', 'web', 'sites/all', 'www/build')
BRUTE_DOC_ROOT_TARGET_MARK = '%TARGET%'
KB_CHARS_BOUNDARY_CHAR = 'q'
HTML_DUMP_CSS_STYLE = '<style>\ntable{\n    margin:10;\n    background-color:#FFFFFF;\n    font-family:verdana;\n    font-size:12px;\n    align:center;\n}\nthead{\n    font-weight:bold;\n    background-color:#4F81BD;\n    color:#FFFFFF;\n}\ntr:nth-child(even) {\n    background-color: #D3DFEE\n}\ntd{\n    font-size:10px;\n}\nth{\n    font-size:10px;\n}\n</style>'