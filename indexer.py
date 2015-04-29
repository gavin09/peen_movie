# -*- coding: utf-8 -*-
import json
import os
import argparse
import sys
import re

class Indexer:
    def __init__(self):
        self.forward_index = dict()

    def create_index(self, raw_data, keyword):
        keyword_utf8 = keyword.decode('utf-8')
        if not self.forward_index.has_key(keyword_utf8):
            self.forward_index[keyword_utf8] = dict()
            self.forward_index[keyword_utf8]['positive'] = list()
            self.forward_index[keyword_utf8]['negative'] = list()
            self.forward_index[keyword_utf8]['others']   = list()

        for data in raw_data:
            if keyword_utf8 in data[1]:
                if '好雷'.decode('utf-8') in data[1]:
                    self.forward_index[keyword_utf8]['positive'].append((data[0], data[1]))
                elif '負雷'.decode('utf-8') in data[1]:
                    self.forward_index[keyword_utf8]['negative'].append((data[0], data[1]))
                else:
                    self.forward_index[keyword_utf8]['others'].append((data[0], data[1]))

    def load_data_from_file(self, dirname, filename):
        if os.path.exists(os.path.join(dirname, filename)):
            with open(os.path.join(dirname, filename), 'r') as readfile:
                self.raw_data = json.load(readfile)

    def get_index(self, keyword, search_type):
        keyword_utf8 = keyword.decode('utf-8')
        if self.forward_index.has_key(keyword_utf8):
            if search_type in ('positive', 'negative', 'others'):
                for result in self.forward_index[keyword_utf8][search_type]:
                    print "Title {}, Link {}".format(result[1].encode('utf-8'), result[0].encode('utf-8'))
                return self.forward_index[keyword_utf8][search_type]
            elif search_type in ('all'):
                return self.forward_index[keyword_utf8]
        else:
            return None

if __name__ == '__main__':
    arguments = argparse.ArgumentParser()
    arguments.add_argument('--dirname', help='directory name')
    arguments.add_argument('--filename', help='filename')
    arguments.add_argument('--keyword', help='keyword to create index')
    args = arguments.parse_args()

    indexer = Indexer()
    if os.path.exists(os.path.join(args.dirname, args.filename)):
        with open(os.path.join(args.dirname, args.filename), 'r') as readfile:
            data = json.load(readfile)
            indexer.create_index(data, args.keyword)
    else:
        sys.exit()
