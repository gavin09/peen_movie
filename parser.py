import urllib2
import json
from bs4 import BeautifulSoup
import argparse
import os
import threading
import re
import time

class Parser(threading.Thread):
    def __init__(self, url, dirname, filename, filelock):
        threading.Thread.__init__(self)
        self.raw_data = []
        self.url = url
        self.dirname = dirname
        self.filename = filename
        self.filelock = filelock

    def run(self):
        self.get_article(self.url)
        self.save_article(self.dirname, self.filename)
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

        html = req.read()
        soup = BeautifulSoup(html)
        articles = soup.find_all('div', class_='title')
        for article in articles:
            if article.a:
                url = article.a.get('href')
                title = article.a.contents[0]
                title_utf8 = title.encode('utf-8')
                self.raw_data.append((url, title_utf8))

    def save_article(self, dirname, filename):
        self.filelock.acquire()
        with open(os.path.join(dirname, filename), 'a') as outfile:
            json.dump(self.raw_data, outfile)
            outfile.close()
        self.filelock.release()


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

    argument = argparse.ArgumentParser()
    argument.add_argument("--filename", help="export filename")
    argument.add_argument("--dirname", help="export directory")
    args = argument.parse_args()

    filelock = threading.Lock()

    if not os.path.exists(args.dirname):
        os.mkdir(args.dirname)

    total_page_num = get_page_number(start_url)

    for page in range(1, total_page_num + 1):
        url = get_page_url(page)
        while True:
            try:
                Parser(url, args.dirname, args.filename, filelock).start()
                break
            except:
                continue
        if page % 10 is 0:
            time.sleep(1)
