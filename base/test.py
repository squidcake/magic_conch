import requests
from bs4 import BeautifulSoup
import re

# import xlwt
#
# import jieba
# import wordcloud


def req():
    url_head = "http://www.chinanews.com/scroll-news/"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    }

    all_news = []
    news_list = [[] for i in range(20)]
    id2tp = {}
    id = {}
    cnt = 0
    txt = " "
    for i in range(10):
        url = url_head + "news" + str(i + 1) + ".html"
        resp = requests.get(url=url, headers=headers)
        resp = resp.content.decode('utf-8', 'ignore')  # 不加第二个参数ignore会报错 忽略掉一些utf编码范围外的不知名字符
        # print(resp)

        soup = BeautifulSoup(resp, 'html.parser')

        news = soup.select('body #content #content_right .content_list ul li')
        # print(news)
        for new in news:
            new = new.text
            if new == '':
                continue

            ti = re.compile("[0-9][0-9]:[0-9][0-9]")
            date = re.compile("[0-9]{1,2}\-[0-9]{1,2}")
            # print(new)
            time = new[-10:]
            new = ti.sub('', new)
            new = date.sub('', new)
            lm = new[1:3]

            if len(lm.strip()) == 1:
                lm = "IT"
            bt = new.split(']')[1].replace(' ', '')
            txt = txt + " " + bt
            if lm not in id.keys():
                id[lm] = cnt
                id2tp[cnt] = lm
                cnt += 1
            all_news.append({
                "lm": lm,
                "bt": bt,
                "time": time
            })
    print(len(all_news))
    print(id)
    # print(id2tp)
    # workbook = xlwt.Workbook()  # 注意Workbook的开头W要大写
    #
    # sheet1 = workbook.add_sheet('sheet1', cell_overwrite_ok=True)

    # sheet1.write(0, 0, "lm")
    # sheet1.write(0, 2, "bt")
    # sheet1.write(0, 4, "time")
    # for idx, dictionary in enumerate(all_news):
    #     news_list[id[dictionary["lm"]]].append(dictionary["bt"])
    #     sheet1.write(idx + 1, 0, dictionary["lm"])
    #     sheet1.write(idx + 1, 2, dictionary["bt"])
    #     sheet1.write(idx + 1, 4, dictionary["time"])
    # workbook.save('news.xls')

    # for i in range(13):
    #     print(id2tp[i], len(news_list[i]))
    #
    # w = wordcloud.WordCloud(width=1000, font_path='chinese.ttf', height=700, background_color='white')
    # lis = jieba.lcut(txt)
    # 人为设置一些停用词
    # string = " ".join(lis).replace('的', '').replace('在', '').replace('为', '').replace('是', '').replace('有', '').replace(
    #     '和', '')
    # print(string)
    # w.generate(string)
    # w.to_file("news.png")


if __name__ == "__main__":
    req()
    # test()

