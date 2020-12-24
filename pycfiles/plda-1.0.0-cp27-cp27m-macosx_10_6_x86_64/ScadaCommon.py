# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\lib\ScadaCommon.py
# Compiled at: 2019-02-25 21:47:28
from lib.JsonClass import CJSON
from lib.File import FSO
import os, copy, random, wx

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


class CGDI_RecipeGrid:

    def __init__(self):
        self.template = '{"CNSDrawRecipeGrid":{"ItemDataArray":[]},"DrawObj":{"Data":{"Rect":{"Bottom":507,"Left":76,"Right":657,"Top":84}},"ExpManager":{"List":[]},"Layer":0,"Locked":false,"Name":"recipe1","ShowSelectedFrame":false,"SupportGroupEvent":false,"SupportHidedEvent":false,"ToolTip":"","Visible":true},"DrawWidget":{},"Type":32}'

    def create(self):
        objJSON = CJSON()
        return objJSON.loadstr(self.template)

    def SetRowNum(self, ctrl, num):
        ctrl['CNSDrawRecipeGrid']['RowCount'] = num

    def SetColNum(self, ctrl, num):
        ctrl['CNSDrawRecipeGrid']['ColumnCount'] = num

    def findCell(self, ctrl, row, col):
        for i in range(len(ctrl['CNSDrawRecipeGrid']['ItemDataArray'])):
            cell = ctrl['CNSDrawRecipeGrid']['ItemDataArray'][i]
            if cell['RowIdx'] == row and cell['ColumnIdx'] == col:
                return i

        return -1

    def AddText(self, ctrl, row, col, txt):
        dc = {}
        dc['RowIdx'] = row
        dc['ColumnIdx'] = col
        dc['DisplayRole'] = txt
        dc['OriginText'] = txt
        dc['Editable'] = False
        dc['ItemType'] = 1001
        if ctrl['CNSDrawRecipeGrid'].has_key('ItemDataArray') == False:
            ctrl['CNSDrawRecipeGrid']['ItemDataArray'] = []
        ctrl['CNSDrawRecipeGrid']['ItemDataArray'].append(dc)

    def EditText(self, ctrl, row, col, txt):
        idx = self.findCell(ctrl, row, col)
        if idx == -1:
            self.AddText(ctrl, row, col, txt)
        else:
            dc = copy.deepcopy(ctrl['CNSDrawRecipeGrid']['ItemDataArray'][idx])
            dc['RowIdx'] = row
            dc['ColumnIdx'] = col
            dc['DisplayRole'] = txt
            dc['OriginText'] = txt
            dc['Editable'] = False
            dc['ItemType'] = 1001
            ctrl['CNSDrawRecipeGrid']['ItemDataArray'][idx] = dc

    def AddRealVar(self, ctrl, row, col, var, decimal=0, bEdit=True, bCheck=False, ckmin=0, ckmax=100):
        dc = {}
        dc['RowIdx'] = row
        dc['ColumnIdx'] = col
        dc['DataSource'] = 1
        dc['DecimalCount'] = decimal
        dc['DisplayRole'] = var
        dc['Editable'] = bEdit
        dc['ItemType'] = 1001
        dc['MinValue'] = ckmin
        dc['MaxValue'] = ckmax
        dc['VRCheckable'] = bCheck
        if ctrl['CNSDrawRecipeGrid'].has_key('IteItemDataArraym') == False:
            ctrl['CNSDrawRecipeGrid']['IteItemDataArraym'] = []
        ctrl['CNSDrawRecipeGrid']['ItemDataArray'].append(dc)

    def EditRealVar(self, ctrl, row, col, var, decimal=0, bEdit=True, bCheck=False, ckmin=0, ckmax=100):
        idx = self.findCell(ctrl, row, col)
        if idx == -1:
            self.AddRealVar(ctrl, row, col, var, decimal, bEdit, bCheck, ckmin, ckmax)
        else:
            dc = copy.deepcopy(ctrl['CNSDrawRecipeGrid']['ItemDataArray'][idx])
            dc['RowIdx'] = row
            dc['ColumnIdx'] = col
            dc['DataSource'] = 1
            dc['DecimalCount'] = decimal
            dc['DisplayRole'] = var
            dc['Editable'] = bEdit
            dc['ItemType'] = 1001
            dc['MinValue'] = ckmin
            dc['MaxValue'] = ckmax
            dc['VRCheckable'] = bCheck
            ctrl['CNSDrawRecipeGrid']['ItemDataArray'][idx] = dc

    def AddRecipeVar(self, ctrl, row, col, recipe, var, decimal=0, bEdit=True, bCheck=False, ckmin=0, ckmax=100):
        dc = {}
        dc['RowIdx'] = row
        dc['ColumnIdx'] = col
        dc['DataSource'] = 2
        dc['DecimalCount'] = decimal
        dc['RecipeName'] = recipe
        dc['DisplayRole'] = var
        dc['Editable'] = bEdit
        dc['ItemType'] = 1001
        dc['MinValue'] = ckmin
        dc['MaxValue'] = ckmax
        dc['VRCheckable'] = bCheck
        ctrl['CNSDrawRecipeGrid']['ItemDataArray'].append(dc)

    def EditRecipeVar(self, ctrl, row, col, recipe, var, decimal=0, bEdit=True, bCheck=False, ckmin=0, ckmax=100):
        idx = self.findCell(ctrl, row, col)
        if idx == -1:
            self.AddRealVar(ctrl, row, col, recipe, var, decimal, bEdit, bCheck, ckmin, ckmax)
        else:
            dc = copy.deepcopy(ctrl['CNSDrawRecipeGrid']['ItemDataArray'][idx])
            dc['RowIdx'] = row
            dc['ColumnIdx'] = col
            dc['DataSource'] = 2
            dc['DecimalCount'] = decimal
            dc['RecipeName'] = recipe
            dc['DisplayRole'] = var
            dc['Editable'] = bEdit
            dc['ItemType'] = 1001
            dc['MinValue'] = ckmin
            dc['MaxValue'] = ckmax
            dc['VRCheckable'] = bCheck
            ctrl['CNSDrawRecipeGrid']['ItemDataArray'][idx] = dc


