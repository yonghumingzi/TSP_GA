#coding: utf-8

import random
import math
import sys
import io

if sys.version_info.major < 3:
      import Tkinter
else:
      import tkinter as Tkinter
      from tkinter import *
      
from GA import GA
class Application(object):
    def __init__(self, master=None):
        self.master = master
        frame = Frame(master)
        frame.pack(expand = 'yes', fill="both")
        self.msgVar = StringVar()
        self.msgVar.set("all")
        self.msgVar1 = StringVar()
        self.msgVar1.set("西安")
        self.msgVar2 = StringVar()
        self.msgVar2.set(10)
        self.button1 = Button(frame, text="城市", command=self.load)
        self.button1.pack()
        self.input = Entry(frame, textvariable=self.msgVar)
        self.input.pack(fill='x', padx=100, pady=10)
        self.button3 = Button(frame, text="起始城市", command=self.load)
        self.button3.pack()
        self.start = Entry(frame, textvariable=self.msgVar1)
        self.start.pack(fill='x', padx=100, pady=10)
        self.button3 = Button(frame, text="方案个数", command=self.load)
        self.button3.pack()
        self.plans = Entry(frame, textvariable=self.msgVar2)
        self.plans.pack(fill='x', padx=100, pady=10)
        self.caption = Label(frame, text='')
        self.caption.pack(expand="yes")
        commandpane = Frame(frame)
        commandpane.pack(pady=10)
        self.btnHello = Button(commandpane, text="Load", command=self.load)
        self.btnHello.pack(side="left")
        self.button = Button(commandpane, text="Exit", command=frame.quit)
        self.button.pack()

    def load(self):
        global input_cities
        global start_city
        global plans
        get_input = self.input.get()
        plans = self.plans.get()
        if get_input == "all":
            input_cities = ""
            start_city = self.start.get()
            self.caption["text"] = "Loading Complete"
        else:
            start_city = self.start.get()
            in_list = get_input.split(' ')
            start_city = in_list[0]
            self.caption["text"] = "LoadingComplete"
            input_cities = in_list

