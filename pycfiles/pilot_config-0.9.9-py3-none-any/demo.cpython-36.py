# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/amd/work/pilot/pilotconfig/pilot/devices/demo.py
# Compiled at: 2020-04-19 11:27:53
# Size of source mod 2**32: 1796 bytes


def getDevice(model, module, compiler, helpers):
    return O8Device(model, module, compiler, helpers)


def toGPIO(this, items):
    return 'GPIO' + chr(items + 65)


def default_config():
    return {}


class O8Device:
    size = 1
    ctype = 'uint8_t'
    rusttype = 'u8'
    length = 1
    include = ['stm32f10x.h']
    init_source = ''
    dev_to_mem_source = ''
    mem_to_dev_source = ''
    mem_doc = []
    decl = {'c':{'name':'o8_t', 
      'decl':'typedef uint8_t o8_t;'}, 
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
        inputs_template = self.compiler.compile('// input source for device {{device.name}}\n  {{#each device.hw.Inputs}}\n  BITBAND_SRAM(&plc_mem_devices.m{{../device.slot}}, {{IO}}) = BITBAND_PERI({{gpio GPIO}}_BASE + 8, {{Pin}});\n{{/each}}\n    ')
        outputs_template = self.compiler.compile('// output source for device {{device.name}}\n  {{#each device.hw.Outputs}}\n  GPIO_OUT_SET({{gpio GPIO}}_BASE, {{Pin}}, BITBAND_SRAM(&plc_mem_devices.m{{../device.slot}}, {{IO}}));\n{{/each}}\n    ')
        self.dev_to_mem_source = inputs_template(self.module, self.helpers)
        self.mem_to_dev_source = outputs_template(self.module, self.helpers)
        self.mem_doc = [{'name':'i{}'.format(i),  'desc':'digital input {}'.format(i),  'byte':0,  'bit':i,  'datatype':'bool',  'read':True,  'write':False} for i in range(4)]
        self.mem_doc.append([{'name':'o{}'.format(i),  'desc':'digital output {}'.format(i),  'byte':0,  'bit':i,  'datatype':'bool',  'write':True,  'read':False} for i in range(4)])