class CGDI:

    def __init__(self):
        self.emptygdi = '{"Environment":{"BrushManager":{"BrushManager":{"Angle":0,"Color":4290822336,"ImageName":"","Position":0,"Stops":[{"First":0,"Second":4278190080},{"First":1,"Second":4294901760}],"Type":1}},"CloseActions":{"List":[]},"CloseSecurity":{"@EL":false,"@PM":0,"@ST":1,"ID":{"@N":"","@OT":3,"@T":82},"OperatorGroupList":[],"VerifierGroupList":[]},"DefaultLayer":0,"ExpManager":{"List":[]},"FormType":0,"FullScreen":true,"HasFrame":true,"LockedLayers":[false,false,false,false,false,false,false,false,false,false],"MouseDownActions":{"List":[]},"MouseUpActions":{"List":[]},"Objs":[],"OpenActions":{"List":[]},"OpenSecurity":{"@EL":false,"@PM":0,"@ST":1,"ID":{"@N":"","@OT":3,"@T":81},"OperatorGroupList":[],"VerifierGroupList":[]},"PrintBottom":5,"PrintDateFormat":"yyyy-MM-dd","PrintFooter":8,"PrintHeader":8,"PrintLeft":5,"PrintLeftFooter":"","PrintLeftHeader":"","PrintMiddleFooter":"","PrintMiddleHeader":"","PrintRight":5,"PrintRightFooter":"","PrintRightHeader":"","PrintTimeFormat":"hh:mm:ss","PrintTop":5,"Rect":{"Bottom":599,"Left":0,"Right":799,"Top":0},"RightMouseDonwActions":{"List":[]},"RightMouseUpActions":{"List":[]},"ScriptCode":"","Text":"","VisibleLayers":[true,true,true,true,true,true,true,true,true,true]},"Head":{"Version":1}}'

    def ctrlname(self):
        lt = []
        for i in range(0, 10):
            asc = random.randint(65, 90)
            lt.append(chr(asc))

        return ('').join(lt)

    def CreateGDI(self, data, path):
        objJSON = CJSON()
        objJSON.writefile(data, path)

    def newGDI(self):
        objJSON = CJSON()
        return objJSON.loadstr(self.emptygdi)

    def loadGDI(self, filepath):
        objJSON = CJSON()
        return objJSON.loadfile(filepath)

    def loadBlock(self, filepath):
        objJSON = CJSON()
        return objJSON.loadfile(filepath)

    def loadBlock(self, txt):
        objJSON = CJSON()
        return objJSON.loadstr(txt)

    def AddCtrl(self, gdi, ctrl, x, y):
        d = copy.deepcopy(ctrl)
        gdi['Environment']['Objs'].append(self.moveBlock(d, x, y))

    def AddCtrl_nomove(self, gdi, ctrl):
        d = copy.deepcopy(ctrl)
        gdi['Environment']['Objs'].append(d)

    def moveCtrl(self, ctrl, xoffset, yoffset):
        ctrl['DrawObj']['Data']['Rect']['Bottom'] += yoffset
        ctrl['DrawObj']['Data']['Rect']['Top'] += yoffset
        ctrl['DrawObj']['Data']['Rect']['Left'] += xoffset
        ctrl['DrawObj']['Data']['Rect']['Right'] += xoffset
        ctrl['DrawObj']['Name'] = self.ctrlname()
        if ctrl['Type'] == 12 or ctrl['Type'] == 9:
            for node in ctrl['DrawNode']['Nodes']:
                node['node']['X'] += xoffset
                node['node']['Y'] += yoffset

        if ctrl['Type'] == 0:
            for son in ctrl['DrawMulti']['ObjList']:
                self.moveCtrl(son, xoffset, yoffset)

    def moveBlock(self, ctrl, x, y):
        ox = ctrl['DrawObj']['Data']['Rect']['Left']
        oy = ctrl['DrawObj']['Data']['Rect']['Top']
        ex = x - ox
        ey = y - oy
        ctrl['DrawObj']['Data']['Rect']['Bottom'] += ey
        ctrl['DrawObj']['Data']['Rect']['Top'] += ey
        ctrl['DrawObj']['Data']['Rect']['Left'] += ex
        ctrl['DrawObj']['Data']['Rect']['Right'] += ex
        ctrl['DrawObj']['Name'] = self.ctrlname()
        if ctrl.has_key('DrawMulti'):
            for son in ctrl['DrawMulti']['ObjList']:
                self.moveCtrl(son, ex, ey)

        else:
            self.moveCtrl(ctrl, ex, ey)
        return ctrl

    def output(self, data):
        objJSON = CJSON()
        return objJSON.outputjson_min(data)

    def find_ctrl(self, dw, name):
        for ctrl in dw['Environment']['Objs']:
            if ctrl['Type'] != 0:
                if ctrl['DrawObj']['Name'] == name:
                    return ctrl
            else:
                if ctrl['DrawObj']['Name'] == name:
                    return ctrl
                else:
                    return self.find_ctrl_ingroup(ctrl['DrawMulti']['ObjList'], name)

        return

    def find_ctrl_ingroup(self, group, name):
        for ctrl in group:
            if ctrl['Type'] != 0:
                if ctrl['DrawObj']['Name'] == name:
                    return ctrl
            else:
                if ctrl['DrawObj']['Name'] == name:
                    return ctrl
                res = self.find_ctrl_ingroup(ctrl['DrawMulti']['ObjList'], name)
                if res != None:
                    return res

        return

    def set_group_size(self, group, w, h):
        pass

    def set_ctrl_text(self, ctrl, txt):
        ctrl['DrawText']['Text'] = txt

    def set_ctrl_itemlist(self, ctrl, list):
        ctrl['DrawComboBox']['ItemAdd'] = list


