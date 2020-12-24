# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/networklib.py
# Compiled at: 2018-09-20 03:30:03
import fileinput
from scipy import misc
import sys, os, argparse, numpy as np, random
from time import sleep
import time, datetime, scipy.misc, argparse, hashlib, urllib2, json
from qcloud_cos import CosClient
from qcloud_cos import ListFolderRequest
from qcloud_cos import DownloadFileRequest
import MySQLdb
from DBUtils.PooledDB import PooledDB
import traceback, cv2
from PIL import Image
import imageio
from qcloud_cos import CosClient
from qcloud_cos import UploadFileRequest
import shutil
from ai_eye import has_closed_eye
from skimage import io
from ai_tools import video2img as fi
from ai_tools import photo_stiching as ps
from ai_tools import insert_image2db as iim
from ai_tools import class2info as ci
from functools import wraps
from zprint import *
import requests, pdb
reload(sys)
sys.setdefaultencoding('utf-8')
pre_log_str = 'global:'

def get_cos_client_upload(pre_log_str):
    global bucket
    global bucket_upload
    global cos_client_upload
    zprint('_start')
    appid = 1253210315
    secret_id = 'AKIDKgsytdmdrsxvjKiy1vpYAcsytcDdDtkQ'
    secret_key = 'c3IMFxUwGRRGuNfmiS0MbfYGm9KJID2g'
    region = 'shanghai'
    cos_client_upload = CosClient(appid, secret_id, secret_key, region)
    bucket_upload = 'vodp'
    account = 'duobei'
    key = 'fgPueYSb+UJlhM3I7QKA0+L+kKZJmkoVnNoNxL1YCADe/ccXqI94iNWtgS4+4hSG4v5i+IWk4CRixVHRy0xSAg=='
    endpoint = 'core.chinacloudapi.cn'
    appid = 1253210315
    secret_id = 'AKIDKgsytdmdrsxvjKiy1vpYAcsytcDdDtkQ'
    secret_key = 'c3IMFxUwGRRGuNfmiS0MbfYGm9KJID2g'
    region = 'shanghai'
    cos_client = CosClient(appid, secret_id, secret_key, region)
    bucket = 'playback'
    zprint('[  end]')
    return (cos_client_upload, bucket_upload, bucket)


cos_client_upload, bucket_upload, bucket = get_cos_client_upload(pre_log_str)

def check_dir(dirpath, pre_log_str):
    get_tree()
    pre_log_str += sys._getframe().f_code.co_name + ':'
    zprint('[start]')
    if os.path.exists(dirpath) == False:
        os.makedirs(dirpath)
        zprint('/makedirs=%s' % dirpath)
    else:
        zprint('/dir %s is already exist.' % dirpath)
    zprint('[  end]')


def get_image(rootdir, roleID, infostr, rate=1, is_del_flv=1):
    get_tree()
    print '**********'
    print infostr
    task_dict = {}
    zprint(infostr[0])
    task_dict['online_class_id'] = int(infostr[0])
    task_dict['supplier_code'] = int(infostr[1])
    task_dict['student_id'] = int(infostr[2])
    task_dict['teacher_id'] = int(infostr[3])
    task_dict['classroom'] = infostr[4]
    task_dict['scheduled_date_time'] = infostr[5]
    zprint(infostr[5])
    savedir = rootdir + '/flv/'
    check_dir(savedir, pre_log_str)
    roleID = roleID
    snl = download_flv_roleID(task_dict, savedir, roleID, pre_log_str)
    zprint(snl)
    t2 = time.time()
    imgl = []
    try:
        for flv in snl:
            if flv.endswith('flv'):
                zprint(flv)
                img_tmp = fi.flv2img(flv, rate, 1, 2000)
                for img in img_tmp:
                    imgl.append(img)

                if is_del_flv:
                    os.system('rm -rf %s' % os.path.join(savedir, flv))

        t3 = time.time()
        zprint(' [%d] : %d images,timecost %f s ' % (task_dict['online_class_id'], len(imgl), t3 - t2))
    except Exception as e:
        zprint(e)

    return imgl


