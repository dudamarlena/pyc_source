# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\IDE\Parse.py
# Compiled at: 2020-01-21 01:53:04
import sys, os
reload(sys)
sys.setdefaultencoding('utf8')
from CLogText import LogText
from PLC_IDE.lib.File import FSO
from PLC_IDE.lib.JsonClass import CJSON
from prettytable import PrettyTable
import CHelpBuilder, copy
BasicType = [
 'INT',
 'UINT',
 'WORD',
 'DINT',
 'UDINT',
 'DWORD',
 'FLOAT',
 'DOUBLE']
OFFSET1 = [
 2,
 2,
 2,
 4,
 4,
 4,
 4,
 8]
BasicTypeInfo = {'INT': 2, 
   'UINT': 2, 
   'WORD': 2, 
   'DINT': 4, 
   'UDINT': 4, 
   'DWORD': 4, 
   'FLOAT': 4, 
   'DOUBLE': 8}
HARDWARE_START_SLOT = 2
HARDWARE_VAR = 'CFG'
HARDWARE_VAR_DECLARE = 'extern _CFG CFG;'
Global_H = '\n//AUTO GENERATE\n#pragma once\n#ifndef __GLOBAL_H\n#define __GLOBAL_H\n#include <stdio.h>\n#include <rtdm/udd.h>\n\ntypedef int16_t INT;\ntypedef uint16_t UINT;\ntypedef uint16_t WORD;\ntypedef int32_t DINT;\ntypedef uint32_t UDINT;\ntypedef uint32_t DWORD;\ntypedef float FLOAT;\ntypedef double DOUBLE;\n\n[%CFG%]\n[%IODEF%]\n\n\n#endif // __GLOBAL_H\n'
ALLCLASS = {}
CLASSLIST = []

def Build(data, filepath):
    global ALLCLASS
    global CLASSLIST
    _dir = os.path.dirname(filepath)
    _file = os.path.basename(filepath)
    _hz = os.path.splitext(filepath)[1]
    _name = _file.replace(_hz, '')
    if os.path.exists(os.path.join(_dir, _name)):
        pass
    else:
        os.mkdir(os.path.join(_dir, _name))
    ALLCLASS, CLASSLIST = BuildAllClass(data['File'])
    struct_h = BuildStruct(data['File']['struct'])
    gvl_h = BuildGVL(data['File'])
    glv_member_init_c = BuildVariableInitC(data['File'])
    init_hardware, alias_hardware = BuildHardware(data['File']['hardware']['0'])
    task_h, task_cpp = BuildTask(data['File']['task'], glv_member_init_c, init_hardware)
    prgs = BuildPRGs(data['File']['program'])
    fcs = BuildFunctions(data['File']['function'])
    fso = FSO()
    fso.createfile(os.path.join(_dir, _name, '__struct.h'), struct_h)
    fso.createfile(os.path.join(_dir, _name, '__gvl.h'), gvl_h)
    fso.createfile(os.path.join(_dir, _name, '__global.h'), BuildGlobalH(alias_hardware))
    fso.createfile(os.path.join(_dir, _name, 'Task.h'), task_h)
    fso.createfile(os.path.join(_dir, _name, 'Task.cpp'), task_cpp)
    for p in prgs:
        name = p[0]
        h = p[1]
        cpp = p[2]
        fso.createfile(os.path.join(_dir, _name, '%s.h' % name), h)
        fso.createfile(os.path.join(_dir, _name, '%s.cpp' % name), cpp)

    fso.createfile(os.path.join(_dir, _name, '__function.h'), fcs)
    fbs = BuildFBs(data['File']['class'])
    for p in fbs:
        name = p[0]
        h = p[1]
        cpp = p[2]
        fso.createfile(os.path.join(_dir, _name, '%s.h' % name), h)
        fso.createfile(os.path.join(_dir, _name, '%s.cpp' % name), cpp)

    gvlVar = ExpandGvlVariable(data['File'])
    allvar, dcVar = AddrGvlVariable(gvlVar, 2, 1)
    dataDriver, dataVar = BuildScadaVariable(dcVar)
    objJSON = CJSON()
    objJSON.writefile(dataDriver, os.path.join(_dir, _name, 'SCADA', 'Device.config'))
    objJSON.writefile(dataVar, os.path.join(_dir, _name, 'SCADA', 'Variable.config'))
    LogText('Project Build OK!!')


def BuildGlobalH(iodef):
    global Global_H
    global HARDWARE_VAR_DECLARE
    h = Global_H.replace('[%CFG%]', HARDWARE_VAR_DECLARE)
    h = h.replace('[%IODEF%]', iodef)
    return h


def BuildProjectInfo(filepath):
    _dir = os.path.dirname(filepath)
    _file = os.path.basename(filepath)
    _hz = os.path.splitext(filepath)[1]
    _name = _file.replace(_hz, '')
    CHelpBuilder.Build(os.path.join(_dir, _name), _name)
    LogText('Project Description Build OK!!')


def Clear(filepath):

    def del_file(path_data):
        for i in os.listdir(path_data):
            file_data = path_data + '\\' + i
            if os.path.isfile(file_data) == True:
                os.remove(file_data)
            else:
                del_file(file_data)

    _dir = os.path.dirname(filepath)
    _file = os.path.basename(filepath)
    _hz = os.path.splitext(filepath)[1]
    _name = _file.replace(_hz, '')
    _folder = os.path.join(_dir, _name)
    if os.path.exists(_folder):
        del_file(_folder)
    LogText('PATH:' + _folder + ' clear out!!')


def BuildStruct(data):
    global BasicType
    mapps = {}

    def sort(lt1, lt2):
        while len(lt2) > 0:
            rmlt = []
            for i in xrange(len(lt2)):
                l = lt2[i]
                if mapps.has_key(l) == False:
                    lt1.append(l)
                    rmlt.append(i)
                else:
                    find = 0
                    for yl in mapps[l]:
                        if yl in lt1:
                            find += 1

                    if find == len(mapps[l]):
                        lt1.append(l)
                        rmlt.append(i)

            ltn = []
            for i in xrange(len(lt2)):
                if i in rmlt:
                    pass
                else:
                    ltn.append(lt2[i])

            lt2 = ltn

    c = ''
    lts = {}
    for i in data.keys():
        ms = data[i]
        lt = [
         '#pragma pack(4)',
         'struct _%s{' % i]
        for m in ms:
            _name = m[0]
            _type = m[1]
            _lenth = m[2]
            _cmt = m[3]
            if _name == '' or _type == '':
                continue
            if _type in BasicType:
                pass
            elif mapps.has_key(i):
                mapps[i].append(_type)
            else:
                mapps[i] = [
                 _type]
            if _lenth == '' or int(_lenth) == 0:
                txt = '%s %s;//%s' % (_type, _name, _cmt)
            else:
                txt = '%s %s[%s];//%s' % (_type, _name, _lenth, _cmt)
            lt.append(txt)

        lt.append('};')
        lt.append('#pragma pack()')
        x = ('\n').join(lt)
        x += '\n'
        lts[i] = x

    lt_ok = []
    lt_nok = data.keys()
    sort(lt_ok, lt_nok)
    c = ''
    for l in lt_ok:
        c += lts[l]

    lt = [
     '//AUTO GENERATE',
     '#pragma once',
     '#ifndef __STRUCT_H',
     '#define __STRUCT_H',
     '#include "__global.h"']
    for i in data.keys():
        lt.append('typedef struct _%s %s;' % (i, i))

    x = ('\n').join(lt)
    x += '\n'
    c = x + c + '\n'
    c += '#endif //__STRUCT_H\n'
    return c


