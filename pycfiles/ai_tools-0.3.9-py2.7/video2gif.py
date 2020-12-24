# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ai_tools/video2gif.py
# Compiled at: 2018-11-05 01:18:45
import numpy, imageio
from ai_tools import video2img as vi
from vcvf_emotion import face_emotion as fe
import pdb, os, cv2, sys
fe0 = fe.face_emotion()

def get_smile(images):
    images_smile = []
    c = 1
    for img in images:
        score, rect, time_cost = fe0.face_emotion(img)
        if len(score) > 0 and score[0] > 0.8:
            images_smile.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            sys.stdout.write('\rlen(images),len(smile)=[%d,%d/%d],score=%s,%s' % (len(images), len(images_smile), c, score, score[0] > 0.8))
        c = c + 1

    return images_smile


def create_gif(gif_name, video_url):
    images = vi.flv2img(video_url, 1, 0, 4000)
    image_smile = get_smile(images)
    dura = 0.1
    imageio.mimsave(gif_name + '%s.gif' % (len(image_smile) * 0.05), list(numpy.array(image_smile)[numpy.array(range(0, len(image_smile), 2))]), duration=dura)
    print 'gif duraton:%s s' % (len(image_smile) * 0.1 * 0.5)


def create_gif_wget(gif_name, images):
    image_smile = images
    dura = 0.1
    imageio.mimsave(gif_name + '%s.gif' % (len(image_smile) * 0.05), list(numpy.array(image_smile)[numpy.array(range(0, len(image_smile), 2))]), duration=dura)
    print 'gif duraton:%s s' % (len(image_smile) * 0.1 * 0.5)


if __name__ == '__main__':
    base_url = '/data1/mingmingzhao/data_sets/mp4/'
    video_all = 'vipkid_jz3bc4e1e7458f49a381297ee384773637_f_1522312337659_t_1522313938697.mp4,vipkid_jz40c0afcf42a54577ae80a668a8593600_f_1532087814504_t_1532089561969.mp4,vipkid_jz932a9ba4f1fd4fd5809b333a366dd64a_f_1530336593475_t_1530338142709.mp4,vipkid_jzbfad3425917946f0abaafaea966117a9_f_1531744118258_t_1531745977835.mp4,vipkid_jzc0fc4672202b492594b3d094b010a6e1_f_1531826923257_t_1531828692939.mp4,vipkid_jzd28621035a7c4304805b38d397d148ae_f_1530872632184_t_1530874638548.mp4'
    video_list = video_all.split(',')
    for video in video_list:
        video_url = os.path.join(base_url, video)
        gif_name = video.split('_')[1]
        create_gif(gif_name, video_url)