class CVar:

    def __init__(self, driver):
        self.driver = driver

    def Set_SCADA_Variable(self, ltcsv):
        dcTab = self.create_new_variabletab()
        for i in range(0, len(ltcsv)):
            aj_name = ltcsv[i][0]
            aj_type = ltcsv[i][1]
            aj_addr = ltcsv[i][2]
            aj_block = ltcsv[i][3]
            aj_comment = ltcsv[i][5]
            path = aj_name.split('.')
            node = self.find_and_create_scada_node(dcTab, path[:-1])
            if node.has_key('VS') == False:
                node['VS'] = []
            node = node['VS']
            self.add_new_variable(node, path[(-1)], aj_type, 'PLC', aj_addr, aj_block, ltcsv, aj_comment)

        return dcTab

    def find_and_create_scada_node(self, root, lt):
        node = root
        for k in lt:
            k = k.strip()
            k = k.replace('[', '_')
            k = k.replace(']', '')
            if node.has_key('GS') == False:
                node['GS'] = []
                node = self.add_new_group(node['GS'], k)
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
                    node = self.add_new_group(node, k)

        return node

    def create_new_variabletab(self):
        dc = {}
        dc['H'] = {}
        dc['H']['V'] = '1'
        dc['H']['Type'] = 'VariableConfig'
        dc['GS'] = []
        return dc

    def add_new_group(self, gslt, name, cmt=''):
        dc = {}
        dc['@N'] = name
        dc['@D'] = cmt
        dc['@PI'] = ''
        gslt.append(dc)
        return gslt[(len(gslt) - 1)]

    def add_new_variable(self, vslt, name, datatype, device, addr, block, ltinfo, cmt=''):
        if self.driver == 'MODBUS':
            addr = addr + 1 + 40000
        elif self.driver == 'CODESYS':
            addr = addr
        dcVar = self.set_variable_general(name, datatype, device, addr, block, cmt)
        vslt.append(dcVar)

    def set_variable_general(self, name, datatype, device, addr, block, cmt=''):
        dc = {}
        name = name.strip()
        name = name.replace('[', '_')
        name = name.replace(']', '')
        dc['@N'] = name
        dc['@D'] = cmt
        dc['@DN'] = device
        dc['@AD'] = block + '.' + str(addr)
        dc['@DT'] = self.get_scada_datatype(datatype)
        dc['@VT'] = '1'
        dc['@ODT'] = self.get_scada_datatype(datatype)
        dc['@OI'] = ''
        dc['@PCS'] = 4
        dc['@UNIT'] = ''
        dc['@IV'] = '0'
        dc['@LV'] = ''
        dc['ACV'] = self.set_variable_ACV()
        dc['WP'] = self.set_variable_WP()
        dc['CVT'] = self.set_variable_CVT()
        dc['ATS'] = self.set_variable_ATS()
        return dc

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

    def get_scada_datatype(self, aj_type):
        dc = {}
        dc['BOOL'] = '0'
        dc['INT'] = '5'
        dc['WORD'] = '6'
        dc['DINT'] = '5'
        dc['DWORD'] = '6'
        dc['REAL'] = '9'
        dc['LREAL'] = '10'
        dc['TIME'] = '5'
        return dc[aj_type]


