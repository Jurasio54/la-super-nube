import requests
from bs4 import BeautifulSoup
import json

def parse(urls):
    strurls = ''
    i = 0
    for u in urls:
        strurls += str(u)
        if i < len(urls)-1:
            strurls += '\n'
        i+=1
    api = 'https://xd-core-api.onrender.com/xdlinks/encode'
    jsondata = {'channelid':'','urls':strurls}
    resp = requests.post(api,data=json.dumps(jsondata),headers={ "Content-Type": "application/json",
                                                                'Accept': '*/*',
                                                                'Origin':'https://xdownloader.surge.sh',
                                                                'Referer':'https://xdownloader.surge.sh/'})
    jsonresp = json.loads(resp.text)
    if 'data' in jsonresp:
        return jsonresp['data']
    return None

#parse(['https://repotematico.uo.edu.cu/sites/default/files/Paquete_contenido/AgADOwMAAm3wcEc_part1.rar')