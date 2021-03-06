# coding=utf-8
from bs4 import BeautifulSoup
from CrossList import *

class way:
    '''
    定义地图数据中的way
    '''
    def __init__(self, wid):
        self.point = [] #way中包含的节点
        self.attr = {} #way的特殊属性
        self.id = wid #way的id

class map:
    """
    从xml中提取数据
    """
    def __init__(self, filename):
        self.keynode = [] #关键节点，即有特殊属性的节点
        self.ways = [] #way的列表
        self.cross_list = crosslist() #十字链表
        with open(filename,'r',encoding="utf8") as f:
            soup = BeautifulSoup(f.read(),"html.parser")
            for n in soup.find_all('node'):
                self.cross_list.add_node(n['id'],float(n['lat']),float(n['lon']))
                tags = n.find_all('tag')
                for tag in tags:
                    try:
                        self.cross_list.get_node(n['id']).attr[tag['k']] = tag['v']
                    except:
                        continue
                if len(tags) != 0:
                    self.keynode.append(self.cross_list.get_node(n['id']))
            for e in soup.find_all('way'):
                new_way = way(e['id'])
                nds = e.find_all('nd')
                tags = e.find_all('tag')
                for nd in nds:
                    new_way.point.append(nd)
                for tag in tags:
                    new_way.attr[tag['k']] = tag['v']
                self.ways.append(new_way)
                length = len(new_way.point)
                if new_way.attr.get('access') == 'permissive':
                    for i in range(length - 1):
                        self.cross_list.add_edge(self.cross_list.get_node(new_way.point[i]['ref']),
                                                 self.cross_list.get_node(new_way.point[i + 1]['ref']), 1)
                else:
                    for i in range(length - 1):
                        self.cross_list.add_edge(self.cross_list.get_node(new_way.point[i]['ref']),
                                                 self.cross_list.get_node(new_way.point[i + 1]['ref']))
            self.cross_list.cartesian_coordinate()
            for knd in self.keynode:
                try:
                    name = knd.attr['name']
                    if name.find("银行") != -1 or name.find("同仁堂") != -1 or name.find("清华大学西门") != -1 \
                            or name.find("大石桥北") != -1 or name.find("圆明园") != -1:
                        continue
                    if name == "北门" or name == "五道口" or name == "万泉河":
                        name = " "
                    for wy in self.ways:
                        try:
                            x = wy.attr['highway']
                            continue
                        except KeyError:
                            pass
                        try:
                            x = wy.attr['name']
                            continue
                        except KeyError:
                            pass
                        length = len(wy.point) - 1
                        nCross = 0
                        for i in range(length):
                            pt1 = self.cross_list.get_node(wy.point[i]['ref'])
                            pt2 = self.cross_list.get_node(wy.point[i + 1]['ref'])
                            if pt1.y == pt2.y or knd.y < min([pt1.y, pt2.y]) or knd.y > max([pt1.y, pt2.y]):
                                continue
                            x = (knd.y - pt1.y) * (pt2.x - pt1.x) / (pt2.y - pt1.y) + pt1.x
                            if x > knd.x:
                                nCross += 1
                        if nCross % 2 == 1:
                            wy.attr['name'] = name
                except KeyError:
                    continue
        for wy in self.ways:
            if 'highway' in wy.attr.keys():
                for nd in wy.point:
                    nid = nd.attrs.get('ref')
                    clo_node = self.cross_list.nodes.get(nid)
                    clo_node.is_highway = 1


    def way_rect(self, wy):
        min_x = min_y = 10000
        max_x = max_y = 0
        for nd in wy.point:
            pt = self.cross_list.get_node(nd['ref'])
            if min_x > pt.x:
                min_x = pt.x
            if min_y > pt.y:
                min_y = pt.y
            if max_x < pt.x:
                max_x = pt.x
            if max_y < pt.y:
                max_y = pt.y
        return min_x, min_y, max_x - min_x, max_y - min_y