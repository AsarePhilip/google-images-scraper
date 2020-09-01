import requests
import threading
import os

class Scraper(object):
    def __init__(self):
        self.imagelist = []
        self.validfiles = ['JPEG','JFIF','JPG','TIFF','GIF','BMP','PNG','PPM','PGM','PBM','PNM','WEBP']

    def getImages(self, response):
        imagerange = response.split('\\u003dqdr:y","Past year",')[1]
        for line in imagerange.splitlines():
            if line.startswith(',["http') and line.endswith(']'):
                self.imagelist.append('http' + line.split('http')[1].split('"')[0])
    
    def writeImages(self):
        print(f'[+] Found {str(len(self.imagelist))} images')
        name = 0
        for image in self.imagelist:
            try:
                r = requests.get(image)
                contenttype = r.headers['content-type']
                for ftype in self.validfiles:
                    if ftype.lower() in contenttype:
                        name = name + 1
                        f = open(f'{self.term}/{str(name)}.{ftype.lower()}', 'wb')
                        for chunk in r:
                            f.write(chunk)
                        print(f'[!] Wrote {str(name)}.{ftype.lower()}')
            except:
                pass
    
    def run(self, term):
        self.term = term
        req = requests.get(f'https://www.google.com/search?q={self.term.replace(" ", "+")}&tbm=isch',
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
        })
        self.getImages(req.text)
        self.writeImages()

if __name__ == "__main__":
    term = input('[!] Search Term: ')
    os.makedirs(term)
    Scraper().run(term)