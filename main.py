# -*- coding: utf-8 -*
import jieba
import jieba.posseg as pseg
import urllib.request
import cv2
import numpy as np


# 提取名词
keyword = []
# 原取“白日依山尽，黄河入海流”，因诗词提取效果不好，用译文代替
words = pseg.cut("太阳依傍山峦渐渐下落，黄河向着大海滔滔流趟。")
for word, flag in words:
    # print('%s %s' % (word, flag))
    if 'n' in flag:
        keyword.append(word)

# keyword = ['太阳', '山峦', '黄河', '大海']
# print(keyword)

# 利用ERNIE-ViLG为每个名词生成图像
import wenxin_api
from wenxin_api.tasks.text_to_image import TextToImage
wenxin_api.ak = ""
wenxin_api.sk = ""

url_sum = []
for i in range(len(keyword)):
    input_dict = {
        "text": keyword[i],
        "style": "卡通"
    }
    rst = TextToImage.create(**input_dict)
    img_url = rst['imgUrls'][0] # 保存生成的第一张图片
    url_sum.append(img_url)

save_img_count = 0
background_path = "picture1.png"
background = cv2.imread(background_path)
# 背景图片取四个点覆盖
for i, img_url in enumerate(url_sum):
    resp = urllib.request.urlopen(img_url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    cv2.imwrite(f"save_img/{keyword[i]}.png", image)
    image = cv2.resize(image, (90, 60))
    if i % 4 == 0:
        background[150:210, 60:150] = image
    if i % 4 == 1:
        background[500:560, 100:190] = image
    if i % 4 == 2:
        background[50:110, 600:690] = image
    if i % 4 == 3:
        background[300:360, 850:940] = image
        cv2.imwrite(f"result_pic/result_{save_img_count}.png", background)
        save_img_count += 1
        background = cv2.imread(background_path)
    if i == len(url_sum) - 1 and i % 4 != 3:
        cv2.imwrite(f"result_pic/result_{save_img_count}.png", background)
