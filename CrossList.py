from math import pi,sin,cos,acos

R = 6371004

class node:
    def __init__(self, nid, lat, lon, origin):
        self.id = nid
        self.lat = lat
        self.lon = lon
        self.nedge = None
        if origin:
            self.x = cos(40 * pi / 180) * (self.lon - origin.lon) * R / 360
            self.y = (self.lat - origin.lat) * R / 360
        else:
            self.x = 0
            self.y = 0
    def distance(self, other):
        c = sin(self.lat * pi / 180) * sin(other.lat * pi /180)+ cos(self.lat * pi / 180) * cos(other.lat * pi / 180) * cos((self.lon - other.lon) * pi / 180)
        distance = R * acos(c) * pi / 180
        return distance

class edge:
    def __init__(self, node1, node2):
        self.ivex = node1
        self.ilink = None
        self.jvex = node2
        self.jlink = None
        self.length = node1.distance(node2)