def BuildGVL(data):
    c = ''
    lt = [
     '//AUTO GENERATE',
     '#pragma once',
     '#ifndef __GVL_H',
     '#define __GVL_H',
     '#include "all.h"']
    prgs = data['program'].keys()
    for prg in prgs:
        lt.append('#include "%s.h"' % prg)

    lt.append('#include "__struct.h"')
    lt.append('#pragma pack(4)')
    lt.append('typedef struct __GVL_t{')
    for i in data['gvl'].keys():
        ms = data['gvl'][i]
        for m in ms:
            _name = m[0]
            _type = m[1]
            _lenth = m[2]
            _cmt = m[3]
            if _name == '' or _type == '':
                continue
            if _lenth == '' or int(_lenth) == 0:
                txt = '%s %s;///< %s' % (_type, _name, _cmt)
            else:
                txt = '%s %s[%s];///< %s' % (_type, _name, _lenth, _cmt)
            lt.append(txt)

    for prg in prgs:
        lt.append('C%s %s;///< Program:%s 实例化' % (prg, prg, prg))

    _axisnames = GetSingleAxisName(data['motion'])
    for i in _axisnames:
        lt.append('CSingleAxis %s;///< 轴%s 实例化' % (i, i))

    lt.append('} _GVL,*pGVL;')
    lt.append('extern pGVL _pGVL;')
    lt.append('#defin GVL (*_pGVL);')
    lt.append('#pragma pack()')
    lt.append('#endif //__GVL_H')
    c += ('\n').join(lt)
    c += '\n'
    return c


def BuildInitVariable(lt, fix):
    import re
    txt = ''
    for m in lt:
        if m['name'] == '' or m['type'] == '':
            continue
        if m['type'] in BasicType:
            if m['def'] != '' and m['def'].isdigit():
                txt += '%s%s = %s;\n' % (fix, m['name'], m['def'])
            else:
                value = re.compile('^[-+]?[0-9]+\\.[0-9]+$')
                result = value.match(m['def'])
                if result:
                    txt += '%s%s = %s;\n' % (fix, m['name'], m['def'])
                else:
                    txt += '%s%s = %s;\n' % (fix, m['name'], '0')
        elif m['type'] in CLASSLIST:
            txt += '%s%s.init();\n' % (fix, m['name'])
        else:
            txt += BuildInitVariable(m['child'], fix + m['name'] + '.')

    return txt


def BuildVariableInitC(data):
    dcSturct = {}
    ms = data['gvl']['GVL']
    lt = []
    for m in ms:
        _name = m[0]
        _type = m[1]
        _lenth = m[2]
        _def = m[3]
        _cmt = m[4]
        if _name == '' or _type == '':
            continue
        if _lenth == '' or int(_lenth) == 0:
            dc = {'name': _name, 
               'type': _type, 
               'cmmt': _cmt, 
               'def': _def, 
               'addr': 0}
            if _type in BasicType:
                pass
            else:
                dc['child'] = ALLCLASS[_type]['member']
            lt.append(dc)
        else:
            for idx in xrange(int(_lenth)):
                dc = {'name': _name + '[%d]' % idx, 'type': _type, 
                   'cmmt': _cmt, 
                   'def': _def, 
                   'addr': 0}
                if _type in BasicType:
                    pass
                else:
                    dc['child'] = ALLCLASS[_type]['member']
                lt.append(dc)

    init_txt = ''
    init_gvl_menber = BuildInitVariable(lt, 'GVL.')
    lt = []
    i = 0
    for p in data['motion']['axis']:
        if p[0] == '':
            continue
        lt.append('GVL.%s.index = %d;' % (p[0], i))
        lt.append('GVL.%s.setInst(pMC);' % p[0])
        i += 1

    init_axis = ('\n').join(lt)
    lt = []
    for p in data['program'].keys():
        lt.append('GVL.%s.init();' % p)

    init_prg = ('\n').join(lt)
    lt = [
     '//gvl init',
     '//custom member init',
     init_gvl_menber,
     '',
     '//axis init',
     init_axis,
     '',
     '//prg init',
     init_prg,
     '']
    init_txt = ('\n').join(lt)
    return init_txt


def CalcModbus(lt, startaddr, maxlenth):
    blocks = []

    def printvariable(lt, fix):
        for m in lt:
            if m['type'] in BasicType:
                print '%s%s %s %s %s' % (fix, m['name'], m['type'], m['cmmt'], m['addr'])
            else:
                print '%s%s %s %s --GROUP--' % (fix, m['name'], m['type'], m['cmmt'])
                printvariable(m['child'], fix + '  ')

    def calc_addr(lt, mode, begin):
        global OFFSET1
        addr = begin
        for m in lt:
            if m['type'] in BasicType:
                m['addr'] = addr
                addr += OFFSET1[BasicType.index(m['type'])] / mode
            else:
                addr = calc_addr(m['child'], mode, addr)

        return addr

    def split_block(lt, begin, maxlenth):
        for m in lt:
            if m['type'] in BasicType:
                curaddr = m['addr']
                m['addr'] = 'b%d.%d' % (len(blocks), 400000 + m['addr'] + 1)
                if curaddr + OFFSET1[BasicType.index(m['type'])] / 2 - begin > maxlenth:
                    dc = {'start': begin + 1, 
                       'end': curaddr + OFFSET1[BasicType.index(m['type'])] / 2 - 1}
                    blocks.append(dc)
                    begin = dc['end'] + 1
            else:
                begin = split_block(m['child'], begin, maxlenth)

        return begin

    calc_addr(lt, 2, startaddr)
    split_block(lt, 0, 100)
    printvariable(lt, '')


