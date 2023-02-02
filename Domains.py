from selenium import webdriver
from time import sleep
import random
import os
from pyperclip import copy as clipCopy
from sys import argv
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import urllib.request
import csv
import sys
import time
import datetime
import openpyxl
from os import fsync
import sys
from openpyxl import load_workbook


driver= None
options = webdriver.ChromeOptions()
options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
options.add_argument("--disable-gpu")
options.add_argument("--silent")
#options.add_argument("--headless")  
options.add_argument("--start-minimized")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome('chromedriver', options=options)



def get_domains() :
    global driver
    global city
    driver.get('https://www.google.com.sa/maps')
    try:
        block= driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div/div/button')
        block.click()
        search_box= driver.find_element_by_xpath('//*[@id="searchboxinput"]')
        with open('city data.csv') as csvDataFile:
            csvReader = csv.DictReader(csvDataFile)
            for row in csvReader:
                city= row['name']
                full_search = "hotels near "+ city
                search_box.clear()
                search_box.send_keys(full_search)
                print('I will search about ' + full_search)
                search_box.send_keys(Keys.ENTER)
                sleep(3)
                get_urls()
    except:
        search_box= driver.find_element_by_xpath('//*[@id="searchboxinput"]')
        with open('city data.csv') as csvDataFile:
            csvReader = csv.DictReader(csvDataFile)
            for row in csvReader:
                    city= row['name']
                    full_search = "hotels near "+ city
                    search_box.clear()
                    search_box.send_keys(full_search)
                    print('I will search about ' + full_search)
                    search_box.send_keys(Keys.ENTER)
                    sleep(3)
                    get_urls()
        



def get_urls():
    Hotels_urls = []
    hotels_exp=[]
    for x in range(5,25,2) :
        try: 
            workbook_name = 'dataDomains.xlsx'
            wb = load_workbook(workbook_name)
            page = wb.active
            one_hotel = driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[3]/div[1]/div['+str(x)+']/div/a')
            hotel_href = one_hotel.get_attribute('href')
            #print(hotel_href)  
            driver.execute_script("window.open('"+hotel_href+"','_blank')")
            sleep(3)
            driver.switch_to.window(driver.window_handles[1])  
            sleep(2)
            driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]').send_keys(Keys.PAGE_DOWN)
            sleep(2)
            url= driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[13]/div[3]/button/div[1]/div[2]/div[1]').text
            site_valid = "."
            if (site_valid in url) : 
                print(url)
                Hotels_urls.append(url)
            else:
                print('not url')
                sleep(2)
                url=driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[13]/div[2]/button/div[1]/div[2]/div[1]').text
                Hotels_urls.append(url)
            print(Hotels_urls)
            sleep(int(x))
            driver.get('https://www.whois.com/whois/'+url)
            stime=(random.randint(3,12))
            print (stime)
            sleep(stime)
            expire_date= driver.find_element_by_xpath('//*[@id="page-wrapper"]/div/div[1]/div[3]/div[2]/div[5]/div[2]').text
            print(expire_date)
            hotels_exp.append(expire_date)
            new_urlData = [[url,expire_date]]
            for info in new_urlData:
                 page.append(info)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            wb.save(filename=workbook_name)
        except:
            #driver.close()
            driver.switch_to.window(driver.window_handles[0])
    


if __name__ == '__main__' :
    print('-'*50)
    get_domains()



