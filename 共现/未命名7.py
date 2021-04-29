# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 12:57:27 2021

@author: 18000
"""
import selenium
import time
from selenium import webdriver

browser = webdriver.Chrome() #chrome 是对象

browser.get('http://www.pku.edu.cn')

time.sleep(5)

print(browser.current_url)
print(browser.page_source)

time.sleep(3)

browser.close()
