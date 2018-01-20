# coding:utf-8
import json
import math
import matplotlib.pyplot as plt
from population import population

class TSP(object):

    def __init__(self):
        self.initCitys()
        self.population = population(
            crossRate = 0.7,
            mutationRate = 0.02,
            lifeCount = 100,
            geneLength = len(self.citys),
            matchFunc = self.matchFunc()
        )

    def initCitys(self):
        self.citys = []
        #接下来导入数据
        citys_list = loadJson()
        print(len(citys_list))
        for i in range(len(citys_list)-1):
            self.citys.append(citys_list[i])
            self.citys[i]["longitude"] = float(self.citys[i]["longitude"])
            self.citys[i]["latitude"] = float(self.citys[i]["latitude"])



    def matchFunc(self):
        #这里就直接= =把距离取个倒数作为评判的标准。
        return lambda life: 1.0 / self.getDistance(life.gene)

    def getDistance(self, order):
        distance = 0.0
        for i in range(0, len(self.citys)-1):
            index1, index2 = order[i], order[i+1]
            city1, city2 = self.citys[index1], self.citys[index2]
            #这里直接用欧氏距离来算了
            distance += math.sqrt((city1["longitude"] - city2["longitude"])**2 + (city1["latitude"] - city2["latitude"])**2)

        return distance
    def printResult(self, generations):
        finalGene = self.population.best.gene
        for city in finalGene:
            if (city!=finalGene[-1]):
                print("%s->"%self.citys[city]["name"],end="")
            else:
                print("%s\n"%self.citys[city]["name"])
        plt.plot(range(generations),self.result)
        plt.show()

    def run(self, generations):
        self.result = []
        for i in range(generations):
            self.population.generate()
            distance = self.getDistance(self.population.best.gene)
            if(i == 0):
                print("原种群计算出的距离:%f" %distance)
            else:
                print("第%d次种群繁衍后距离:%f" %(i, distance))
            self.result.append(distance)
        self.printResult(generations)


def loadJson():
    cityFile = open("data.json",encoding="utf-8")
    return json.load(cityFile)


if __name__ == '__main__':
    times = input("请输入循环的代数:")
    try:
        times = int(times)
    except:
        print("要输入整数哦")
        times = 1000
    tsp = TSP()
    tsp.run(times)
    # loadJson()









