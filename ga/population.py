# coding: utf-8
import random
from individual import individual

class population(object):

    def __init__(self, crossRate, mutationRate, lifeCount, geneLength, matchFunc):
        self.crossRate = crossRate
        self.mutationRate = mutationRate
        self.lifeCount = lifeCount
        self.geneLength = geneLength
        self.matchFunc = matchFunc #计算匹配值的函数
        self.lives = []
        self.best = None
        self.generation = 0
        self.crossCount = 0
        self.mutationCount = 0
        self.bounds = 0.0 #适配值总和

        self.initPopulation()

    def initPopulation(self):
        self.lives = []
        for i in range(self.lifeCount):
            gene = [x for x in range(self.geneLength)]
            random.shuffle(gene)
            life = individual(gene)
            self.lives.append(life)

    def judge(self):
        #计算匹配值和最好的
        self.bounds = 0.0
        self.best = self.lives[0]
        for life in self.lives:
            life.score = self.matchFunc(life)
            self.bounds += life.score
            if self.best.score < life.score:
                self.best = life

    def cross(self, parent1, parent2):
        #单点交叉
        index1 = random.randint(0, self.geneLength-1)
        index2 = random.randint(index1, self.geneLength-1)
        tempGene = parent2.gene[index1:index2]
        newGene = []
        for index, g in zip(range(self.geneLength),parent1.gene):
            #我觉得这个插入有点问题诶= =
            if index == index1:
                newGene.extend(tempGene)
            if g not in tempGene:
                newGene.append(g)

        return newGene

    def mutation(self, gene):
        """突变"""
        index1 = random.randint(0, self.geneLength - 1)
        index2 = random.randint(0, self.geneLength - 1)

        newGene = gene[:]
        newGene[index1], newGene[index2] = newGene[index2], newGene[index1]
        self.mutationCount += 1
        return newGene


    def getOne(self):
        """选择一个个体"""
        #轮盘赌的算法来找个体。
        r = random.uniform(0, self.bounds)
        for life in self.lives:
              r -= life.score
              if r <= 0:
                    return life

        raise Exception("选择错误", self.bounds)

    def newChild(self):
        #产生新个体
        parent1 = self.getOne()
        rate = random.random()
        if rate <= self.crossRate:
            parent2 = self.getOne()
            gene = self.cross(parent1,parent2)
        else:
            gene = parent1.gene

        #突变
        rate = random.random()
        if rate <= self.mutationRate:
            gene = self.mutation(gene)

        #根据新的基因返回一个新的对象
        return individual(gene)

    def generate(self):
        #下一代
        self.judge()
        newPopulation = []
        newPopulation.append(self.best)
        while len(newPopulation) < self.lifeCount:
            newPopulation.append(self.newChild())
        self.lives = newPopulation
        self.generation+=1




