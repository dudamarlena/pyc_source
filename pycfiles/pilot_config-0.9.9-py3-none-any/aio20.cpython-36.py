# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/amd/work/pilot/pilotconfig/pilot/devices/aio20.py
# Compiled at: 2020-01-31 13:02:03
# Size of source mod 2**32: 1799 bytes


def getDevice(model, module, compiler, helpers):
    return I8Device(model, module, compiler, helpers)


def toGPIO(this, items):
    return 'GPIO' + chr(items + 65)


def default_config():
    return {}


class I8Device:
    size = 1
    ctype = 'uint16_t[16]'
    rusttype = 'u8'
    include = ['aio20.h']
    init_source = ''
    dev_to_mem_source = ''
    mem_to_dev_source = ''
    mem_doc = []
    decl = {'c':{'name':'aio20_t', 
      'decl':'typedef struct { \n  uint16_t aio1;\n  uint16_t aio0;\n  uint16_t aio3;\n  uint16_t aio2;\n  uint16_t r1;\n  uint16_t aio5;\n  uint16_t aio4;\n  uint16_t r2;\n  uint16_t aio7;\n  uint16_t aio6;\n  uint16_t aio9;\n  uint16_t aio8;\n  uint16_t r3;\n  uint16_t aio11;\n  uint16_t aio10;\n  uint16_t aio13;\n  uint16_t aio12;\n  uint16_t r4;\n  uint16_t aio14;\n  uint16_t aio15;\n} aio20_t;'}, 
     'rust':{'name':'Aio20', 
      'decl':'#[repr(C)]\npub struct Aio20 { \n  pub aio1: u16,\n  pub aio0: u16,\n  pub aio3: u16,\n  pub aio2: u16,\n  r1: u16,\n  pub aio5: u16,\n  pub aio4: u16,\n  r2: u16,\n  pub aio7: u16,\n  pub aio6: u16,\n  pub aio9: u16,\n  pub aio8: u16,\n  r3: u16,\n  pub aio11: u16,\n  pub aio10: u16,\n  pub aio13: u16,\n  pub aio12: u16,\n  r4: u16,\n  pub aio14: u16,\n  pub aio15: u16,\n}'}}
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
        dev_to_mem_str = '// source for device {{device.name}}\n  single_ended_adc_read_all({{device.index}}, (uint8_t *) &plc_mem_devices.m{{device.slot}}); \n  '
        dev_to_mem_template = self.compiler.compile(dev_to_mem_str)
        self.dev_to_mem_source = dev_to_mem_template(self.module, self.helpers)