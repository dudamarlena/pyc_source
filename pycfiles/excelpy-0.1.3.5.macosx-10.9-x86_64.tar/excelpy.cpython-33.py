# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/edmondwells/venvs/excelpy/lib/python3.3/site-packages/src/excelpy/excelpy.py
# Compiled at: 2014-03-04 03:14:44
# Size of source mod 2**32: 24545 bytes
import os, shutil
from lxml import etree
from zipfile import ZipFile
import fnmatch, json, re
UTF_8 = 'utf-8'
from xlsx_ns import NS_SPREADSHEETML, NS_CONTENT_TYPES, NS_PROPERTIES, NS_DOC_PROPS_VTYPES, NS_RELS, NS_REL_WORKSHEET, NS_WORKSHEET_R

class ExcelPy(object):
    __doc__ = ' ExcelPy class\n    '

    def __init__(self, excel_file_path):
        self.last_worksheet_num = 0
        excel_dir = os.path.dirname(excel_file_path)
        dst_name = os.path.basename(excel_file_path).rsplit('.', 1)[0]
        self.zipped_file_path = os.path.join(excel_dir, dst_name + '.zip')
        self.xlsx_file_path = os.path.join(excel_dir, dst_name + '.xlsx')
        shutil.copy2(excel_file_path, self.zipped_file_path)
        self.target_dir = os.path.join(excel_dir, dst_name)
        self.z = ZipFile(self.zipped_file_path)
        try:
            shutil.rmtree(self.target_dir)
        except:
            pass

        os.mkdir(self.target_dir)
        self.z.extractall(self.target_dir)
        self._getSharedString()

    def __del__(self):
        """remove working directory and file.
        """
        try:
            shutil.rmtree(self.target_dir)
            os.remove(self.zipped_file_path)
            os.remove(self.xlsx_file_path)
        except:
            pass

    def _getEtree(self, xml_file_path):
        """ return etree.XML(xml_file_path)
        """
        with open(xml_file_path) as (f):
            s = f.read()
            return etree.XML(bytes(s, UTF_8))

    def _saveEtree(self, bytes_string, xml_file_path):
        """ Write bytes string to xml file.
        """
        with open(xml_file_path, 'w') as (f):
            f.write(str(bytes_string, UTF_8))
            return True

    def _makeXMLfilename(self, filename, filepath=None):
        if filepath:
            return os.path.join(filepath, 'sheet') + filename + '.xml'
        return 'sheet' + filename + '.xml'

    def _getSharedString(self):
        """ get sharedString.xml """
        self.SharedStringsFile = 'sharedStrings.xml'
        self.SharedStringXML = self._getEtree(os.path.join(self.target_dir, 'xl', self.SharedStringsFile))
        self.sst = self.SharedStringXML
        self.sis = self.SharedStringXML.xpath('//ns:si', namespaces={'ns': NS_SPREADSHEETML})

    @property
    def sheetnames(self):
        """get sheet names
        """
        WORKBOOK_NAME = 'workbook.xml'
        workbook_XML = self._getEtree(os.path.join(self.target_dir, 'xl', WORKBOOK_NAME))
        sheet_elems = workbook_XML.xpath('//ns:sheet', namespaces={'ns': NS_SPREADSHEETML})
        sheetnames = [sheet_elem.get('name') for sheet_elem in sheet_elems]
        return sheetnames

    def _modContentTypes(self, deleteSheetNum=None):
        """ modify [Content_Types].xml """
        Content_Types_Name = '[Content_Types].xml'
        Content_Types_XML = self._getEtree(os.path.join(self.target_dir, Content_Types_Name))
        ContentType = 'application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml'
        overrides = Content_Types_XML.xpath('//ns:Override[@ContentType="{}"]'.format(ContentType), namespaces={'ns': NS_CONTENT_TYPES})
        for override in overrides:
            _worksheet = override.get('PartName').rsplit('/', 1)[1]
            _worksheet_num = int(_worksheet[5:-4])
            if self.last_worksheet_num < _worksheet_num:
                self.last_worksheet_num = _worksheet_num
                continue

        if not deleteSheetNum:
            new_worksheet_num = int(self.last_worksheet_num) + 1
            new_worksheet = self._makeXMLfilename(str(new_worksheet_num))
            new_override = etree.Element('Override')
            new_override.set('PartName', os.path.join('/', 'xl', 'worksheets', new_worksheet))
            new_override.set('ContentType', ContentType)
            Content_Types_XML.insert(len(overrides), new_override)
            self.last_worksheet_num = new_worksheet_num
        else:
            if deleteSheetNum and not self.last_worksheet_num == 1:
                deletePartName = os.path.join('/', 'xl', 'worksheets', 'sheet' + str(self.last_worksheet_num) + '.xml')
                deleteElem = Content_Types_XML.find('.//ns:Override[@PartName="{0}"]'.format(deletePartName), namespaces={'ns': NS_CONTENT_TYPES})
                deleteElem.getparent().remove(deleteElem)
                self.last_worksheet_num = int(self.last_worksheet_num) - 1
            else:
                print('Excel file must have one sheet at least.')
                raise
        Content_Types_str = etree.tostring(Content_Types_XML, encoding=UTF_8)
        return self._saveEtree(Content_Types_str, os.path.join(self.target_dir, Content_Types_Name))

    def _modApp(self, sheetname, delete=False):
        """ modify docProps/app.xml """
        APP_NAME = 'app.xml'
        app_XML = self._getEtree(os.path.join(self.target_dir, 'docProps', APP_NAME))
        TitleOfParts = app_XML.find('./ns:TitlesOfParts', namespaces={'ns': NS_PROPERTIES})
        TitleOfPartsVector = TitleOfParts.find('./vt:vector', namespaces={'vt': NS_DOC_PROPS_VTYPES})
        i4 = app_XML.find('.//vt:i4', namespaces={'vt': NS_DOC_PROPS_VTYPES})
        lpstrs = TitleOfPartsVector.findall('ns:lpstr', namespaces={'ns': NS_DOC_PROPS_VTYPES})
        count = len(lpstrs)
        if delete:
            count -= 1
        else:
            count += 1
        self.count = str(count)
        i4.text = self.count
        for lpstr in lpstrs:
            if sheetname == lpstr.text and delete:
                new_vector_size = self.count
                TitleOfPartsVector.set('size', new_vector_size)
                lpstr.getparent().remove(lpstr)
                continue

        if not delete:
            new_vector_size = self.count
            TitleOfPartsVector.set('size', new_vector_size)
            NSMAP = {'vt': NS_DOC_PROPS_VTYPES}
            new_sheet_elem = etree.Element('{%s}lpstr' % NSMAP['vt'], nsmap=NSMAP)
            new_sheet_elem.text = sheetname
            TitleOfPartsVector.insert(len(lpstrs), new_sheet_elem)
        app_str = etree.tostring(app_XML, encoding=UTF_8)
        return self._saveEtree(app_str, os.path.join(self.target_dir, 'docProps', APP_NAME))

    def _chkExistWord(self, word):
        """ check the word is already used. if True, return index."""
        for index, si in enumerate(self.sis):
            t = si.find('./ns:t', namespaces={'ns': NS_SPREADSHEETML}).text
            if t is None:
                print('ERROR: Cannot find <t> element.')
                raise
            if word == t:
                return index

        return False

    def _makeXlsx(self):
        """ make xlsx
        """
        shutil.make_archive(self.target_dir, 'zip', self.target_dir)
        os.rename(self.zipped_file_path, self.xlsx_file_path)
        return True

    def _workbook(self, sheetname, new_sheet_name=None, delete=False):
        """
        modify workbook.xml file
        """
        workbook_name = 'workbook.xml'
        workbook_XML = self._getEtree(os.path.join(self.target_dir, 'xl', workbook_name))
        sheets = workbook_XML.find('ns:sheets', namespaces={'ns': NS_SPREADSHEETML})
        if delete:
            deleteId = self._getSheetNum(sheetname)
            deleteElem = workbook_XML.find('.//ns:sheet[@sheetId="{0}"]'.format(deleteId), namespaces={'ns': NS_SPREADSHEETML})
            deleteElem.getparent().remove(deleteElem)
            sheet_elems = workbook_XML.findall('.//ns:sheet', namespaces={'ns': NS_SPREADSHEETML})
            for el in sheet_elems:
                rId = el.get('{%s}id' % NS_WORKSHEET_R)[3:]
                if int(rId) > int(deleteId):
                    el.set('{%s}id' % NS_WORKSHEET_R, 'rId' + str(int(rId) - 1))
                    el.set('sheetId', str(int(rId) - 1))
                    continue

        else:
            if new_sheet_name:
                cur_sheetname_node = workbook_XML.find('.//ns:sheet[@name="{}"]'.format(sheetname), namespaces={'ns': NS_SPREADSHEETML})
                cur_sheetname_node.set('name', new_sheet_name)
            else:
                _sheets = workbook_XML.xpath('//ns:sheet', namespaces={'ns': NS_SPREADSHEETML})
                _Ids = []
                for sheet in _sheets:
                    _Ids.append(int(sheet.get('sheetId')))

                new_id = str(max(_Ids) + 1)
                NSMAP = {'r': NS_WORKSHEET_R}
                new_sheet = etree.Element('sheet', name=sheetname, sheetId=new_id)
                new_sheet.set('{%s}id' % NSMAP['r'], 'rId' + new_id)
                sheets.insert(len(sheets), new_sheet)
        workbook_str = etree.tostring(workbook_XML, encoding=UTF_8)
        return self._saveEtree(workbook_str, os.path.join(self.target_dir, 'xl', workbook_name))

    def _workbook_refs(self, sheetname=None):
        """
        modify xl/_refs/workbook.xml.rels file.
        """
        RELS_NAME = 'workbook.xml.rels'
        Relationship_XML = self._getEtree(os.path.join(self.target_dir, 'xl', '_rels', RELS_NAME))
        relationships = Relationship_XML.findall('ns:Relationship', namespaces={'ns': NS_RELS})
        rId_str = 'rId'
        rId_len = len(rId_str)
        if sheetname:
            dataSheets = Relationship_XML.xpath('//ns:Relationship[@Type="{0}"]'.format(NS_REL_WORKSHEET), namespaces={'ns': NS_RELS})
            target = self._makeXMLfilename(str(len(dataSheets)), 'worksheets')
            deleteElem = Relationship_XML.find('.//ns:Relationship[@Target="{0}"]'.format(target), namespaces={'ns': NS_RELS})
            deleteElem.getparent().remove(deleteElem)
            relationships = Relationship_XML.findall('ns:Relationship', namespaces={'ns': NS_RELS})
            for el in relationships:
                _id = int(el.get('Id')[len(rId_str):])
                if _id > len(dataSheets):
                    el.set('Id', 'rId' + str(_id - 1))
                    continue

        else:
            rIds = [int(relationship.get('Id')[rId_len:]) for relationship in relationships]
            rIds = sorted(rIds, reverse=True)
            changeIds = list(filter(lambda rId: rId >= int(self.count), rIds))
            for rId in changeIds:
                Id = rId_str + str(rId + 1)
                _elem = Relationship_XML.find('ns:Relationship[@Id="rId{0}"]'.format(rId), namespaces={'ns': NS_RELS})
                _elem.set('Id', Id)

            new_rId = 'rId' + self.count
            Target = 'worksheets/sheet{0}.xml'.format(self.count)
            Target = self._makeXMLfilename(self.count, 'worksheets')
            new_relationship = etree.Element('Relationship', Id=new_rId, Type=NS_REL_WORKSHEET, Target=Target)
            _relationship = Relationship_XML.xpath('//ns:Relationships', namespaces={'ns': NS_RELS})[0]
            _relationship.insert(len(relationships), new_relationship)
        Relationship_str = etree.tostring(Relationship_XML, encoding=UTF_8)
        return self._saveEtree(Relationship_str, os.path.join(self.target_dir, 'xl', '_rels', RELS_NAME))

    def _makeSheet(self):
        """
        copy template file to xl/worksheets/sheet[n].xml
        """
        template = os.path.join(os.path.dirname(__file__), 'templates', 'xl', 'worksheets', 'sheet.xml')
        new_sheet_file_name = self._makeXMLfilename(self.count)
        target = os.path.join(self.target_dir, 'xl', 'worksheets', new_sheet_file_name)
        shutil.copy2(template, target)

    def _getSheetNum(self, sheetname):
        """
        Get sheet id number.
        """
        if sheetname not in self.sheetnames:
            print('Sheet name [{0}] does not exist'.format(sheetname))
            raise
        try:
            WORKBOOK_NAME = 'workbook.xml'
            workbook_XML = self._getEtree(os.path.join(self.target_dir, 'xl', WORKBOOK_NAME))
            sheet = workbook_XML.find('.//ns:sheet[@name="{}"]'.format(sheetname), namespaces={'ns': NS_SPREADSHEETML})
            return sheet.get('sheetId')
        except:
            print('ERROR: Cannot get sheet number from workbook.xml')
            raise

    def _copySheet(self, orig_sheetname, copy_name):
        sheetnum = self._getSheetNum(orig_sheetname)
        file_name = self._makeXMLfilename(str(sheetnum))
        new_file_name = self._makeXMLfilename(self.count)
        orig_sheet_file = os.path.join(self.target_dir, 'xl', 'worksheets', file_name)
        new_sheet_file = os.path.join(self.target_dir, 'xl', 'worksheets', new_file_name)
        shutil.copy2(orig_sheet_file, new_sheet_file)

    def _step_uniqueCount(self, step=1):
        new_uniqueCount = int(self.sst.get('uniqueCount')) + step
        self.sst.set('uniqueCount', str(new_uniqueCount))

    def addSheet(self, new_sheet_name):
        self._modContentTypes()
        self._modApp(new_sheet_name)
        self._workbook(new_sheet_name)
        self._workbook_refs()
        self._makeSheet()

    def copySheet(self, orig_sheetname, copy_name=None):
        if copy_name is None:
            copy_name = orig_sheetname + ' copy'
        self._modContentTypes()
        if self._modApp(copy_name):
            self.save()
        else:
            print('Failed to copy. The sheet name is already used. Use another name.')
            return False
        self._workbook(copy_name)
        self._workbook_refs()
        self._copySheet(orig_sheetname, copy_name)
        return

    def deleteSheet(self, sheetname):
        self._del_sheet_id = self._getSheetNum(sheetname)
        sheetidx = self._makeXMLfilename(self._del_sheet_id)
        self._modContentTypes(sheetidx)
        self._modApp(sheetname, delete=True)
        self._workbook_refs(sheetname)
        self._workbook(sheetname, delete=True)
        worksheets_path = os.path.join(self.target_dir, 'xl', 'worksheets')
        target = os.path.join(worksheets_path, sheetidx)
        os.remove(target)
        pattern_sheets = 'sheet*.xml'
        xmls = fnmatch.filter(os.listdir(worksheets_path), pattern_sheets)
        for xml in xmls:
            num = int(xml[5:-4])
            if num > int(self._del_sheet_id):
                new_name = self._makeXMLfilename(str(num - 1))
                os.rename(os.path.join(worksheets_path, xml), os.path.join(worksheets_path, new_name))
                continue

    def renameSheet(self, orig_sheetname, new_sheet_name):
        self._workbook(orig_sheetname, new_sheet_name)

    def _saveSharedString(self):
        """ save sharedString.xml """
        self._saveEtree(etree.tostring(self.SharedStringXML, encoding='utf-8'), os.path.join(self.target_dir, 'xl', self.SharedStringsFile))

    def _set_v_text(self, cell, index):
        v = cell.find('./ns:v', namespaces={'ns': NS_SPREADSHEETML})
        v.text = str(index)

    def edit(self, sheetname, changed_data_json):
        if sheetname not in self.sheetnames:
            print('Sheet name [{0}] does not exist'.format(sheetname))
            raise
        sheet_number = self._getSheetNum(sheetname)
        self.changed = json.loads(changed_data_json)
        worksheet_dir = os.path.join(self.target_dir, 'xl', 'worksheets')
        xml_file = self._makeXMLfilename(sheet_number, worksheet_dir)
        self.sheetXML = etree.parse(xml_file).getroot()
        cells = self.changed.keys()
        for _cell in cells:
            cell = self.sheetXML.find('.//ns:c[@r="{0}"]'.format(_cell), namespaces={'ns': NS_SPREADSHEETML})
            if cell is None:
                r = re.findall('\\d+', _cell)[0]
                row = self.sheetXML.xpath('//ns:row[@r="{}"]'.format(r), namespaces={'ns': NS_SPREADSHEETML})
                if len(row) is 0:
                    NSMAP = {'ns': NS_SPREADSHEETML}
                    new_row = etree.Element('{%s}row' % NSMAP['ns'], nsmap=NSMAP, r=r)
                    sheetData = self.sheetXML.find('ns:sheetData', namespaces={'ns': NS_SPREADSHEETML})
                    sheetData.append(new_row)
                    row = sheetData.find('.//ns:row[@r="{}"]'.format(r), namespaces={'ns': NS_SPREADSHEETML})
                new_v = etree.Element('v')
                if isinstance(self.changed[_cell], int):
                    new_c = etree.Element('c', r=_cell, s='1')
                    new_v.text = str(self.changed[_cell])
                    new_c.append(new_v)
                    row.append(new_c)
                else:
                    new_c = etree.Element('{%s}c' % NSMAP['ns'], r=_cell, t='s')
                    new_v = etree.Element('{%s}v' % NSMAP['ns'])
                    new_c.insert(0, new_v)
                    index = self._chkExistWord(self.changed[_cell])
                    if index:
                        self._set_v_text(new_c, index)
                    else:
                        self._step_uniqueCount(step=1)
                        new_si = etree.Element('{%s}si' % NSMAP['ns'])
                        new_t = etree.Element('{%s}t' % NSMAP['ns'])
                        new_t.text = self.changed[_cell]
                        new_si.insert(0, new_t)
                        sis = self.SharedStringXML.findall('ns:si', namespaces={'ns': NS_SPREADSHEETML})
                        self.sst.insert(len(sis), new_si)
                        sis = self.SharedStringXML.findall('ns:si', namespaces={'ns': NS_SPREADSHEETML})
                        new_v_num = len(sis)
                        new_v.text = str(new_v_num - 1)
                        self._saveEtree(etree.tostring(self.SharedStringXML), os.path.join(self.target_dir, 'xl', 'sharedStrings.xml'))
                    count = str(int(self.sst.get('count')) + 1)
                    self.sst.set('count', count)
                    new_c.append(new_v)
                    row.append(new_c)
            else:
                v = cell.find('ns:v', namespaces={'ns': NS_SPREADSHEETML})
                if isinstance(self.changed[_cell], int):
                    try:
                        cell.attrib.pop('t')
                    except:
                        pass

                    v.text = str(self.changed[_cell])
                else:
                    try:
                        cell.set('t', 's')
                    except:
                        pass

                    if v is None:
                        new_v = etree.Element('v')
                        cell.insert(0, new_v)
                    child = cell.find('ns:v', namespaces={'ns': NS_SPREADSHEETML})
                    if child is not None:
                        index = self._chkExistWord(self.changed[_cell])
                        if index:
                            self._set_v_text(cell, index)
                        else:
                            self._step_uniqueCount(step=1)
                            NSMAP = {'ns': NS_SPREADSHEETML}
                            new_si = etree.Element('{%s}si' % NSMAP['ns'], nsmap=NSMAP)
                            new_t = etree.Element('t')
                            new_t.text = self.changed[_cell]
                            len_sis = len(self.SharedStringXML.findall('ns:si', namespaces={'ns': NS_SPREADSHEETML}))
                            new_si.insert(0, new_t)
                            self.SharedStringXML.insert(len_sis, new_si)
                            v = cell.find('ns:v', namespaces={'ns': NS_SPREADSHEETML})
                            if v is not None:
                                v.text = str(len_sis)
                            self._saveEtree(etree.tostring(self.SharedStringXML), os.path.join(self.target_dir, 'xl', 'sharedStrings.xml'))
                    count = str(int(self.sst.get('count')) + 1)
                    self.sst.set('count', count)

        self._saveSharedString()
        return self._saveEtree(etree.tostring(self.sheetXML), self._makeXMLfilename(sheet_number, worksheet_dir))

    def save(self):
        self._makeXlsx()