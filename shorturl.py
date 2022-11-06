import requests
from bs4 import BeautifulSoup

def parse(url):
    try:
        urlapi = 'https://acortar.link'
        session = requests.Session()
        resp = session.get(urlapi)
        soup = BeautifulSoup(resp.text,'html.parser')
        token = soup.find('input',{'name':'_token'})['value']
        payload = {'link-url':url,'custom-ending':'','_token':token}
        resp = session.post(urlapi+'/shorten',data=payload)
        soup = BeautifulSoup(resp.text,'html.parser')
        return soup.find('input',{'id':'short_url'})['value']
    except Exception as ex:
        print(str(ex))
        return url


#url1 = parse('https://repotematico.uo.edu.cu/sites/default/files/Paquete_contenido/AgADOwMAAm3wcEc_part1.rar')
#url2 = parse('https://repotematico.uo.edu.cu/sites/default/files/Paquete_contenido/AgADOwMAAm3wcEc_part2.rar')
#url3 = parse('https://repotematico.uo.edu.cu/sites/default/files/Paquete_contenido/AgADOwMAAm3wcEc_part3.rar')
#print(url)