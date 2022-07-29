# coding = utf-8
import os
from bs4 import BeautifulSoup
import requests
import re


def get_fenshuxiandizhi_01():  ## 获取首页的所有新闻，检查是否有所需要的url
    url = "http://jyt.hunan.gov.cn/jyt/sjyt/hnsjyksy/web/ksyzkzx/index.html"

    res = requests.get(url)

    body = res.content.decode('utf-8')
    try:
        regular_v1 = re.findall(r"普通高校招生录取控制分数线\" href=\"(.+?)普通高校招生录取控制分数线</a>", body)
        dizhi_1 = str(regular_v1[0])

        dizhi_2 = re.sub(".html(.+?)湖南", "", dizhi_1, count=0, flags=0)
        dizhi_3 = re.sub("省(.+)", "", dizhi_2, count=0, flags=0)

        dizhi_4 = "http://jyt.hunan.gov.cn" + dizhi_3 + ".html"
    except:
        dizhi_4 = "首页无"

    return dizhi_4


def xunhuan_get_url(): ## 循环翻页30页
    dizhi = []
    for page in range(2, 30):
        url = "http://jyt.hunan.gov.cn/jyt/sjyt/hnsjyksy/web/ksyzkzx/index_" + str(page)
        html = ".html"
        qinqiu = url + html
        res = requests.get(qinqiu)

        body = res.content.decode('utf-8')
        try:
            regular_v1 = re.findall(r"普通高校招生录取控制分数线\" href=\"(.+?)普通高校招生录取控制分数线</a>", body)
            dizhi_1 = str(regular_v1[0])

            dizhi_2 = re.sub(".html(.+?)湖南", "", dizhi_1, count=0, flags=0)
            dizhi_3 = re.sub("省(.+)", "", dizhi_2, count=0, flags=0)

            dizhi_4 = "http://jyt.hunan.gov.cn" + dizhi_3 + ".html"
            dizhi.append(dizhi_4)
        except:
            continue

    return dizhi


def get_pic_all():  ## 获取所有图片
    tupian = []

    ## 首页
    shouye = get_fenshuxiandizhi_01()
    if shouye == "首页无":
        print("首页没数据，就循环翻30页")
        urllist = xunhuan_get_url()


        for i in urllist:

            res = requests.get(i)

            body_v1 = res.content.decode('utf-8')
            soup = BeautifulSoup(body_v1, 'html.parser')
            body_v2 = soup.select('#j-show-body')

            regular_v1 = re.findall(r"src=\"(.+?)\"", str(body_v2))

            tupian.append(regular_v1)
    else:
        print("首页有数据，直接用首页的url数据，去解析取图")
        res = requests.get(shouye)
        body_v1 = res.content.decode('utf-8')
        soup = BeautifulSoup(body_v1, 'html.parser')
        body_v2 = soup.select('#j-show-body')

        regular_v9 = re.findall(r"src=\"(.+?)\"", str(body_v2))
        tupian.append(regular_v9)

    return tupian


def get_pic_clear():  ## 去掉不需要的图片
    list_tu = get_pic_all()

    lastlist = []

    ishttp = "http"
    laodizhi = "http://jyt.hunan.gov.cn/jyt/sjyt/hnsjyksy/web/ksyzkzx/202106/"
    for i in list_tu:
        for j in i:
            if ishttp in j:
                lastlist.append(j)
            else:

                lastlist.append(laodizhi + j)

    return lastlist


def save_pic():  ## 最终保存图片

    new_list = get_pic_clear()

    for i in new_list:

        filename = os.path.basename(i)
        print(filename)

        r = requests.get(i, stream=True)
        with open(filename, 'wb') as fd:
            for chunk in r.iter_content():
                fd.write(chunk)

    return "保存完毕"


print(save_pic())
