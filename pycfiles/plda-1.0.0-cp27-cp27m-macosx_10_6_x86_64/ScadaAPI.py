# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\lib\ScadaAPI.py
# Compiled at: 2019-02-26 01:12:15
import os
from JsonClass import CJSON

class CProject:

    def __init__(self):
        self.varinfo = None
        return

    @classmethod
    def get_project_folder(cls, prjpath):
        if os.path.isdir(prjpath):
            return prjpath
        else:
            return os.path.dirname(prjpath)

    @classmethod
    def get_allvarinfo(cls, prjpath):
        pass

    def open_varfile(self, prjpath):
        if self.varinfo == None:
            _folder = self.get_project_folder(prjpath)
            filepath = _folder + '/DataAcquisition/Variable.config'
            objJSON = CJSON()
            data = objJSON.loadfile(filepath)
            if data['Index']['Revision'] != '2.0':
                return
            self.varinfo = {}
            for g in data['GS']:
                _gname = g['@N']
                if g.has_key('VS'):
                    self.varinfo.update(self._loadvariable(_gname, g))
                if g.has_key('GS'):
                    self.varinfo.update(self._loadgroup(_gname, g))

        return

    def _loadgroup(self, path, node):
        dc = {}
        for g in node['GS']:
            _gname = g['@N']
            if g.has_key('VS'):
                dc.update(self._loadvariable(path + '.' + _gname, g))
            if g.has_key('GS'):
                dc.update(self._loadgroup(path + '.' + _gname, g))

        return dc

    def _loadvariable(self, path, node):
        dc = {}
        for v in node['VS']:
            _var = self.loadvarinfo(v)
            _name = path + '.' + getattr(_var, 'name')
            dc[_name] = _var

        return dc

    def loadvarinfo(self, v):
        _name = v['@N']
        _dtype = v['@DT']
        _vtype = v['@VT']
        _cmmt = v['@D']
        v = VarInfo(_name, _cmmt, int(_dtype), int(_vtype))
        return v

    def close(self):
        del self.varinfo
        self.varinfo = None
        return

    def get_varinfo(self, var, param):
        kw = [
         'name', 'datatype', 'variabletype', 'comment']
        if var in self.varinfo.keys():
            if param in kw:
                return getattr(self.varinfo[var], param)
            else:
                return

        else:
            return
        return

    def print_var(self):
        if self.varinfo == None:
            return
        else:
            for v, item in self.varinfo.items():
                print '================================='
                print 'path:%s \nvar:%s' % (v, str(item))

            return


class VarInfo:

    def __init__(self, name, comment, datatype, variabletype):
        self.name = name
        self.datatype = datatype
        self.variabletype = variabletype
        self.comment = comment

    def __str__(self):
        txt = 'name:%s \ndatatype:%d \nvariabletype:%s \ncomment:%s' % (
         self.name, self.datatype, self.variabletype, self.comment)
        return txt


