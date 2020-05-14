# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import requests

class HttpGetTools:
    def getHttpBodyHtml(url):
        res = requests.get(url)
        res.encoding = 'utf-8'
        return res.text

    def getSoup(htmlText):
        return BeautifulSoup(htmlText, "html.parser")

    def getHttpById(soup,id):
        return soup.find_all(id=id)

    def getHttpByClassName(soup,className):
        return soup.find_all(class_=className)

    def getHttpByTag(soup,tag):
        return soup.find_all(tag)