class CDataGroup:

    def __init__(self):
        self.template = '{"DataGroup":{"description":"","enable":false,"items":[{"DataItem":{"description":"记录时间","fixed":true,"name":"RecordTime","varData":"","varType":11,"version":1}},{"DataItem":{"description":"记录时间毫秒","fixed":true,"name":"RecordTimeMS","varData":"","varType":5,"version":1}}],"name":"xxxxx","version":1}}'
        self.tempsource = '{"DataSource":{"DBParam":{"Version":"1","cmdTimeOut":3000,"dbHost":"","dbName":"","dbPassword":"","dbPath":"","dbServerPort":-1,"dbType":0,"dbUser":""},"DataTables":[{"DataTable":{"dataGroupName":"AlarmDataGroup","description":"AlarmDataGroup","enable":false,"fields":[{"DataField":{"dataItemName":"ID","dataType":12,"description":"ID","enableNull":true,"itemType":12,"name":"ID","primarykey":false,"size":250}},{"DataField":{"dataItemName":"Name","dataType":12,"description":"名称","enableNull":true,"itemType":12,"name":"Name","primarykey":false,"size":250}},{"DataField":{"dataItemName":"Message","dataType":12,"description":"消息","enableNull":true,"itemType":12,"name":"Message","primarykey":false,"size":250}},{"DataField":{"dataItemName":"AlarmLevel","dataType":12,"description":"报警等级","enableNull":true,"itemType":12,"name":"AlarmLevel","primarykey":false,"size":250}},{"DataField":{"dataItemName":"StartValue","dataType":12,"description":"发生值","enableNull":true,"itemType":12,"name":"StartValue","primarykey":false,"size":250}},{"DataField":{"dataItemName":"EndValue","dataType":12,"description":"结束值","enableNull":true,"itemType":12,"name":"EndValue","primarykey":false,"size":250}},{"DataField":{"dataItemName":"StartTime","dataType":11,"description":"发生时间","enableNull":true,"itemType":11,"name":"StartTime","primarykey":false,"size":8}},{"DataField":{"dataItemName":"StartTimeMS","dataType":5,"description":"发生时间毫秒","enableNull":true,"itemType":5,"name":"StartTimeMS","primarykey":false,"size":4}},{"DataField":{"dataItemName":"EndTime","dataType":11,"description":"结束时间","enableNull":true,"itemType":11,"name":"EndTime","primarykey":false,"size":8}},{"DataField":{"dataItemName":"EndTimeMS","dataType":5,"description":"结束时间毫秒","enableNull":true,"itemType":5,"name":"EndTimeMS","primarykey":false,"size":4}},{"DataField":{"dataItemName":"ConfirmTime","dataType":11,"description":"确认时间","enableNull":true,"itemType":11,"name":"ConfirmTime","primarykey":false,"size":8}},{"DataField":{"dataItemName":"ConfirmTimeMS","dataType":5,"description":"确认时间毫秒","enableNull":true,"itemType":5,"name":"ConfirmTimeMS","primarykey":false,"size":4}},{"DataField":{"dataItemName":"Status","dataType":5,"description":"状态","enableNull":true,"itemType":5,"name":"Status","primarykey":false,"size":4}},{"DataField":{"dataItemName":"CurrentUser","dataType":12,"description":"当前用户","enableNull":true,"itemType":12,"name":"CurrentUser","primarykey":false,"size":250}},{"DataField":{"dataItemName":"ForeColor","dataType":10,"description":"前景色","enableNull":true,"itemType":10,"name":"ForeColor","primarykey":false,"size":8}},{"DataField":{"dataItemName":"BackColor","dataType":10,"description":"背景色","enableNull":true,"itemType":10,"name":"BackColor","primarykey":false,"size":8}}],"name":"AlarmDataGroup","version":1}},{"DataTable":{"dataGroupName":"LogDataGroup","description":"LogDataGroup","enable":false,"fields":[{"DataField":{"dataItemName":"RecordTime","dataType":11,"description":"记录时间","enableNull":true,"itemType":11,"name":"RecordTime","primarykey":false,"size":8}},{"DataField":{"dataItemName":"RecordTimeMS","dataType":5,"description":"记录时间毫秒","enableNull":true,"itemType":5,"name":"RecordTimeMS","primarykey":false,"size":4}},{"DataField":{"dataItemName":"CurrentUser","dataType":12,"description":"当前用户","enableNull":true,"itemType":12,"name":"CurrentUser","primarykey":false,"size":250}},{"DataField":{"dataItemName":"Message","dataType":12,"description":"消息","enableNull":true,"itemType":12,"name":"Message","primarykey":false,"size":250}},{"DataField":{"dataItemName":"Type","dataType":5,"description":"对象类型","enableNull":true,"itemType":5,"name":"Type","primarykey":false,"size":4}},{"DataField":{"dataItemName":"Name","dataType":12,"description":"对象名称","enableNull":true,"itemType":12,"name":"Name","primarykey":false,"size":250}},{"DataField":{"dataItemName":"ProtectMode","dataType":5,"description":"保护模式","enableNull":true,"itemType":5,"name":"ProtectMode","primarykey":false,"size":4}},{"DataField":{"dataItemName":"Operater","dataType":12,"description":"操作者","enableNull":true,"itemType":12,"name":"Operater","primarykey":false,"size":250}},{"DataField":{"dataItemName":"OperateTime","dataType":11,"description":"操作时间","enableNull":true,"itemType":11,"name":"OperateTime","primarykey":false,"size":8}},{"DataField":{"dataItemName":"Verifier","dataType":12,"description":"校验者","enableNull":true,"itemType":12,"name":"Verifier","primarykey":false,"size":250}},{"DataField":{"dataItemName":"VerifyTime","dataType":11,"description":"校验时间","enableNull":true,"itemType":11,"name":"VerifyTime","primarykey":false,"size":8}},{"DataField":{"dataItemName":"OperateComment","dataType":12,"description":"操作说明","enableNull":true,"itemType":12,"name":"OperateComment","primarykey":false,"size":250}},{"DataField":{"dataItemName":"VerifyComment","dataType":12,"description":"校验说明","enableNull":true,"itemType":12,"name":"VerifyComment","primarykey":false,"size":250}}],"name":"LogDataGroup","version":1}}],"createDefaultTable":true,"dataTablePrefix":"","description":"","enable":false,"enableCreateDataBase":false,"enableDataTablePrefix":false,"enableVerificationA":false,"enableVerificationB":false,"name":"xxxxxxxx","showTable":true}}'
        self.dataGroup = {}
        self.path = ''

    def equaltosource(self, name, filepath):
        src = {}
        src['DataSources'] = []
        s1 = self._create_source()
        s1['DataSource']['name'] = name
        src['DataSources'].append(s1)
        tables = []
        tables.append(self.dataGroup['alarmDataGroup']['DataGroup'])
        tables.append(self.dataGroup['logDataGroup']['DataGroup'])
        for his in self.dataGroup['hisDataGroups']:
            tables.append(his['DataGroup'])

        for table in tables:
            t = self._create_datatable()
            t['DataTable']['name'] = table['name']
            t['DataTable']['dataGroupName'] = table['name']
            t['DataTable']['description'] = table['description']
            for item in table['items']:
                aj_des = item['DataItem']['description']
                aj_name = item['DataItem']['name']
                aj_type = item['DataItem']['varType']
                aj_field = self._create_field()
                aj_field['DataField']['datatype'] = aj_type
                aj_field['DataField']['itemType'] = aj_type
                aj_field['DataField']['dataItemName'] = aj_name
                aj_field['DataField']['name'] = aj_name
                aj_field['DataField']['description'] = aj_des
                t['DataTable']['fields'].append(aj_field)

            s1['DataSource']['DataTables'].append(t)

        objJSON = CJSON()
        objJSON.writefile(src, filepath)

    def _create_source(self):
        dc = {}
        dc['DataSource'] = {}
        dc['DataSource']['DBParam'] = {}
        dc['DataSource']['DBParam']['Version'] = 1
        dc['DataSource']['DBParam']['cmdTimeOunt'] = 3000
        dc['DataSource']['DBParam']['dbHost'] = ''
        dc['DataSource']['DBParam']['dbName'] = ''
        dc['DataSource']['DBParam']['dbPassword'] = ''
        dc['DataSource']['DBParam']['dbPath'] = ''
        dc['DataSource']['DBParam']['dbServerPort'] = -1
        dc['DataSource']['DBParam']['dbType'] = 0
        dc['DataSource']['DBParam']['dbUser'] = ''
        dc['DataSource']['DataTables'] = []
        dc['DataSource']['createDefaultTable'] = True
        dc['DataSource']['dataTablePrefix'] = ''
        dc['DataSource']['description'] = ''
        dc['DataSource']['enable'] = False
        dc['DataSource']['enableCreateDataBase'] = False
        dc['DataSource']['enableDataTablePrefix'] = False
        dc['DataSource']['enableVerificationA'] = False
        dc['DataSource']['enableVerificationB'] = False
        dc['DataSource']['name'] = ''
        dc['DataSource']['showTable'] = True
        return dc

    def _create_datatable(self):
        dc = {}
        dc['DataTable'] = {}
        dc['DataTable']['dataGroupName'] = ''
        dc['DataTable']['description'] = ''
        dc['DataTable']['enable'] = False
        dc['DataTable']['fields'] = []
        dc['DataTable']['name'] = ''
        dc['DataTable']['version'] = 1
        return dc

    def _create_field(self):
        dc = {}
        dc['DataField'] = {}
        dc['DataField']['dataItemName'] = ''
        dc['DataField']['dataType'] = 0
        dc['DataField']['description'] = ''
        dc['DataField']['enableNull'] = True
        dc['DataField']['itemType'] = 0
        dc['DataField']['name'] = ''
        dc['DataField']['peimmarykey'] = False
        dc['DataField']['size'] = 0
        return dc

    def load(self, filepath):
        self.path = filepath
        objJSON = CJSON()
        self.dataGroup = objJSON.loadfile(filepath)

    def save(self):
        objJSON = CJSON()
        objJSON.writefile(self.dataGroup, self.path)

    def addHisgroup(self, his):
        self.dataGroup['hisDataGroups'].append(his)

    def createHisgroup(self, name):
        objJSON = CJSON()
        data = objJSON.loadstr(self.template)
        data['DataGroup']['name'] = name
        self.addHisgroup(data)
        return data

    def additem(self, group, varname, datatype):
        dc = {}
        dc['DataItem'] = {}
        dc['DataItem']['description'] = ''
        dc['DataItem']['fixed'] = False
        dc['DataItem']['name'] = varname
        dc['DataItem']['varData'] = ''
        dc['DataItem']['varType'] = self.get_scada_datatype(datatype)
        dc['DataItem']['version'] = 1
        group['DataGroup']['items'].append(dc)

    def get_scada_datatype(self, aj_type):
        dc = {}
        dc['BOOL'] = 0
        dc['INT'] = 5
        dc['WORD'] = 6
        dc['DINT'] = 5
        dc['DWORD'] = 6
        dc['REAL'] = 9
        dc['LREAL'] = 10
        dc['TIME'] = 5
        return dc[aj_type]