class CVariable:

    def __init__(self, filepath):
        if os.path.exists(filepath) == False:
            self.data = self.CreateEmpty(filepath)
        else:
            objJSON = CJSON()
            self.data = objJSON.loadfile(filepath)
        self.file = filepath

    def CreateEmpty(self, filepath):
        dc = {}
        dc['Index'] = {}
        dc['Index']['Revision'] = '2.0'
        dc['GS'] = []
        return dc

    def Save(self):
        objJSON = CJSON()
        objJSON.writefile(self.data, self.file)

    def find_group(self, lt):
        root = self.data
        node = root
        for k in lt:
            k = k.strip()
            k = k.replace('[', '_')
            k = k.replace(']', '')
            if node.has_key('GS') == False:
                node['GS'] = []
                node = self.AddGroup(node['GS'], k)
            else:
                node = node['GS']
                bfind = 0
                for aj_group in node:
                    if aj_group['@N'] == k:
                        node = aj_group
                        bfind = 1
                        break

                if bfind == 1:
                    continue
                else:
                    node = self.AddGroup(node, k)

        return node

    def find_group_bypath(self, path=''):
        if path == '':
            return
        else:
            paths = path.split('.')
            if len(paths) == 1:
                lt = paths
                return self.find_group(paths)
            if len(paths) > 1:
                return self.find_group(paths[:-1])
            return

    def AddGroup(self, node, name):

        def createnode():
            dc = {}
            dc['@N'] = name
            dc['@D'] = ''
            dc['@OI'] = ''
            return dc

        node1 = createnode()
        node.append(node1)
        return node1

    def AddVariable(self, node, name, datatype, device='', block='', addr='', cmt='', vartype='1'):
        u"""
        添加变量
        :param node:组节点
        :param name: 名称
        :param datatype: 数据类型
        :param device: 设备名称
        :param block: 数据库名称
        :param addr: 地址
        :param cmt: 描述
        :return:
        """
        dc = {}
        dc['@N'] = name
        dc['@D'] = cmt
        dc['@DN'] = device
        dc['@AD'] = block + '.' + str(addr)
        dc['@DT'] = self.get_scada_datatype(datatype)
        dc['@VT'] = vartype
        dc['@ODT'] = self.get_scada_datatype(datatype)
        dc['@OI'] = ''
        dc['@PCS'] = 4
        dc['@UNIT'] = ''
        dc['@IV'] = '0'
        dc['@LV'] = ''
        dc['ACV'] = self.set_variable_ACV()
        dc['WP'] = self.set_variable_WP()
        dc['CVT'] = self.set_variable_CVT()
        dc['@AUTH'] = self.set_variable_AUTH()
        if node.has_key('VS') == False:
            node['VS'] = []
        idx = -1
        for i in xrange(len(node['VS'])):
            var = node['VS'][i]
            if var['@N'] == name:
                idx = i

        if idx >= 0:
            node['VS'].pop(idx)
        node['VS'].append(dc)

    def edit_variable_wp(self, node, min, max):
        node['WP']['@WMIV'] = str(min)
        node['WP']['@WMAV'] = str(max)

    def edit_variable_decimal(self, node, decimal):
        node['@PCS'] = int(decimal)

    def edit_variable_unit(self, node, unit):
        node['@UNIT'] = str(unit)

    def find_var(self, varpath):
        lt = varpath.split('.')
        if len(lt) > 1:
            node = self.find_group(lt[:-1])['VS']
        else:
            node = self.data['VS']
        varname = lt[(-1)]
        for var in node:
            if var['@N'] == varname:
                return var

        return

    def set_variable_ACV(self):
        dc = {}
        dc['@AM'] = '0'
        dc['@AR'] = '0'
        dc['@AI'] = '1'
        dc['@ATP'] = '360'
        return dc

    def set_variable_WP(self):
        dc = {}
        dc['@EW'] = '1'
        dc['@EWP'] = '1'
        dc['@WMAV'] = ''
        dc['@WMIV'] = ''
        dc['@ELP'] = '1'
        return dc

    def set_variable_CVT(self):
        dc = {}
        dc['@CT'] = '0'
        dc['@ELC'] = '0'
        dc['@OI'] = ''
        dc['@PMAV'] = '0'
        dc['@PMIV'] = '0'
        dc['@OMAV'] = '0'
        dc['@OMIV'] = '0'
        return dc

    def set_variable_ATS(self):
        lt = []
        dc = {}
        dc['@EL'] = '0'
        dc['@PM'] = '0'
        dc['@ST'] = '1'
        dcID = {}
        dcID['@N'] = ''
        dcID['@OT'] = '2'
        dcID['@T'] = '4'
        dc['@ID'] = dcID
        lt.append(dc)
        return lt

    def set_variable_AUTH(self):
        lt = []
        dc = {}
        dc['@EL'] = 0
        dc['@PM'] = 0
        dc['@ST'] = 1
        dc['OKI'] = {}
        dc['OKI']['@Comment'] = ''
        dc['OKI']['@N'] = ''
        dc['OKI']['@OT'] = 2
        dc['OKI']['@T'] = 41
        lt.append(dc)
        return lt

    def get_scada_datatype(self, aj_type):
        dc = {}
        dc['BOOL'] = '0'
        dc['INT'] = '3'
        dc['WORD'] = '4'
        dc['DINT'] = '5'
        dc['DWORD'] = '6'
        dc['FLOAT'] = '9'
        dc['REAL'] = '9'
        dc['LREAL'] = '10'
        dc['TIME'] = '5'
        return dc[aj_type]


