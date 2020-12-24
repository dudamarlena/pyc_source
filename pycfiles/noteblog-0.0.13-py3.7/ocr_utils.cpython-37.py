# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/noteblog/fzutils/ocr_utils.py
# Compiled at: 2019-05-05 05:26:25
# Size of source mod 2**32: 14154 bytes
"""
@author = super_fazai
@File    : ocr_utils.py
@connect : superonesfazai@gmail.com
"""
from cv2 import imread, cvtColor, COLOR_BGR2GRAY, matchTemplate, TM_CCOEFF_NORMED
from numpy import where
from aip import AipOcr
import requests
from time import sleep
from .internet_utils import get_random_pc_ua
from .img_utils import read_img_use_base64
from .common_utils import json_2_dict
from spider.fz_requests import Requests
__all__ = [
 'baidu_ocr_captcha',
 'yundama_ocr_captcha',
 'baidu_orc_image_main_body',
 'get_tracks_based_on_distance',
 'crack_wy_point_select_captcha',
 'dichotomy_match_gap_distance']

def baidu_ocr_captcha(app_id, api_key, secret_key, img_path, orc_type=3) -> dict:
    """
    百度ocr识别captcha
    :param app_id:
    :param api_key:
    :param secret_key:
    :param img_path:
    :param orc_type: 1: basic_general 2: general 3: web_image
    :return:
    """

    def basic_general():
        res = api_orc.basicGeneral(image=(get_img_content(img_path)), options=basic_general_options)
        return res

    def general():
        general_options = basic_general_options
        general_options.update({'vertexes_location': 'true'})
        res = api_orc.general(image=(get_img_content(img_path)), options=general_options)
        return res

    def web_image():
        general_options = basic_general_options
        general_options.update({'vertexes_location': 'true'})
        res = api_orc.webImage(image=(get_img_content(img_path)), options=general_options)
        return res

    def get_img_content(img_path):
        """读取img内容"""
        with open(img_path, 'rb') as (f):
            return f.read()

    api_orc = AipOcr(app_id, api_key, secret_key)
    basic_general_options = {'detect_direction':'true', 
     'detect_language':'true', 
     'language_type':'CHN_ENG', 
     'classify_dimension':'lottery'}
    if orc_type == 1:
        return basic_general()
    if orc_type == 2:
        return general()
    if orc_type == 3:
        return web_image()
    raise ValueError('orc_type赋值异常!')


def baidu_orc_image_main_body(img_url='', local_img_path=None) -> dict:
    """
    百度orc图像主体位置识别
    hack 百度图像主体检测功能演示, 旨在: 常规使用不付费
    https://ai.baidu.com/tech/imagerecognition/general
    :param img_url: 跟下面参数, 二选一
    :param local_img_path: 如果没有url, 则可通过本地图片path
    :return:
        success eg:
            {
                'errno': 0,
                'msg': 'success',
                'data': {
                    'log_id': '2587356961021549289',
                    'result': {
                        'width': 103,   # 宽度103px
                        'top': 2,       # 距上2px
                        'left': 10,     # 距左10px
                        'height': 115,  # 高度115px
                    }
                }
            }
    """
    cookies = {'BAIDUID': 'D668B34BE04D9BF359FB05917F1E1340:FG=1'}
    headers = {'Origin':'https://ai.baidu.com', 
     'Accept-Encoding':'gzip, deflate, br', 
     'Accept-Language':'zh-CN,zh;q=0.9', 
     'User-Agent':get_random_pc_ua(), 
     'Content-Type':'application/x-www-form-urlencoded', 
     'Accept':'*/*', 
     'Connection':'keep-alive'}
    img_content = ''
    if local_img_path is not None:
        img_content = read_img_use_base64(file_path=local_img_path)
        img_url = ''
    data = [
     (
      'image', img_content),
     (
      'image_url', img_url),
     ('type', 'object_detect')]
    response = requests.post('https://ai.baidu.com/aidemo', headers=headers, cookies=cookies, data=data)
    return json_2_dict(response.text)


def get_tracks_based_on_distance(distance: int) -> dict:
    """
    根据给与的距离生成不规律的移动轨迹tracks
    :param distance:
    :return: {'forward_tracks': [...], 'back_tracks': [...]}
    """
    print('移动距离为:{}'.format(distance))
    distance += 20
    v = 0
    t = 0.2
    forward_tracks = []
    current = 0
    mid = distance * 3 / 5
    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3
        s = v * t + 0.5 * a * t ** 2
        v = v + a * t
        current += s
        forward_tracks.append(round(s))

    back_tracks = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -1]
    return {'forward_tracks':forward_tracks, 
     'back_tracks':back_tracks}


