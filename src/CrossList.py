# coding=utf-8
from math import pi,sin,cos,acos

R = 6371004

class node:
    '''
    定义图中的节点
    '''
    def __init__(self, nid, lat, lon):
        self.id = nid #节点的id
        self.lat = lat #节点的纬度
        self.lon = lon #节点的经度
        self.edges = [] #与节点相连的第一条边
        self.x = 0
        self.y = 0
        self.attr={} #节点的额外属性

    def distance(self, other):
        #计算两节点的距离
        c = sin(self.lat * pi / 180) * sin(other.lat * pi /180)+ cos(self.lat * pi / 180) * cos(other.lat * pi / 180) * cos((self.lon - other.lon) * pi / 180)
        distance = R * acos(c) * pi / 180
        return distance

    def cartesian_coordinate(self, origin):
        #通过将一个点定义为远点计算节点的直角坐标
        self.x = cos(40 * pi / 180) * (self.lon - origin.lon) * R / 360
        self.y = (self.lat - origin.lat) * R / 360


class edge:
    '''
    定义十字链表中的边
    '''
    def __init__(self, node1, node2):
        self.ivex = node1 #边的第一个节点
        self.jvex = node2 #边的第二个节点
        self.length = node1.distance(node2) #边长


class crosslist:
    def __init__(self):
        self.nodes = {} #图中所有节点，为节点id到节点对象的字典
        self.origin = node('0', 10000, 10000) #定义一个假的节点为当前最左上点（原点）
        self.farthest_node = node('1', 0, 0) #定义一个假节点为当前最右下点（最远点）
        self.nodes['1'] = self.farthest_node
        self.nodes['0'] = self.origin
        self.edges = []

    def add_node(self, nid, lat, lon):
        #添加一个节点，传入节点id，精度，维度
        new_node = node(nid, lat, lon)
        self.nodes[nid] = new_node
        if lat < self.origin.lat:
            self.origin.lat = lat
        if lon < self.origin.lon:
            self.origin.lon = lon
        if lat > self.farthest_node.lat:
            self.farthest_node.lat = lat
        if lon > self.farthest_node.lon:
            self.farthest_node.lon = lon

    def cartesian_coordinate(self):
        #计算当前图内所有点的直角坐标
        for n in self.nodes.values():
            n.cartesian_coordinate(self.origin)

    def add_edge(self, node1, node2):
        #为节点node1和node2添加一条边
        new_edge = edge(node1, node2)
        node1.edges.append(new_edge)
        node2.edges.append(new_edge)
        self.edges.append(new_edge)

    def get_node(self, id):
        #通过节点id获得一个节点对象
        return self.nodes[id]

    def get_edge(self, node1, node2 = None):
        #寻找传入的两节点对象node1，node2的一条边，若无边返回None
        if node2:
            result = None
            for e in node1.edges:
                if (e.node1 == node1 and e.node2 == node2) or (e.node1 == node2 and e.node2 == node1):
                    result = e
                    break
            return result
        #若未传入node2参数，返回一个列表，元素为所有与node1关联的边
        else:
            return node1.edges