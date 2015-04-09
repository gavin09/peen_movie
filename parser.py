import urllib2
from bs4 import BeautifulSoup

class Parser:
    def __init__(self):
        self.test = 0

    def get_article(self, url):
        req = urllib2.urlopen(url)
        html = req.read()
        soup = BeautifulSoup(html)
        articles = soup.find_all('div', class_='title')
        for article in articles:
            if article.a:
                url = article.a.get('href')
                title = article.a.contents[0]
                title_utf8 = title.encode('utf-8')
                print title_utf8

    def get_previous_page_url(self, url):
        req = urllib2.urlopen(url)
        html = req.read()
        soup = BeautifulSoup(html)
        pre_btn = soup.find_all('a', class_='btn')[3]

        if 'disabled' in soup.find_all('a', class_='btn')[3]['class']:
            return None
        print pre_btn['href']
        return pre_btn['href']

if __name__ == '__main__':
    base_url = 'https://www.ptt.cc/'
    start_url = 'https://www.ptt.cc/bbs/movie/index.html'
    parser = Parser()

    url = start_url
    while True:
        parser.get_article(url)
        next_url = parser.get_previous_page_url(url)
        if next_url == None:
            break

        url = base_url + next_url
