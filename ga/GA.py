import random
from Life import Life

class GA(object):
    def __init__(self, aCrossRate, aMutationRage, aLifeCount, aGeneLength, aMatchFun = lambda life : 1, PlanNum = 0):
        self.PlanNum = PlanNum
        self.crossRate = aCrossRate
        self.mutationRate = aMutationRage
        self.lifeCount = aLifeCount
        self.geneLenght = aGeneLength
        self.matchFun = aMatchFun
        self.lives = []
        self.best = None
        self.generation = 1
        self.crossCount = 0
        self.mutationCount = 0
        self.bounds = 0.0
        self.initPopulation()


    def initPopulation(self):
        self.lives = []
        # 有lifeCount个种群
        for i in range(self.lifeCount):
            gene = [ x for x in range(self.geneLenght) ]
            random.shuffle(gene)
            life = Life(gene)
            self.lives.append(life)

    def judge(self):
        self.bounds = 0.0
        self.best = self.lives[0]
        for life in self.lives:
              life.score = self.matchFun(life)
              self.bounds += life.score
              if self.best.score < life.score:
                    self.best = life
        self.plans = []
        lives = list(set(self.lives))
        if self.PlanNum > len(lives):
            self.PlanNum = len(lives)
        for i in range(self.PlanNum):
            bounds = 0.0
            best = lives[0]
            best_index = 0
            for i in range(len(lives)):
                life = lives[i]
                life.score = self.matchFun(life)
                bounds += life.score
                if best.score < life.score:
                    best = life
                    best_index = i

            a = lives.pop(best_index)
            self.plans.append(a)

    def cross(self, parent1, parent2):
        index1 = random.randint(0, self.geneLenght - 1)
        index2 = random.randint(index1, self.geneLenght - 1)
        temp = parent2.gene[index1:index2]  # 交叉的基因片段
        new = []
        p1len = 0
        for g in parent1.gene:
            if p1len == index1:
                new.extend(temp)
                p1len += 1
            # 把index1之前的位置按原序加入，后面悉数补上(顺序一致)
            if g not in temp:
                new.append(g)
                p1len += 1
        self.crossCount += 1
        return new

    def mutation(self, gene):
        index1 = random.randint(0, self.geneLenght - 1)
        index2 = random.randint(0, self.geneLenght - 1)
        newGene = gene[:]
        newGene[index1], newGene[index2] = newGene[index2], newGene[index1]
        self.mutationCount += 1
        return newGene

    def getOne(self):
        r = random.uniform(0, self.bounds)
        for life in self.lives:
            r -= life.score
            if r <= 0:
                return life
        raise Exception("选择错误", self.bounds)

    def newChild(self):
        parent1 = self.getOne()
        rate = random.random()
        if rate < self.crossRate:
            parent2 = self.getOne()
            gene = self.cross(parent1, parent2)
        else:
            gene = parent1.gene
        rate = random.random()
        if rate < self.mutationRate:
            gene = self.mutation(gene)
        return Life(gene)

    def next(self):
        self.judge()
        newLives = []
        newLives.append(self.best)
        while len(newLives) < self.lifeCount:
            newLives.append(self.newChild())
        self.lives = newLives
        self.generation += 1