def BuildMainC(data):
    txt = ''
    if data.has_key('__main__'):
        txt = data['__main__']['Code']
    h = '\n    #pragma once\n    #ifndef __MAIN_H\n    #define __MAIN_H\n    \n    #include "__glv.h"\n    \n    \n    void __main__(_GVL& GVL);\n    #endif //__MAIN_H\n    \n    '
    cpp = '\n    #include "__main__.h"\n    void __main__(_GVL& GVL){\n\n    ' + txt + '\n    }\n    '
    return (
     h, cpp)


def GetSingleAxisName(data):
    dc = data['axis']
    lt = []
    for a in dc:
        if a[0] != '':
            lt.append(a[0])

    return lt


def BuildTask(data, init_c, init_hardware):
    _lenth = len(data.keys())

    def build_H():
        template = '\n//AUTO GENERATE\n#pragma once\n\n#ifndef _TASK_H\n#define _TASK_H\n\n#include "__gvl.h"\n\nclass CTask\n{\npublic:\n\tCTask(void);\n\t~CTask(void);\n#pragma pack(4)\nprivate:\n[%maker%]\n#pragma pack()\npublic:\n\tvoid exec();\n\tvoid init(UDINT* pMC);\n};\n\n#endif\n    \n    '
        h = ''
        lt = []
        for i in xrange(_lenth):
            lt.append('TON T%d;///< Task%d 定时器' % (i, i + 1))

        h = template.replace('[%maker%]', ('\n').join(lt))
        return h

    def build_cpp():
        template = '\n//AUTO GENERATE\n#include "Task.h"\n\nCTask::CTask(void)\n{\n\n}\n\n\nCTask::~CTask(void)\n{\n}\n\n/**\n* PLC任务执行程序 ...\n*/\nvoid CTask::exec(){\n[%marker1%]\n}\n\n\nvoid init_hardware(){\n[%hardware%]\n}\n\n/**\n   * @brief PLC任务初始化程序 ...\n   * \n   * @param pMC [in] 运动基本地址\n   * @return void \n   */\nvoid CTask::init(UDINT* pMC){\n[%marker2%]\n}\n        '
        cpp = ''
        exec_c = ''
        lt = []
        i = 0
        for n in data.keys():
            _time = data[n]['scantime']
            _prgs = data[n]['list']
            lt.append('//task:%s' % n)
            lt.append('T%d.delay(!T%d.Q,%s);' % (i, i, _time))
            lt.append('if(T%d.Q){' % i)
            for p in _prgs:
                if p[0] != '':
                    lt.append('GVL.%s.exec();' % p[0])

            lt.append('}')
            i += 1

        exec_c = ('\n').join(lt)
        cpp = template.replace('[%marker1%]', exec_c)
        cpp = cpp.replace('[%marker2%]', init_c)
        cpp = cpp.replace('[%hardware%]', init_hardware)
        return cpp

    return (build_H(), build_cpp())


def BuildPRGs(data):
    lt = []
    for p in data.keys():
        h, cpp = BuildPRG(p, data[p])
        lt.append([p, h, cpp])

    return lt


def BuildPRG(name, data):
    member = {}

    def build_H():
        h = ''
        template = '\n//AUTO GENERATOR\n#pragma once\n#ifndef C[%marker1%]_H\n#define C[%marker1%]_H\n#include "all.h"\n#include "__struct.h"\n/**\n * class [%marker1%] [%marker3%]\n */\nclass C[%marker1%]\n{\npublic:\n\tC[%marker1%](void);\n\t~C[%marker1%](void);\npublic:\n\tvoid exec();\n\tvoid init();\n\npublic:\n\t//member\n#pragma pack(4)\n\t[%marker2%]\n#pragma pack()\n};\n#endif  //C[%marker1%]_H\n        '
        dec_member = ''
        lt = []
        for m in member['VAR']:
            _name = m['name']
            _type = m['type']
            _lenth = m['lenth']
            _cmt = m['cmmt']
            if _lenth == '' or int(_lenth) == 0:
                txt = '%s %s;///< %s' % (_type, _name, _cmt)
            else:
                txt = '%s %s[%s];///< %s' % (_type, _name, _lenth, _cmt)
            lt.append(txt)

        dec_member = ('\n').join(lt)
        h = template.replace('[%marker1%]', name)
        h = h.replace('[%marker2%]', dec_member)
        _cmmt = ''
        if data.has_key('Cmmt'):
            _cmmt = data['Cmmt']
        h = h.replace('[%marker3%]', _cmmt)
        return h

    def build_CPP():
        cpp = ''
        template = '\n//AUTO GENERATOR\n#include <stdio.h>\n#include "[%marker1%].h"\n#include "__gvl.h"\n#include "__function.h"\n\nC[%marker1%]::C[%marker1%](void)\n{\n}\n\n\nC[%marker1%]::~C[%marker1%](void)\n{\n}\n\n\n/**\n* [%marker1%]的执行程序...\n* ...\n*/\nvoid C[%marker1%]::exec()\n{\n\n    [%marker4%]\n\t{// custom code\n\t\t\n\t[%marker2%]\n\t}\n\t\n}\n\n/**\n* [%marker1%]的初始化程序...\n* ...\n*/\nvoid C[%marker1%]::init()\n{\n    [%marker3%]\n}\n'
        dec_temp = ''
        lt = []
        for m in member['TEMP']:
            _name = m['name']
            _type = m['type']
            _lenth = m['lenth']
            _cmt = m['cmmt']
            if _lenth == '' or int(_lenth) == 0:
                txt = '%s %s;//%s' % (_type, _name, _cmt)
            else:
                txt = '%s %s[%s];//%s' % (_type, _name, _lenth, _cmt)
            lt.append(txt)

        dec_temp = ('\n').join(lt)
        cus_code = data['Code']
        lt = []
        for m in member['VAR']:
            _lenth = m['lenth']
            if _lenth == '' or int(_lenth) == 0:
                if m['type'] in ALLCLASS.keys():
                    m['child'] = ALLCLASS[m['type']]['member']
                lt.append(m)
            else:
                for idx in xrange(int(_lenth)):
                    dc = {'name': m['name'] + '[%d]' % idx, 
                       'type': m['type'], 
                       'cmmt': m['cmmt'], 
                       'def': m['def'], 
                       'addr': 0}
                    if m['type'] in BasicType:
                        pass
                    else:
                        dc['child'] = ALLCLASS[m['type']]['member']
                    lt.append(dc)
                    idx += 1

        init_code = BuildInitVariable(lt, '')
        cpp = template.replace('[%marker1%]', name)
        cpp = cpp.replace('[%marker2%]', cus_code)
        cpp = cpp.replace('[%marker3%]', init_code)
        cpp = cpp.replace('[%marker4%]', dec_temp)
        return cpp

    def build_interface():
        member = {'VAR': [], 'TEMP': []}
        for m in data['Declare']:
            _class = m[0]
            dc = {'name': m[1], 
               'type': m[2], 
               'lenth': m[3], 
               'def': m[4], 
               'cmmt': m[5]}
            if _class == '' or _class == 'VAR':
                member['VAR'].append(dc)
            elif _class == 'VAR_TEMP':
                member['TEMP'].append(dc)

        return member

    member = build_interface()
    return (
     build_H(), build_CPP())


