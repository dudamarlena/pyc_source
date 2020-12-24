# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ai_tools/insert_image2db.py
# Compiled at: 2018-08-27 08:18:56
__doc__ = '\nCreated on Fri Jul 20 18:34:07 2018\n\n@author: wuhongrui\n'
import sys, MySQLdb, os
from PIL import Image

def image2db():
    localpath = 'D:/file/try/try_png'
    projectName = 'name'
    db = MySQLdb.connect(host='localhost', user='root', passwd='123456', charset='utf8')
    cursor = db.cursor()
    cursor.execute('CREATE DATABASE if not exists %s DEFAULT CHARACTER SET utf8' % projectName)
    cursor.execute('USE %s' % projectName)
    imgTbName = projectName + 'img'
    sql = "Create table if not exists %s (id int(10) unsigned primary key auto_increment, image_name varchar(200), raw_data longblob, is_marking char(20) default 'no', if_verify char(20) default 'no') default character set utf8" % imgTbName
    cursor.execute(sql)
    for imagefile in os.listdir(localpath):
        with open(os.path.join(localpath, imagefile), 'rb') as (f):
            img_data = f.read()
            f.close()
        image_name = str(imagefile)[:-4]
        sql = "INSERT INTO %s (image_name, raw_data) VALUES ('%s', '%s')" % (imgTbName, image_name, MySQLdb.escape_string(img_data))
        cursor.execute(sql)
        db.commit()

    xmlTbName = projectName + 'xml'
    sql = 'Create table if not exists %s (id int(10) unsigned primary key auto_increment, image_name varchar(200), xml_content varchar(2000), marker_id char(20)) default character set utf8' % xmlTbName
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()


def insert2db(image_name, projectName, dbindex=0):
    if dbindex == 0:
        db = MySQLdb.connect(host='172.23.250.51', user='root', passwd='20180712', charset='utf8')
    if dbindex == 1:
        db = MySQLdb.connect(host='10.106.5.9', user='oco', passwd='MyNewPass4!', charset='utf8')
    cursor = db.cursor()
    cursor.execute('CREATE DATABASE if not exists %s DEFAULT CHARACTER SET utf8' % projectName)
    cursor.execute('USE %s' % projectName)
    imgTbName = projectName + 'img'
    sql = "Create table if not exists %s (id int(10) unsigned primary key auto_increment, image_name varchar(200), raw_data longblob, is_marking char(20) default 'no', if_verify char(20) default 'no') default character set utf8" % imgTbName
    cursor.execute(sql)
    with open(os.path.join(image_name), 'rb') as (f):
        img_data = f.read()
        f.close()
    sql = "INSERT INTO %s (image_name, raw_data) VALUES ('%s', '%s')" % (imgTbName, image_name, MySQLdb.escape_string(img_data))
    print 'insert %s into %s.%s' % (image_name, projectName, imgTbName)
    cursor.execute(sql)
    db.commit()
    xmlTbName = projectName + 'xml'
    sql = 'Create table if not exists %s (id int(10) unsigned primary key auto_increment, image_name varchar(200), xml_content varchar(2000), marker_id char(20)) default character set utf8' % xmlTbName
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()


def create_db(projectName):
    db = MySQLdb.connect(host='172.23.250.51', user='root', passwd='20180712', charset='utf8')
    cursor = db.cursor()
    cursor.execute('CREATE DATABASE if not exists %s DEFAULT CHARACTER SET utf8' % projectName)
    cursor.execute('USE %s' % projectName)
    imgTbName = projectName + 'img'
    sql = "Create table if not exists %s (id int(10) unsigned primary key auto_increment, image_name varchar(200), raw_data longblob, is_marking char(20) default 'no', if_verify char(20) default 'no') default character set utf8" % imgTbName
    cursor.execute(sql)
    xmlTbName = projectName + 'xml'
    sql = 'Create table if not exists %s (id int(10) unsigned primary key auto_increment, image_name varchar(200), xml_content varchar(2000), marker_id char(20)) default character set utf8' % xmlTbName
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()


def jpg2png():
    jpgpath = 'D:/file/try/try_jpg'
    pngpath = 'D:/file/try/try_png'
    for imagefile in os.listdir(jpgpath):
        f = Image.open(os.path.join(jpgpath, imagefile))
        imagefile = str(imagefile)[:-4] + '.png'
        f.save(os.path.join(pngpath, imagefile))


if __name__ == '__main__':
    create_db('similar_students_010')
    create_db('similar_students_011')
    create_db('similar_students_012')
    create_db('similar_students_013')
    create_db('similar_students_014')