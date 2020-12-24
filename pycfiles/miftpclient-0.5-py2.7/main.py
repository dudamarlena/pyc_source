# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/miftpclient/main.py
# Compiled at: 2015-09-05 02:50:21
import argparse, sys
from colorama import Fore, init
from ftpclient import connect_server
from ipparser import parse_ip
from scan import scan_miftp_ip, make_ip
init(autoreset=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='short_host', help='IP的最后一段,如107', type=int)
    parser.add_argument('-t', dest='timeout', help='超时时长', type=float)
    args = parser.parse_args()
    lan_ip = parse_ip()
    if not lan_ip:
        print Fore.RED + '\n[错误]没有找到内网IP.'
        sys.exit(0)
    if args.short_host:
        ftp_ip = make_ip(lan_ip, str(args.short_host))
    else:
        ftp_ips = scan_miftp_ip(lan_ip, args.timeout if args.timeout else 0.3)
        if not ftp_ips:
            print Fore.RED + '\n[错误]没有找到FTP, 请检查手机端是否开启FTP.'
            sys.exit(0)
        elif len(ftp_ips) == 1:
            ftp_ip = ftp_ips[0]
        else:
            print Fore.GREEN + '\n在您的子网内发现如下小米FTP:'
            for i, ip in enumerate(ftp_ips):
                print Fore.GREEN + '%s. %s' % (i, ip)

            try:
                index = input('请输入序号选择您想连接的FTP: ')
                ftp_ip = ftp_ips[int(index)]
            except (IndexError, ValueError, NameError):
                print Fore.RED + '[错误]错误的输入'
                sys.exit(0)

    connect_server(ftp_ip)
    print Fore.GREEN + '\nFTP(%s:2121)已经在firefox中打开, 请查看' % ftp_ip


if __name__ == '__main__':
    main()