class CDriver:

    def __init__(self, filepath):
        if os.path.exists(filepath) == False:
            self.data = self.CreateEmpty(filepath)
        else:
            objJSON = CJSON()
            self.data = objJSON.loadfile(filepath)
        self.file = filepath

    def CreateEmpty(self, filepath):
        dc = {}
        dc['DEVS'] = []
        return dc

    def CreateDriver(self, drvtype, name, ip):

        def MindTechPLC(drv):
            drv['@DRV'] = 'MD.RTDB.Drivers.MindTechPLCC'
            drv['Name'] = name
            drv['Description'] = ''
            drv['Enabled'] = '1'
            drv['CommType'] = 'TCP'
            drv['CommParameter'] = 'Client,%s,1025,,' % ip
            drv['ReplyTimeOut'] = '1000'
            drv['Retries'] = '3'
            drv['DataBlocks'] = []

        def ModBusTCP(drv):
            drv['@DRV'] = 'MD.RTDB.Drivers.ModBusTCPC'
            drv['Name'] = name
            drv['Description'] = ''
            drv['Enabled'] = '1'
            drv['CommType'] = 'TCP'
            drv['CommParameter'] = 'Client,%s,502,,' % ip
            drv['ReplyTimeOut'] = '1000'
            drv['Retries'] = '3'
            drv['DataBlocks'] = []

        idx = self._find_drv(name)
        if idx >= 0:
            self.data['DEVS'].pop(idx)
        drv = {}
        if drvtype == 'MindTechPLC':
            MindTechPLC(drv)
        elif drvtype == 'ModBusTCP':
            ModBusTCP(drv)
        else:
            return 0
        self.data['DEVS'].append(drv)

    def _find_drv(self, name):
        for i in xrange(len(self.data['DEVS'])):
            obj = self.data['DEVS'][i]
            if obj['Name'] == name:
                return i

        return -1

    def AddBlock(self, drvname, drvtype, blkname, regtype, saddr, eaddr):

        def ModBusTCP(drv):
            blk = {}
            blk['Name'] = blkname
            blk['Description'] = ''
            blk['Enabled'] = '1'
            blk['PollRate'] = '1000'
            blk['RegisterType'] = regtype
            blk['StartAddress'] = str(saddr)
            blk['EndAddress'] = str(eaddr)
            drv['DataBlocks'].append(blk)

        def MindTechPLC(drv):
            if len(drv['DataBlocks']) == 0:
                blk = {}
                blk['Name'] = blkname
                blk['Description'] = ''
                blk['Enabled'] = '1'
                blk['PollRate'] = '1000'
                blk['Registers'] = []
                drv['DataBlocks'].append(blk)
            else:
                blk = drv['DataBlocks'][0]
            regs = {}
            regs['RegisterType'] = regtype
            regs['StartAddress'] = str(saddr)
            regs['EndAddress'] = str(eaddr)
            blk['Registers'].append(regs)

        idx = self._find_drv(drvname)
        if idx >= 0:
            drv = self.data['DEVS'][idx]
        else:
            return -1
        if drvtype == 'MindTechPLC':
            MindTechPLC(drv)
        elif drvtype == 'ModBusTCP':
            ModBusTCP(drv)

    def Save(self):
        objJSON = CJSON()
        objJSON.writefile(self.data, self.file)


