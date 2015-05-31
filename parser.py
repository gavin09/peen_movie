import urllib2
import json
from bs4 import BeautifulSoup
import argparse
import os
import threading
import re
import time
from pymongo import MongoClient

class Parser(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        self.client = MongoClient()

    def run(self):
        self.get_article(self.url)
        print 'Done: ' + self.url

    def get_article(self, url):
        while True:
            try:
                req = urllib2.urlopen(url)
                break
            except  urllib2.HTTPError:
                continue
            except urllib2.URLError:
                continue
            else:
                continue

        db = self.client.peen_movie
        collections = db.articles
        html = req.read()
        soup = BeautifulSoup(html)
        articles = soup.find_all('div', class_='title')
        for article in articles:
            if article.a:
                url = article.a.get('href')
                title = article.a.contents[0]
                title_utf8 = title.encode('utf-8')
                if collections.find({'url': url}).count() is 0:
                    collections.insert({'url': url, 'title': title_utf8})

def get_page_number(url):
    req = urllib2.urlopen(url)
    html = req.read()
    soup = BeautifulSoup(html)
    pre_btn = soup.find_all('a', class_='btn')[3]

    if 'disabled' in soup.find_all('a', class_='btn')[3]['class']:
        return None

    print pre_btn['href']
    prev_url_str = str(pre_btn['href'])
    print re.search('\d+', prev_url_str).group()
    pre_page_num = int(re.search('\d+', prev_url_str).group())
    total = pre_page_num + 1
    return total

def get_page_url(page):
    return 'https://www.ptt.cc/bbs/movie/index' + str(page) + '.html'

if __name__ == '__main__':
    start_url = 'https://www.ptt.cc/bbs/movie/index.html'
    total_page_num = get_page_number(start_url)

    for page in range(1, total_page_num + 1):
        url = get_page_url(page)
        while True:
            try:
                Parser(url).start()
                break
            except:
                continue
        if threading.active_count() > 20:
            time.sleep(1)
