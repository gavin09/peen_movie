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
        if not self.forward_index.has_key(keyword):
            self.forward_index[keyword] = dict()
            self.forward_index[keyword]['positive'] = list()
            self.forward_index[keyword]['negative'] = list()
            self.forward_index[keyword]['others']   = list()

        for data in raw_data:
            if keyword in data[1]:
                if '好雷'.decode('utf-8') in data[1]:
                    self.forward_index[keyword]['positive'].append((data[0], data[1]))
                elif '負雷'.decode('utf-8') in data[1]:
                    self.forward_index[keyword]['negative'].append((data[0], data[1]))
                else:
                    self.forward_index[keyword]['others'].append((data[0], data[1]))

    def load_data_from_file(self, dirname, filename):
        if os.path.exists(os.path.join(dirname, filename)):
            with open(os.path.join(dirname, filename), 'r') as readfile:
                self.raw_data = json.load(readfile)

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