class CGDI_Object:

    def __init__(self):
        pass

    def load(self, filepath):
        objJSON = CJSON()
        return objJSON.loadfile(filepath)

    def _findctrlname(self, obj, ltname):
        if obj['Type'] == 0:
            groupname = obj['DrawObj']['Name']
            ltname.append(groupname)
            for sonobj in grouplist:
                self._findctrlname(sonobj, ltname)

            return
        objname = obj['DrawObj']['Name']
        ltname.append(objname)
        return

    def addobject(self, gdi, obj):
        ctrlnames = []
        self._findctrlname(obj, ctrlnames)
        namemap = {}
        for ctrlname in ctrlnames:
            namemap[ctrlname] = self._replacename(ctrlname)

        self._replacename(obj, namemap)
        return 1

    def _changename(self, name):
        return 1

    def _replacename(self, obj, nmap):
        if obj['Type'] == 0:
            name = obj['DrawObj']['Name']
            obj['DrawObj']['Name'] = nmap[name]
            for sonobj in grouplist:
                self._replacename(sonobj, nmap)

            return
        name = obj['DrawObj']['Name']
        obj['DrawObj']['Name'] = nmap[name]
        return

    def _replaceexpression(self, obj, prefix):
        objJSON = CJSON()
        objstring = objJSON.outputjson_min(obj)
        fx = '[%'
        ex = '%]'
        ltexp = []
        for exp in ltexp:
            oldexp = fx + exp + ex
            objstring = objstring.replace(oldexp, prefix + '.' + exp)

        newobj = objJSON.loadstr(objstring)
        return newobj

    def _replacescript(self, code, nmmap):
        for oldname in nmmap.keys():
            newname = nmmap[oldname]
            oldevent = ''
            newevent = ''
            code = code.replace(oldevent, newevent)

        return code


