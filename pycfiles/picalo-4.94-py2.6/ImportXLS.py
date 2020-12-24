# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/picalo/lib/pyExcelerator/ImportXLS.py
# Compiled at: 2008-03-17 12:58:00
__rev_id__ = '$Id: ImportXLS.py,v 1.6 2005/10/26 07:44:24 rvk Exp $'
import UnicodeUtils, CompoundDoc, ExcelMagic
from struct import pack, unpack

def parse_xls(filename, encoding=None):

    def process_BOUNDSHEET(biff8, rec_data):
        (sheet_stream_pos, visibility, sheet_type) = unpack('<I2B', rec_data[:6])
        sheet_name = rec_data[6:]
        if biff8:
            (chars_num, options) = unpack('2B', sheet_name[:2])
            chars_start = 2
            runs_num = 0
            asian_phonetic_size = 0
            result = ''
            compressed = options & 1 == 0
            has_asian_phonetic = options & 4 != 0
            has_format_runs = options & 8 != 0
            if has_format_runs:
                (runs_num,) = unpack('<H', sheet_name[chars_start:chars_start + 2])
                chars_start += 2
            if has_asian_phonetic:
                (asian_phonetic_size,) = unpack('<I', sheet_name[chars_start:chars_start + 4])
                chars_start += 4
            if compressed:
                chars_end = chars_start + chars_num
                result = sheet_name[chars_start:chars_end].decode('latin_1', 'replace')
            else:
                chars_end = chars_start + 2 * chars_num
                result = sheet_name[chars_start:chars_end].decode('utf_16_le', 'replace')
            tail_size = 4 * runs_num + asian_phonetic_size
        else:
            result = sheet_name[1:].decode(encoding, 'replace')
        return result

    def unpack2str(biff8, label_name):
        if biff8:
            (chars_num, options) = unpack('<HB', label_name[:3])
            chars_start = 3
            runs_num = 0
            asian_phonetic_size = 0
            result = ''
            compressed = options & 1 == 0
            has_asian_phonetic = options & 4 != 0
            has_format_runs = options & 8 != 0
            if has_format_runs:
                (runs_num,) = unpack('<H', label_name[chars_start:chars_start + 2])
                chars_start += 2
            if has_asian_phonetic:
                (asian_phonetic_size,) = unpack('<I', label_name[chars_start:chars_start + 4])
                chars_start += 4
            if compressed:
                chars_end = chars_start + chars_num
                result = label_name[chars_start:chars_end].decode('latin_1', 'replace')
            else:
                chars_end = chars_start + 2 * chars_num
                result = label_name[chars_start:chars_end].decode('utf_16_le', 'replace')
            tail_size = 4 * runs_num + asian_phonetic_size
        else:
            result = label_name[2:].decode(encoding, 'replace')
        return result

    def process_LABEL(biff8, rec_data):
        (row_idx, col_idx, xf_idx) = unpack('<3H', rec_data[:6])
        label_name = rec_data[6:]
        result = unpack2str(biff8, label_name)
        return (row_idx, col_idx, result)

    def process_LABELSST(rec_data):
        (row_idx, col_idx, xf_idx, sst_idx) = unpack('<3HI', rec_data)
        return (row_idx, col_idx, sst_idx)

    def process_RSTRING(biff8, rec_data):
        if biff8:
            return process_LABEL(biff8, rec_data)
        (row_idx, col_idx, xf_idx, length) = unpack('<4H', rec_data[:8])
        result = rec_data[8:8 + length].decode(encoding, 'replace')
        return (
         row_idx, col_idx, result)

    def decode_rk(encoded):
        (b0, b1, b2, b3) = unpack('4B', encoded)
        is_multed_100 = b0 & 1 != 0
        is_integer = b0 & 2 != 0
        if is_integer:
            (result,) = unpack('<i', encoded)
            result >>= 2
        else:
            ieee754 = struct.pack('8B', 0, 0, 0, 0, b0 & 252, b1, b2, b3)
            (result,) = unpack('<d', ieee754)
        if is_multed_100:
            result /= 100.0
        return result

    def process_RK(rec_data):
        (row_idx, col_idx, xf_idx, encoded) = unpack('<3H4s', rec_data)
        result = decode_rk(encoded)
        return (row_idx, col_idx, result)

    def process_MULRK(rec_data):
        (row_idx, first_col_idx) = unpack('<2H', rec_data[:4])
        (last_col_idx,) = unpack('<H', rec_data[-2:])
        xf_rk_num = last_col_idx - first_col_idx + 1
        results = []
        for i in range(xf_rk_num):
            (xf_idx, encoded) = unpack('<H4s', rec_data[4 + 6 * i:4 + 6 * (i + 1)])
            results.append(decode_rk(encoded))

        return zip([row_idx] * xf_rk_num, range(first_col_idx, last_col_idx + 1), results)

    def process_NUMBER(rec_data):
        (row_idx, col_idx, xf_idx, result) = unpack('<3Hd', rec_data)
        return (row_idx, col_idx, result)

    def process_SST(rec_data, sst_continues):
        (total_refs, total_str) = unpack('<2I', rec_data[:8])
        pos = 8
        curr_block = rec_data
        curr_block_num = -1
        curr_str_num = 0
        SST = {}
        while curr_str_num < total_str:
            if pos >= len(curr_block):
                curr_block_num += 1
                curr_block = sst_continues[curr_block_num]
                pos = 0
            (chars_num, options) = unpack('<HB', curr_block[pos:pos + 3])
            pos += 3
            asian_phonetic_size = 0
            runs_num = 0
            has_asian_phonetic = options & 4 != 0
            has_format_runs = options & 8 != 0
            if has_format_runs:
                (runs_num,) = unpack('<H', curr_block[pos:pos + 2])
                pos += 2
            if has_asian_phonetic:
                (asian_phonetic_size,) = unpack('<I', curr_block[pos:pos + 4])
                pos += 4
            curr_char = 0
            result = ''
            while curr_char < chars_num:
                if pos >= len(curr_block):
                    curr_block_num += 1
                    curr_block = sst_continues[curr_block_num]
                    options = ord(curr_block[0])
                    pos = 1
                compressed = options & 1 == 0
                if compressed:
                    chars_end = pos + chars_num - curr_char
                else:
                    chars_end = pos + 2 * (chars_num - curr_char)
                splitted = chars_end > len(curr_block)
                if splitted:
                    chars_end = len(curr_block)
                if compressed:
                    result += curr_block[pos:chars_end].decode('latin_1', 'replace')
                else:
                    result += curr_block[pos:chars_end].decode('utf_16_le', 'replace')
                pos = chars_end
                curr_char = len(result)

            tail_size = 4 * runs_num + asian_phonetic_size
            if len(curr_block) < pos + tail_size:
                pos = pos + tail_size - len(curr_block)
                curr_block_num += 1
                curr_block = sst_continues[curr_block_num]
            else:
                pos += tail_size
            SST[curr_str_num] = result
            curr_str_num += 1

        return SST

    import struct
    encodings = {367: 'ascii', 
       437: 'cp437', 
       720: 'cp720', 
       737: 'cp737', 
       775: 'cp775', 
       850: 'cp850', 
       852: 'cp852', 
       855: 'cp855', 
       857: 'cp857', 
       858: 'cp858', 
       860: 'cp860', 
       861: 'cp861', 
       862: 'cp862', 
       863: 'cp863', 
       864: 'cp864', 
       865: 'cp865', 
       866: 'cp866', 
       869: 'cp869', 
       874: 'cp874', 
       932: 'cp932', 
       936: 'cp936', 
       949: 'cp949', 
       950: 'cp950', 
       1200: 'utf_16_le', 
       1250: 'cp1250', 
       1251: 'cp1251', 
       1252: 'cp1252', 
       1253: 'cp1253', 
       1254: 'cp1254', 
       1255: 'cp1255', 
       1256: 'cp1256', 
       1257: 'cp1257', 
       1258: 'cp1258', 
       1361: 'cp1361', 
       10000: 'mac_roman', 
       32768: 'mac_roman', 
       32769: 'cp1252'}
    biff8 = True
    SST = {}
    sheets = []
    sheet_names = []
    values = {}
    ws_num = 0
    BOFs = 0
    EOFs = 0
    ole_streams = CompoundDoc.Reader(filename).STREAMS
    if 'Workbook' in ole_streams:
        workbook_stream = ole_streams['Workbook']
    elif 'Book' in ole_streams:
        workbook_stream = ole_streams['Book']
    else:
        raise Exception, 'No workbook stream in file.'
    workbook_stream_len = len(workbook_stream)
    stream_pos = 0
    while stream_pos < workbook_stream_len and EOFs <= ws_num:
        (rec_id, data_size) = unpack('<2H', workbook_stream[stream_pos:stream_pos + 4])
        stream_pos += 4
        rec_data = workbook_stream[stream_pos:stream_pos + data_size]
        stream_pos += data_size
        if rec_id == 2057:
            BOFs += 1
            (ver, substream_type) = unpack('<2H', rec_data[:4])
            if substream_type == 5:
                biff8 = ver >= 1536
            elif substream_type == 16:
                pass
            else:
                (rec_id, data_size) = unpack('<2H', workbook_stream[stream_pos:stream_pos + 4])
                while rec_id != 10:
                    stream_pos += 4
                    stream_pos += data_size
                    (rec_id, data_size) = unpack('<2H', workbook_stream[stream_pos:stream_pos + 4])

        elif rec_id == 10:
            if BOFs > 1:
                sheets.extend([values])
                values = {}
            EOFs += 1
        elif rec_id == 66:
            (cp,) = unpack('<H', rec_data)
            if not encoding:
                encoding = encodings[cp]
        elif rec_id == 133:
            ws_num += 1
            b = process_BOUNDSHEET(biff8, rec_data)
            sheet_names.extend([b])
        elif rec_id == 252:
            sst_data = rec_data
            sst_continues = []
            (rec_id, data_size) = unpack('<2H', workbook_stream[stream_pos:stream_pos + 4])
            while rec_id == 60:
                stream_pos += 4
                rec_data = workbook_stream[stream_pos:stream_pos + data_size]
                sst_continues.extend([rec_data])
                stream_pos += data_size
                (rec_id, data_size) = unpack('<2H', workbook_stream[stream_pos:stream_pos + 4])

            SST = process_SST(sst_data, sst_continues)
        elif rec_id == 253:
            (r, c, i) = process_LABELSST(rec_data)
            values[(r, c)] = SST[i]
        elif rec_id == 516:
            (r, c, b) = process_LABEL(biff8, rec_data)
            values[(r, c)] = b
        elif rec_id == 214:
            (r, c, b) = process_RSTRING(biff8, rec_data)
            values[(r, c)] = b
        elif rec_id == 638:
            (r, c, b) = process_RK(rec_data)
            values[(r, c)] = b
        elif rec_id == 189:
            for (r, c, b) in process_MULRK(rec_data):
                values[(r, c)] = b

        elif rec_id == 515:
            (r, c, b) = process_NUMBER(rec_data)
            values[(r, c)] = b
        elif rec_id == 6:
            (r, c, x) = unpack('<3H', rec_data[0:6])
            if rec_data[12] == b'\xff' and rec_data[13] == b'\xff':
                if rec_data[6] == '\x00':
                    got_str = False
                    if ord(rec_data[14]) & 8:
                        (rec_id, data_size) = unpack('<2H', workbook_stream[stream_pos:stream_pos + 4])
                        stream_pos += 4
                        rec_data = workbook_stream[stream_pos:stream_pos + data_size]
                        stream_pos += data_size
                        if rec_id == 519:
                            got_str = True
                        elif rec_id not in (545, 1212, 566, 55, 54):
                            raise Exception('Expected ARRAY, SHRFMLA, TABLEOP* or STRING record')
                    if not got_str:
                        (rec_id, data_size) = unpack('<2H', workbook_stream[stream_pos:stream_pos + 4])
                        stream_pos += 4
                        rec_data = workbook_stream[stream_pos:stream_pos + data_size]
                        stream_pos += data_size
                        if rec_id != 519:
                            raise Exception('Expected STRING record')
                    values[(r, c)] = unpack2str(biff8, rec_data)
                elif rec_data[6] == '\x01':
                    v = ord(rec_data[8])
                    values[(r, c)] = bool(v)
                elif rec_data[6] == '\x02':
                    v = ord(rec_data[8])
                    if v in ExcelMagic.error_msg_by_code:
                        values[(r, c)] = ExcelMagic.error_msg_by_code[v]
                    else:
                        values[(r, c)] = '#UNKNOWN ERROR!'
                elif rec_data[6] == '\x03':
                    values[(r, c)] = ''
                else:
                    raise Exception('Unknown value for formula result')
            else:
                (d,) = unpack('<d', rec_data[6:14])
                values[(r, c)] = d

    encoding = None
    return zip(sheet_names, sheets)