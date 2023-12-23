# -*- coding: utf-8 -*-
# @Time : 2022-11-01 23:05
# @Author : beita
# @Email : 1090409167@qq.com
# @File : spider.py
# @Project : Douban_flask

from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行excel操作
import sqlite3  # 进行SQLit数据库操作

URL = "https://movie.douban.com/top250?start="


def main():
    base_url = "https://movie.douban.com/top250?start="
    # 1.爬取网页
    date_list = getData(base_url)
    # 3.保存数据

    # 保存在excel表格为xls文件
    # save_path = "./douban_data.xls"
    # save_data(date_list, save_path)

    # 保存数据库，sqlite
    save_db_path = "./douban_data.db"
    save_data_sqlit(date_list, save_db_path)    # The second parameter is the address of the database


# 影片详情链接规则
find_link = re.compile(r'<a href="(.*?)">')  # re.compile()创建正则表达式对象，表示字符串规则  'r'忽略转义字符
# 影片封面图片规则
find_image = re.compile(r'<img alt=".*?" class="" src="(.*?)" width="100"/>', re.S)  # 正则表达式()中为选择
# 影片片名
find_movie_name = re.compile(r'<span class="title">(.*?)</span>', re.S)
# 电影分数 movie grades
find_movie_grade = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
# 评价人数 the number of people who rated this movie
find_num_judge = re.compile(r'<span>(\d*)人评价</span>')
# 电影概述 overview of this movie
find_overview = re.compile(r'<span class="inq">(.*)</span>')
# 影片相关内容 relevant content of this movie
find_bd = re.compile(r'<p class="">(.*?)</p>', re.S)


# 爬取网页
def getData(base_url):
    data_list = []
    for i in range(0, 10):  # 调用获取html网页十次
        url = URL + str(i * 25)
        html = askURL(url)  # 保存获取到的原码
        # 2.解析数据
        # print(html)
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all("div", class_="item"):  # 查找符合要求的字符串，形成列表
            # print(item)  # 测试: 查看一部电影的所有信息
            data = []  # 保存一部电影的所有信息
            item = str(item)
            link = re.findall(find_link, item)[0]  # 通过re库进行正则表达式匹配
            image_url = re.findall(find_image, item)[0]
            movie_names = re.findall(find_movie_name, item)
            movie_grade = re.findall(find_movie_grade, item)[0]
            num_judge = re.findall(find_num_judge, item)[0]
            overviews = re.findall(find_overview, item)
            bd = re.findall(find_bd, item)[0]
            data.append(link)
            data.append(image_url)
            if len(movie_names) == 2:
                cname = movie_names[0]
                fname = movie_names[1].replace("\xa0/\xa0", "")
                data.append(cname)
                data.append(fname)
            else:
                data.append(movie_names[0].replace("\xa0/\xa0", ""))
                data.append("")
            data.append(movie_grade)
            data.append(num_judge)
            if len(overviews) != 0:
                data.append(overviews[0].replace("。", "").strip())
            else:
                data.append("")
            bd = re.sub(r'<br(\s+)?/>(\s+)?', "", bd)  # remove <br>
            data.append(bd.replace(r"\n", "").strip().replace("\xa0", " "))
            data_list.append(data)

    return data_list


# movie.douban.com/top250?start=0
# 得到指定一个网址的url
def askURL(url):
    head = {  # 伪装成浏览器
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/106.0.0.0 Safari/537.36 "
    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# save data (xls文件 excel
def save_data(data_list, save_path):
    print("saving...")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet("豆瓣电影TOP250", cell_overwrite_ok=True)
    col = ("link of detail", "url of picture", "chinese name", "foreign name", "score", "num of grades", "overview",
           "relevant info")
    for i in range(0, len(col)):
        sheet.write(0, i, col[i])  # 标题
    for n in range(0, len(data_list)):
        # print(f"打印第{n + 1}个...")
        data = data_list[n]
        for c in range(0, len(data)):
            sheet.write(n + 1, c, data[c])
    book.save(save_path)


# save data (database sqlite3
def save_data_sqlit(data_list, db_path):
    print("saving...")
    init_db(db_path)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    for data in data_list:
        sql = "insert into movie250 (link, pic_link, cname, fname, score, num_rate, overview, info) values ("
        for index in range(len(data)):
            sql = sql + ' "' + data[index] + '",'
        sql = sql[:-1] + ")"
        # print(sql)
        cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


def init_db(db_path):
    sql = """
        create table movie250
        (
            id integer primary key autoincrement,
            link text,
            pic_link text,
            cname varchar,
            fname varchar,
            score numeric, 
            num_rate numeric,
            overview text,
            info text
        )
    """  # create database 创建数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # invoke function
    main()
    print("python finished")
