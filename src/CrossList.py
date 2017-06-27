# coding=utf-8
from math import pi,sin,cos,acos

R = 6371004

class node:
    def __init__(self, nid, lat, lon):
        self.id = nid
        self.lat = lat
        self.lon = lon
        self.nedge = None
        self.x = 0
        self.y = 0
        self.attr={}

    def distance(self, other):
        c = sin(self.lat * pi / 180) * sin(other.lat * pi /180)+ cos(self.lat * pi / 180) * cos(other.lat * pi / 180) * cos((self.lon - other.lon) * pi / 180)
        distance = R * acos(c) * pi / 180
        return distance

    def cartesian_coordinate(self, origin):
        self.x = cos(40 * pi / 180) * (self.lon - origin.lon) * R / 360
        self.y = (self.lat - origin.lat) * R / 360


class edge:
    def __init__(self, node1, node2):
        self.ivex = node1
        self.ilink = None
        self.jvex = node2
        self.jlink = None
        self.length = node1.distance(node2)


class crosslist:
    def __init__(self):
        self.nodes = {}
        self.origin = node('0', 10000, 10000)
        self.farthest_node = node('1', 0, 0)

    def add_node(self, nid, lat, lon):
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
        for n in self.nodes.values():
            n.cartesian_coorinate()

    def add_edge(self, id1, id2):
        node1 = self.nodes[id1]
        node2 = self.nodes[id2]
        new_edge = edge(node1, node2)
        if node1.nedge:
            temp = node1.nedge
            node1.nedge = new_edge
            new_edge.ilink = temp
        else:
            node1.nedge = new_edge
        if node2.nedge:
            temp = node2.nedge
            node2.nedge = new_edge
            new_edge.ilink = temp
        else:
            node2.nedge = new_edge

    def get_node(self, id):
        return self.nodes[id]

    def get_edge(self, node1, node2):
        result = node1.nedge
        while True:
            if result == None:
                return None
            elif (result.ivex == node1 and result.jvex == node2) or (result.ivex == node2 and result.jvex == node1):
                return result
            elif result.ivex == node1:
                result = result.ilink
            elif result.jvex == node1:
                result = result.jlink
            else:
                raise Exception("Points and edges have Errors!")