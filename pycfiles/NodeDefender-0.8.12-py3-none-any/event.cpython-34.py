# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/icpe/event.py
# Compiled at: 2018-01-09 06:06:44
# Size of source mod 2**32: 2630 bytes
import NodeDefender

def system_status(mac_address, payload):
    operation, status = payload['stat'].split(',')
    if operation == '0' and status == '0':
        pass
    else:
        if operation == '1' and status == '0':
            pass
        else:
            if operation == '2' and status == '0':
                pass
            else:
                if operation == '3':
                    if status == '0':
                        NodeDefender.mqtt.command.icpe.zwave.node.list(mac_address)
                else:
                    if operation == '4' and status == '0':
                        pass
                    else:
                        if operation == '5':
                            if status == '0':
                                NodeDefender.mqtt.command.icpe.zwave.node.list(mac_address)
                        else:
                            if operation == '6' and status == '0':
                                pass
                            else:
                                if operation == '7' and status == '0':
                                    pass
                                else:
                                    if operation == '8' and status == '0':
                                        pass
                                    else:
                                        if operation == '9' and status == '0':
                                            pass
                                        else:
                                            if operation == '10' and status == '0':
                                                pass
                                            else:
                                                if operation == '11' and status == '0':
                                                    pass
                                                else:
                                                    if operation == '13' and status == '0':
                                                        pass
                                                    else:
                                                        if operation == '14' and status == '0':
                                                            pass
                                                        else:
                                                            if operation == '15' and status == '0':
                                                                pass
                                                            else:
                                                                if operation == '50' and status == '0':
                                                                    pass
                                                                elif operation == '51' and status == '0':
                                                                    pass
                home_id = payload['netid']
                controller_id = payload['controllerid']
                automatic_polling = bool(eval(payload['aopoll']))
                always_reporting = bool(eval(payload['awrpt']))
                general_wakeup = payload['acwkup']
                forward_unsolicited = bool(eval(payload['unsolicit']))
                auto_isolate = bool(eval(payload['autoisolate']))
                battery_warning = bool(eval(payload['bnlevel']))
                health_check_interval = payload['hcinterval']
                NodeDefender.db.icpe.update_redis(mac_address, home_id=home_id, controller_id=controller_id, automatic_polling=automatic_polling, always_reporting=always_reporting, general_wakeup=general_wakeup, forward_unsolicited=forward_unsolicited, auto_isolate=auto_isolate, battery_warning=battery_warning, health_check_interval=health_check_interval)
    return True