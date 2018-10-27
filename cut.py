# -*- coding: utf-8 -*-

import jieba
import csv

class Cutter():

    def __init__(self, import_filename, export_filename):
        self.__reader = csv.reader(open(import_filename, 'r'))
        self.__writer = csv.writer(open(export_filename, 'w'))
        self.__use_stop_words = False

    def run(self):
        for row in self.__import_data():
            seg_list = self.__sentences_to_words(row[1])
            if seg_list and self.__use_stop_words:
                seg_list = self.__remove_stop_words(seg_list)
            if seg_list:
                self.__export_data(seg_list)

    def set_stop_words(self, stop_words_filename):
        with open(stop_words_filename) as f:
            self.__stop_words = f.read().splitlines()
        self.__use_stop_words = True

    def __import_data(self):
        for row in self.__reader:
            yield row

    def __sentences_to_words(self, sentences):
        return [seg for seg in jieba.lcut(sentences, cut_all=False) if len(seg) >= 2 and not seg.isnumeric()]
    
    def __export_data(self, seg_list):
        self.__writer.writerow(seg_list)

    def __remove_stop_words(self, seg_list):
        return [seg for seg in seg_list if seg not in self.__stop_words]


if __name__ == '__main__':
    cutter = Cutter('news.csv', 'cut_news.csv')
    cutter.set_stop_words('stop_words.txt')
    cutter.run()