class TSP_WIN(object):
      #可视化大小
      def __init__(self, aRoot, aLifeCount = 80, aWidth = 880, aHeight = 600):
            self.root = aRoot
            self.lifeCount = aLifeCount #
            self.width = aWidth
            self.height = aHeight
            self.canvas = Tkinter.Canvas(
                        self.root,
                        width = self.width,
                        height = self.height,
                  )
            self.canvas.pack(expand = Tkinter.YES, fill = Tkinter.BOTH)
            self.bindEvents()
            self.initCitys()
            self.new()
            self.title("TSP")


      def initCitys(self):
            file = open("data.txt",'r',encoding="gbk")
            self.citys = [] #城市坐标
            self.cityNames = [] #城市名字
            self.getCity = [] #读取粗略数据
            
            lines = file.readlines()

            #处理数据，获取坐标元组
            for x in lines:
                  self.getCity.append(x.strip('\n').split(',', 1))
            
            for val in self.getCity:
                  self.citys.append(tuple(map(float,val[1].split(','))))
                  self.cityNames.append(val[0])

            #获取城市名字
            print(self.cityNames)
            file.close()

            #坐标变换
            minX, minY = self.citys[0][0], self.citys[0][1]
            maxX, maxY = minX, minY
            for city in self.citys[1:]:
                  if minX > city[0]:
                        minX = city[0]
                  if minY > city[1]:
                        minY = city[1]
                  if maxX < city[0]:
                        maxX = city[0]
                  if maxY < city[1]:
                        maxY = city[1]

            w = maxX - minX
            h = maxY - minY
            xoffset = 30
            yoffset = 30
            ww = self.width - 2 * xoffset
            hh = self.height - 2 * yoffset
            xx = ww / float(w)
            yy = hh / float(h)
            r = 5
            self.nodes = []
            self.nodes2 = []
            self.nameNode = []
            for city in self.citys:
                  x = (city[0] - minX ) * xx + xoffset
                  y = hh - (city[1] - minY) * yy + yoffset
                  self.nodes.append((x, y))
                  #欧氏距离求解城市间的距离
                  node = self.canvas.create_oval(x - r, y -r, x + r, y + r,
                        fill = "#ff0000",
                        outline = "#000000",
                        tags = "node",)
                  self.nodes2.append(node)
            length = len(self.nodes2)
            for i in range(34):
                  nameN = self.canvas.create_text(self.nodes[i][0]+30,self.nodes[i][1],  
                        text = self.cityNames[i],
                        fill = 'black')

            

            
      def distance(self, order):
            distance = 0.0
            for i in range(-1, len(self.TSPcitys) - 1):
                  index1, index2 = order[i], order[i + 1]
                  city1, city2 = self.TSPcitys[index1], self.TSPcitys[index2]
                  distance += math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)
            return distance


      def matchFun(self):
            return lambda life: 1.0 / self.distance(life.gene)


      def title(self, text):
            self.root.title(text)


      def line(self, order):
            self.canvas.delete("line")
            print(order)
            for i in range(-1, len(order) -1):
                  p1 = self.TSPnodes[order[i]]
                  p2 = self.TSPnodes[order[i + 1]]
                  self.canvas.create_line(p1, p2, fill = "#000000", tags = "line")
                  self.canvas.create_text(abs(p2[0]+p1[0])/2+10, abs(p2[1]+p1[1])/2, fill = "blue", text = i+2, font = ('Times',15))
 


      def bindEvents(self):
            self.root.bind("n", self.new)
            self.root.bind("a", self.start)
            self.root.bind("s", self.stop)


      def new(self, evt = None):
            '''总和功能的函数'''
            #获取输入

            

            self.TSPcitys = [] #最终使用的城市
            self.TSPnodes = []
            tempIndex = [] #存储索引

            print(getInput)
            if getInput == ['all']:
                  self.TSPcitys = self.citys
                  self.TSPnodes = self.nodes
            else:
                  print(getInput)
                  for city in getInput:
                        tempIndex.append(self.cityNames.index(city))

                  
                  for index in tempIndex:
                        self.TSPcitys.append(self.citys[index])
                        self.TSPnodes.append(self.nodes[index])

                  self.canvas.create_text(self.TSPnodes[0][0]+80,self.TSPnodes[0][1],  
                        text = '（起始城市）',
                        fill = 'black')

            print(self.TSPnodes)
            order = range(len(self.TSPcitys))
            self.line(order)
            
            self.ga = GA(aCrossRate = 0.7, 
                  aMutationRage = 0.02, 
                  aLifeCount = self.lifeCount, 
                  aGeneLength = len(self.TSPcitys), 
                  aMatchFun = self.matchFun())
            self.isRunning = False


      def start(self, evt = None):
            self.isRunning = True
            flag = 0
            distance = 0
            while self.isRunning:
                  self.ga.next()

                  #判断基因的改变是否趋于稳定
                  #若是则flag+1
                  if self.ga.best.score == self.ga.parents.score:
                        flag += 1
                  else:
                        flag = 0

                  print(flag)
                  #若经过若干代基因的适应度未发生改变，则可认为趋于稳定，这里选取1000代
                  if flag == 1000:
                        self.isRunning = False
                        self.canvas.create_text(440,100,  
                        text = '迭代完成',
                        fill = 'blue',
                        font = ('Times',45))
                  distance = self.distance(self.ga.best.gene)
                  self.line(self.ga.best.gene)
                  self.title("TSP-gen: %d" % self.ga.generation)
                  self.canvas.update()


      def stop(self, evt = None):
            self.isRunning = False


      def mainloop(self):
            self.root.mainloop()


def main():
      tsp = TSP_WIN(Tkinter.Tk())

      tsp.mainloop()



if __name__ == '__main__':
      get = input('请输入方案数：')
      getInput = input('请输入你要生成的城市并以空格隔开,输入all表示选中所有城市：').split(' ')
      main()