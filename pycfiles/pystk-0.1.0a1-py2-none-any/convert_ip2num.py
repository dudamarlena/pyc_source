# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pystk/convert_ip2num.py
# Compiled at: 2018-06-22 06:33:55
import argparse, logging, os
from config import output_log
output_log.init_log('./log/converter')

def convert_to_num(ip_address):
    """Convert ip into number.

    Convert ip address into 32-bit integer number.

    :param ip_address: The ip address, eg. 127.125.5.1.

    :return: The 32-bit number converted from ip address.
    """
    number = 0
    part_num = 0
    part_str = ''
    for i in xrange(len(ip_address)):
        num = len(ip_address) - i - 1
        if ip_address[num] == '.' or num == 0:
            if num == 0:
                part_str = ip_address[num] + part_str
            if len(part_str.strip()) > 4:
                logging.error('The ip address %s has wrong length in some parts.\n' % ip_address)
                return 'Error'
            try:
                number = number + int(part_str.strip()) * 2 ** (part_num * 8)
            except ValueError as e:
                logging.error('The ip address %s is in error: %s.\n' % (ip_address, str(e)))
                return 'Error'

            if int(part_str.strip()) > 255 or int(part_str.strip()) < 0:
                logging.error('The ip address %s has abnormal number out of bound 0~255.\n' % ip_address)
                return 'Error'
            part_num += 1
            part_str = ''
        else:
            part_str = ip_address[num] + part_str

    if part_num != 4:
        logging.error('The ip address %s is in wrong length.\n' % ip_address)
        return 'Error'
    return number


def main():
    """The main function to convert ip address into 32-bit integer.

    :return: Save result into text file.
    """
    parser = argparse.ArgumentParser(description='This is script to convert ip address into integer.')
    parser.add_argument('-f', required=True, help='The file which saves ip addresses.')
    args = parser.parse_args()
    file_name = args.f
    ip_list = []
    try:
        with open(file_name, 'r') as (f):
            for line in f.readlines():
                ip_list.append(line.strip())

    except IOError as e:
        logging.error('Not found the input file with error info: %s.\n' % str(e))
        return 1

    file_path = 'result/ip_num_result.txt'
    directory = os.path.dirname(file_path)
    try:
        os.stat(directory)
    except OSError as e:
        logging.error('Not found the input directory with error info: %s.\n' % str(e))
        os.mkdir(directory)

    with open(file_path, 'w') as (f):
        for ip in ip_list:
            num = convert_to_num(ip)
            f.writelines(str(ip) + ' : ' + str(num) + '\n')


if __name__ == '__main__':
    main()