# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/emulator/functions.py
# Compiled at: 2018-09-18 06:58:30
"""
Created on Mon Apr 30 16:10:55 2018

@author: ashraya
"""
import os, json, time, uuid, random
log_file = 'log.log'
DEBUG = True

def Log(log):
    if DEBUG == True:
        with open(log_file, 'a') as (logFp):
            logFp.write(log + '\n')


def serv_topic(service, address, resource_name):
    return ('/rt:dev/rn:{}/ad:1/sv:{}/ad:{}_0').format(resource_name, service, address)


def get_services(name):
    switch = {'binary': 'binary', 'red': 'color_ctrl', 'blue': 'color_ctrl', 'green': 'color_ctrl', 'kWh': 'meter_elec', 'W': 'meter_elec', 'A': 'meter_elec', 'V': 'meter_elec'}
    strip = {'battery': 'battery', 'temper_invalid_code': 'alarm_burglar', 'sensor_contact': 'sensor_contact'}
    plug = {}
    light = {'warm_w': 'color_ctrl', 'cold_w': 'color_ctrl', 'red': 'color_ctrl', 'blue': 'color_ctrl', 'green': 'color_ctrl'}
    thermostat = {}
    motion = {}
    multi = {'battery': 'battery', 'sensor_presence': 'sensor_presence', 'temper_removed_cover': 'alarm_burglar', 'C': 'sensor_temp', 'F': 'sensor_temp', 'Lux': 'sensor_lumin', '%': 'sensor_humid', 'index': 'sensor_uv'}
    dimmer = {'battery': 'battery', 'overheat': 'alarm_heat', 'surge': 'alarm_power', 'voltage_drop': 'alarm_power', 'over_current': 'alarm_power', 'load_error': 'alarm_power', 'hw_failure': 'alarm_system', 
       'W': 'sensor_power'}
    flood = {'battery': 'battery', 'leak': 'alarm_water', 'gp': 'alarm_gp', 'C': 'sensor_temp'}
    window = {}
    lock = {'battery': 'battery', 'door_is_closed': 'door_lock', 'rf_not_locked': 'alarm_lock', 'sensor_presence': 'sensor_presence'}
    climax = {'battery': 'battery', 'temper_removed_cover': 'alarm_burglar', 'ac_on': 'alarm_power', 'ac_off': 'alarm_power', 
       'overheat': 'alarm_heat', 'CO': 'alarm_gas', 'smoke': 'alarm_fire', 
       'smoke_test': 'alarm_fire', 'C': 'sensor_temp', '%': 'sensor_humid', 'on': 'siren_ctrl', 
       'off': 'siren_ctrl', 'heat': 'siren_ctrl', 'smoke_on': 'siren_ctrl', 'CO_on': 'siren_ctrl'}
    alarm = {'battery': 'battery', 'temper_removed_cover': 'alarm_burglar', 'ac_on': 'alarm_power', 'ac_off': 'alarm_power', 'overheat': 'alarm_heat', 'CO': 'alarm_gas', 'smoke': 'alarm_fire', 
       'smoke_test': 'alarm_fire'}
    serv_dict = {'switch': switch, 'plug': plug, 
       'light': light, 
       'thermostat': thermostat, 
       'alarm': alarm, 
       'motion': motion, 
       'multi': multi, 
       'dimmer': dimmer, 
       'flood': flood, 
       'window': window, 
       'lock': lock, 
       'climax': climax, 
       'strip': strip}
    return serv_dict[name]


def color_map(color):
    if color == 'red':
        return {'red': 200}
    if color == 'blue':
        return {'blue': 100}
    if color == 'green':
        return {'green': 45}
    if color == 'cold_w':
        return {'cold_w': random.randint(0, 255)}
    if color == 'warm_w':
        return {'warm_w': random.randint(0, 255)}


def battery_map(state):
    Log('battery_map : ' + str(state))
    s_value = 0
    s_value2 = {}
    if state == 'full':
        s_value = 100
        return s_value
    else:
        if state == 'half':
            s_value = 50
            return s_value
        if state == 'low':
            s_value2 = {'event': 'low_battery', 'status': 'activ'}
            return s_value2
        if state == 'dead':
            s_value2 = {'event': 'low_battery', 'status': 'inactiv'}
            return s_value2
        return 'Error'


