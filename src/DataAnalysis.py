# coding=utf-8
from bs4 import BeautifulSoup
from src.CrossList import *

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
                        n.attr[tag['k']] = tag['v']
                    except:
                        continue
                if len(tags) != 0:
                    self.keynode.append(n)
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
                for i in range(length - 1):
                    self.cross_list.add_edge(self.cross_list.get_node(new_way.point[i]['ref']),self.cross_list.get_node( new_way.point[i + 1]['ref']))