def download_flv_roleID(task_dict, student_video_flv_dir, roleID, pre_log_str):
    get_tree()
    pre_log_str += sys._getframe().f_code.co_name + ':'
    zprint('[start]')
    savenamel = []
    online_class_id = task_dict['online_class_id']
    supplier_code = task_dict['supplier_code']
    student_id = task_dict['student_id']
    teacher_id = task_dict['teacher_id']
    room_id = task_dict['classroom']
    scheduled_time = task_dict['scheduled_date_time']
    scheduled_time = scheduled_time[0:19]
    scheduled_time_sec = int(time.mktime(time.strptime(scheduled_time, '%Y-%m-%d %H:%M:%S')))
    flvs = list_flvs(room_id, pre_log_str)
    if len(flvs) == 0:
        zprint(' room_id=%s,len(flvs)==0' % room_id)
        return
    else:
        systemIdSet = set()
        flv_dict = {}
        for flv in flvs:
            url = flv
            if url.startswith('out-video') == False and url.startswith('out-audio') == False:
                continue
            items = url.split('-')
            flv_type = items[1]
            items = items[2].split('_')
            systemId = items[0]
            from_date_str = int(items[2])
            to_date_str = int(items[4][:-4])
            systemIdSet.add(systemId)
            flv_dict[flv] = {'url': url, 'flv_type': flv_type, 'systemId': systemId, 'from_date_str': from_date_str, 'to_date_str': to_date_str}

        if len(list(systemIdSet)) == 0:
            zprint(' len(list(systemIdSet))=0')
            return
        systemId_uid_dict = get_role(list(systemIdSet))
        if systemId_uid_dict == None:
            zprint(' systemId_uid_dict=None')
            return
        find_audio_video_flvs(flv_dict, systemId_uid_dict, online_class_id, student_id, teacher_id, pre_log_str)
        for flv, flv_dict_value in flv_dict.items():
            systemId = flv_dict_value['systemId']
            save_name = None
            if roleID == 1:
                role_id = teacher_id
            else:
                role_id = student_id
            if systemId_uid_dict.has_key(systemId) and systemId_uid_dict[systemId]['role'] == roleID and int(systemId_uid_dict[systemId]['uid']) == role_id:
                zprint('student info  download')
                if flv_dict_value['flv_type'] == 'video':
                    save_name = '%s/%d_roleid_%d_%d_%s' % (student_video_flv_dir, online_class_id, roleID, scheduled_time_sec, flv_dict_value['url'])
            if save_name != None:
                try:
                    origin_filename = '/%s/streams/%s' % (room_id, flv)
                    if not os.access(save_name, os.F_OK):
                        request = DownloadFileRequest(bucket, origin_filename, save_name)
                        download_ret = cos_client_upload.download_file(request)
                    savenamel.append(save_name)
                    pathname, filename = os.path.split(save_name)
                    zprint('path    : [%s]' % pathname)
                    zprint('name    : [%s]' % filename)
                    zprint('response: [message=%s,code=%d]' % (download_ret['message'], download_ret['code']))
                except Exception as e:
                    zprint(e.message)

        zprint('[  end]')
        return savenamel


def download_flv(task_dict, student_video_flv_dir, pre_log_str):
    get_tree()
    pre_log_str += sys._getframe().f_code.co_name + ':'
    zprint('[start]')
    roleID = 2
    download_flv_roleID(task_dict, student_video_flv_dir, roleID, pre_log_str)
    zprint('[  end]')


def find_audio_video_flvs(flv_dict, systemId_uid_dict, online_class_id, student_id, teacher_id, pre_log_str):
    get_tree()
    pre_log_str += sys._getframe().f_code.co_name + ':'
    zprint('[start]')
    audio_flvs = []
    video_flvs = []
    for flv, flv_dict_value in flv_dict.items():
        systemId = flv_dict_value['systemId']
        if systemId_uid_dict.has_key(systemId) == False:
            continue
        elif flv_dict_value['flv_type'] == 'video':
            role = None
            if systemId_uid_dict[systemId]['role'] == 2 and int(systemId_uid_dict[systemId]['uid']) == student_id:
                role = 'student'
            elif systemId_uid_dict[systemId]['role'] == 1 and int(systemId_uid_dict[systemId]['uid']) == teacher_id:
                role = 'teacher'
            if role != None:
                video_flvs.append({'flv': flv_dict_value['url'], 'role': role})

    zprint('[  end]')
    return


def newfunc(pre_log_str):
    pre_log_str += sys._getframe().f_code.co_name + ':'
    zprint(pre_log_str)