def BuildMemberInitC(data, dcS):
    dcSturct = {}

    def findall(_type, lt):
        if _type in dcSturct.keys():
            for m in dcSturct[_type]:
                if m['type'] in BasicType:
                    dc = {'name': m['name'], 'type': m['type'], 
                       'cmmt': m['cmmt'], 
                       'def': m['def'], 
                       'addr': 0}
                    lt.append(dc)
                else:
                    dc = {'name': m['name'], 
                       'type': m['type'], 
                       'cmmt': m['cmmt'], 
                       'def': m['def'], 
                       'addr': 0}
                    ms = []
                    findall(m['type'], ms)
                    dc['child'] = ms
                    lt.append(dc)

        else:
            print 'error: not find struct:%s!!!!' % _type
            sys.exit(0)

    def _BuildInitVariable(lt, fix):
        import re
        txt = ''
        for m in lt:
            if m['type'] in BasicType:
                if m['def'] != '' and m['def'].isdigit():
                    txt += '%s%s = %s;\n' % (fix, m['name'], m['def'])
                else:
                    value = re.compile('^[-+]?[0-9]+\\.[0-9]+$')
                    result = value.match(m['def'])
                    if result:
                        txt += '%s%s = %s;\n' % (fix, m['name'], m['def'])
                    else:
                        txt += '%s%s = %s;\n' % (fix, m['name'], '0')
            elif m['type'] in CLASSLIST:
                txt += '%s%s.init();\n' % (fix, m['name'])
            else:
                txt += BuildInitVariable(m['child'], fix + m['name'] + '.')

        return txt

    for i in dcS.keys():
        ms = dcS[i]
        dcSturct[i] = []
        lt = []
        for m in ms:
            _name = m[0]
            _type = m[1]
            _lenth = m[2]
            _def = m[3]
            _cmt = m[4]
            if _name == '' or _type == '':
                continue
            if _lenth == '' or int(_lenth) == 0:
                dc = {'name': _name, 
                   'type': _type, 
                   'cmmt': _cmt, 
                   'def': _def}
                lt.append(dc)
            else:
                for idx in xrange(int(_lenth)):
                    dc = {'name': _name + '[%d]' % idx, 'type': _type, 
                       'cmmt': _cmt, 
                       'def': _def}
                    lt.append(dc)

        dcSturct[i] = lt

    ms = data
    lt = []
    for m in ms:
        _name = m['name']
        _type = m['type']
        _lenth = m['lenth']
        _def = m['def']
        _cmt = m['cmmt']
        if _name == '' or _type == '':
            continue
        if _lenth == '' or int(_lenth) == 0:
            dc = {'name': _name, 
               'type': _type, 
               'cmmt': _cmt, 
               'def': _def, 
               'addr': 0}
            if _type in BasicType:
                pass
            else:
                members = []
                findall(_type, members)
                dc['child'] = members
            lt.append(dc)
        else:
            for idx in xrange(int(_lenth)):
                dc = {'name': _name + '[%d]' % idx, 'type': _type, 
                   'cmmt': _cmt, 
                   'def': _def, 
                   'addr': 0}
                if _type in BasicType:
                    pass
                else:
                    members = []
                    findall(_type, members)
                    dc['child'] = members
                lt.append(dc)

    init_txt = ''
    init_gvl_menber = _BuildInitVariable(lt, '')
    return init_gvl_menber


def BuildFunctions(data):
    template = '\n//AUTO GENERATOR\n#pragma once\n#include "__gvl.h"\n#ifndef _FUNCTION_H\n#define _FUNCTION_H\n\n\n[%marker1%]\n\n\n#endif\n'
    lt = []
    for fc in data.keys():
        lt.append(BuildFunction(data[fc], fc))

    h = template.replace('[%marker1%]', ('\n').join(lt))
    return h


def BuildFunction(data, name, mode=0, clsn=''):
    u"""

    :param data:
    :param name:
    :param mode: 0 实现,1 声明
    :param clsn: 类名称
    :return:
    """
    template = '{0} {3}{1}({2})'
    if data.has_key('Cmmt') == False:
        cmmt = ''
    else:
        cmmt = data['Cmmt']

    def build_function_comment_doxygen(member):
        """/**
       * @brief {cmmt} ...
       *
       * @param x [in] comment
       * @return void
       */
        """
        lt = []
        lt.append('/**')
        lt.append('* @brief %s ...' % cmmt)
        lt.append('*')
        for m in member['VAR_INPUT']:
            lt.append(('* @param {0} [in] {1}').format(m['name'], m['cmmt']))

        for m in member['VAR_OUTPUT']:
            lt.append(('* @param {0} [out] {1}').format(m['name'], m['cmmt']))

        for m in member['RETURN']:
            lt.append(('* @return {0} {1}').format(m['type'], m['cmmt']))

        lt.append('*/')
        lt.append('')
        return ('\n').join(lt)

    def build_interface():
        member = {'VAR_INPUT': [], 'VAR_OUTPUT': [], 'TEMP': [], 'RETURN': []}
        for m in data['Declare']:
            _class = m[0]
            dc = {'name': m[1], 
               'type': m[2], 
               'lenth': m[3], 
               'cmmt': m[4]}
            if _class == '' or _class in ['VAR_INPUT', 'VAR_OUTPU', 'VAR_TEMP', 'RETURN'] == False:
                member['TEMP'].append(dc)
            else:
                member[_class].append(dc)

        return member

    member = build_interface()
    _return = ''
    _dec = ''
    if len(member['RETURN']) == 0 or member['RETURN'][0]['type'] == '':
        _return = 'void'
    else:
        _return = member['RETURN'][0]['type']
    lt = []
    for m in member['VAR_INPUT']:
        _lenth = m['lenth']
        _name = m['name']
        _type = m['type']
        if _lenth == '' or int(_lenth) == 0:
            txt = '%s %s' % (_type, _name)
        else:
            txt = 'const %s (&%s)[%s]' % (_type, _name, _lenth)
        lt.append(txt)

    for m in member['VAR_OUTPUT']:
        _lenth = m['lenth']
        _name = m['name']
        _type = m['type']
        if _lenth == '' or int(_lenth) == 0:
            txt = '%s %s' % (_type, _name)
        else:
            txt = '%s (&%s)[%s]' % (_type, _name, _lenth)
        lt.append(txt)

    _dec = (',').join(lt)
    if mode == 0:
        c = build_function_comment_doxygen(member)
        c += template.format(_return, name, _dec, clsn)
        c += '{\n' + data['Code'] + '\n}\n'
    else:
        c = template.format(_return, name, _dec, clsn)
        c += ';'
    return c


