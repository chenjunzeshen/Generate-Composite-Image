# coding:utf-8
from LAC import LAC
import jieba
import jieba.posseg as pseg
import paddle


def get_key_words(cut_type, text):
    keywords = []
    try:
        if cut_type == "LAC":
            # 装载LAC模型
            lac = LAC(mode='lac')
            lac_result = lac.run(text)
            for i in range(len(lac_result[1])):
                if 'n' in lac_result[1][i]:
                    keywords.append(lac_result[0][i])
        elif cut_type == "jieba":
            words = pseg.cut(text)
            for word, flag in words:
                if 'n' in flag:
                    keywords.append(word)
        else:   # jieba_use_paddle
            paddle.enable_static()
            jieba.enable_paddle()
            words = pseg.cut(text, use_paddle=True)
            for word, flag in words:
                if 'n' in flag:
                    keywords.append(word)
    except:
        keywords = []
    return keywords