def list_flvs(room_id, pre_log_str):
    get_tree()
    pre_log_str += sys._getframe().f_code.co_name + ':'
    zprint('[start]')
    flvs = []
    try:
        dirname = '/%s/streams/' % room_id
        zprint(bucket)
        request = ListFolderRequest(bucket, dirname)
        list_folder_ret = cos_client_upload.list_folder(request)
        data = list_folder_ret['data']
        infos = data['infos']
        for info in infos:
            if info['name'].endswith('.flv') == False:
                continue
            if 'audio' in info['name']:
                continue
            flvs.append(info['name'])

    except Exception as e:
        zprint(e)

    zprint('[end]/flvs_number=%d' % len(flvs))
    return flvs


def get_role(systemIdList):
    get_tree()
    if len(systemIdList) == 0:
        return None
    else:
        appKey = '9f96268be9a24b1ebad7ad001c5ad82d'
        a = time.time()
        seconds = int(a)
        st = time.localtime(seconds)
        str1 = time.strftime('%Y-%m-%d %H:%M:%S', st)
        timestr = str(seconds * 1000)
        url = 'timestamp=%s%s' % (timestr, appKey)
        m = hashlib.md5()
        m.update(url)
        sign = m.hexdigest()
        url = 'http://admin.jiangzuotong.com/api/room/getUidAndRole?timestamp=%s&sign=%s' % (timestr, sign)
        url = 'http://admin.duobeiyun.com/api/room/getUidAndRole?timestamp=%s&sign=%s' % (timestr, sign)
        headers = {'Content-Type': 'application/json'}
        data = {}
        data['systemIdList'] = systemIdList
        dump_data = json.dumps(data)
        request = urllib2.Request(url=url, headers=headers, data=dump_data)
        try_times = 3
        try_time = 0
        while try_time < try_times:
            try:
                time.sleep(2)
                zprint(url)
                response = urllib2.urlopen(request, timeout=5).read()
                zprint(url)
                break
            except Exception as e:
                zprint('Execption:%s' % e)
                zprint('traceback.format_exc():\n%s' % traceback.format_exc())
                try_time = try_time + 1

        if try_time >= 3:
            return None
        res_dict = json.loads(response)
        systemId_uid_dict = {}
        if res_dict['success'] == False:
            return None
        systemIdList = res_dict['info']
        for systemId in systemIdList:
            systemId_uid_dict[systemId['systemId']] = systemId

        return systemId_uid_dict


def get_date_str(scheduled_date_time):
    items = scheduled_date_time.split(' ')
    date_str = items[0]
    items = date_str.split('-')
    date_str = '%s%s%s' % (items[0], items[1], items[2])
    return date_str


def get_host_id(pre_log_str):
    pre_log_str += sys._getframe().f_code.co_name + ':'
    zprint('[start]')
    cmd_str = 'hostname'
    content = os.popen(cmd_str).read()
    zprint('[' + content + ']')
    ip = content.strip('\n')
    ip = ip.lstrip('l-duobei-oco')
    host_id = ip.rstrip('.bgd.prod.ten.dm')
    host_id = host_id.lstrip('video-vipkid')
    zprint('[' + host_id + ']')
    zprint('[  end]')
    if len(host_id) == 0:
        host_id = 23
    return int(host_id)


def create_gif(gif_save_name, analyzed_images, pre_log_str):
    get_tree()
    pre_log_str += sys._getframe().f_code.co_name + ':'
    zprint('[start]')
    images = []
    if len(analyzed_images) < 1:
        return unicode('image_too_less', 'utf-8')
    imageio.imsave(gif_save_name, analyzed_images[0]['image_data'])
    zprint(' gif_save_name:%s' % gif_save_name)
    zprint('[  end]')
    return unicode(gif_save_name, 'utf-8')


def create_gif_pil(gif_save_name, analyzed_images, pre_log_str):
    get_tree()
    pre_log_str += sys._getframe().f_code.co_name + ':'
    zprint('[start]')
    images = []
    im = analyzed_images[0]['image_data']
    for i in range(1, 20):
        images.append(analyzed_images[i]['image_data'])

    im.save(gif_save_name, save_all=True, append_images=images)
    zprint(' gif_save_name:%s' % gif_save_name)
    zprint('[  end]')
    return unicode(gif_save_name, 'utf-8')


