#!/usr/bin/env python
# encoding: utf-8
# @author: jiajia
# @time: 2018/9/10 16:54
# @Version : Python3.6

import re

from PIL import Image
import tesserocr
import matplotlib.pyplot as plt


# 图像识别类
class ImageProcessing(object):
    def __init__(self, img):
        self.img = img

    # 去除噪点
    def __RemoveNoise(self):
        # 将图片转换成灰度图
        im = Image.open(self.img)
        im = im.convert('L')
        # 二值化阈值
        threshold = 200
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        # 根据阈值进行值化
        image = im.point(table, '1')
        # 获得值化后的图像
        pix = image.load()
        # 遍历其像素值，找出噪点
        xiangsu = []
        for i in range(im.size[1]):#27
            for j in range(im.size[0]):#72
                # 四个边界点置为1
                if pix[0, 0] == 0 or pix[0, im.size[1] - 1] == 0 or pix[im.size[0] - 1, 0] == 0 \
                        or pix[im.size[0] - 1, im.size[1] - 1] == 0:
                    pix[j, i] = 1
                # 上边界点
                elif j == 0:
                    # 如果为黑点
                    if pix[0, i] == 0:
                        sign = 0
                        # 找出周围5个点为黑点个数
                        for number in range(i-1, i+1):
                            if pix[1, number] == 0:
                                sign += 1
                        if pix[0, i-1] == 0 or pix[0, i+1] == 0:
                            sign += 1
                        # 如果周围黑点个数小于或等于1个，判断为噪点，写入xiangsu中
                        if sign <= 1:
                            xiangsu.append((j, i))
                # 下边界点
                elif j == im.size[0] - 1:
                    if pix[im.size[0] - 1, i] == 0:
                        sign = 0
                        for number in range(i-1, i+1):
                            if pix[im.size[0] - 2, number] == 0:
                                sign += 1
                        if pix[im.size[0] - 1, i-1] == 0 or pix[im.size[0] - 1, i+1] == 0:
                            sign += 1
                        if sign <= 1:
                            xiangsu.append((j, i))
                # 左边界点
                elif i == 0:
                    if pix[i, 0] == 0:
                        sign = 0
                        for number in range(j-1, j+1):
                            if pix[number, 1] == 0:
                                sign += 1
                        if pix[j - 1, 0] == 0 or pix[j + 1, 0] == 0:
                            sign += 1
                        if sign <= 1:
                            xiangsu.append((j, i))
                # 右边界点
                elif i == im.size[1] - 1:
                    if pix[j, im.size[1] - 1] == 0:
                        sign = 0
                        for number in range(j-1, j+1):
                            if pix[number, im.size[1] - 1] == 0:
                                sign += 1
                        if pix[j - 1, im.size[1] - 1] == 0 or pix[j + 1, im.size[1] - 1] == 0:
                            sign += 1
                        if sign <= 1:
                            xiangsu.append((j, i))
                # 其他点位
                else:
                    if pix[j, i] == 0:
                        sign = 0
                        # 寻找周围8个点位
                        for number in range(j-1, j+1):
                            if pix[number, i - 1] == 0:
                                sign += 1
                            if pix[number, i + 1] == 0:
                                sign += 1
                        if pix[j - 1, i] == 0 or pix[j + 1, i] == 0:
                            sign += 1
                        # 如果周围黑点个数小于等于2，记录
                        if sign <= 2:
                            xiangsu.append((j, i))
        # 对记录为噪点的像素点置换成1，即由黑变白
        for i in xiangsu:
            pix[i[0], i[1]] = 1
        return image

    # 去除干扰线
    def __RemoveInterferenceIines(self):
        img = self.__RemoveNoise()
        return img

    # 切割图形
    def __CutPictures(self):
        img = self.__RemoveInterferenceIines()
        return img

    # 偏移图形
    def __RotatePictures(self):
        img = self.__CutPictures()
        return img

    # 实现识别
    def ImageRecognition(self):
        pointArr = self.__RotatePictures()
        plt.imshow(pointArr)
        plt.show()
        # 使用tesserocr进行识别，lang选择自己训练的语言库
        result = tesserocr.image_to_text(pointArr, lang='fontyp')
        # 格式化输出结果
        result = [re.findall('[A-Za-z0-9\u4e00-\u9fa5]', result[i]) for i in range(len(result))]
        result = ''.join([i[0] if i else '' for i in result])
        return result


if __name__ == '__main__':
    img = r'F:\验证码\image12.jpg'
    cutPictures = ImageProcessing(img).ImageRecognition()
    print(cutPictures)