class CRecipe:
    template = '{"Authorize":[{"@EL":0,"@OKI":{"@Comment":"","@N":"","@OT":5,"@T":65},"@PM":0,"@ST":1,"InspectorGroupArray":[],"WorkerGroupArray":[]},{"@EL":1,"@OKI":{"@Comment":"","@N":"","@OT":5,"@T":66},"@PM":1,"@ST":1,"InspectorGroupArray":[],"WorkerGroupArray":[]},{"@EL":0,"@OKI":{"@Comment":"","@N":"","@OT":5,"@T":67},"@PM":0,"@ST":1,"InspectorGroupArray":[],"WorkerGroupArray":[]},{"@EL":0,"@OKI":{"@Comment":"","@N":"","@OT":5,"@T":68},"@PM":0,"@ST":1,"InspectorGroupArray":[],"WorkerGroupArray":[]},{"@EL":0,"@OKI":{"@Comment":"","@N":"","@OT":5,"@T":69},"@PM":0,"@ST":1,"InspectorGroupArray":[],"WorkerGroupArray":[]}],"Download":{"IsCheckCompletionOnVariableChanged":0,"IsNotFixedValue":0,"IsOnlyDiffValue":1,"Pattern":0,"Retrys":4,"Timeout":2,"VariablePacketSize":50},"VariableArray":[]}'

    def __init__(self, folder):
        self.prjfolder = folder + '/Formula'

    def AddGroup(self, name):
        path = self.prjfolder + '/' + name
        if os.path.exists(path):
            os.makedirs(path)

    def AddRecipe(self, groupname, rcpname, ltvar):
        filepath = ''
        if os.path.exists(self.prjfolder + '/' + groupname) == False:
            curcwd = os.getcwd()
            os.chdir(self.prjfolder)
            os.mkdir(groupname)
            os.chdir(curcwd)
        objJSON = CJSON()
        data = objJSON.loadstr(self.template)
        for var in ltvar:
            dc = {}
            dc['Key'] = var
            dc['Value'] = ''
            data['VariableArray'].append(dc)

        filepath = self.prjfolder + '/' + groupname + '/' + rcpname + '.formula'
        objJSON.writefile(data, filepath)

    def AddRecipeValue(self, groupname, rcpname, ltvar, ltval):
        filepath = ''
        if os.path.exists(self.prjfolder + '/' + groupname) == False:
            curcwd = os.getcwd()
            os.chdir(self.prjfolder)
            os.mkdir(groupname)
            os.chdir(curcwd)
        objJSON = CJSON()
        data = objJSON.loadstr(self.template)
        for i in range(len(ltvar)):
            dc = {}
            dc['Key'] = ltvar[i]
            dc['Value'] = str(ltval[i])
            data['VariableArray'].append(dc)

        filepath = self.prjfolder + '/' + groupname + '/' + rcpname + '.formula'
        objJSON.writefile(data, filepath)


class DataBase:

    def __init__(self, folder=''):
        self.dbsource = CDataSource(folder + '/Database.config')
        self.table = CTableModel(folder + '/TableModel.config')

    def create_histable(self, name, ltvar, varinfo):
        self.table.CreateHisTable(name, ltvar, varinfo)

    def create_dbsource(self, name, dbtype):
        tbs = self.table.copy_alltabel_to_source()
        self.dbsource.Append(name, dbtype, tbs)

    def save(self):
        self.table.save()
        self.dbsource.save()


