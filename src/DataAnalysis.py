# coding=utf-8
from bs4 import BeautifulSoup
from src.CrossList import *

class way:
    def __init__(self, wid):
        self.point = []
        self.attr = {}
        self.id = wid

class map:
    """
    todo:ectract infomation from xml file
    """
    def __init__(self, filename):
        self.keynode = []
        self.ways = []
        self.cross_list = crosslist()
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
                nds = n.find_all('nd')
                tags = n.find_all('tag')
                for nd in nds:
                    new_way.point.append(nd)
                for tag in tags:
                    new_way.attr[tag['k']] = tag['v']
                self.ways.append(new_way)
                length = len(new_way.point)
                for i in range(length - 1):
                    self.cross_list.add_edge(new_way.point[i], new_way.point[i + 1])
