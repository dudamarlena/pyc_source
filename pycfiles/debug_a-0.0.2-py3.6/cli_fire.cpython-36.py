# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\debug_a\cli_fire.py
# Compiled at: 2018-06-02 23:42:01
# Size of source mod 2**32: 943 bytes
import fire

def print_rules(explain=False):
    """rules | 打印股市交易纪律"""
    from debug_a import print_constitutions
    print_constitutions(explain)


def sm_price_section_monitor(code, low, high):
    """sm_price_section_monitor | 监控单只股票的价格区间"""
    from debug_a.monitor.single_monitor import price_section_monitor
    price_section_monitor((str(code)), (float(low)), (float(high)), max_nums=3)


def env_status():
    """env_status | 获取当前的市场涨跌情况"""
    from debug_a.monitor.env_monitor import get_env_status
    get_env_status()


def main():
    cli = {'rules':print_rules, 
     'psc':sm_price_section_monitor, 
     'env':env_status}
    fire.Fire(cli)


if __name__ == '__main__':
    main()