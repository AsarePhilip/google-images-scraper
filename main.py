import requests, time, os
from selenium import webdriver
from colorama import Fore, init
init(convert=True)

num = 0
linklist = []
validimagetype = ['JPEG','JFIF','JPG','TIFF','GIF','BMP','PNG','PPM','PGM','PBM','PNM','WEBP']

print(Fore.CYAN, end='')
searchterm = input(f"[!] Search term: ")

os.makedirs(searchterm)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('log-level=3')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome("chromedriver.exe", options=options)
driver.get(f'https://www.google.com/search?q={searchterm.replace(" ", "+")}&tbm=isch')

time.sleep(5)

imagebox = driver.page_source.split('\\u003dqdr:y","Past year",')[1]

for line in imagebox.splitlines():
    if 'http' and '",' in line and line.startswith(',["') and line.endswith(']'):
        try:
            linklist.append('http' + line.split('http')[1].split('"')[0])
        except: pass

for link in linklist:
    try:
        r = requests.get(link)
        ftype = r.headers['content-type'].split('/')[1]
        if ';' in ftype:
            ftype = ftype.split(';')[0]
        if ftype.upper() in validimagetype:
            num = num + 1
            f = open(f"{searchterm}\\{str(num)}.{ftype}", 'wb')
            for chunk in r:
                f.write(chunk)
    except Exception as e: pass

driver.close()
print(f"{Fore.CYAN}[!] Done!")