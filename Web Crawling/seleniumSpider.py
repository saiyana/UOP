import time
import requests
import sys
import json
import os
import re
import itertools
import xlsxwriter
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def getTweetsData(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")

    browser=webdriver.Chrome(chrome_options=chrome_options)
    browser.get(url)
    body=browser.find_element_by_tag_name('body')

    numberOfTweets = input("Number of tweets: ")

    ended=True
    while ended:
        body.send_keys(Keys.PAGE_DOWN)
        newCount=int(browser.execute_script("return document.querySelectorAll('.tweet-text').length"));
        if(newCount>=numberOfTweets):
            ended=False

    tweets=browser.find_elements_by_class_name('tweet-text')
    tweeters = browser.find_elements_by_css_selector('strong.fullname.show-popup-with-id.u-textTruncate')

    wfile=open("TwitterData.txt", mode='w')
    workbook = xlsxwriter.Workbook('TwitterData.xlsx')
    worksheet = workbook.add_worksheet()
    data={}
    i=0
    for tweeter,tweet in zip(tweeters,tweets):
        s=str(tweet.text.encode('ascii','ignore').decode('ascii'))
        p=str(tweeter.text.encode('ascii', 'ignore').decode('ascii'))
        p=p.strip()
        s=s.strip()
        p=re.sub(' +',' ',p)
        s=re.sub(' +',' ',s)
        p=p.replace('\n', '')
        p=p.replace('\t', '')
        s=s.replace('#','')
        s=s.replace('$','')
        s=s.replace('@','')
        s=s.replace('\n','')
        s=s.replace('\t','')
        s=re.sub(r"http\S+","",s)
        data['name']=p
        data['tweet'] = s
        wfile.write(str(data)+'\n')
        worksheet.write_string(i,0,p)
        worksheet.write_string(i,1,s)
        i=i+1

def start():
    searchTag=raw_input("Search Tag: ")
    url="https://twitter.com/search?src=typd&q=%23"+searchTag
    print "\nGetting tweets with #"+searchTag
    response=None

    try:
        response=requests.get(url)
    except Exception as e:
        print repr(e)
        sys.exit(1)

    if response.status_code!=200:
        print "Non success status code returned "+str(response.status_code)
        sys.exit(1)

    tweets=getTweetsData(url)

if __name__=="__main__":
    start()