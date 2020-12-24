# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xsrfprobe/files/dcodelist.py
# Compiled at: 2020-01-29 10:31:04
# Size of source mod 2**32: 5336 bytes
HASH_DB = (('Blowfish (Eggdrop)', '^\\+[a-zA-Z0-9\\/\\.]{12}$'), ('Blowfish (OpenBSD)', '^\\$2a\\$[0-9]{0,2}?\\$[a-zA-Z0-9\\/\\.]{53}$'),
           ('Blowfish Crypt', '^\\$2[axy]{0,1}\\$[a-zA-Z0-9./]{8}\\$[a-zA-Z0-9./]{1,}$'),
           ('DES (Unix)', '^.{0,2}[a-zA-Z0-9\\/\\.]{11}$'), ('MD5 (Unix)', '^\\$1\\$.{0,8}\\$[a-zA-Z0-9\\/\\.]{22}$'),
           ('MD5 (APR)', '^\\$apr1\\$.{0,8}\\$[a-zA-Z0-9\\/\\.]{22}$'), ('MD5 (MyBB)', '^[a-fA-F0-9]{32}:[a-z0-9]{8}$'),
           ('MD5 (ZipMonster)', '^[a-fA-F0-9]{32}$'), ('MD5 crypt', '^\\$1\\$[a-zA-Z0-9./]{8}\\$[a-zA-Z0-9./]{1,}$'),
           ('MD5 apache crypt', '^\\$apr1\\$[a-zA-Z0-9./]{8}\\$[a-zA-Z0-9./]{1,}$'),
           ('MD5 (Joomla)', '^[a-fA-F0-9]{32}:[a-zA-Z0-9]{16,32}$'), ('MD5 (Wordpress)', '^\\$P\\$[a-zA-Z0-9\\/\\.]{31}$'),
           ('MD5 (phpBB3)', '^\\$H\\$[a-zA-Z0-9\\/\\.]{31}$'), ('MD5 (Cisco PIX)', '^[a-zA-Z0-9\\/\\.]{16}$'),
           ('MD5 (osCommerce)', '^[a-fA-F0-9]{32}:[a-zA-Z0-9]{2}$'), ('MD5 (Palshop)', '^[a-fA-F0-9]{51}$'),
           ('MD5 (IP.Board)', '^[a-fA-F0-9]{32}:.{5}$'), ('MD5 (Chap)', '^[a-fA-F0-9]{32}:[0-9]{32}:[a-fA-F0-9]{2}$'),
           ('Juniper Netscreen/SSG (ScreenOS)', '^[a-zA-Z0-9]{30}:[a-zA-Z0-9]{4,}$'),
           ('Fortigate (FortiOS)', '^[a-fA-F0-9]{47}$'), ('Minecraft (Authme)', '^\\$sha\\$[a-zA-Z0-9]{0,16}\\$[a-fA-F0-9]{64}$'),
           ('Lotus Domino', '^\\(?[a-zA-Z0-9\\+\\/]{20}\\)?$'), ('Lineage II C4', '^0x[a-fA-F0-9]{32}$'),
           ('CRC-96 (ZIP)', '^[a-fA-F0-9]{24}$'), ('NT crypt', '^\\$3\\$[a-zA-Z0-9./]{8}\\$[a-zA-Z0-9./]{1,}$'),
           ('Skein-1024', '^[a-fA-F0-9]{256}$'), ('RIPEMD-320', '^[A-Fa-f0-9]{80}$'),
           ('EPi hash', '^0x[A-F0-9]{60}$'), ('EPiServer 6.x < v4', '^\\$episerver\\$\\*0\\*[a-zA-Z0-9]{22}==\\*[a-zA-Z0-9\\+]{27}$'),
           ('EPiServer 6.x >= v4', '^\\$episerver\\$\\*1\\*[a-zA-Z0-9]{22}==\\*[a-zA-Z0-9]{43}$'),
           ('Cisco IOS SHA256', '^[a-zA-Z0-9]{43}$'), ('oRACLE 11g/12c', '^(S:)?[a-f0-9]{40}(:)?[a-f0-9]{20}$'),
           ('SHA-1 (Django)', '^sha1\\$.{0,32}\\$[a-fA-F0-9]{40}$'), ('SHA-1 crypt', '^\\$4\\$[a-zA-Z0-9./]{8}\\$[a-zA-Z0-9./]{1,}$'),
           ('SHA-1 (Hex)', '^[a-fA-F0-9]{40}$'), ('SHA-1 (LDAP) Base64', '^\\{SHA\\}[a-zA-Z0-9+/]{27}=$'),
           ('SHA-1 (LDAP) Base64 + salt', '^\\{SSHA\\}[a-zA-Z0-9+/]{28,}[=]{0,3}$'),
           ('SHA-512 (Drupal)', '^\\$S\\$[a-zA-Z0-9\\/\\.]{52}$'), ('SHA-512 crypt', '^\\$6\\$[a-zA-Z0-9./]{8}\\$[a-zA-Z0-9./]{1,}$'),
           ('SHA-256 (Django)', '^sha256\\$.{0,32}\\$[a-fA-F0-9]{64}$'), ('SHA-256 crypt', '^\\$5\\$[a-zA-Z0-9./]{8}\\$[a-zA-Z0-9./]{1,}$'),
           ('SHA-384 (Django)', '^sha384\\$.{0,32}\\$[a-fA-F0-9]{96}$'), ('SHA-256 (Unix)', '^\\$5\\$.{0,22}\\$[a-zA-Z0-9\\/\\.]{43,69}$'),
           ('SHA-512 (Unix)', '^\\$6\\$.{0,22}\\$[a-zA-Z0-9\\/\\.]{86}$'), ('SHA-384', '^[a-fA-F0-9]{96}$'),
           ('SHA-512', '^[a-fA-F0-9]{128}$'), ('SipHash', '^[a-f0-9]{16}:2:4:[a-f0-9]{32}$'),
           ('SSHA-1', '^({SSHA})?[a-zA-Z0-9\\+\\/]{32,38}?(==)?$'), ('SSHA-1 (Base64)', '^\\{SSHA\\}[a-zA-Z0-9]{32,38}?(==)?$'),
           ('SSHA-512 (Base64)', '^\\{SSHA512\\}[a-zA-Z0-9+]{96}$'), ('Oracle 11g', '^S:[A-Z0-9]{60}$'),
           ('SMF >= v1.1', '^[a-fA-F0-9]{40}:[0-9]{8}&'), ('MySQL 5.x', '^\\*[a-f0-9]{40}$'),
           ('MySQL 3.x', '^[a-fA-F0-9]{16}$'), ('OSX v10.7', '^[a-fA-F0-9]{136}$'),
           ('OSX v10.8', '^\\$ml\\$[a-fA-F0-9$]{199}$'), ('SAM (LM_Hash:NT_Hash)', '^[a-fA-F0-9]{32}:[a-fA-F0-9]{32}$'),
           ('MSSQL (2000)', '^0x0100[a-f0-9]{0,8}?[a-f0-9]{80}$'), ('Cisco Type 7', '^[a-f0-9]{4,}$'),
           ('Snefru-256', '^(\\\\$snefru\\\\$)?[a-f0-9]{64}$'), ('MSSQL (2005)', '^0x0100[a-f0-9]{0,8}?[a-f0-9]{40}$'),
           ('MSSQL (2012)', '^0x02[a-f0-9]{0,10}?[a-f0-9]{128}$'), ('TIGER-160 (HMAC)', '^[a-f0-9]{40}$'),
           ('SHA-256', '^[a-fA-F0-9]{64}$'), ('SHA-1 (Oracle)', '^[a-fA-F0-9]{48}$'),
           ('SHA-224', '^[a-fA-F0-9]{56}$'), ('Adler32', '^[a-f0-9]{8}$'), ('CRC-16-CCITT', '^[a-fA-F0-9]{4}$'),
           ('NTLM', '^[0-9A-Fa-f]{32}$'))
IP = '((25[0-5]|2[0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]{0,1})\\.){3}(25[0-5]|2[0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]{0,1})'
RID_DOUBLE = '/\\.\\./'
RID_SINGLE = '\\./'
RID_COMPILE = '/[^/]*/../'
NUM_SUB = '=[0-9]+'
NUM_COM = '(title=)[^&]*'
BINARY = '^[01]+$'
DEC = '&#.*;+'
PROTOCOLS = '(.*\\/)[^\\/]*'