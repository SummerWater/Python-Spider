import re
from urllib import request


class Spider():
    url = 'https://www.douyu.com/directory/game/LOL'
    root_pattern = '<div class="mes">([\s\S]*?)</p>'
    name_pattern = '<span class="dy-name ellipsis fl">([\s\S]*?)</span>'
    number_pattern = '<span class="dy-num fr"([\s\S]*?)>([\s\S]*?)</span>'

    # 获取内容
    def __fetch_content(self):
        htmls = request.urlopen(self.url)
        htmls = str(htmls.read(), encoding='utf-8')
        htmls = re.findall(self.root_pattern, htmls)
        return htmls

    # 解析内容
    def __analysis(self, anchors):
        res = []
        for anchor in anchors:
            name = re.findall(self.name_pattern, anchor)
            number = re.findall(self.number_pattern, anchor)
            data = {"name": name[0], "number": number[0][1]}
            res.append(data)

        return res

    # 排序
    def __sort(self, anchors):
        anchors = sorted(anchors, key=self.__sort_seed, reverse=True)
        return anchors

    def __sort_seed(self, anchor):
        r = re.findall('[^万]*', anchor['number'])

        r = float(r[0])
        if '万' in anchor['number']:
            r *= 10000

        return r

    # 展示
    def __show(self, anchors):
        for rank in range(0, len(anchors)):
            print('rank:' + str(rank + 1) + ' ' + anchors[rank]['name'] + '-----' + anchors[rank]['number'])

    # 入口
    def go(self):
        print('爬虫开始执行,目标：斗鱼TV英雄联盟人气排行；网址：' + self.url)
        anchors = self.__fetch_content()
        anchors = self.__analysis(anchors)
        anchors = self.__sort(anchors)
        self.__show(anchors)


spider = Spider()
spider.go()
