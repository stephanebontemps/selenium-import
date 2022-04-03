from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import requests as req

from urllib.parse import urlparse

url = 'https://www.sec.gov/Archives/edgar/data/760326/0001193125-13-226195-index.htm'
#get the domain part of the url
domain = urlparse(url).netloc
#array of item objects 
finalResuls = []

class item(object):
    def __init__(self, title, body): 
        self.title = title 
        self.body = body

#init webdriver
browser = webdriver.Chrome()
#browse to the url
browser.get(url)
#get hml content
html = browser.page_source

#extract HTML Link 
soup = BeautifulSoup(html, features="html.parser")
#research for all the <p> tag
for p in soup.find_all('a'):
   
   if (p.text.find('8k.htm') != -1):
        
        #extract local url from html tag.
        documentUrl = p.get("href")
        
        #construct url & open the child document
        browser.get("https://" + domain + documentUrl )
        #get html from child document
        documentHtml = browser.page_source
        #extract for BeautifulSoup
        docSoup = BeautifulSoup(documentHtml, features="html.parser")
         
        #1) find table (title)
        table = docSoup.find_all('table')
        
        for t in table:
             #looking for Item... = title
            if (t.text.find('Item') != -1): 
                #looking for all next <p> that contain the body of the item (loop until the next <table)
                p=""
                #emulate do loop ... :(
                tag = t
                while True:
                    np = tag.findNext('p')
                    if(np.text != '\xa0'):
                        p += "\n" + np.text
                        tag=tag.findNext('p')
                    else:
                        break
                #create final object and store it in an array
                finalResuls.append(item(t.text,p))

#check if its ok...
for obj in finalResuls:
    print( obj.title, obj.body, sep =' ' )

browser.close()