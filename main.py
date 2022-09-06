# coding:utf-8
import get_keywords
import use_qa_adjust_keywords
import get_ernie_vilg_pic
import math
import cv2
from PIL import Image
import urllib.request
import numpy as np
import traceback
import time


if __name__ == '__main__':
    """
    分词类型：LAC、jieba、jieba_use_paddle、key_words
    key_words为自己输入关键词,关键词用逗号隔开
    例： LAC 太阳依傍山峦渐渐下落，黄河向着大海滔滔流趟。
        jieba 太阳依傍山峦渐渐下落，黄河向着大海滔滔流趟。
        jieba_use_paddle 太阳依傍山峦渐渐下落，黄河向着大海滔滔流趟。
        key_words 太阳,山峦,黄河,大海,太阳,山峦,黄河,大海,太阳,山峦,黄河
    """
    while True:
        text = input('请输入分词类型 文本,输入"exit"退出：')
        if text == "exit":
            break

        while len(text.split(" ")) != 2 or text.split(" ")[0] not in ['LAC','jieba','jieba_use_paddle','key_words']:
            print("输入格式错误，请重新输入")
            text = input("请输入分词类型 文本")
        try:
            cut_type = text.split(" ")[0]
            contents = text.split(" ")[1]
            if cut_type == "key_words":
                contents = contents.replace("，", ",")
                key_words = contents.split(",")
            else:
                key_words = get_keywords.get_key_words(cut_type, contents)
        except:
            traceback.print_exc()
            print("分词过程发生错误，请重试")
            continue

        if len(key_words) == 0:
            print("未提取出关键词，请重新输入")
            continue

        print("key_words: ", key_words)

        # 获取记忆宫殿图像背景和坐标
        try:
            background_keywords = []
            background_coordinate = []
            with open("background_information.txt", 'r', encoding='utf-8') as f:
                background_contents = f.readlines()
                for background_content in background_contents:
                    background_keywords.append(background_content.strip().split(" ")[0])
                    background_coordinate.append(background_content.strip().split(" ")[1].split(","))
                background_coordinate = [list(map(eval, coordinate)) for coordinate in background_coordinate]
        except:
            traceback.print_exc()
            print("background_information.txt获取失败，请检查文件内容和格式")
            continue

        if len(background_keywords) == 0:
            print("背景关键词数为0，请检测background_information.txt文件")
            break

        # 是否通过 ERNIE 的自由问答功能进行造句，生成与背景更加契合的图像
        use_qa_text = input('是否需要使用自由问答进行造句，如果需要输入”yes“，输入其他为不使用：')
        if use_qa_text == "yes":
            print("正在使用 ERNIE 的自由问答造句")
            new_background_keywords = background_keywords * math.ceil(len(key_words) / len(background_keywords))
            for i in range(len(key_words)):
                try:
                    result = use_qa_adjust_keywords.get_sentence(new_background_keywords[i], key_words[i])
                    sentence = result.split(" ")[0]
                    if len(sentence) < 5 or len(sentence) > 50:
                        sentence = result.strip().split("。")[0]
                    if len(sentence) < 5 or len(sentence) > 50:
                        # 如果造的句子过长或过短则改为两个关键词空格隔开
                        sentence = f"{new_background_keywords[i]} {key_words[i]}"
                    key_words[i] = sentence
                except:
                    sentence = f"{new_background_keywords[i]} {key_words[i]}"
                    key_words[i] = sentence

        # 输出关键词（或造的句子）
        print("生成的关键词为：", key_words)

        len_background_coordinate = len(background_coordinate)

        # 使用ERNIE-ViLG生成图像，取每个关键词生成第一张图像的url
        try:
            url_sum = []
            for key_word in key_words:
                url = get_ernie_vilg_pic.get_create_pic_url(key_word)
                url_sum.append(url)
        except:
            traceback.print_exc()
            print("图像生成错误，请检查关键词内容与调用额度")
            continue

        # print("url_sum: ", url_sum)

        background_path = "picture1.png"  # 背景图像路径
        background = cv2.imread(background_path)
        save_img_count = 0
        t1 = str(time.time()).split(".")[0]  # 时间戳加入命名，避免下次运行覆盖生成图像

        try:
            # 背景图片取四个点覆盖
            for i, img_url in enumerate(url_sum):
                resp = urllib.request.urlopen(img_url)
                image = np.asarray(bytearray(resp.read()), dtype="uint8")
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)
                image1 = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                image1.save(f"save_img/{key_words[i].replace(' ', '_')}.png")

                yu = i % len_background_coordinate
                coordinates = background_coordinate[yu]
                image = cv2.resize(image, (coordinates[2] - coordinates[0], coordinates[3] - coordinates[1]))
                background[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]] = image
                if yu == len_background_coordinate - 1 or (i == len(url_sum) - 1):
                    cv2.imwrite(f"result_pic/{t1}_result_{save_img_count}.png", background)
                    save_img_count += 1
                    background = cv2.imread(background_path)
        except:
            traceback.print_exc()
            print("生成图像覆盖背景出错")
            continue
        print("图像生成完毕！")
