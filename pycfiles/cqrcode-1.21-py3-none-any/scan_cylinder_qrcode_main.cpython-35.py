# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\Programmer\PYTHON\cqrcode\app\scan_qrcode\scan_cylinder_qrcode_main.py
# Compiled at: 2020-04-07 10:13:40
# Size of source mod 2**32: 9103 bytes
"""
@File       :   scan_cylinder_qrcode_main.py
@Author     :   jiaming
@Modify Time:   2020/4/3 20:00
@Contact    :   https://blog.csdn.net/weixin_39541632
@Version    :   1.0
@Desciption :   None
"""
import cv2, numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from cqrcode.static._static_data import dataPath

def return_start_point(figure=None):
    """

    :param figure:
    :return:
    """
    width, height = figure.size
    img_array = figure.load()
    x = y = -1
    for i in range(width // 8):
        for j in range(height // 8):
            if img_array[(i, j)] == (255, 255, 255):
                for k in range(i, width // 8):
                    if img_array[(k, j)] != (255, 255, 255):
                        break
                else:
                    x = i

                for k in range(j, height // 8):
                    if img_array[(i, k)] != (255, 255, 255):
                        break
                else:
                    y = j

                if x != -1 and y != -1 and img_array[(i + 1, y + 1)] == (0, 0, 0):
                    return (
                     x, y)


def return_box(figure_path=None):
    """

    :param figure:
    :return:
    """
    figure = Image.open(figure_path)
    figure = figure.convert('RGB')
    width, height = figure.size
    img_array = figure.load()
    print('图片尺寸：', width, height)
    x, y = return_start_point(figure)
    print('start point: ', x, y)
    boxlist = []
    count = 0
    for i in range(x + 1, width):
        if img_array[(i, y + 1)] == (0, 0, 0):
            count += 1
        else:
            break

    boxlist.append(count // 5)
    x1 = y1 = -1
    count = 0
    for j in range(y + 1, height):
        if img_array[(x + 1, j)] == (0, 0, 0):
            count += 1
        else:
            x1 = x
            y1 = j
            break

    boxlist.append(count // 5)
    count = 0
    for i in range(1, width):
        if img_array[(x1 + i, (y1 - y) // 2)] == (0, 0, 0):
            count += 1
        else:
            break

    boxlist.append(count)
    prebox = int(round(sum(boxlist) / len(boxlist), 0))
    tmplistblack = []
    countblack = 0
    for j in range(y, height):
        if img_array[(x + prebox // 2, j)] == (0, 0, 0):
            countblack += 1
        else:
            tmplistblack.append(countblack)
            countblack = 0

    countblack = 0
    for j in range(y, height):
        if img_array[(x + prebox // 2 + 1, j)] == (0, 0, 0):
            countblack += 1
        else:
            tmplistblack.append(countblack)
            countblack = 0

    from collections import Counter
    word_counts = Counter(tmplistblack)
    top_five = word_counts.most_common(5)
    print(top_five)
    for i in top_five:
        if i[0] != 0:
            boxlist.append(i[0])
            break

    print(boxlist)


def returnBitOrNot(figure=None, coordinate=None, rate=0.8, step=5):
    """

    :param figure:
    :param coordinate:
    :param rate:
    :param step:
    :return:
    """
    pass


def return_version(figure=None, coordinate=None, box=-1):
    """

    :param figure:
    :param coordinate:
    :param box:
    :return:
    """
    pass


def scan_qrcode(image_file=dataPath + 'target1.png'):
    """

    :param image_path:
    :return:
    """
    image = cv2.imread(image_file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_file = dataPath + 'gray.png'
    Laplacian = cv2.Laplacian(gray, cv2.CV_32F, ksize=3)
    Laplacian_img = cv2.convertScaleAbs(Laplacian)
    laplacian_file = dataPath + 'laplacian.png'
    blurred = cv2.blur(Laplacian_img, (3, 3))
    _, thresh = cv2.threshold(blurred, 128, 255, cv2.THRESH_BINARY)
    thresh_file = dataPath + 'thresh.png'
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    closed = cv2.erode(closed, None, iterations=4)
    closed = cv2.dilate(closed, None, iterations=4)
    erode_dilate_file = dataPath + 'erode_dilate.png'
    cnts, hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
    rect = cv2.minAreaRect(c)
    width, height = rect[1]
    print('矩形：', rect)
    box = np.int0(cv2.boxPoints(rect))
    print('最小外接矩形4个顶点坐标:', box, type(box))
    cv2.drawContours(image, [box], 0, (255, 0, 0), 3)
    drawContours_file = dataPath + 'drawContours.png'
    new_width = int(width)
    new_height = int(height)
    pts1 = np.float32([box])
    pts2 = np.float32([
     [
      0, new_height], [0, 0], [new_width, 0], [new_width, new_height]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    warpPerspective = cv2.warpPerspective(gray, M, (new_width, new_height))
    warpPerspective_file = dataPath + 'warpPerspective_file.png'
    _, thresh_warpPerspective = cv2.threshold(warpPerspective, 0, 255, cv2.THRESH_OTSU)
    thresh_warpPerspective_file = dataPath + 'thresh_warpPerspective.png'
    cv2.imwrite(gray_file, gray)
    cv2.imwrite(laplacian_file, Laplacian_img)
    cv2.imwrite(thresh_file, thresh)
    cv2.imwrite(drawContours_file, image)
    cv2.imwrite(erode_dilate_file, closed)
    cv2.imwrite(warpPerspective_file, warpPerspective)
    cv2.imwrite(thresh_warpPerspective_file, thresh_warpPerspective)
    filePath = [
     image_file,
     gray_file,
     laplacian_file,
     thresh_file,
     erode_dilate_file,
     drawContours_file,
     warpPerspective_file,
     thresh_warpPerspective_file]
    for i in range(len(filePath)):
        plt.title(str(i))
        plt.subplot(3, 3, i + 1)
        img = cv2.imread(filePath[i], 3)
        plt.xticks([])
        plt.imshow(img)

    plt.title(str(len(filePath)))
    file = dataPath + 'procession.png'
    plt.savefig(file, dpi=300, bbox_inchs='tight')
    plt.show()
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    return_box(figure_path=dataPath + 'thresh_warpPerspective.png')