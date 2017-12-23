# coding:utf-8

INITIAL_SCORE = -1

class individual(object):
    def __init__(self, gene = None):
        self.gene = gene
        self.score = INITIAL_SCORE