def dump_inclusion_report(req, address=1):
    req['serv'] = 'emul'
    req['val']['address'] = address
    req['val']['comm_tech'] = 'emul'
    for ad in req['val']['services']:
        ad['address'] = ad['address'][:ad['address'].rfind(':') + 1] + address + '_0'
        ad['address'] = ad['address'].replace('zw', 'emul')

    Log('dump_inclusion_report : services : ' + str(req['val']['services']))
    return req


def dump_exclusion_report(address='1', service='emul'):
    return {'ctime': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 
       'props': {}, 'serv': service, 
       'tags': [], 'type': 'evt.thing.exclusion_report', 
       'val': {'address': str(address)}, 'val_t': 'object', 
       'uid': str(uuid.uuid4())}


def dump_trigger_report(device, address, event, status, service, s_value=''):
    if event == 'state':
        value = 'dev_sys'
        topic = ('pt:j1/mt:evt/rt:dev/rn:{}/ad:1/sv:{}/ad:{}_0').format(service, value, address)
        if status == 'true':
            status = 'UP'
        else:
            status = 'DOWN'
        return (
         topic,
         {'ctime': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 
            'props': {}, 'serv': value, 
            'tags': [], 'type': 'evt.state.report', 
            'val': status, 
            'val_t': 'string', 
            'ver': 1, 
            'uid': str(uuid.uuid4())})
    if event == 'ping':
        topic = ('pt:j1/mt:evt/rt:ad/rn:{}/ad:1').format(service)
        if status == 'true':
            status = 'SUCCESS'
        else:
            status = 'FAILED'
        return (
         topic,
         {'ctime': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 
            'props': {}, 'serv': service, 
            'tags': [], 'type': 'evt.' + event + '.report', 
            'val': {'address': address, 
                    'status': status}, 
            'val_t': 'str_map', 
            'ver': 1, 
            'uid': str(uuid.uuid4())})
    svcs_dict = get_services(device)
    Log('dump_trigger_report: key : ' + event)
    topic = ''
    try:
        if event == 'full' or event == 'half' or event == 'low' or event == 'dead':
            value = 'alarm_battery'
            topic = ('pt:j1/mt:evt/rt:dev/rn:{}/ad:1/sv:{}/ad:{}_0').format(service, 'battery', address)
        else:
            value = svcs_dict[event]
    except KeyError:
        Log('dump_trigger_report: KeyError! : ' + str(event))
        return ('', {})

    if topic == '':
        topic = ('pt:j1/mt:evt/rt:dev/rn:{}/ad:1/sv:{}/ad:{}_0').format(service, value, address)
    st = ''
    if status == True:
        st = 'activ'
    else:
        st = 'inactiv'
    if value.find('lock') > -1:
        return (
         topic,
         {'ctime': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 
            'props': {}, 'serv': value, 
            'tags': [], 'type': 'evt.' + value[:value.find('_')] + '.report', 
            'val': {'event': event, 
                    'status': st}, 
            'val_t': 'bool_map', 
            'ver': 1, 
            'uid': str(uuid.uuid4())})
    if value.find('battery') > -1:
        Log('dump_trigger_report : in battery : ' + str(s_value))
        s_value = battery_map(event)
        Log('dump_trigger_report : in battery : ' + str(s_value))
        if isinstance(s_value, int):
            return (
             topic,
             {'ctime': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 
                'props': {}, 'serv': 'battery', 
                'tags': [], 'type': 'evt.lvl.report', 
                'val': s_value, 
                'val_t': 'int', 
                'ver': 1, 
                'uid': str(uuid.uuid4())})
        return (
         topic,
         {'ctime': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 
            'props': {}, 'serv': 'battery', 
            'tags': [], 'type': 'evt.' + value[:value.find('_')] + '.report', 
            'val': s_value, 
            'val_t': 'str_map', 
            'ver': 1, 
            'uid': str(uuid.uuid4())})
    else:
        if value.find('siren') > -1:
            if event.find('smoke') > -1 or event.find('CO') > -1:
                event = event[:event.find('_')]
            return (
             topic,
             {'ctime': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 
                'props': {}, 'serv': value, 
                'tags': [], 'type': 'evt.mode.report', 
                'val': event, 
                'val_t': 'string', 
                'ver': 1, 
                'uid': str(uuid.uuid4())})
        if value.find('color') > -1:
            return (
             topic,
             {'ctime': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 
                'props': {}, 'serv': value, 
                'tags': [], 'type': 'evt.' + value[:value.find('_')] + '.report', 
                'val': color_map(event), 
                'val_t': 'int_map', 
                'ver': 1, 
                'uid': str(uuid.uuid4())})
        if s_value == '':
            value2 = ''
            if value == 'sensor_contact':
                value2 = 'evt.open.report'
            else:
                value2 = 'evt.' + value[:value.find('_')] + '.report'
            if value.find('sensor') > -1:
                return (
                 topic,
                 {'ctime': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 
                    'props': {}, 'serv': value, 
                    'tags': [], 'type': value2, 
                    'val': status, 
                    'val_t': 'bool', 
                    'ver': 1, 
                    'uid': str(uuid.uuid4())})
            return (
             topic,
             {'ctime': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 
                'props': {}, 'serv': value, 
                'tags': [], 'type': value2, 
                'val': {'event': event, 
                        'status': st}, 
                'val_t': 'str_map', 
                'ver': 1, 
                'uid': str(uuid.uuid4())})
        elif value.find('sensor') > -1 or value.find('meter') > -1:
            return (
             topic,
             {'ctime': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 
                'props': {'unit': event}, 'serv': value, 
                'tags': [], 'type': 'evt.' + value[:value.find('_')] + '.report', 
                'val': float(s_value), 
                'val_t': 'float', 
                'ver': 1, 
                'uid': str(uuid.uuid4())})


