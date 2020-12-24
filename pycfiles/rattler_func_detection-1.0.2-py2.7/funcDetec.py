# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/src/funcDetec.py
# Compiled at: 2020-02-19 02:57:10
import re, os, click, json, io, logging
try:
    import requests
except ImportError as er:

    class NullHandler(logging.Handler):

        def emit(self, record):
            pass


    raise ImportError('引入requests库失败！', er.message)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def contains(string, search):
    if string.find(search) != -1:
        return True
    return False


def getFunctionStatic(filePath):
    u"""
    :param filePath: 扫描文件路径
    :return:
    """
    functionMapDict = {}
    functionLineCount = {}
    funcPattern = '(?P<access>public|private|protected)(\\s)*(?P<static>static)?(?P<final>final)?(\\s)*(?P<returnType>[\\w<>]+)\\s(?P<funcName>\\w+)[(](?P<params>.*)[)](?P<extra>.*)'
    funcPatternExec = re.compile(funcPattern)
    lineNum = 0
    if not os.path.exists(filePath):
        raise RuntimeError('该文件不存在: %s' % filePath)
    with io.open(filePath, 'r+', encoding='utf-8') as (fr):
        logging.info('filePath: %s' % filePath)
        lines = fr.readlines()
        funcName = ''
        for line in lines:
            lineNum += 1
            funcSearchRes = funcPatternExec.search(line)
            if funcSearchRes:
                resDic = funcSearchRes.groupdict()
                funcName = resDic['funcName']
                if not len(funcName):
                    raise RuntimeError('获取函数名称出错')
                functionMapDict[funcName] = 1 if resDic['extra'] and resDic['extra'].find('{') != -1 else 0
                functionLineCount[funcName] = [lineNum]
            else:
                if line.strip().startswith('//'):
                    continue
                if len(funcName):
                    if contains(line, '{'):
                        functionMapDict[funcName] += 1
                    if contains(line, '}'):
                        functionMapDict[funcName] -= 1
                    if not functionMapDict[funcName]:
                        functionLineCount[funcName].append(lineNum)
                        funcName = ''
                else:
                    continue

    logging.info('函数和行号的映射关系如下:' + str(functionLineCount))
    return functionLineCount


def codeDiffStatic(filePath):
    """
    diff_demo   -> diff --git a/account-service/pom.xml b/account-service/pom.xml
    change_demo -> @@ -730,6 +730,19 @@
    :return:
    """
    fileName = ''
    fileNameLine = {}
    diffFilePattern = 'diff\\s--git\\sa/(?P<source>(.*java))(\\s)b/(?P<target>(.*java))'
    lineChangePattern = '@@ -(?P<begin>(\\d+)),(?P<interval>(\\d+))\\s[+](?P<begin2>\\d+),(?P<interval2>\\d+) @@'
    diffFilePatternExec = re.compile(diffFilePattern)
    lineChangePatternExec = re.compile(lineChangePattern)
    with io.open(filePath, 'r+', encoding='utf-8') as (fr):
        lines = fr.readlines()
        for line in lines:
            diffRes = diffFilePatternExec.search(line)
            if diffRes:
                diffResDict = diffRes.groupdict()
                fileName = diffResDict['source']
                if not len(fileName):
                    raise RuntimeError('diff --git pattern 解析失败')
                fileNameLine[fileName] = []
                continue
            elif fileName:
                changeDiff = lineChangePatternExec.search(line)
                if changeDiff:
                    changeDiffRes = changeDiff.groupdict()
                    if not changeDiffRes:
                        raise RuntimeError('@@ -a,b +c,d @@ 解析失败')
                    for index in range(0, int(changeDiffRes['interval2'])):
                        lineNo = int(changeDiffRes['begin2']) + index
                        fileNameLine[fileName].append(lineNo)

                    fileName = None

    logging.info('源文件变动的行数如下: ' + str(fileNameLine))
    return fileNameLine


@click.command()
@click.option('--root_path', default='', help='扫描根路径,git clone代码后根目录')
@click.option('--diff_path', default='', help='git diff文件路径')
@click.option('--server_id', default='', help='server_id,服务唯一标识')
@click.option('--upload_url', default='', help='upload_url,数据上送地址')
def collisonDect(server_id, root_path, diff_path, upload_url=''):
    u"""
    :param rootPath: 扫描根路径
    :param diffFilePath:
    :return:
    """
    if not (root_path and diff_path):
        raise RuntimeError('rootPath或者diffFilePath为空,请使用 --help查看详情')
    changeDetail = codeDiffStatic(diff_path)
    collisonFunc = []
    for fileName, lineNumList in changeDetail.items():
        filePath = root_path + fileName
        try:
            funcLineMap = getFunctionStatic(filePath)
            for lineNo in lineNumList:
                for funcName, lineNoList in funcLineMap.items():
                    if lineNoList and int(lineNo) >= int(lineNoList[0]) and int(lineNo) <= int(lineNoList[1]) and funcName not in collisonFunc:
                        logging.debug('')
                        collisonFunc.append(funcName)

        except IOError as e:
            logging.error('文件打开存在异常,请检查源文件: %s' % e.message)
        except RuntimeError as err:
            logging.error(err.message.encode('utf-8'))

    if len(collisonFunc):
        logging.info('碰撞后得到函数列表如下: %s' % (',').join(collisonFunc))
    else:
        logging.error('碰撞后结果为空,请检查patch文件与源文件的对应关系！')
    res = ''
    if server_id and collisonFunc and len(upload_url) != 0 and upload_url.strip().startswith('http'):
        headers = {'Content-Type': 'application/json;charset=UTF-8', 'Connection': 'Keep-Alive', 'Content-length': '200'}
        response = requests.post(url=upload_url, json={'server_id': server_id, 'methodsList': (',').join(collisonFunc)}, headers=headers)
        if not response:
            raise RuntimeError('上送请求返回信息为空')
        res = json.loads(response.text)
        if res['resCode'] != '0':
            logging.error('Result: %s' % response.text)
            raise RuntimeError('服务端处理出现异常,请检查服务端日志')
        logging.info('Result: %s' % res)
    if res:
        return res
    return (',').join(collisonFunc)


if __name__ == '__main__':
    res = collisonDect()