class CGDI_Menubar:

    def __init__(self):
        self.template_item = '{"DrawObj":{"Data":{"Rect":{"Bottom":44,"Left":7,"Right":154,"Top":9}},"ExpManager":{"List":[]},"Layer":0,"Locked":false,"Name":"text1","ShowSelectedFrame":false,"SupportGroupEvent":false,"SupportHidedEvent":false,"ToolTip":"","Visible":true},"DrawText":{"Alignment":132,"DateFormat":"yyyy-MM-dd hh:mm:ss","Decimal":0,"Font":{"Capitalization":0,"Family":"SimSun","HintingPreference":0,"Italic":false,"Kerning":true,"OverLine":false,"PixelSize":-1,"PointSize":8,"Stretch":0,"StrikeOut":false,"Style":0,"StyleHint":5,"StyleStrategy":1,"UnderLine":false,"Weight":50,"WordSpacing":0},"IsButtonFrame":false,"MaxLength":50,"Text":"Text","TextBrushManager":{"BrushManager":{"Angle":0,"Color":4278190080,"ImageName":"","Position":0,"Stops":[{"First":0,"Second":4278190080},{"First":1,"Second":4294901760}],"Type":1}},"WrapMode":3},"DrawVector":{"BrushManager":{"BrushManager":{"Angle":45,"Color":4278190080,"ImageName":"","Position":0,"Stops":[{"First":0,"Second":3372154880},{"First":1,"Second":3355443455}],"Type":0}},"DataVector":{"IsFlipX":false,"IsFlipY":false,"RotateAngle":0,"RotatePoint":{"X":0.5,"Y":0.5},"ScalePoint":{"X":0.5,"Y":0.5},"Shear":0},"DynamicBrush":{"List":[],"Type":0},"DynamicPen":{"List":[],"Type":1},"Fill":{"BrushManager":{"BrushManager":{"Angle":0,"Color":4294967040,"ImageName":"","Position":0,"Stops":[{"First":0,"Second":4278190080},{"First":1,"Second":4294901760}],"Type":1}},"Direction":1,"DynamicBrush":{"List":[],"Type":0},"Max":100,"Min":0},"InputVariable":"","MouseDownActions":{"List":[]},"MouseUpActions":{"List":[]},"PenManager":{"BrushManager":{"Angle":0,"Color":4278190080,"ImageName":"","Position":0,"Stops":[{"First":0,"Second":4278190080},{"First":1,"Second":4294901760}],"Type":1},"PenManager":{"CapStyle":16,"JoinStyle":64,"Style":1,"Width":1}},"RightMouseDownActions":{"List":[]},"RightMouseUpActions":{"List":[]}},"Type":7}'
        self.count = 0
        self.items = []
        self.codes = []
        self.itemheight = 0
        self._getheight()

    def _getheight(self):
        objJSON = CJSON()
        item = objJSON.loadstr(self.template_item)
        b = item['DrawObj']['Data']['Rect']['Bottom']
        t = item['DrawObj']['Data']['Rect']['Top']
        hh = b - t
        self.itemheight = hh

    def buildcode(self, ctrlname, winname):
        txt = 'function ' + ctrlname + '_onMouseDown(x, y){' + '\r\n'
        txt += 'g_HMIExpert.open("' + winname + '");' + '\r\n'
        txt += 'form.close();\r\n'
        txt += '}\r\n'
        return txt

    def additem(self, text, winname):
        objJSON = CJSON()
        newItem = objJSON.loadstr(self.template_item)
        ctrlname = 'menu_item_' + str(self.count)
        newItem['DrawText']['Text'] = text
        newItem['DrawObj']['Name'] = ctrlname
        newItem['DrawObj']['Data']['Rect']['Top'] = 9 + self.count * self.itemheight
        newItem['DrawObj']['Data']['Rect']['Bottom'] = newItem['DrawObj']['Data']['Rect']['Top'] + self.itemheight
        self.items.append(newItem)
        self.codes.append(self.buildcode(ctrlname, winname))
        self.count += 1

    def bind(self, gdi):
        gdi['Environment']['Objs'] = copy.deepcopy(self.items)
        scriptcode = ('\r\n').join(self.codes)
        gdi['Environment']['ScriptCode'] = scriptcode
        gdi['Environment']['Rect']['Bottom'] = gdi['Environment']['Rect']['Top'] + 18 + self.count * self.itemheight


class CScada_Event:

    def __init__(self):
        pass

    def load(self, filepath):
        objJSON = CJSON()
        self.data = objJSON.loadfile(filepath)

    def save(self, filepath):
        objJSON = CJSON()
        objJSON.writefile(self.data, filepath)

    def new(self):
        self.data = {}
        self.data['Head'] = {}
        self.data['Head']['Type'] = 'Event'
        self.data['Head']['Version'] = 1
        self.data['Content'] = []

    def create_varchangeequal(self, name, var, val):
        dc = {}
        dc['EventProperty'] = {}
        dc['EventProperty']['ActionNameList'] = []
        dc['EventProperty']['Comment'] = ''
        dc['EventProperty']['Enable'] = ''
        dc['EventProperty']['EnableLog'] = ''
        dc['EventProperty']['Expression'] = ''
        dc['EventProperty']['Name'] = name
        dc['EventProperty']['ObjName'] = var
        dc['EventProperty']['Type'] = 66
        dc['VariableValueChangedInRange'] = {}
        dc['VariableValueChangedInRange']['RangeCondition'] = {}
        dc['VariableValueChangedInRange']['RangeCondition']['Bit1'] = 0
        dc['VariableValueChangedInRange']['RangeCondition']['Bit2'] = 0
        dc['VariableValueChangedInRange']['RangeCondition']['Operand1'] = str(val)
        dc['VariableValueChangedInRange']['RangeCondition']['Operand2'] = '0'
        dc['VariableValueChangedInRange']['RangeCondition']['Operator1'] = 3
        dc['VariableValueChangedInRange']['RangeCondition']['Operator2'] = 3
        dc['VariableValueChangedInRange']['RangeCondition']['RelationshipBetween1and2'] = 1
        self.add_event(dc)
        return dc

    def create_cycle(self, name, period):
        dc = {}
        dc['TimeCycle'] = {}
        dc['TimeCycle']['TimeCycle'] = period
        dc['EventProperty'] = {}
        dc['EventProperty']['ActionNameList'] = []
        dc['EventProperty']['Comment'] = ''
        dc['EventProperty']['Enable'] = ''
        dc['EventProperty']['EnableLog'] = ''
        dc['EventProperty']['Expression'] = ''
        dc['EventProperty']['Name'] = name
        dc['EventProperty']['ObjName'] = ''
        dc['EventProperty']['Type'] = 97
        self.add_event(dc)
        return dc

    def bind_action(self, evt, act):
        evt['EventProperty']['ActionNameList'].append(act)

    def add_event(self, dc):
        self.data['Content'].append(dc)


