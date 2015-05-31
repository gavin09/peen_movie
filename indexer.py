# -*- coding: utf-8 -*-
import json
import os
import argparse
import sys
import re
from pymongo import MongoClient

class Indexer:
    def __init__(self):
        self.forward_index = dict()
        self.client = MongoClient()

    def create_index(self, keyword):
        if not self.forward_index.has_key(keyword):
            # Initialize keyword
            self.forward_index[keyword] = dict()
            self.forward_index[keyword]['positive'] = list()
            self.forward_index[keyword]['negative'] = list()
            self.forward_index[keyword]['others']   = list()

        db = self.client.peen_movie
        articles = db.articles
        for doc in articles.find({'title': {'$regex': '.*'+ keyword +'.*' }}):
            if '好雷'.decode('utf-8') in doc['title']:
                self.forward_index[keyword]['positive'].append((doc['url'], doc['title']))
            elif '負雷'.decode('utf-8') in doc['title']:
                self.forward_index[keyword]['negative'].append((doc['url'], doc['title']))
            else:
                self.forward_index[keyword]['others'].append((doc['url'], doc['title']))

    def get_index(self, keyword, search_type):
        if self.forward_index.has_key(keyword):
            if search_type in ('positive', 'negative', 'others'):
                for result in self.forward_index[keyword][search_type]:
                    print "Title {}, Link {}".format(result[1].encode('utf-8'), result[0].encode('utf-8'))
                return self.forward_index[keyword][search_type]
            elif search_type in ('all'):
                return self.forward_index[keyword]
        else:
            return None

if __name__ == '__main__':
    arguments = argparse.ArgumentParser()
    arguments.add_argument('--keyword', help='keyword to create index')
    args = arguments.parse_args()

    indexer = Indexer()
    indexer.create_index(args.keyword)
