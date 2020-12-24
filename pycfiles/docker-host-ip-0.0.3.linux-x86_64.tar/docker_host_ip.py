# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/docker_host_ip.py
# Compiled at: 2017-01-03 06:15:25
import logging, os, re

def get_ip_within_host():
    cmd = os.popen('/sbin/ip')
    returns = cmd.readall()
    regex = '/default via ((?:[0-9]{1,3}\\.){3}[0-9]{1,3}) dev eth0/'
    return re.findall(regex, returns)


def _get_ifconfig(interface_name):
    cmd = os.popen('ifconfig %s' % interface_name)
    return cmd.read()


def get_docker_host_ip(iface_name='docker0'):
    """
    Only work while docker0 exists
    :return:
    """
    returns = _get_ifconfig(iface_name)
    regex = 'inet\\ addr:((\\d{1,3}\\.){1,3}\\d{1,3})'
    matched = re.findall(regex, returns)
    try:
        return matched[0][0]
    except IndexError:
        logging.exception("Failed to get docker0's ip address, check if it exists.")
        return

    return