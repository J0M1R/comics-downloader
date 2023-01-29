import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

from url_downloader import save_file

			
import zipfile


chrome_service = Service()
options = Options()
#options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=chrome_service, options=options)

page = input('Link to the comic: ')
driver.get(page)
title = driver.find_element(By.XPATH, '//*[@id="leftside"]/div[1]/div[2]/div/a').text
issues =  driver.find_element(By.XPATH,'//*[@id="leftside"]/div[3]/div[2]/div/table/tbody')
links = {}
for target in issues.find_elements(By.TAG_NAME, 'a'):
	link = 'https://readcomiconline.li' + str(target.get_dom_attribute('href')) + str('&readType=1')
	links[link] = target.text
links = dict(reversed(list(links.items())))
volume = 0
try:
	os.mkdir(title)
except:
	print(f'{title} folder already exists')
	exit()	
print('Issues loaded')
captcha = 1
for url in links:
	driver.get(url)
	if captcha != 0 :
		input('Did you solve the captcha? ')
		captcha = 0 
	
	nr = 0
	volume+=1
	os.mkdir(f'{title}\\{links[url]}')
	for element in driver.find_elements(By.TAG_NAME, 'img'):
		if 'blogspot.com' in element.get_dom_attribute('src'):
			png = element.get_dom_attribute('src')
			nr+=1
			save_file(url=png, file_path=f"{title}\\{links[url]}", file_name=f'{nr}.jpg')

			newZip = zipfile.ZipFile(f'{title}\\{links[url]}.cbr', 'a')
			newZip.write(f'{title}\\{links[url]}\\{nr}.jpg', compress_type=zipfile.ZIP_DEFLATED,arcname=f'{nr}.jpg')
			newZip.close()	

	

	
	print(f'{links[url]} successfully downloaded.')
