# -*- coding: utf-8 -*-
# @Time : 2022-11-10 18:37
# @Author : beita
# @Email : 1090409167@qq.com
# @File : testWordCloud.py
# @Project : Douban_flask

import jieba  # seperate words
from matplotlib import pyplot as plt  # data visualization
from wordcloud import WordCloud  # word cloud
from PIL import Image  # image processing
import numpy as np  # 矩阵运算
import sqlite3  # database
import os.path


# prepare the required words
def words():
    con = sqlite3.connect("../douban_data.db")
    cur = con.cursor()
    sql = 'select overview from movie250'
    data = cur.execute(sql)
    text = ''
    for item in data:
        text = text + item[0]
    cur.close()
    con.close()
    return text


def separate_word(text):
    cut = jieba.cut(text)  # 中文分词1
    string = ' '.join(cut)  # 中文分词2
    return string


def img_creating():
    my_words = words()
    string = separate_word(my_words)
    img = Image.open(r'../static/img/vikki.jpg', 'r')
    img_array = np.array(img)  # 将图片转换为数组
    wc = WordCloud(
        background_color='white',
        mask=img_array,
        scale=1.8,
        font_path="/System/Library/Fonts/Supplemental/Songti.ttc"  # saving path = /System/Library/Fonts/Supplemental、
    )
    wc.generate_from_text(string)

    # image creating
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')   # 是否显示坐标轴
    # plt.show()
    plt.savefig(r'../static/img/testCloud.jpg', dpi=500)

if __name__ == '__main__':
    img_creating()
