# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgp/armor.py
# Compiled at: 2015-08-31 08:17:33
from base64 import b64decode
from base64 import b64encode
import math, re, warnings
from pgp.crc24 import crc24
PGP_MESSAGE = 1
PGP_PUBLIC_KEY_BLOCK = 2
PGP_PRIVATE_KEY_BLOCK = 3
PGP_SIGNATURE = 4
data_types = {PGP_MESSAGE: 'PGP MESSAGE', 
 PGP_PUBLIC_KEY_BLOCK: 'PGP PUBLIC KEY BLOCK', 
 PGP_PRIVATE_KEY_BLOCK: 'PGP PRIVATE KEY BLOCK', 
 PGP_SIGNATURE: 'PGP SIGNATURE'}
DASHES = '-----'
header_line_expr = re.compile('^{dashes}BEGIN (?:(?P<message>{message})(?:, PART (?P<part>[1-9][0-9]*)(?:/(?P<total_parts>[1-9][0-9]*))?)?|(?P<public_key>{public_key})|(?P<private_key>{private_key})|(?P<signature>{signature})){dashes}$'.format(dashes=DASHES, message=data_types[PGP_MESSAGE], public_key=data_types[PGP_PUBLIC_KEY_BLOCK], private_key=data_types[PGP_PRIVATE_KEY_BLOCK], signature=data_types[PGP_SIGNATURE]))

def is_armor(data):
    try:
        canary = data[:len(DASHES)]
        if isinstance(canary, bytes):
            canary = canary.decode('us-ascii')
    except UnicodeError:
        return False

    return canary == DASHES


class ASCIIArmor(object):

    @classmethod
    def from_ascii(cls, text):
        lines = text.splitlines()
        line_no = 0
        while not len(lines[line_no].strip()):
            line_no += 1

        header_line = lines[line_no]
        header_matches = header_line_expr.match(header_line)
        if header_matches is None:
            raise ValueError('{0} is not a valid header.'.format(repr(header_line)))
        line_no += 1
        part = None
        total_parts = None
        if header_matches.group('message'):
            data_type = PGP_MESSAGE
            part = header_matches.group('part')
            if part is not None:
                part = int(part)
            total_parts = header_matches.group('total_parts')
            if total_parts is not None:
                total_parts = int(total_parts)
        else:
            if header_matches.group('public_key'):
                data_type = PGP_PUBLIC_KEY_BLOCK
            else:
                if header_matches.group('private_key'):
                    data_type = PGP_PRIVATE_KEY_BLOCK
                else:
                    if header_matches.group('signature'):
                        data_type = PGP_SIGNATURE
                    else:
                        raise ValueError
        version = None
        comment = None
        message_id = None
        hash_algorithms = None
        charset = None
        extra_headers = {}
        while len(lines[line_no].strip()):
            header_key, header_value = lines[line_no].split(': ', 1)
            if header_key == 'Version':
                version = header_value
            else:
                if header_key == 'Comment':
                    comment = header_value
                else:
                    if header_key == 'MessageID':
                        message_id = header_value
                    else:
                        if header_key == 'Hash':
                            hash_algorithms = header_value
                        else:
                            if header_key == 'Charset':
                                charset = header_value
                            else:
                                warnings.warn('Unsupported armor header, "{0}"'.format(header_key))
                                extra_headers[header_key] = header_value
            line_no += 1

        line_no += 1
        data_lines = []
        while lines[line_no][:1] != '=':
            data_lines.append(lines[line_no])
            line_no += 1

        data = b64decode(''.join(data_lines))
        checksum_data = b64decode(lines[line_no][1:])
        expected_checksum = (checksum_data[0] << 16) + (checksum_data[1] << 8) + checksum_data[2]
        line_no += 1
        actual_checksum = crc24(data)
        if actual_checksum != expected_checksum:
            raise ValueError('Checksum does not match. {0} (actual) != {1} (expected).'.format(repr(actual_checksum), repr(expected_checksum)))
        tail_line = lines[line_no]
        if tail_line != header_line.replace('BEGIN', 'END'):
            raise ValueError('Tail line does not match header line. {0} {1}'.format(repr(header_line), repr(tail_line)))
        return cls(data_type, data, part, total_parts, version, comment, message_id, hash_algorithms, charset)

    def __init__(self, data_type, data, part=None, total_parts=None, version=None, comment=None, message_id=None, hash_algorithms=None, charset=None, extra_headers=None):
        self.data_type = data_type
        self.data = data
        self.part = part
        self.total_parts = total_parts
        self.version = version
        self.comment = comment
        self.message_id = message_id
        self.hash_algorithms = hash_algorithms
        self.charset = charset
        self.extra_headers = extra_headers

    def __str__(self):
        result_lines = []
        if self.data_type != PGP_MESSAGE:
            result_lines.append('{dashes}BEGIN {data_type}{dashes}'.format(dashes=DASHES, data_type=data_types[self.data_type]))
        elif self.data_type == PGP_MESSAGE:
            if self.part is not None and self.total_parts is not None:
                result_lines.append('{dashes}BEGIN {data_type}, PART {part}/{total_parts}{dashes}'.format(dashes=DASHES, data_type=data_types[self.data_type], part=self.part, total_parts=self.total_parts))
            else:
                if self.part is not None:
                    result_lines.append('{dashes}BEGIN {data_type}, PART {part}{dashes}'.format(dashes=DASHES, data_type=data_types[self.data_type], part=self.part))
                else:
                    result_lines.append('{dashes}BEGIN {data_type}{dashes}'.format(dashes=DASHES, data_type=data_types[self.data_type]))
        if self.version is not None:
            result_lines.append('Version: {version}'.format(version=self.version))
        if self.comment is not None:
            result_lines.append('Comment: {comment}'.format(comment=self.comment))
        if self.message_id is not None:
            result_lines.append('MessageID: {message_id}'.format(message_id=self.message_id))
        if self.hash_algorithms is not None:
            result_lines.append('Hash: {hash}'.format(hash=self.hash_algorithms))
        if self.charset is not None:
            result_lines.append('Charset: {charset}'.format(charset=self.charset))
        if self.extra_headers is not None:
            for k, v in self.extra_headers:
                result_lines.append('{0}: {1}'.format(k, v))

        result_lines.append('')
        encoded_data = b64encode(self.data).decode('us-ascii')
        data_lines = []
        for l in range(int(math.ceil(len(encoded_data) / 72.0))):
            data_lines.append(encoded_data[l * 72:l * 72 + 72])

        result_lines.extend(data_lines)
        checksum_value = crc24(self.data)
        checksum_bytes = bytearray([checksum_value >> i * 8 & 255 for i in (2, 1, 0)])
        checksum = b64encode(checksum_bytes).decode('us-ascii')
        result_lines.append('={0}'.format(checksum))
        result_lines.append(result_lines[0].replace('BEGIN', 'END'))
        return '\n'.join(result_lines) + '\n'

    def __bytes__(self):
        return self.data