class CScada_Action:

    def __init__(self):
        pass

    def load(self, filepath):
        objJSON = CJSON()
        self.data = objJSON.loadfile(filepath)

    def save(self, filepath):
        objJSON = CJSON()
        objJSON.writefile(self.data, filepath)

    def new(self):
        self.data = {}
        self.data['Head'] = {}
        self.data['Head']['Type'] = 'Action'
        self.data['Head']['Version'] = 1
        self.data['Content'] = []

    def create_recordhistory(self, name, hisgroup):
        dc = self.create_action()
        dc['ActionProperty']['Name'] = name
        dc['ActionProperty']['ActionID']['@N'] = hisgroup
        dc['ActionProperty']['ActionID']['@OT'] = 8
        dc['ActionProperty']['ActionID']['@T'] = 115
        self.data['Content'].append(dc)
        return dc

    def create_openform(self, name, window):
        dc = self.create_action()
        dc['ActionProperty']['Name'] = name
        dc['ActionProperty']['ActionID']['@N'] = window
        dc['ActionProperty']['ActionID']['@OT'] = 3
        dc['ActionProperty']['ActionID']['@T'] = 81
        self.data['Content'].append(dc)
        return dc

    def create_action(self):
        dc = {}
        dc['ActionProperty'] = {}
        dc['ActionProperty']['ActionID'] = {}
        dc['ActionProperty']['ActionID']['@N'] = ''
        dc['ActionProperty']['ActionID']['@OT'] = 0
        dc['ActionProperty']['ActionID']['@T'] = 0
        dc['ActionProperty']['Comment'] = ''
        dc['ActionProperty']['DelayLength'] = 0
        dc['ActionProperty']['Enable'] = False
        dc['ActionProperty']['EnableDelay'] = False
        dc['ActionProperty']['EnableLog'] = False
        dc['ActionProperty']['Name'] = ''
        dc['ActionProperty']['SPList'] = []
        return dc


class CAlarm:

    def __init__(self):
        self.num = 0

    def add(self, dcAlarm, name, comment, exp, lv):
        dc = {}
        dc['Comment'] = comment
        dc['Expression'] = exp
        dc['LevelName'] = lv
        dc['Name'] = name
        dc['SPLIST'] = []
        dc['SPLIST'].append(self._create_SPList(name))
        dcAlarm['Content'].append(dc)

    def _create_SPList(self, name):
        dc = {}
        dc['@EL'] = False
        dc['@PM'] = 0
        dc['@ST'] = 1
        dc['ID'] = {}
        dc['ID']['@N'] = name
        dc['ID']['@OT'] = 13
        dc['ID']['@T'] = 114
        dc['OperatorGroupList'] = []
        dc['VerifierGroupList'] = []
        return dc


GDI_TYPE = {0: 'group'}

class CGDI_Group:
    PrefixMarker = '[*]'

    def __init__(self, file):
        self.file = file
        objJSON = CJSON()
        self.data = objJSON.loadfile(file)

    def enum(self):
        te = {}
        ctrlnames = []
        node = self.data
        name = node['DrawObj']['Name']
        aj_type = node['Type']
        ctrlnames.append(name)
        if node['Type'] == 0:
            te['name'] = name
            te['type'] = aj_type
            te['items'] = self.enumchild(node['DrawMulti']['ObjList'], ctrlnames)
        else:
            te['name'] = name
            te['type'] = aj_type
            te['items'] = []
        return (
         te, ctrlnames)

    def enumchild(self, node, names):
        items = []
        for obj in node:
            te = {}
            name = obj['DrawObj']['Name']
            names.append(name)
            aj_type = obj['Type']
            if obj['Type'] == 0:
                te['name'] = name
                te['type'] = aj_type
                te['items'] = self.enumchild(obj['DrawMulti']['ObjList'])
                items.append(te)
            else:
                te['name'] = name
                te['type'] = aj_type
                te['items'] = []
                items.append(te)

        return items

    def replace_name(self, mp):
        oname = self.data['DrawObj']['Name']
        if mp.has_key(oname) == True:
            self.data['DrawObj']['Name'] = mp[oname]
        if self.data['Type'] == 0:
            self.data['DrawMulti']['ObjList'] = self.replace_child(self.data['DrawMulti']['ObjList'], mp)

    def replace_child(self, node, mp):
        for obj in node:
            oname = obj['DrawObj']['Name']
            if mp.has_key(oname) == True:
                obj['DrawObj']['Name'] = mp[oname]
            if obj['Type'] == 0:
                self.replace_child(obj['DrawMulti']['ObjList'])

        return node

    def replace_prefix(self, prefix):
        for i in range(len(self.data['DrawObj']['ExpManager']['List'])):
            exp = self.data['DrawObj']['ExpManager']['List'][i]['Expression']
            exp = exp.replace(self.PrefixMarker, prefix)
            self.data['DrawObj']['ExpManager']['List'][i]['Expression'] = exp.replace(self.PrefixMarker, prefix)

        if self.data['Type'] == 0:
            self.replace_childprefix(self.data['DrawMulti']['ObjList'], prefix)

    def replace_childprefix(self, node, prefix):
        for obj in node:
            for i in range(len(obj['DrawObj']['ExpManager']['List'])):
                exp = obj['DrawObj']['ExpManager']['List'][i]['Expression']
                exp = exp.replace(self.PrefixMarker, prefix)
                obj['DrawObj']['ExpManager']['List'][i]['Expression'] = exp.replace(self.PrefixMarker, prefix)

            if obj['Type'] == 0:
                self.replace_childprefix(obj['DrawMulti']['ObjList'], prefix)


