# -*- coding: utf-8 -*
import jieba
import jieba.posseg as pseg
import urllib.request
import cv2
import numpy as np


keyword = []
words = pseg.cut("太阳依傍山峦渐渐下落，黄河向着大海滔滔流趟。")
for word, flag in words:
    # print('%s %s' % (word, flag))
    if 'n' in flag:
        keyword.append(word)

print(keyword)

"""
import wenxin_api # 可以通过"pip install wenxin-api"命令安装
from wenxin_api.tasks.text_to_image import TextToImage
wenxin_api.ak = "38HiO94zM8Ggf8W8BAORPQBg5K6lOsYb"
wenxin_api.sk = "RTpP3e0xvwLxmWqBmZ930dsSVVWzHPIP"
input_dict = {
    "text": keyword[0],
    "style": "卡通"
}
rst = TextToImage.create(**input_dict)
print(rst)
"""

res = {'imgUrls': ['https://wenxin.baidu.com/younger/file/ERNIE-ViLG/3a69d18e7ce0de83c0f042efe9ed0be4ex', 'https://wenxin.baidu.com/younger/file/ERNIE-ViLG/3a69d18e7ce0de83c0f042efe9ed0be4i4', 'https://wenxin.baidu.com/younger/file/ERNIE-ViLG/3a69d18e7ce0de83c0f042efe9ed0be45q', 'https://wenxin.baidu.com/younger/file/ERNIE-ViLG/3a69d18e7ce0de83c0f042efe9ed0be430', 'https://wenxin.baidu.com/younger/file/ERNIE-ViLG/3a69d18e7ce0de83c0f042efe9ed0be4v9', 'https://wenxin.baidu.com/younger/file/ERNIE-ViLG/3a69d18e7ce0de83c0f042efe9ed0be4a2']}
img_url = res['imgUrls'][0]
print(img_url)

resp = urllib.request.urlopen(img_url)
image = np.asarray(bytearray(resp.read()), dtype="uint8")
image = cv2.imdecode(image, cv2.IMREAD_COLOR)
image = cv2.resize(image, (90, 60))
# cv2.imshow("image", image)
# cv2.waitKey(0)

background = cv2.imread("picture1.png")
background[:60, :90] = image

cv2.imshow("image", background)
cv2.waitKey(0)
