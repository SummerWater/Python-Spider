import re
from urllib import request


class Spider():
    url = 'https://www.panda.tv/cate/lol'
    root_pattern = '<div class="video-info">([\s\S]*?)</div>'
    name_pattern = '<span class="video-nickname" title="([\s\S]*?)">'
    number_pattern = '<span class="video-number">([\s\S]*?)</span>'

    # 获取内容
    def __fetch_content(self):
        r = request.urlopen(self.url)
        htmls = r.read()
        htmls = str(htmls, encoding='utf-8')
        return htmls

    # 分析内容
    def __ananysis(self, htmls):
        root_html = re.findall(self.root_pattern, htmls)
        anchors = []
        for html in root_html:
            name = re.findall(self.name_pattern, html)
            number = re.findall(self.number_pattern, html)
            anchor = {'name': name[0], 'number': number[0]}
            anchors.append(anchor)

        return anchors

    # 精炼数据
    def __refine(self, anchors):
        l = lambda anchor: {'name': anchor['name']}

    # 排序
    def __sort(self, anchors):
        anchors = sorted(anchors, key=self.__sort_seed, reverse=True)
        return anchors

    def __sort_seed(self, anchor):
        r = re.findall('\d*', anchor['number'])
        number = float(r[0])
        if '万' in anchor['number']:
            number *= 10000
        return number

    # 展示
    def __show(self, anchors):
        for rank in range(0, len(anchors)):
            print('rank: ' + str(rank + 1) +
                  ':' + anchors[rank]['name'] +
                  ' ' + anchors[rank]['number'])

    def go(self):
        htmls = self.__fetch_content()
        anchors = self.__ananysis(htmls)
        anchors = self.__sort(anchors)
        self.__show(anchors)


spider = Spider()
spider.go()