def BuildFBs(data):
    lt = []
    for k in data.keys():
        h, cpp = BuildFB(k, data[k])
        lt.append([k, h, cpp])

    return lt


def BuildFB(name, data):

    def build_H():
        template = '\n        \n//AUTO GENERATOR\n#pragma once\n#ifndef C[%name%]_H\n#define C[%name%]_H\n#include "all.h"\n#include "__struct.h"\n[%import%]\n/**\n * class [%name%] [%cmmt%]\n */\nclass C[%name%]\n{\npublic:\n    C[%name%](void);\n    ~C[%name%](void);\npublic:\n    [%meth%]\n\npublic:\n    //member\n#pragma pack(4)\n    [%member%]\n#pragma pack()\n};\n#endif  //C[%name%]_H\n\n        '
        lt = []
        for m in data['Declare']:
            _class = m[0]
            _name = m[1]
            _type = m[2]
            _lenth = m[3]
            _cmt = m[5]
            if _name == '' or _type == '':
                continue
            if _class == 'PUBLIC':
                lt.append('public:')
            else:
                lt.append('private:')
            if _lenth == '' or int(_lenth) == 0:
                txt = '%s %s;///< %s' % (_type, _name, _cmt)
            else:
                txt = '%s %s[%s];///< %s' % (_type, _name, _lenth, _cmt)
            lt.append(txt)

        _member = ('\n').join(lt)
        lt = []
        lt.append('public:')
        lt.append('void init();')
        for m in data.keys():
            if m != 'init' and m != 'Declare':
                lt.append(BuildFunction(data[m], m, 1))

        _meth = ('\n').join(lt)
        lt = []
        _includes = ALLCLASS[name]['include']
        for _include in _includes:
            if ALLCLASS[_include]['class'] == 'class':
                lt.append('#include "%s.h"' % _include)
                continue

        _import = ('\n').join(lt)
        h = template.replace('[%name%]', name)
        h = h.replace('[%meth%]', _meth)
        h = h.replace('[%member%]', _member)
        h = h.replace('[%import%]', _import)
        return h

    def build_cpp():
        template = '\n//AUTO GENERATOR\n#include "[%name%].h"\n#include "__gvl.h"\n#include "__function.h"\n\nC[%name%]::C[%name%](void)\n{\n}\n\n\nC[%name%]::~C[%name%](void)\n{\n}\n\n\n[%meth%]\n\n[%init%]\n\n\n\n'
        lt = []
        for m in data.keys():
            if m != 'init' and m != 'Declare':
                lt.append(BuildFunction(data[m], m, 0, 'C' + name + '::'))

        _meth = ('\n').join(lt)
        lt = []
        lt.append('void C%s::init(){' % name)
        lt.append(BuildInitVariable(ALLCLASS[name]['member'], ''))
        lt.append('}')
        _init = ('\n').join(lt)
        cpp = template.replace('[%name%]', name)
        cpp = cpp.replace('[%meth%]', _meth)
        cpp = cpp.replace('[%init%]', _init)
        return cpp

    return (
     build_H(), build_cpp())


