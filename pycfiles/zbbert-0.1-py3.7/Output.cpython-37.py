# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\zbbert\Output.py
# Compiled at: 2019-06-24 00:47:26
# Size of source mod 2**32: 7417 bytes
from kashgari.tasks.seq_labeling import BLSTMCRFModel
from TextProcess import pause
import csv, pymysql

def is_chinese(s):
    rt = False
    if s >= '一':
        if s <= '龦':
            rt = True
    return rt


new_model = BLSTMCRFModel.load_model('./Model_originalBIG6')
with open('C://Users//zhongbiao//Desktop//INFO.csv', 'r', encoding='utf8') as (f):
    with open('C://Users//zhongbiao//Desktop//INFO_result_ER0001_BIG6.csv', 'w', newline='', encoding='utf8') as (csvfile):
        data = csv.reader(f)
        writer = csv.writer(csvfile)
        writer.writerow(['pk', 'bulletin_info_pk', 'content', 'related_orgs', 'predict_orgs'])
        Content = []
        PredictList = []
        WriteList = []
        AllWriteList = []
        NU = []
        pk = 1
        conn = pymysql.connect(host='60.205.149.163', port=3306, user='readuser', passwd='ZB_readuser', db='procurement', charset='utf8')
        cursor = conn.cursor(cursor=(pymysql.cursors.DictCursor))
        for bullinfo_pk in data:
            bulletin_info_pk = bullinfo_pk[0]
            if len(bulletin_info_pk) <= 3:
                continue
            else:
                bulletin_info_pk = bulletin_info_pk.strip()
                WriteList.append(pk)
                WriteList.append(bulletin_info_pk)
                pk += 1
                Command_content = 'select * from procurement.bulletin_info_content_format where bulletin_info_pk = "' + bulletin_info_pk + '"'
                r = cursor.execute(Command_content)
                result = cursor.fetchall()
                if result:
                    WriteList.append(result[0]['bulletin_content'])
                    Content.append(result[0]['bulletin_content'])
                else:
                    WriteList.append(NU)
                    Content.append(NU)
                Command_org = 'select * from procurement.bulletin_info_extend where bulletin_info_pk = "' + bulletin_info_pk + '"'
                r = cursor.execute(Command_org)
                result = cursor.fetchall()
                if result:
                    WriteList.append(result[0]['related_orgs'])
                else:
                    WriteList.append(NU)
            AllWriteList.append(WriteList)
            WriteList = []

        conn.commit()
        cursor.close()
        conn.close()
        word_list = []
        for Data in Content:
            if Data:
                Data = pause(Data, 200)
                Data_split = Data.split('。')
                for i in Data_split[0:-1]:
                    word_list.append(list(i))

            else:
                word_list.append(NU)
            word_list.append(['N', 'E', 'X', 'T'])

        OutputDict = {}
        LabelReturn = new_model.predict(word_list)
        for LabelSentence, OriginalSentence in zip(LabelReturn, word_list):
            if OriginalSentence == ['N', 'E', 'X', 'T']:
                PredictList.append(OutputDict)
                OutputDict = {}
            else:
                for loc in range(len(LabelSentence)):
                    if LabelSentence[loc] != 'O':
                        if LabelSentence[loc] == 'B-ORG1':
                            j = loc
                            if j == len(LabelSentence) - 1:
                                pass
                            else:
                                while LabelSentence[(j + 1)] == 'I-ORG1':
                                    j += 1
                                    if j == len(LabelSentence) - 1:
                                        break

                            Sen = ''.join(OriginalSentence[loc:j + 1])
                            for w in Sen:
                                if is_chinese(w) is not True:
                                    Sen = Sen.strip(w)

                            OutputDict[Sen] = 'ER0001'
                        elif LabelSentence[loc] == 'B-ORG2':
                            j = loc
                            while LabelSentence[(j + 1)] == 'I-ORG2':
                                j += 1
                                if j == len(LabelSentence) - 1:
                                    break

                            Sen = ''.join(OriginalSentence[loc:j + 1])
                            for w in Sen:
                                if is_chinese(w) is not True:
                                    Sen = Sen.strip(w)

                            OutputDict[Sen] = 'ER0002'
                        elif LabelSentence[loc] == 'B-ORG3':
                            j = loc
                            while LabelSentence[(j + 1)] == 'I-ORG3':
                                j += 1
                                if j == len(LabelSentence) - 1:
                                    break

                            Sen = ''.join(OriginalSentence[loc:j + 1])
                            for w in Sen:
                                if is_chinese(w) is not True:
                                    Sen = Sen.strip(w)

                            OutputDict[Sen] = 'ER0003'
                        elif LabelSentence[loc] == 'B-ORG4':
                            j = loc
                            while LabelSentence[(j + 1)] == 'I-ORG4':
                                j += 1
                                if j == len(LabelSentence) - 1:
                                    break

                            Sen = ''.join(OriginalSentence[loc:j + 1])
                            for w in Sen:
                                if is_chinese(w) is not True:
                                    Sen = Sen.strip(w)

                            OutputDict[Sen] = 'ER0004'
                        else:
                            if LabelSentence[loc] == 'B-ORG5':
                                j = loc
                                while LabelSentence[(j + 1)] == 'I-ORG5':
                                    j += 1
                                    if j == len(LabelSentence) - 1:
                                        break

                                Sen = ''.join(OriginalSentence[loc:j + 1])
                                for w in Sen:
                                    if is_chinese(w) is not True:
                                        Sen = Sen.strip(w)

                                OutputDict[Sen] = 'ER0005'
                    if LabelSentence[loc] == 'B-AMO':
                        j = loc
                        while LabelSentence[(j + 1)] == 'I-AMO':
                            j += 1
                            if j == len(LabelSentence) - 1:
                                break

                        Sen = ''.join(OriginalSentence[loc:j + 1])
                        for w in Sen:
                            if is_chinese(w) is not True:
                                Sen = Sen.strip(w)

                        OutputDict[Sen] = 'WinAmount'
                        continue

        assert len(AllWriteList) == len(PredictList)
        for i, j in zip(AllWriteList, PredictList):
            i.append(j)
            i[2] = 'HAHA'
            writer.writerow(i)