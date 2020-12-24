# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/amd/work/pilot/pilotconfig/pilot/devices/i8.py
# Compiled at: 2020-01-31 07:28:31
# Size of source mod 2**32: 1260 bytes


def getDevice(model, module, compiler, helpers):
    return I8Device(model, module, compiler, helpers)


def toGPIO(this, items):
    return 'GPIO' + chr(items + 65)


def default_config():
    return {}


class I8Device:
    size = 1
    ctype = 'uint8_t'
    rusttype = 'u8'
    include = ['stm32f10x.h']
    init_source = ''
    dev_to_mem_source = ''
    mem_to_dev_source = ''
    mem_doc = []
    decl = {'c':{'name':'i8_t', 
      'decl':'typedef uint8_t i8_t;'}, 
     'rust':{'name':'u8', 
      'decl':''}}
    module = None
    model = None
    compiler = None
    helpers = None

    def __init__(self, model, module, compiler, helpers):
        self.size = 1
        self.module = module
        self.helpers = {**{'gpio': toGPIO}, **helpers}
        self.compiler = compiler
        self.model = model

    def compile(self):
        template = self.compiler.compile('// source for device {{device.name}}\n  {{#each device.hw.Inputs}}\n  BITBAND_SRAM(&plc_mem_devices.m{{../device.slot}}, {{IO}}) = BITBAND_PERI({{gpio GPIO}}_BASE + 8, {{Pin}});\n{{/each}}\n    ')
        self.dev_to_mem_source = template(self.module, self.helpers)
        self.mem_doc = [{'name':'i{}'.format(i),  'desc':'digital input {}'.format(i),  'byte':0,  'bit':i,  'datatype':'bool',  'read':True,  'write':False} for i in range(8)]