def BuildAllClass(DATA):
    global BasicTypeInfo
    Align = 4

    def buildStruct(dcS):
        dcSturct = {}
        for i in dcS.keys():
            ms = dcS[i]
            dcSturct[i] = {'class': 'struct', 
               'include': [], 'size': 0, 
               'member': []}
            lt = []
            _includes = []
            for m in ms:
                _name = m[0]
                _type = m[1]
                _lenth = m[2]
                _def = m[3]
                _cmt = m[4]
                if _name == '' or _type == '':
                    continue
                if _lenth == '' or int(_lenth) == 0:
                    dc = {'name': _name, 
                       'type': _type, 
                       'cmmt': _cmt, 
                       'def': _def, 
                       'lenth': '', 
                       'size': BasicTypeInfo[_type] if BasicTypeInfo.has_key(_type) else 0}
                    lt.append(dc)
                else:
                    for idx in xrange(int(_lenth)):
                        dc = {'name': _name + '[%d]' % idx, 'type': _type, 
                           'cmmt': _cmt, 
                           'def': _def, 
                           'lenth': '', 
                           'size': BasicTypeInfo[_type] if BasicTypeInfo.has_key(_type) else 0}
                        lt.append(dc)

                if _type in _includes:
                    pass
                elif (_type in BasicType) is False:
                    _includes.append(_type)

            dcSturct[i]['member'] = lt
            dcSturct[i]['include'] = _includes

        return dcSturct

    def buildClass(dcS):
        dcSturct = {}
        for i in dcS.keys():
            ms = dcS[i]['Declare']
            dcSturct[i] = {'class': 'class', 
               'size': 0, 
               'maxsize': 0, 
               'include': [], 'member': []}
            lt = []
            _includes = []
            for m in ms:
                _class = m[0]
                _name = m[1]
                _type = m[2]
                _lenth = m[3]
                _def = m[4]
                _cmt = m[5]
                if _class == '' or _class in ('PUBLIC', 'PRIVATE'):
                    _class = 'PRIVATE'
                if _name == '' or _type == '':
                    continue
                if _lenth == '' or int(_lenth) == 0:
                    dc = {'name': _name, 
                       'type': _type, 
                       'cmmt': _cmt, 
                       'size': BasicTypeInfo[_type] if BasicTypeInfo.has_key(_type) else 0, 
                       'def': _def, 
                       'lenth': '', 
                       'class': _class}
                    lt.append(dc)
                else:
                    for idx in xrange(int(_lenth)):
                        dc = {'name': _name + '[%d]' % idx, 'type': _type, 
                           'size': BasicTypeInfo[_type] if BasicTypeInfo.has_key(_type) else 0, 
                           'cmmt': _cmt, 
                           'def': _def, 
                           'lenth': '', 
                           'class': _class}
                        lt.append(dc)

                if _type in _includes:
                    pass
                elif (_type in BasicType) is False:
                    _includes.append(_type)

            dcSturct[i]['member'] = lt
            dcSturct[i]['include'] = _includes

        return dcSturct

    def buildPRG(dcS):
        dcSturct = {}
        for i in dcS.keys():
            ms = dcS[i]['Declare']
            dcSturct[i] = {'class': 'class', 
               'size': 0, 
               'maxsize': 0, 
               'include': [], 'member': []}
            lt = []
            _includes = []
            for m in ms:
                _class = m[0]
                _name = m[1]
                _type = m[2]
                _lenth = m[3]
                _def = m[4]
                _cmt = m[5]
                if _class == '' or _class in ('PUBLIC', 'PRIVATE'):
                    _class = 'PRIVATE'
                if _name == '' or _type == '':
                    continue
                if _lenth == '' or int(_lenth) == 0:
                    dc = {'name': _name, 
                       'type': _type, 
                       'cmmt': _cmt, 
                       'size': BasicTypeInfo[_type] if BasicTypeInfo.has_key(_type) else 0, 
                       'def': _def, 
                       'lenth': '', 
                       'class': _class}
                    lt.append(dc)
                else:
                    for idx in xrange(int(_lenth)):
                        dc = {'name': _name + '[%d]' % idx, 'type': _type, 
                           'size': BasicTypeInfo[_type] if BasicTypeInfo.has_key(_type) else 0, 
                           'cmmt': _cmt, 
                           'def': _def, 
                           'lenth': '', 
                           'class': _class}
                        lt.append(dc)

                if _type in _includes:
                    pass
                elif (_type in BasicType) is False:
                    _includes.append(_type)

            dcSturct[i]['member'] = lt
            dcSturct[i]['include'] = _includes

        return dcSturct

    def findall(dc, _type, lt):
        if _type in dc.keys():
            for m in dc[_type]['member']:
                if m['type'] in BasicType:
                    dc = {'name': m['name'], 'type': m['type'], 
                       'cmmt': m['cmmt'], 
                       'def': m['def'], 
                       'addr': 0}
                    if m.has_key('class'):
                        dc['class'] = m['class']
                    lt.append(dc)
                else:
                    dc = {'name': m['name'], 
                       'type': m['type'], 
                       'cmmt': m['cmmt'], 
                       'def': m['def'], 
                       'addr': 0}
                    if m.has_key('class'):
                        dc['class'] = m['class']
                    ms = []
                    findall(ds, m['type'], ms)
                    dc['child'] = ms
                    lt.append(dc)

        else:
            print 'error: not find struct:%s!!!!' % _type
            sys.exit(0)

    def print_all_class(DATA):
        for k in DATA.keys():
            print '==============================='
            print '%s:%s' % (DATA[k]['class'], k)
            print 'include:%s' % (',').join(DATA[k]['include'])
            print 'members:'
            print_member(DATA[k]['member'], '')
            print ''
            print '================================'
            print ''
            print ''
            print ''

    def print_member(DATA, fix):

        def set_table_style(tb):
            tb.align = 'l'
            tb.junction_char = '*'
            tb.left_padding_width = 0

        tb = PrettyTable(['Name', 'Type', 'Value', 'Comment'])
        for d in DATA:
            _name = d['name']
            _type = d['type']
            _def = d['addr']
            _cmt = d['cmmt']
            tb.add_row([fix + _name, _type, _def, _cmt])
            if d.has_key('child'):
                print_member_child(d['child'], fix + _name + '.', tb)

        set_table_style(tb)
        print tb

    def print_member_child(DATA, fix, grid):
        for d in DATA:
            _name = d['name']
            _type = d['type']
            _def = d['addr']
            _cmt = d['cmmt']
            grid.add_row([fix + _name, _type, _def, _cmt])
            if d.has_key('child'):
                print_member_child(d['child'], fix + _name + '.', grid)

    def list_jiao(a, b):
        return [ val for val in a if val in b ]

    def list_cha(a, b):
        return list(set(b).difference(set(a)))

    def expand_all_struct(data):

        def find_all(start, lt):
            for m in lt:
                if m['type'] in BasicTypeInfo.keys():
                    m['addr'] += start
                else:
                    m['addr'] += start
                    m['child'] = find_all(m['addr'], copy.deepcopy(ds[m['type']]['member']))

            return lt

        for k in data.keys():
            start = 0
            for m in data[k]['member']:
                if m['type'] in BasicTypeInfo.keys():
                    m['addr'] += start
                else:
                    m['child'] = find_all(m['addr'] + start, copy.deepcopy(ds[m['type']]['member']))

    ds1 = buildStruct(DATA['struct'])
    ds2 = buildClass(DATA['class'])
    ds3 = buildPRG(DATA['program'])
    ds = merge_dicts(ds1, ds2, ds3)
    nok = ds.keys()
    ok = []
    while len(nok) > 0:
        nok = list_cha(ok, nok)
        for k in nok:
            if len(ds[k]['include']) == 0 or len(ds[k]['include']) == len(list_jiao(ds[k]['include'], ok)):
                begin = 0
                size = 0
                maxsize = 0
                for m in ds[k]['member']:
                    if m['type'] in BasicTypeInfo.keys():
                        _size = m['size']
                        _t = begin % _size
                        if _t == 0:
                            m['addr'] = begin
                        else:
                            m['addr'] = begin + _t
                        begin = m['addr'] + _size
                        maxsize = max(maxsize, _size)
                    else:
                        if (m['type'] in ok) == False:
                            break
                        _size = ds[m['type']]['size']
                        _maxsize = ds[m['type']]['maxsize']
                        _t = begin % _maxsize
                        if _t == 0:
                            m['addr'] = begin
                        else:
                            m['addr'] = begin + _t
                        begin = m['addr'] + _size
                        maxsize = max(maxsize, _maxsize)
                        m['child'] = []

                _t = begin % 4
                if _t == 0:
                    size = begin
                else:
                    size = begin + _t
                ds[k]['size'] = size
                ds[k]['maxsize'] = maxsize
                ok.append(k)
                continue

    dsA = copy.copy(ds)
    expand_all_struct(dsA)
    print_all_class(dsA)
    lt = []
    for k in ds.keys():
        if ds[k]['class'] == 'class':
            lt.append(k)

    return (ds, lt)


def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)

    return result