class CTableModel:
    TYPE_LENTH = {1: 1, 
       2: 2, 
       3: 2, 
       4: 4, 
       5: 4, 
       6: 8, 
       7: 8, 
       8: 8, 
       9: 8, 
       10: 8, 
       11: 8, 
       12: 250}

    def __init__(self, filepath):
        if os.path.exists(filepath) == False:
            self.data = self.CreateEmpty()
        else:
            objJSON = CJSON()
            self.data = objJSON.loadfile(filepath)
        self.file = filepath

    def CreateEmpty(self):
        dc = {}
        _table = 'AlertFieldGroup'
        dc[_table] = {}
        dc[_table]['Name'] = 'AlarmDataGroup'
        dc[_table]['Note'] = 'AlarmDataGroup'
        dc[_table]['Permited'] = False
        dc[_table]['Revision'] = '2.0'
        dc[_table]['FieldArray'] = []
        _table = 'LogFieldGroup'
        dc[_table] = {}
        dc[_table]['Name'] = 'LogDataGroup'
        dc[_table]['Note'] = 'LogDataGroup'
        dc[_table]['Permited'] = False
        dc[_table]['Revision'] = '2.0'
        dc[_table]['FieldArray'] = []
        _table = 'HistoryFieldGroup'
        dc[_table] = []
        return dc

    def CreateHisTable(self, name, ltvar, varinfo):
        dc = {}
        dc['Name'] = name
        dc['Note'] = ''
        dc['Permited'] = False
        dc['Revision'] = '2.0'
        dc['FieldArray'] = []
        dc['FieldArray'].append(self._create_field('RecordTime', '记录时间', 11, True))
        dc['FieldArray'].append(self._create_field('RecordTimeMS', '记录时间毫秒', 5, True))
        for v in ltvar:
            if varinfo.has_key(v) == False:
                raise Exception('Missing variable!')
            else:
                dc['FieldArray'].append(self._create_field(varinfo[v].name, varinfo[v].comment, varinfo[v].datatype, False))

        self.data['HistoryFieldGroup'].append(dc)

    def _create_field(self, var, cmmt, datatype, isdefault=False):
        dc = {}
        dc['IsSystemField'] = isdefault
        dc['Name'] = var
        dc['Note'] = cmmt
        dc['Type'] = datatype
        dc['Value'] = ''
        return dc

    def copy_alltabel_to_source(self):
        lttab = []
        lttab.append(self.copy_table_to_source(self.data['AlertFieldGroup']))
        lttab.append(self.copy_table_to_source(self.data['LogFieldGroup']))
        for his in self.data['HistoryFieldGroup']:
            lttab.append(self.copy_table_to_source(his))

        return lttab

    def copy_table_to_source(self, data):
        ndc = {}
        ndc['Name'] = data['Name']
        ndc['Note'] = data['Note']
        ndc['FieldGroupName'] = data['Name']
        ndc['Permited'] = data['Permited']
        ndc['FieldArray'] = self.copy_filed(data['FieldArray'])
        return ndc

    def copy_filed(self, data):
        lt = []
        for field in data:
            dc = {}
            _type = field['Type']
            _name = field['Name']
            _note = field['Note']
            _lenth = self.TYPE_LENTH[_type]
            dc['Name'] = _name
            dc['NameInFieldGroup'] = _name
            dc['Note'] = _note
            dc['Type'] = _type
            dc['TypeInFieldGroup'] = _type
            dc['Length'] = _lenth
            dc['IsNULLPermited'] = True
            dc['IsPrimaryKey'] = False
            lt.append(dc)

        return lt

    def save(self):
        objJSON = CJSON()
        objJSON.writefile(self.data, self.file)


class CDataSource:

    def __init__(self, filepath):
        if os.path.exists(filepath) == False:
            self.data = self.CreateEmpty()
        else:
            objJSON = CJSON()
            self.data = objJSON.loadfile(filepath)
        self.file = filepath

    def CreateEmpty(self):
        dc = {}
        dc['DataSourceArray'] = []
        return dc

    def Append(self, name, dbtype='sql', tables=[]):
        dc = {}
        dc['Name'] = name
        dc['Note'] = ''
        dc['Permited'] = True
        dc['TableArray'] = []
        dc['TablePrefix'] = ''
        dc['IsCheck1Permited'] = False
        dc['IsCheck2Permited'] = False
        dc['IsCreateDataBasePermited'] = False
        dc['IsCreateDefaultTablePermited'] = True
        dc['IsTablePrefixPermited'] = False
        dc['IsTableVisible'] = True
        dbtype = dbtype.lower()
        if dbtype == 'sql':
            dc['DatabaseParam'] = self._create_sql_param(name)
        else:
            dc['DatabaseParam'] = {}
        dc['TableArray'] = tables

    def _create_sql_param(self, name):
        dc = {}
        dc['Type'] = 0
        dc['Host'] = '127.0.0.1'
        dc['ServerPort'] = '1433'
        dc['Name'] = name
        dc['Path'] = '@ProjectPath/database/'
        dc['OperationTimeout'] = 3000
        dc['User'] = 'sa'
        dc['Password'] = '123'
        return dc

    def save(self):
        objJSON = CJSON()
        objJSON.writefile(self.data, self.file)


if __name__ == '__main__':
    p = CProject()
    p.open_varfile('D:/Work/Project/2019年开发项目/reny_CovertedToMind/test/test.ipro')
    p.print_var()