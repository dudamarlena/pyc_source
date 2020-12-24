# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\kog_lib\textgrid\sf_textgrid.py
# Compiled at: 2020-01-07 05:14:23
# Size of source mod 2**32: 12520 bytes
import os, textgrid, re, chardet

class SFTextGrid:

    def __init__(self, filepath=None):
        dir(textgrid)
        if filepath:
            if not os.path.isfile(filepath):
                raise FileNotFoundError('文件{}不存在'.format(filepath))
            else:
                self.textgrid_content = self.load(filepath)
                self.textgrid_path = filepath

    @staticmethod
    def help():
        print('\n        ------------------SFTextGrid类 使用方法-----------------------------------------\n        import kog_lib\n\n        类实例化\n            方式1: \n                my_tg = kog_lib.SFTextGrid() \n                my_tg.load(path)\n            方式2: \n                my_tg = kog_lib.SFTextGrid(path)\n\n        获取有效时长等信息：\n            : t_file, t_effect, t_invalid, n_invalid = \n                            my_tg.get_textgrid_stat(re_str)  # re_str是正则表达式\n            : 返回， 总时长、有效时长、无效时长、无效个数\n\n        修改textgrid中相关内容\n            : my_tg.sup_interval(item_ind,interval_ind,type,sup_str)\n                item_ind: item的序号, 0 或者 1\n                ind_ininterval_indterval:interval的序号，从1开始\n                type: 修改interval的哪个字段,maxtime、mintime、mark\n                sup_str:修改成sup_str\n\n        textgrid中speaker检测：\n            : my_tg.check_with_txt(txt_path)\n                txt_path: 记录speaker相关信息的txt文件\n            先检查textgrid是否有误、在检查txt_path是否正确，最后看textgrid中的speaker是否在txt中\n\n        textgrid检查：\n            : my_tg.check():\n        -------------------------------------------------------------------------------\n        ')

    def load(self, filepath):
        tg = textgrid.TextGrid()
        self.textgrid_path = filepath
        try:
            try:
                tg.read(filepath)
                self.textgrid_content = tg
            except:
                self._SFTextGrid__convert2UTF8()
                self._SFTextGrid__restructuretextgrid()

        finally:
            try:
                if not self.textgrid_content:
                    tg.read(filepath)
                    self.textgrid_content = tg
                return tg
            except:
                raise IOError('文件{}读取失败'.format(filepath))

    def get_textgrid_stat(self, re_str):
        if not self.textgrid_content:
            raise ValueError('尚未读取TextGrid文件')
        return self._SFTextGrid__get_textgrid_stat(re_str, self.textgrid_content)

    def sup_interval(self, item_ind, interval_ind, type, sup_str):
        if not self.textgrid_content:
            raise ValueError('尚未读取TextGrid文件')
        self._SFTextGrid__sup_interval(item_ind, interval_ind, type, sup_str)

    def check(self):
        if not self.textgrid_content:
            raise ValueError('尚未读取TextGrid文件')
        else:
            tg = self.textgrid_content
            file = self.textgrid_path
            error_list = []
            if len(tg.tiers) != 2:
                error_list.append(f"item数量不是2个,是{len(tg.tiers)}个")
            for item in tg.tiers:
                if item.minTime != tg.minTime or item.maxTime != tg.maxTime:
                    error_list.append(f"{item.name}时间区域和文件总的时间区域不相等")
                for ind, interv in enumerate(item, 1):
                    if ind == 1:
                        if interv.minTime != item.minTime:
                            error_list.append(f"第一个interval({ind})的开始时间和{item.name}的开始时间不符")
                        if ind == len(item) and interv.maxTime != item.maxTime:
                            error_list.append(f"最后一个interval({ind})的结束时间和{item.name}的结束时间不符")

            if len(tg.tiers[0]) != len(tg.tiers[1]):
                error_list.append('两个tiers的interval数量不一致,不一致开始的地方：' + str(self._SFTextGrid__compare_interv()))
        return error_list

    def check_with_txt(self, txt_path):
        error_list = self.check()
        tg = self.textgrid_content
        file = self.textgrid_path
        sex_speaker_dict, errors = self.get_speaker_info(txt_path)
        error_list.extend(errors)
        if len(errors) > 0:
            return error_list
        else:
            for ind, interv in enumerate(tg.tiers[1], 1):
                if interv.mark.strip() not in sex_speaker_dict.keys() and interv.mark != '':
                    error_list.append('txt文件或者textgrid文件可能有误 ' + interv.mark + ',查看下txt文件，和textgrid中第' + str(ind) + '个interval')

            return error_list

    def get_speaker_info(self, txt_path):
        error_list = []
        sex_speaker_dict = {}
        txt_lines = self.get_file_lines(txt_path)
        if txt_lines == False:
            error_list.append(txt_path + '  内容有误：未知错误')
            return (
             sex_speaker_dict, error_list)
        else:
            try:
                try:
                    for line in txt_lines:
                        speaker = 'N'
                        speaker_sex = 'N'
                        line = line.strip()
                        if 'speaker' not in line:
                            error_list.append(txt_path + '内容有误：没有speaker字段')
                        if ':' in line:
                            speaker = line.split(':')[0].replace('speaker', '').strip()
                            speaker_sex = line.split(':')[1]
                        else:
                            if '：' in line:
                                speaker = line.split('：')[0].replace('speaker', '').strip()
                                speaker_sex = line.split('：')[1]
                            else:
                                error_list.append(txt_path + '内容有误：没有冒号或文件为空')
                        if speaker == '' or speaker == 'N':
                            error_list.append(txt_path + '内容有误：说话人设定有误')
                        sex_speaker_dict[speaker] = speaker_sex

                except:
                    error_list.append(txt_path + '  内容有误:其他')

            finally:
                return

            return (
             sex_speaker_dict, error_list)

    def get_file_lines(self):
        new_lines = []
        try:
            with open(file, 'r', encoding='utf-8') as (f):
                for line in f:
                    new_lines.append(line.strip())

            return new_lines
        except:
            try:
                with open(file, 'r') as (f):
                    for line in f:
                        new_lines.append(line.strip())

                return new_lines
            except:
                return False

    def __compare_interv(self):
        tg = self.textgrid_content
        try:
            for ind, interv in enumerate(tg.tiers[0]):
                if interv.minTime != tg.tiers[1][ind].minTime:
                    return ind + 1

        except Exception as e:
            error_list.append('    textgrid两个item比较时出错，进行到第' + str(ind + 1) + '个时出错，检查一下interval: size')
            return ind + 1

    def __convert2UTF8(self):
        try:
            with open(self.textgrid_path, 'rb') as (fc):
                data = fc.read()
            filecode = chardet.detect(data)
            filecode = filecode['encoding']
            with open((self.textgrid_path), 'r', encoding=filecode) as (fr):
                new_content = fr.read()
            data = new_content
            if self.has_bom(new_content):
                data = self.clean_bom(new_content)
            with open((self.textgrid_path), 'w', encoding='UTF-8') as (fw):
                fw.write(data)
            print('convert from', filecode, 'to UTF-8:', self.textgrid_path)
        except IOError as err:
            print('I/O error: {0}'.format(err))

    @staticmethod
    def has_bom(text):
        if text.startswith('\ufeff'):
            return True
        else:
            return False

    @staticmethod
    def clean_bom(text):
        return text.encode('utf8')[3:].decode('utf8')

    def __restructuretextgrid(self):
        print('restruct', self.textgrid_path)
        lines = self.get_file_lines(self.textgrid_path)
        intervalsize = []
        count = 0
        for ind, line in enumerate(lines):
            if 'xmin' in line or 'xmax' in line or 'text' in line:
                lines[ind] = '            ' + line
            if 'intervals [' in line or 'intervals:' in line or 'name =' in line or 'class = ' in line and 'Object' not in line:
                lines[ind] = '        ' + line
            if 'item [' in line:
                if 'item []' not in line:
                    lines[ind] = '    ' + line
                if 'intervals:' in line:
                    intervalsize.append(int(line[line.rfind('=', 0) + 1:].strip()))
                if len(line.strip()) == 0:
                    del lines[ind]

        lines.insert(2, '')
        lines[3] = lines[3].strip()
        lines[4] = lines[4].strip()
        lines[11] = '        ' + lines[11].strip()
        lines[12] = '        ' + lines[12].strip()
        intervalsize.pop()
        for x in intervalsize:
            lines[12 + 4 * x + 6] = '        ' + lines[(12 + 4 * x + 6)].strip()
            lines[12 + 4 * x + 7] = '        ' + lines[(12 + 4 * x + 7)].strip()

        self.write_lines(self.textgrid_path, lines)
        return restructfilespath

    def write_lines(self, file_path, lines):
        with open(file_path, 'w', encoding='utf-8') as (f):
            con = '\n'.join(lines)
            con += '\n'
            f.write(con)

    def get_file_lines(self, file):
        new_lines = []
        with open(file, 'r', encoding='utf-8') as (f):
            for line in f:
                new_lines.append(line.strip())

        return new_lines

    def __sup_interval(self, item_ind, interval_ind, type, sup_str):
        try:
            tg = self.textgrid_content
            if type == 'mark':
                tg.tiers[item_ind][(interval_ind - 1)].mark = sup_str
            else:
                if type == 'maxTime':
                    tg.tiers[item_ind][(interval_ind - 1)].maxTime = sup_str
                else:
                    if type == 'minTime':
                        tg.tiers[item_ind][(interval_ind - 1)].minTime = sup_str
                    else:
                        print('type error:', type)
                        return False
            tg.write(self.textgrid_path)
            return True
        except Exception as e:
            print('error:', e)
            return False

    def __get_textgrid_stat(self, re_str, tg_content):
        t_invalid = 0
        n_invalid = 0
        t_effect = 0
        t_file = tg_content.maxTime - tg_content.minTime
        for interv in tg_content.tiers[0]:
            if re.search(re_str, interv.mark):
                t_effect += interv.duration()
            else:
                n_invalid += 1
                t_invalid += interv.duration()

        return (
         t_file, t_effect, t_invalid, n_invalid)