def ExpandGvlVariable(data):
    lt = []
    dcPRG = {}
    dcGVL = {}

    def readdr_all_struct(start, data):

        def find_all(start, lt):
            for m in lt:
                if m['type'] in BasicTypeInfo.keys():
                    m['addr'] += start
                else:
                    m['addr'] += start
                    m['child'] = find_all(start, m['child'])

            return lt

        for m in data:
            if m['type'] in BasicTypeInfo.keys():
                m['addr'] += start
            else:
                m['addr'] += start
                find_all(start, m['child'])

    def addprg():
        lt = []
        for i in data['program'].keys():
            l = []
            l.append(i)
            l.append(i)
            l.append('')
            l.append('')
            l.append('PRG:%s 实例' % i)
            lt.append(l)

        return lt

    for i in data['gvl'].keys():
        ms = copy.deepcopy(data['gvl'][i])
        ms.extend(addprg())
        lt = []
        begin = 0
        maxsize = 0
        for m in ms:
            _name = m[0]
            _type = m[1]
            _lenth = m[2]
            _cmt = m[4]
            if _name == '' or _type == '':
                continue
            if _lenth == '' or int(_lenth) == 0:
                dc = {'name': _name, 'type': _type, 
                   'lenth': 0, 
                   'cmmt': _cmt, 
                   'addr': 0, 
                   'size': BasicTypeInfo[_type] if BasicTypeInfo.has_key(_type) else 0}
                if _type in BasicTypeInfo.keys():
                    _size = dc['size']
                    _t = begin % _size
                    if _t == 0:
                        dc['addr'] = begin
                    else:
                        dc['addr'] = begin + _t
                    begin = dc['addr'] + _size
                    maxsize = max(maxsize, _size)
                else:
                    _size = ALLCLASS[_type]['size']
                    _maxsize = ALLCLASS[_type]['maxsize']
                    _t = begin % _maxsize
                    if _t == 0:
                        dc['addr'] = begin
                    else:
                        dc['addr'] = begin + _t
                    if _type in ALLCLASS.keys():
                        dc['child'] = copy.deepcopy(ALLCLASS[_type]['member'])
                        readdr_all_struct(dc['addr'], dc['child'])
                        maxsize = max(maxsize, _maxsize)
                        begin = dc['addr'] + _size
                lt.append(dc)
            else:
                for idx in xrange(int(_lenth)):
                    dc = {'name': _name + '[%d]' % idx, 
                       'type': _type, 
                       'cmmt': _cmt, 
                       'lenth': 0, 
                       'addr': 0, 
                       'size': BasicTypeInfo[_type] if BasicTypeInfo.has_key(_type) else 0}
                    if _type in BasicTypeInfo.keys():
                        _size = dc['size']
                        _t = begin % _size
                        if _t == 0:
                            dc['addr'] = begin
                        else:
                            dc['addr'] = begin + _t
                        begin = dc['addr'] + _size
                        maxsize = max(maxsize, _size)
                    else:
                        _size = ALLCLASS[_type]['size']
                        _maxsize = ALLCLASS[_type]['maxsize']
                        _t = begin % _maxsize
                        if _t == 0:
                            dc['addr'] = begin
                        else:
                            dc['addr'] = begin + _t
                        if _type in ALLCLASS.keys():
                            dc['child'] = ALLCLASS[_type]['member']
                            readdr_all_struct(dc['addr'], dc['child'])
                            begin = dc['addr'] + _size
                    lt.append(dc)

        dcGVL[i] = lt

    return dcGVL['GVL']


def AddrGvlVariable(data, mode, offset):
    allvar = []
    dcVar = []

    def print_member(DATA, fix, start, node):

        def set_table_style(tb):
            tb.align = 'l'
            tb.junction_char = '*'
            tb.left_padding_width = 0

        tb = PrettyTable(['Name', 'Type', 'Comment'])
        tb1 = PrettyTable(['Name', 'Type', 'Address', 'Comment'])
        for d in DATA:
            _name = d['name']
            _type = d['type']
            _addr = d['addr'] / mode + offset
            _cmt = d['cmmt']
            tb.add_row([fix + _name, _type, _cmt])
            dc = {'name': _name, 
               'type': _type, 
               'addr': _addr, 
               'cmt': _cmt}
            if _type in BasicType:
                idx = BasicType.index(_type)
                tb1.add_row([fix + _name, _type, _addr, _cmt])
                allvar.append([fix + _name, _type, _addr, _cmt])
                node.append(dc)
            else:
                dc['type'] = 'GROUP'
                dc['child'] = []
                node.append(dc)
            if d.has_key('child'):
                print_member_child(d['child'], fix + _name + '.', tb, tb1, start, node[(len(node) - 1)]['child'])

        set_table_style(tb)
        set_table_style(tb1)
        print '=====GVL====='
        print tb
        print '============='

    def print_member_child(DATA, fix, grid, grid2, start, node):
        for d in DATA:
            _name = d['name']
            _type = d['type']
            _addr = d['addr'] / mode + offset
            _cmt = d['cmmt']
            grid.add_row([fix + _name, _type, _cmt])
            dc = {'name': _name, 
               'type': _type, 
               'addr': _addr, 
               'cmt': _cmt}
            if _type in BasicType:
                idx = BasicType.index(_type)
                grid2.add_row([fix + _name, _type, _addr, _cmt])
                allvar.append([fix + _name, _type, _addr, _cmt])
                node.append(dc)
            else:
                dc['type'] = 'GROUP'
                dc['child'] = []
                node.append(dc)
            if d.has_key('child'):
                print_member_child(d['child'], fix + _name + '.', grid, grid2, start, node[(len(node) - 1)]['child'])

        return start

    def print_variable(tb, DATA, fix):
        print '=============================================================='
        for d in DATA:
            _name = d['name']
            _type = d['type']
            _addr = d['addr']
            _cmt = d['cmt']
            print _addr
            if _type == 'GROUP':
                _type = ''
                _addr = ''
            tb.add_row([' ' * len(fix) + _name, _type, _addr, _cmt])
            if d.has_key('child'):
                print_variable(tb, d['child'], fix + _name)

    def set_table_style(tb):
        tb.align = 'l'
        tb.junction_char = '*'
        tb.left_padding_width = 0

    print_member(data, 'GVL.', 0, dcVar)
    tb = PrettyTable(['Name', 'Type', 'Address', 'Comment'])
    tb.add_row(['GVL', '', '', ''])
    print_variable(tb, dcVar, 'GVL')
    set_table_style(tb)
    print tb
    return (
     allvar, dcVar)