def yundama_ocr_captcha(username, pwd, img_path, app_key: str, app_id=4039, code_type=5000, timeout=60) -> str:
    """
    云打码识别captcha
    :param username: 用的是普通用户的账号密码，而不是开发者的
    :param pwd:
    :param app_id: 软件id, 登录开发者后台【我的软件】获得
    :param app_key: 软件密钥, 登录开发者后台【我的软件】获得
    :param img_path: 图片路径
    :param code_type: 验证码类型 eg: 1004表示4位字母数字，不同类型收费不同: http://www.yundama.com/price.html
    :param timeout: 超时时长, 单位秒
    :return: 识别结果字符串
    """

    class YDMClient:
        __doc__ = '云打码官方示例'

        def __init__(self, username, password, appid, app_key):
            self.api_url = 'http://api.yundama.com/api.php'
            self.username = username
            self.pwd = password
            self.app_id = str(appid)
            self.app_key = app_key

        def request(self, fields, files=[]):
            response = self.post_url(self.api_url, fields, files)
            res = json_2_dict(response)
            return res

        def balance(self):
            data = {'method':'balance', 
             'username':self.username, 
             'password':self.pwd, 
             'appid':self.app_id, 
             'appkey':self.app_key}
            response = self.request(data)
            if response:
                if response['ret']:
                    if response['ret'] < 0:
                        return response['ret']
                return response['balance']
            else:
                return -9001

        def login(self):
            data = {'method':'login', 
             'username':self.username, 
             'password':self.pwd, 
             'appid':self.app_id, 
             'appkey':self.app_key}
            response = self.request(data)
            if response:
                if response['ret']:
                    if response['ret'] < 0:
                        return response['ret']
                return response['uid']
            else:
                return -9001

        def upload(self, img_path, code_type, timeout):
            data = {'method':'upload', 
             'username':self.username, 
             'password':self.pwd, 
             'appid':self.app_id, 
             'appkey':self.app_key, 
             'codetype':str(code_type), 
             'timeout':str(timeout)}
            file = {'file': img_path}
            response = self.request(data, file)
            if response:
                if response['ret']:
                    if response['ret'] < 0:
                        return response['ret']
                return response['cid']
            else:
                return -9001

        def result(self, cid):
            data = {'method':'result', 
             'username':self.username, 
             'password':self.pwd, 
             'appid':self.app_id, 
             'appkey':self.app_key, 
             'cid':str(cid)}
            response = self.request(data)
            return response and response['text'] or ''

        def decode(self, img_path, code_type, timeout) -> tuple:
            cid = self.upload(img_path, code_type, timeout)
            if cid > 0:
                for i in range(0, timeout):
                    result = self.result(cid)
                    if result != '':
                        return (
                         cid, result)
                    sleep(1)

                return (-3003, '')
            return (cid, '')

        def post_url(self, url, fields, files=[]):
            for key in files:
                files[key] = open(files[key], 'rb')

            res = requests.post(url, files=files, data=fields)
            return res.text

    yundama = YDMClient(username, pwd, app_id, app_key)
    uid = yundama.login()
    balance = yundama.balance()
    cid, res = yundama.decode(img_path, code_type, timeout)
    return res


def crack_wy_point_select_captcha(username, pwd, id, referer, r_username='', r_pwd='') -> str:
    """
    接入第三方获取validate, 破解网易点选验证码
    :param username: 用户名
    :param pwd: 密码
    :param id: 抓包到的id, 详情见: https://www.kancloud.cn/chensuilong/jiyan/546145
    :param referer: 抓包的请求的referer
    :param r_username: kancloud支持的其他平台的账号
    :param r_pwd: 其他平台的密码
    :return: '' 表示出错
    """
    url = 'http://wyydapi.c2567.com:10001/wyyd/shibie'
    params = (
     (
      'username', username),
     (
      'password', pwd),
     (
      'id', id),
     (
      'referer', referer),
     ('supportclick', ''),
     (
      'supportuser', r_username),
     (
      'supportpass', r_pwd))
    body = Requests.get_url_body(url=url, use_proxy=False, params=params)
    res = json_2_dict(body)
    validate = res.get('validate', '') if res.get('status', 'fail') == 'ok' else ''
    return validate


def dichotomy_match_gap_distance(bg_img_path, slide_img_path) -> (
 int, float):
    """
    用二分法匹配滑块与缺口间的距离
    :slide_img_path: 滑块的save path
    :bg_img_path: 背景图的save path
    :return:
    """
    img_rgb = imread(slide_img_path)
    img_gray = cvtColor(img_rgb, COLOR_BGR2GRAY)
    template = imread(bg_img_path, 0)
    run = 1
    w, h = template.shape[::-1]
    res = matchTemplate(img_gray, template, TM_CCOEFF_NORMED)
    L = 0
    R = 1
    loc = None
    while run < 30:
        run += 1
        threshold = (R + L) / 2
        if threshold < 0:
            print('Error')
            return
        loc = where(res >= threshold)
        if len(loc[1]) > 1:
            L += (R - L) / 2
        elif len(loc[1]) == 1:
            print('目标区域起点x坐标为：%d' % loc[1][0])
            break
        elif len(loc[1]) < 1:
            R -= (R - L) / 2

    try:
        res = loc[1][0]
    except TypeError:
        raise AssertionError('res获取失败!')

    return res