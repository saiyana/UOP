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

def getTweets(searchTag):
    url = "https://twitter.com/search?src=typd&q=%23" + searchTag
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get(url)
    body = browser.find_element_by_tag_name('body')
    numberOfTweets = 100
    ended = True
    j = 1
    first = True
    oldCount = 0
    while ended:
        body.send_keys(Keys.PAGE_DOWN)
        newCount = int(browser.execute_script("return document.querySelectorAll('.tweet-text').length"));
        if first == True:
            oldCount = newCount
            j = j + 1
            first = False
        if oldCount == newCount:
            j = j + 1
        else:
            j = 1
        oldCount = newCount
        if (newCount >= numberOfTweets or j > 50):
            ended = False

    tweets = browser.find_elements_by_class_name('tweet-text')
    tweeters = browser.find_elements_by_css_selector('strong.fullname.show-popup-with-id.u-textTruncate')

    tweetsList = []
    tweetersList = []
    for tweeter, tweet in zip(tweeters, tweets):
        s = str(tweet.text.encode('ascii', 'ignore').decode('ascii'))
        p = str(tweeter.text.encode('ascii', 'ignore').decode('ascii'))
        p = p.strip()
        s = s.strip()
        p = re.sub(' +', ' ', p)
        s = re.sub(' +', ' ', s)
        p = p.replace('\n', '')
        p = p.replace('\t', '')
        s = s.replace('#', '')
        s = s.replace('$', '')
        s = s.replace('@', '')
        s = s.replace('\n', '')
        s = s.replace('\t', '')
        s = re.sub(r"http\S+", "", s)
        tweetsList.append(s)
        tweetersList.append(p)

    res=[]
    for i in range(0,len(tweetersList)):
        res.append({'name':tweetersList[i],'tweet':tweetsList[i]})
    return res