def BuildScadaVariable(data):
    _driver_name = 'miPLC'
    _variable_root = 'GVL'
    _offset = 2
    _block_size = 100

    def find_end_addr(data):
        _len = len(data)
        if data[(_len - 1)].has_key('child'):
            _size = find_end_addr(data[(_len - 1)]['child'])
            return _size
        else:
            _addr = data[(_len - 1)]['addr']
            _type = data[(_len - 1)]['type']
            _endaddr = _addr + 2
            _size = _endaddr - 0 + 1
            return _size

    def build_driver(size):
        template = '\n            {\n            "DEVS":[\n                {\n                    "@DRV":"MDDRV.ModBusTCPC",\n                    "Name":"miPLC",\n                    "Description":"",\n                    "Enabled":"1",\n                    "CommType":"TCP",\n                    "CommParameter":"Client,192.167.8.21,1502,,",\n                    "ReplyTimeout":"1000",\n                    "Retries":"3",\n                    "Station":"1",\n                    "DataBlocks":[\n                    ]\n                }\n            ]\n        }\n        '
        objJSON = CJSON()
        dc = objJSON.loadstr(template)
        block_num = size // 100 + (1 if size % 100 > 0 else 0)
        _start_addr = 1
        lt = []
        for i in xrange(block_num):
            bl = {'Name': 'D0', 'Description': '', 
               'Enabled': '1', 
               'PollRate': '10', 
               'RegisterType': 'HoldingRegister', 
               'StartAddress': '1', 
               'EndAddress': '100'}
            bl['Name'] = 'D%d' % i
            bl['StartAddress'] = '%d' % _start_addr
            bl['EndAddress'] = '%d' % (_start_addr + 100 - 1)
            _start_addr += 100
            lt.append(bl)

        dc['DEVS'][0]['DataBlocks'] = lt
        return dc

    def build_variable_table(_data):
        template = '\n        {\n            "Index":\n                {\n                    "Revision":"2.0"\n                },\n            "GS":[\n                {\n                    "@N":"GVL",\n                    "@D":"PLC 全局变量",\n                    "@OI":"",\n                    "VS":[],\n                    "GS":[]\n                }\n            ]\n        }\n        '
        objJSON = CJSON()
        dc = objJSON.loadstr(template)
        node = dc['GS'][0]
        for m in _data:
            if m['type'] == 'GROUP':
                build_var_group(m, node['GS'])
            else:
                build_var_one(m, node['VS'])

        return dc

    def build_var_group(_data, node):
        template = '\n        {\n            "@N":"A0",\n            "@D":"",\n            "@OI":"",\n            "VS":[\n                \n            ]\n        }\n        '
        objJSON = CJSON()
        dc = objJSON.loadstr(template)
        _name = _data['name']
        _cmt = _data['cmt']
        dc['@N'] = _name
        dc['@D'] = _cmt
        dc['GS'] = []
        for m in _data['child']:
            _fffff = m['name']
            if m['type'] == 'GROUP':
                build_var_group(m, dc['GS'])
                node.append(dc)
            else:
                build_var_one(m, dc['VS'])
                node.append(dc)

    def build_var_one(_data, node):
        template = '\n            {\n                "@N":"a",\n                "@D":"",\n                "@DN":"miPLC",\n                "@AD":"D0.400001",\n                "@DT":"3",\n                "@VT":"1",\n                "@ODT":"3",\n                "@OI":"",\n                "@PCS":3,\n                "@UNIT":"",\n                "ACV":\n                {\n                    "@AM":"0",\n                    "@AR":"0",\n                    "@AI":"1",\n                    "@ATP":"360"\n                },\n                "WP":\n                {\n                    "@EW":"1",\n                    "@EWP":"1",\n                    "@WMAV":"",\n                    "@WMIV":"",\n                    "@ELP":"1"\n                },\n                "CVT":\n                {\n                    "@CT":"0",\n                    "@ELC":"0",\n                    "@OI":"",\n                    "@PMAV":"0",\n                    "@PMIV":"0",\n                    "@OMAV":"0",\n                    "@OMIV":"0"\n                },\n                "@AUTH":[\n                    {\n                        "@EL":0,\n                        "@OKI":\n                        {\n                            "@Comment":"",\n                            "@N":"",\n                            "@OT":2,\n                            "@T":41\n                        },\n                        "@PM":0,\n                        "@ST":1\n                    }\n                ],\n                "@IV":"0",\n                "@LV":""\n            }\n            '
        objJSON = CJSON()
        dc = objJSON.loadstr(template)
        _name = _data['name']
        _cmt = _data['cmt']
        _type = _data['type']
        _addr = _data['addr']
        _modaddr = _addr + 400000
        _blidx = _addr // 100 + (1 if _addr % 100 > 0 else 0)
        _blidx -= 1
        dc['@N'] = _name
        dc['@AD'] = 'D%d.%d' % (_blidx, _modaddr)
        TYPE_NUM = {'INT': '3', 
           'UINT': '4', 
           'DINT': '5', 
           'UDINT': '6', 
           'FLOAT': '9'}
        if _type in TYPE_NUM:
            dc['@DT'] = TYPE_NUM[_type]
            dc['@ODT'] = TYPE_NUM[_type]
        node.append(dc)

    _size_addr = find_end_addr(data)
    print _size_addr
    _dcDrv = build_driver(_size_addr)
    _dcVar = build_variable_table(data)
    print 11
    return (
     _dcDrv, _dcVar)


def FindTypeLenth(_type):
    if _type in BasicType:
        idx = BasicType.index(_type)
        return OFFSET1[idx]
    else:
        print 'ERROR BasicType:%s' % _type
        return 0


def BuildHardware(data):
    global HARDWARE_START_SLOT
    global HARDWARE_VAR
    dc = {'DI': [], 'DO': [], 'AI': [], 'AO': []}
    idx = HARDWARE_START_SLOT
    for m in data['Slot']:
        name = m[0]
        if name in dc.keys():
            dc[name].append({'slot': idx})
        idx += 1

    lt = []
    lt.append('%s.DI_COUNT = %d;' % (HARDWARE_VAR, len(dc['DI'])))
    lt.append('%s.DO_COUNT = %d;' % (HARDWARE_VAR, len(dc['DO'])))
    for i in xrange(len(dc['AI'])):
        lt.append('%s.AI%d_SLOT = %d;' % (HARDWARE_VAR, i, dc['AI'][i]['slot']))

    for i in xrange(len(dc['AO'])):
        lt.append('%s.AI%d_SLOT = %d;' % (HARDWARE_VAR, i, dc['AO'][i]['slot']))

    c = ('\n').join(lt)
    lt = []
    for m in data['Alias']:
        channel = m[0]
        alias = m[1]
        commnt = m[2]
        if channel == '' or alias == '':
            pass
        else:
            lt.append('#define %s %s //%s' % (alias, channel, commnt))

    t = ('\n').join(lt)
    return (
     c, t)