def Log_mqtt(topic, payload):
    Log('Topic:' + topic)
    formatted = json.dumps(payload, sort_keys=True, indent=4, separators=(',', ': '))
    try:
        from pygments import highlight, lexers, formatters
        Log(highlight(formatted, lexers.JsonLexer(), formatters.TerminalFormatter()))
    except:
        Log(formatted)


def generate_inclusion_report(req, address):
    Log('generate_inclusion_report : address : ' + address)
    topic = ('pt:j1/mt:evt/rt:ad/rn:{}/ad:{}_0').format('emul', address)
    report = dump_inclusion_report(req, address)
    return (
     topic, report)


def generate_exclusion_report(address):
    Log('generate_exclusion_report : address : ' + address)
    topic = ('pt:j1/mt:evt/rt:ad/rn:{}/ad:1').format('emul')
    report = dump_exclusion_report(address)
    return (
     topic, report)


def generate_trigger_report(event, address, device, status, value=''):
    triggers = []
    topic, report = dump_trigger_report(device, address, event, status, 'emul', value)
    if topic == '':
        return ('', {})
    triggers.append(report)
    return (
     topic, report)


def generate_alive_messages(device):
    Log('generate_alive_messages : ' + str(device))
    topic = ('pt:j1/mt:evt/rt:dev/rn:{}/ad:1/sv:{}/ad:{}_0').format('emul', 'battery', device['id'])
    state = battery_map(device['battery'])
    if isinstance(state, int):
        return (
         topic,
         {'ctime': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 
            'props': {}, 'serv': 'battery', 
            'tags': [], 'type': 'evt.lvl.report', 
            'val': state, 
            'val_t': 'int', 
            'ver': 1, 
            'uid': str(uuid.uuid4())})
    else:
        return (topic,
         {'ctime': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 
            'props': {}, 'serv': 'battery', 
            'tags': [], 'type': 'evt.alarm.report', 
            'val': state, 
            'val_t': 'str_map', 
            'ver': 1, 
            'uid': str(uuid.uuid4())})