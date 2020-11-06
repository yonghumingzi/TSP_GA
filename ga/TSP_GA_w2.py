import math
from tkinter import *
from GA import GA

input_cities = []
start_city = ""
plans = 0

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
        self.button1 = Button(frame, text="cities", command=self.load)
        self.button1.pack()
        self.input = Entry(frame, textvariable=self.msgVar)
        self.input.pack(fill='x', padx=100, pady=10)
        self.button3 = Button(frame, text="begin", command=self.load)
        self.button3.pack()
        self.start = Entry(frame, textvariable=self.msgVar1)
        self.start.pack(fill='x', padx=100, pady=10)
        self.button3 = Button(frame, text="schemes", command=self.load)
        self.button3.pack()
        self.plans = Entry(frame, textvariable=self.msgVar2)
        self.plans.pack(fill='x', padx=100, pady=10)
        self.caption = Label(frame, text='')
        self.caption.pack(expand="yes")
        commandpane = Frame(frame)
        commandpane.pack(pady=10)
        self.btnHello = Button(commandpane, text="load", command=self.load)
        self.btnHello.pack(side="left")
        self.button = Button(commandpane, text="exit", command=frame.quit)
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
            self.caption["text"] = "Loading Complete"
            input_cities = in_list


class TSP_WIN(object):
    def __init__(self, aRoot, aLifeCount = 100, aWidth = 960, aHeight = 730):
        self.root = aRoot
        self.lifeCount = aLifeCount
        self.width = aWidth
        self.height = aHeight
        self.canvas = Canvas(
                    self.root,
                    width = self.width,
                    height = self.height,
                )
        self.canvas.pack(expand = YES, fill = BOTH)
        self.bindEvents()
        # self.initCitys()
        self.new()
        self.title("TSP")
        self.plans = 0


    def initCitys(self):

        self.citys = []
        self.cityNames = []
        self.citysAll = []
        self.genelist = []
        global input_cities

        with open("data.txt", 'r',encoding="gbk") as f:
            lines = f.readlines()
            index = -1
            for i in lines:
                index += 1
                line_ = i.split(',')
                if line_[0] == start_city:
                    start_pos = (float(line_[1]), float(line_[2]))

                self.citysAll.append((float(line_[1]), float(line_[2])))
                self.cityNames.append(line_[0])
                if input_cities != "":
                    if line_[0] in input_cities:
                        self.citys.append((float(line_[1]), float(line_[2])))
                else:
                    self.citys.append((float(line_[1]), float(line_[2])))

        #坐标变换
        minX, minY = self.citysAll[0][0], self.citysAll[0][1]
        maxX, maxY = minX, minY
        for city in self.citysAll[1:]:
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
        self.nodeLine = []
        for city in self.citysAll:
              x = (city[0] - minX ) * xx + xoffset
              y = hh - (city[1] - minY) * yy + yoffset
              self.nodes.append((x, y))
              if city in self.citys:
                  self.nodeLine.append((x, y))

              if city == start_pos:
                  start_node = (x, y)

              node = self.canvas.create_oval(x - r, y -r, x + r, y + r,
                    fill = "#00E5EE",
                    outline = "#104E8B",
                    tags = "node",)
              self.nodes2.append(node)

        for i in range(len(self.citysAll)):
            if start_node == self.nodes[i]:
                nameN = self.canvas.create_text(self.nodes[i][0] + 30, self.nodes[i][1],
                                                text=self.cityNames[i]+"(起始城市)",
                                                fill='black')
            else:
                nameN = self.canvas.create_text(self.nodes[i][0] + 30, self.nodes[i][1],
                                                text=self.cityNames[i],
                                                fill='black')

    def distance(self, order):
        distance = 0.0
        for i in range(-1, len(self.citys) - 1):
            index1, index2 = order[i], order[i + 1]
            city1, city2 = self.citys[index1], self.citys[index2]
            distance += math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)
        return distance

    def matchFun(self):
        return lambda life: 1.0 / self.distance(life.gene)

    def title(self, text):
        self.root.title(text)

    def line(self, order, fill="#000000"):
        self.canvas.delete("line")
        self.canvas.delete("number")
        for i in range(-1, len(order) -1):
            p1 = self.nodeLine[order[i]]
            p2 = self.nodeLine[order[i + 1]]
            self.canvas.create_line(p1, p2, fill=fill , tags = "line")
            self.canvas.create_text(abs(p2[0]+p1[0])/2+10, abs(p2[1]+p1[1])/2, fill = "blue", text = i+2, font = ('Times',15), tags= "number")
 

    def bindEvents(self):
        self.root.bind("n", self.new)
        self.root.bind("g", self.start)
        self.root.bind("s", self.stop)
        self.root.bind("c", self.another)


    def another(self, evt=None):
        gene = self.ga.plans[self.plan]
        self.line(gene.gene, f"#{self.plan}00000")
        self.title(f"方案{self.plan}")
        self.canvas.update()
        self.plan += 1

        best = gene.gene
        best_city = []
        for i in best:
            name = self.cityNames[self.citysAll.index(self.citys[i])]
            best_city.append(name)
        while best_city[0] != start_city:
            c = best_city.pop(0)
            best_city.append(c)

        c = best_city.pop(0)
        best_city.append(c)
        best_city.reverse()

    def new(self, evt = None):
        app = Application(Tk())
        app.master.mainloop()
        self.initCitys()
        self.isRunning = False
        order = range(len(self.citys))
        self.line(order)
        self.ga = GA(aCrossRate = 0.7,
                  aMutationRage = 0.02, 
                  aLifeCount = self.lifeCount, 
                  aGeneLength = len(self.citys), 
                  aMatchFun = self.matchFun(),
                  PlanNum = int(plans))


    def start(self, evt = None):
        self.isRunning = True
        while self.isRunning:
            self.ga.next()
            distance = self.distance(self.ga.best.gene)
            print("最近距离:", distance)
            self.line(self.ga.best.gene)
            self.title("TSP-gen: %d" % self.ga.generation)
            self.canvas.update()


    def stop(self, evt = None):
        self.isRunning = False
        best = self.ga.best.gene
        best_city = []
        for i in best:
            name = self.cityNames[self.citysAll.index(self.citys[i])]
            best_city.append(name)
        while best_city[0] != start_city:
            c = best_city.pop(0)
            best_city.append(c)
        print("最优路线 1："+"->".join(best_city))
        c = best_city.pop(0)
        best_city.append(c)
        best_city.reverse()
        print("最优路线 2：" + "->".join(best_city))
        self.plan = 0

    def mainloop(self):
        self.root.mainloop()


def main():
    tsp = TSP_WIN(Tk())
    tsp.mainloop()


if __name__ == '__main__':
    main()