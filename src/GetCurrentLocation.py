import platform
import requests
import json

def getLocationByIpAddress():
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    return [lon, lat]

def getLocationByWinAPI():
    #Todo: Add locate methods specific for Windows through hardware, which is more accuarate.
    from ctypes import cdll



def getLocation():
    if platform.system() == "Windows":
        return getLocationByIpAddress()
        #Todo: Use the function below when it's completed.
        #return getLocationByWinAPI()
    else:
        return getLocationByIpAddress()