def upload_gif_for_yearbook(local_file, online_class_id, student_id, index, root_dir, pre_log_str):
    get_tree()
    cover_image_root_dir = root_dir['cover_image']
    pre_log_str += sys._getframe().f_code.co_name + ':'
    zprint('[start]')
    remote_url = '%s%s/%s_%s_%f_for_birthday.gif' % (cover_image_root_dir, student_id, online_class_id, student_id, random.random())
    zprint('[    local_file]:%s,type:%s' % (local_file, type(local_file)))
    url = upload_file(local_file, remote_url, pre_log_str)
    if url != None:
        ret_image_path = 'https://vodp.vipkid.com.cn%s' % remote_url
    else:
        ret_image_path = 'None'
    zprint('[ret_image_path]:%s' % ret_image_path)
    zprint('[ret_image_path]:%s' % ret_image_path.replace(':', '*'))
    zprint('[  end]')
    return ret_image_path


def upload_file(local_file, remote_url, pre_log_str):
    get_tree()
    pre_log_str += sys._getframe().f_code.co_name + ':'
    zprint('[start]')
    remote_url = '/cltvprocess/cover/' + remote_url
    zprint('%s,%s' % (local_file, remote_url))
    request = UploadFileRequest(bucket_upload, remote_url, local_file)
    upload_file_ret = cos_client_upload.upload_file(request)
    url = None
    zprint(' ' + upload_file_ret['message'])
    if upload_file_ret['message'] == 'SUCCESS':
        url = upload_file_ret['data']['source_url']
    elif upload_file_ret['message'] == 'ERROR_CMD_COS_FILE_EXIST':
        url = 'https://vodp.vipkid.com.cn' + remote_url
    zprint('[  end]')
    return url


def curl(img_url, img_localpath):
    response = requests.get(img_url)
    with open(img_localpath, 'wb') as (code):
        code.write(response.content)
    zprint('save to:%s' % img_localpath)


def demo_download():
    get_tree()
    infostr = 'id 82167225,supplier_code 2,student_id 11237902,teacher_id 5836483,classroom jz0d178fae8d43459bb345e0cc60c9fbc1,scheduled_date_time 2018-05-06 19:00:00.0'
    task_dict = {}
    task_dict['online_class_id'] = int(infostr.split(',')[0].split(' ')[1])
    task_dict['supplier_code'] = int(infostr.split(',')[1].split(' ')[1])
    task_dict['student_id'] = int(infostr.split(',')[2].split(' ')[1])
    task_dict['teacher_id'] = int(infostr.split(',')[3].split(' ')[1])
    task_dict['classroom'] = infostr.split(',')[4].split(' ')[1]
    task_dict['scheduled_date_time'] = infostr.split(',')[5].split(' ')[1] + ' ' + infostr.split(',')[5].split(' ')[2]
    savedir = '/data1/mingmingzhao/demo_down/'
    check_dir(savedir, pre_log_str)
    roleID = 1
    snl = download_flv_roleID(task_dict, savedir, roleID, pre_log_str)
    for name in snl:
        zprint(name)


def simple_get_image(class_id_str):
    image_dict = {}
    infolistall = ci.get_class_info(class_id_str)
    for infostrl in infolistall:
        imagelist = get_image('./', 1, infostrl)
        image_dict[infostrl[0]] = imagelist

    zprint(image_dict.keys())
    return image_dict


def demo_get_image_auto(class_id_str):
    infolistall = ci.get_class_info(class_id_str)
    for infostrl in infolistall:
        imagelist = get_image('./', 1, infostrl)
        zprint(len(imagelist))


def demo_get_image(a):
    get_tree()
    infostr = '26423226,2,3583950,2806579,jz9b116755879b49aba9fbbff930bdcf2d,2017-06-29 16:00:00'
    infolist = infostr.strip().split(',')
    zprint(infolist)
    imagelist = get_image('./', 1, infolist)


def demo_upload_file():
    local_file = 'test.jpg'
    remote_path = 'test/1.jpg'
    url = upload_file(local_file, remote_path, pre_log_str)
    zprint(url)


def test():
    zprint('test')


if __name__ == '__main__':
    url = 'https://vodp.vipkid.com.cn/cltvprocess/cover/teacher_vs_avotar/1998103_131410976_0.425909_0.000000.png'
    curl(url, 'tmp.jpg')
    class_id_str = '137881030,137072776'
    simple_get_image(class_id_str)