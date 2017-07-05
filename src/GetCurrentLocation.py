import platform
import requests
import json
import re
import uuid
import urllib.request
import urllib.parse


class GeoWifi():

    KEY = "AIzaSyB2Iq4b6hYre2jS66Qn5bmKqg3LcVkdybQ"
    HEADERS = { 'Content-Type' : 'application/json' }

    def request(self, addr1, addr2):
        url = "https://www.googleapis.com/geolocation/v1/geolocate?key=" + self.KEY
        text = self.buildJson(addr1, addr2)
        data = urllib.parse.urlencode(text).encode(encoding="utf-8")
        req = urllib.request.Request(url, data, self.HEADERS)
        res = urllib.request.urlopen(req)
        body = res.read()

        return self.parseResponse(body)

    def buildJson(self, addr1, addr2):
        obj = {}
        obj["wifiAccessPoints"] = self.buildAddressList(addr1, addr2)
        #text = json.dumps(obj)
        return obj

    def buildAddressList(self, addr1, addr2):
        list = []
        list.append(self.buildAddress(addr1))
        list.append(self.buildAddress(addr2))
        return list

    def buildAddress(self, addr):
        dict = {"macAddress": addr}
        return dict

    def parseResponse(self, res):
        obj = json.loads(res)
        if obj["location"] is None:
            print(res)
            return None
        if obj["location"]["lat"] is None:
            print(res)
            return None
        if obj["location"]["lng"] is None:
            print(res)
            return None
        if obj["accuracy"] is None:
            accuracy = 0
        else:
            accuracy = obj["accuracy"]
        ret = {}
        ret["lat"] = obj["location"]["lat"]
        ret["lng"] = obj["location"]["lng"]
        ret["accuracy"] = accuracy
        return ret



def getLocationByIpAddress():
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    return [lon, lat]

def getLocationByWifiMACAddress():
    mac = hex(uuid.getnode())
    mac_bytes = [mac[x:x + 2] for x in range(0, len(mac), 2)]
    mac_address = ':'.join(mac_bytes[1:7])
    geo = GeoWifi()
    res = geo.request(mac_address, mac_address)
    if res is None:
        print('Fail to response!')
        exit()
    print(str(res["lat"]) + " " + str(res["lng"]) + " " + str(res["accuracy"]))


getLocationByWifiMACAddress()

"""
def getLocation():
    if platform.system() == "Windows":
        return getLocationByIpAddress()
        #Todo: Use the function below when it's completed.
        #return getLocationByWinAPI()
    else:
        return getLocationByIpAddress()
"""

