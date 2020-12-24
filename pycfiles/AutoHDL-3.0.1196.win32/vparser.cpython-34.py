# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python34\Lib\site-packages\autohdl\verilog\vparser.py
# Compiled at: 2015-05-12 08:09:02
# Size of source mod 2**32: 6369 bytes
import re
regex_module_name_content = re.compile('module\\s*(?P<module_name>\\w+)\\s*.*?;(?P<module_contents>.*?)endmodule', flags=re.MULTILINE | re.S)

class Parser(object):
    __doc__ = '\n    input: preprocessed content (without comments)\n    output: dict\n      {module_name0: set(inst0, inst1, ...),\n       module_name1: set(inst0, inst2, ...),\n       ...,\n      }\n    '

    def __init__(self, data):
        self.input = data
        self.output = {}
        self.keywords = ['always', 'and', 'assign', 'automatic', 'begin', 'buf', 'bufif0', 'bufif1', 'case', 'casex',
         'casez', 'cell', 'cmos', 'config', 'deassign', 'default', 'defparam', 'design', 'disable',
         'edge', 'else', 'end', 'endcase', 'endconfig', 'endfunction', 'endgenerate', 'endmodule',
         'endprimitive', 'endspecify', 'endtable', 'endtask', 'event', 'for', 'force', 'forever',
         'fork', 'function', 'generate', 'genvar', 'highz0', 'highz1', 'if', 'ifnone', 'incdir',
         'include', 'initial', 'inout', 'input', 'instance', 'integer', 'join', 'large', 'liblist',
         'library', 'localparam', 'macromodule', 'medium', 'module', 'nand', 'negedge', 'nmos', 'nor',
         'noshowcancelled', 'not', 'notif0', 'notif1', 'or', 'output', 'parameter', 'pmos', 'posedge',
         'primitive', 'pull0', 'pull1', 'pulldown', 'pullup', 'pulsestyle_onevent',
         'pulsestyle_ondetect', 'rcmos', 'real', 'realtime', 'reg', 'release', 'repeat', 'rnmos',
         'rpmos', 'rtran', 'rtranif0', 'rtranif1', 'scalared', 'showcancelled', 'signed', 'small',
         'specify', 'specparam', 'strong0', 'strong1', 'supply0', 'supply1', 'table', 'task', 'time',
         'tran', 'tranif0', 'tranif1', 'tri', 'tri0', 'tri1', 'triand', 'trior', 'trireg', 'unsigned',
         'use', 'vectored', 'wait', 'wand', 'weak0', 'weak1', 'while', 'wire', 'wor', 'xnor', 'xor', 'string', 'int']

    def parse(self):
        for res in regex_module_name_content.finditer(self.input):
            self.module_name = res.group('module_name')
            self.output[self.module_name] = set()
            module_content = res.group('module_contents')
            self.get_instance_names(module_content)

        return self.output

    def get_instance_names(self, module_content):
        for i in module_content.split(';'):
            res = self.proc_client(i)
            if res:
                self.output[self.module_name].add(res)
                continue

    def proc_client(self, aline):
        aline = aline.strip()
        state = 'st_module_name'
        module_name = []
        inst_name = []
        ports = []
        params = []
        in_parentheses = 0
        for sym in aline:
            if state == 'st_module_name':
                if re.match('\\w', sym):
                    module_name.append(sym)
                else:
                    if re.match('[\\s\n]', sym):
                        state = 'st_wait_par_or_inst'
                    else:
                        if re.match('#', sym):
                            state = 'st_param'
                        else:
                            return
            elif state == 'st_wait_par_or_inst':
                if re.match('\\w', sym):
                    inst_name.append(sym)
                    state = 'st_inst_name'
                else:
                    if re.match('[\\s\n]', sym):
                        pass
                    else:
                        if re.match('#', sym):
                            state = 'st_param'
                        else:
                            return
            elif state == 'st_inst_name':
                if re.match('\\w', sym):
                    inst_name.append(sym)
                elif re.match('\\(', sym):
                    ports.append(sym)
                    state = 'st_ports'
            elif state == 'st_ports':
                ports.append(sym)
            elif state == 'st_param':
                if re.match('[\\s\n]', sym):
                    pass
                else:
                    if re.match('\\(', sym):
                        params.append(sym)
                        in_parentheses += 1
                    else:
                        if re.match('\\)', sym):
                            params.append(sym)
                            in_parentheses -= 1
                        else:
                            if re.match('\\w', sym):
                                if not in_parentheses:
                                    inst_name.append(sym)
                                    state = 'st_inst_name'
                                else:
                                    params.append(sym)
                            else:
                                continue

        instantiated_module = ''.join(module_name)
        inst_name = ''.join(inst_name)
        if instantiated_module in self.keywords:
            return
        return instantiated_module


if __name__ == '__main__':
    t = "\n`timescale 1ps / 1ps\nmodule dcs_packet_v2_tb;\n    parameter pDataWidth = 20;\n    parameter pBaud = 115200;\n\n    reg iClk;\n    reg iRst;\n    reg [pDataWidth-1:0]iData;\n    reg iEnStr;\n    wire oDoneStr;\n    wire oTxD;\n\n    dcs_packet_tx_v2 #(\n        .pDataWidth(pDataWidth),\n        .pBaud(pBaud),\n        .pStopBits(2))\n        tx (.iClk(iClk),\n        .iRst(iRst),\n        .iData(iData),\n        .iEnStr(iEnStr),\n        .oDoneStr(oDoneStr),\n        .oTxD(oTxD)\n        );\n\n\n    wire [pDataWidth-1:0] res;\n    wire doneRes;\n    dcs_packet_rx_v2 #(\n        .pDataWidth(pDataWidth),\n        .pBaud(pBaud),\n        .pStopBits(1)\n        ) rx (\n        .iClk(iClk),\n        .iRst(iRst),\n        .iRxD(oTxD),\n        .oData(res),\n        .oDoneStr(doneRes),\n        .oMaskErrStr(),\n        .oCrcErrStr()\n        );\n\n    initial begin\n            iClk <= 0;\n            forever #10ns iClk <= ~iClk;\n        end\n\n    initial begin\n            iRst <= 1;\n            #100ns iRst <= 0;\n            iData <= 20'haaaaa;\n            @(posedge iClk) iEnStr <= 1;\n            @(posedge iClk) iEnStr <= 0;\n        end\n\nendmodule\n\nmodule b; as sdsd(); endmodule\n\n"
    p = Parser(data=t)
    p.parse()
    print(p.output)