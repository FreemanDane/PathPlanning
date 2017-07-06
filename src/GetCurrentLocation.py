import requests

def getLocationByIpAddress():
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    return [lon, lat]

def getLocation():
    getLocationByIpAddress()