class CGDI_GDI(CGDI_Group):

    def __init__(self, file):
        CGDI_Group.__init__(self, file)

    def save(self):
        objJSON = CJSON()
        objJSON.writefile(self.data, self.file)

    def enum(self):
        te = []
        ctrlnames = []
        for obj in self.data['Environment']['Objs']:
            if obj['Type'] == 0:
                ctrl = {}
                ctrl['name'] = obj['DrawObj']['Name']
                ctrl['type'] = obj['Type']
                ctrl['items'] = self.enumchild(obj['DrawMulti']['ObjList'], ctrlnames)
                te.append(ctrl)
                ctrlnames.append(obj['DrawObj']['Name'])
            else:
                ctrl = {}
                ctrl['name'] = obj['DrawObj']['Name']
                ctrl['type'] = obj['Type']
                ctrl['items'] = []
                te.append(ctrl)
                ctrlnames.append(obj['DrawObj']['Name'])

        return (
         te, ctrlnames)

    def enumchild(self, node, names):
        items = []
        for obj in node:
            te = {}
            name = obj['DrawObj']['Name']
            names.append(name)
            aj_type = obj['Type']
            if obj['Type'] == 0:
                te['name'] = name
                te['type'] = aj_type
                te['items'] = self.enumchild(obj['DrawMulti']['ObjList'])
                items.append(te)
            else:
                te['name'] = name
                te['type'] = aj_type
                te['items'] = []
                items.append(te)

        return items

    def replace_gdiname(self, mp):
        for obj in self.data['Environment']['Objs']:
            if obj['Type'] == 0:
                oname = obj['DrawObj']['Name']
                if mp.has_key(oname) == True:
                    obj['DrawObj']['Name'] = mp[oname]
                self.replace_groupname(obj['DrawMulti']['ObjList'], mp)
            else:
                oname = obj['DrawObj']['Name']
                if mp.has_key(oname) == True:
                    obj['DrawObj']['Name'] = mp[oname]

    def replace_groupname(self, node, mp):
        for obj in node:
            oname = obj['DrawObj']['Name']
            if mp.has_key(oname) == True:
                obj['DrawObj']['Name'] = mp[oname]
            if obj['Type'] == 0:
                self.replace_groupname(obj['DrawMulti']['ObjList'], mp)


class CDialog_VarViewer(wx.Dialog):

    def __init__(self, parent, prjFolder):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition, size=wx.Size(496, 510), style=wx.DEFAULT_DIALOG_STYLE)
        bSizer73 = wx.BoxSizer(wx.VERTICAL)
        self.m_treeCtrl = wx.TreeCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE)
        self.m_treeCtrl.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        bSizer73.Add(self.m_treeCtrl, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(bSizer73)
        self.Layout()
        self.m_treeCtrl.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.Render(self.m_treeCtrl, prjFolder)
        self.Centre(wx.BOTH)

    def Render(self, tree, prjFolder):
        filepath = prjFolder + '/RTDB/variables.json'
        objJSON = CJSON()
        dcInfo = objJSON.loadfile(filepath)
        root = tree.AddRoot('Variables')
        tree.SetItemData(root, None)
        for obj in dcInfo['GS']:
            aj_name = obj['@N']
            node = tree.AppendItem(root, aj_name)
            tree.SetItemData(node, None)
            if obj.has_key('GS'):
                self.RenderGroup(tree, obj['GS'], node, aj_name)

        tree.ExpandAll()
        return

    def RenderGroup(self, tree, dc, node, path):
        for obj in dc:
            aj_name = obj['@N']
            son = tree.AppendItem(node, aj_name)
            tree.SetItemData(son, None)
            if obj.has_key('VS'):
                self.RenderVariable(tree, obj['VS'], son, path + '.' + aj_name)
            if obj.has_key('GS'):
                self.RenderGroup(tree, obj['GS'], son, path + '.' + aj_name)

        return

    def RenderVariable(self, tree, dc, node, path):
        for obj in dc:
            aj_name = obj['@N']
            son = tree.AppendItem(node, aj_name)
            tree.SetItemData(son, path + '.' + aj_name)

    def OnLeftDClick(self, event):
        pt = event.GetPosition()
        item, flags = self.m_treeCtrl.HitTest(pt)
        if item:
            v = self.m_treeCtrl.GetItemData(item)
            if v != None:
                self.selvar = v
                self.Close()
            else:
                self.selvar = ''
        event.Skip()
        return

    def __del__(self):
        pass


class CDriver:

    def __init__(self, filepath):
        if os.path.exists(filepath) == False:
            self.CreateEmpty(filepath)
        objJSON = CJSON()
        self.data = objJSON.loadfile(filepath)
        self.file = filepath

    def CreateEmpty(self, filepath):
        dc = {}
        dc['DEVS'] = []
        objJSON = CJSON()
        objJSON.writefile(dc, filepath)

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


class CVariable:

    def __init__(self, filepath):
        if os.path.exists(filepath) == False:
            self.CreateEmpty(filepath)
        objJSON = CJSON()
        self.data = objJSON.loadfile(filepath)
        self.file = filepath

    def CreateEmpty(self, filepath):
        dc = {}
        dc['H'] = {}
        dc['H']['Type'] = 'VariableConfig'
        dc['H']['V'] = '1'
        dc['GS'] = []
        objJSON = CJSON()
        objJSON.writefile(dc, filepath)

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

    def AddVariable(self, node, name, datatype, device='', block='', addr='', cmt=''):
        dc = {}
        dc['@N'] = name
        dc['@D'] = cmt
        dc['@DN'] = device
        dc['@AD'] = block + '.' + str(addr)
        dc['@DT'] = self.get_scada_datatype(datatype)
        dc['@VT'] = '1'
        dc['@ODT'] = self.get_scada_datatype(datatype)
        dc['@OI'] = ''
        dc['@PCS'] = 4
        dc['@UNIT'] = ''
        dc['@IV'] = '0'
        dc['@LV'] = ''
        dc['ACV'] = self.set_variable_ACV()
        dc['WP'] = self.set_variable_WP()
        dc['CVT'] = self.set_variable_CVT()
        dc['ATS'] = self.set_variable_ATS()
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