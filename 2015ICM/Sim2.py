import random
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import copy

class CT():
    def __init__(self):
        self.tot = 0
        self.num = 0
        self.PN = [6,30,52,66,71,79,90] #wait
        self.CA = [6,30,52,66,71,79,90]
        self.EXP = [0,0,12,12,24,24,36]
        self.NEW_EXP = [2,1,3,4,5,6,7]
        self.alp = [1,1,1,2,2,2,1]
        self.cost_of_recruitment = [0.3,0.1,0.3,0.6,0.6,0.7,1.2]
        self.salary = [0.9,0.9,1,1.5,2,4,8]
        self.training_cost = [0.05,0.3,0.1,0.3,0.2,0.6,0.5]
    def new_id(self):
        ret = self.tot
        self.tot += 1
        return ret
    def check(self,a):
        if (a < 0):
            return 0
        if (a > 100):
            return 100
        return a

ct = CT()
class Worker():
    def __init__(self, lv=0, name_of_department = "" ,new=False):
        self.PN = ct.check(random.gauss(50,20))
        self.CA = ct.check(random.gauss(50,20))
        self.EXP = random.randint(0,10)
        self.name_of_department = name_of_department
        self.id = ct.new_id()
        self.level = lv
        self.sum_leave = 0
        if new == True:
            self.EXP = -ct.NEW_EXP[self.level]
    def cal_proformance(self):
        return 0.45 * self.CA + 0.05 * self.EXP + 0.5 * self.PN

class Department():
    def __init__(self, name_of_department, list_of_worker):
        self.name = name_of_department
        self.list_of_worker = list()
        self.fa = ""
        for i in range(7):
            for j in range(list_of_worker[i]):
                self.list_of_worker.append(Worker(i,name_of_department))

class Human_Capital_Network():
    def __init__(self,o):
        self.number_of_invite = 0
        self.department = dict()
        self.position = list()
        self.level_of_position = list()
        self.department_of_position = list()
        self.month = 0
        self.proformance_of_department = dict()
        self.draw_pos = None
        self.g = None
        self.color = None
        self.node_size = None
        self.cost = 0
        self.o = o
        ###################
        f = open("list.in")
        lines = f.readlines()
        for line in lines:
            str = line.split('(')
            name = str[0]
            num = str[1].split(')')[0]
            num = num.split('/')
            num = [int(i) for i in num]
            print num
            self.add_department(name,num)
        f.close()
        self.add_fa_department('VP','CEO')
        self.add_fa_department('HR','CEO')
        self.add_fa_department('CFO*','CEO')
        self.add_fa_department('CIO*','CEO')
        self.add_fa_department('Research','CEO')
        self.add_fa_department('Facilities','CEO')
        self.add_fa_department('Sales Markting','CEO')
        self.add_fa_department('Networks*','Research')
        self.add_fa_department('Infomation*','Research')
        self.add_fa_department('Program Manager*','VP')
        self.add_fa_department('Production Manager*','VP')
        self.add_fa_department('Plant Blue*','Facilities')
        self.add_fa_department('Plant Green*','Facilities')
        self.add_fa_department('Ragional*','Sales Markting')
        self.add_fa_department('Inrernet*','Sales Markting')
        self.add_fa_department('World Wids*','Sales Markting')
        self.add_fa_department('Director1','Production Manager*')
        self.add_fa_department('Director2','Production Manager*')
        self.add_fa_department('Director3','Production Manager*')
        self.add_fa_department('Director4','Production Manager*')
        self.add_fa_department('Director5','Production Manager*')
        self.add_fa_department('Director6','Production Manager*')
        self.add_fa_department('Branch A*','Director1')
        self.add_fa_department('Branch B*','Director1')
        self.add_fa_department('Branch C*','Director2')
        self.add_fa_department('Branch D*','Director2')
        self.add_fa_department('Branch E*','Director3')
        self.add_fa_department('Branch F*','Director3')
        self.add_fa_department('Branch G*','Director3')
        self.add_fa_department('Branch H*','Director4')
        self.add_fa_department('Branch I*','Director5')
        self.add_fa_department('Branch J*','Director5')
        self.add_fa_department('Branch K*','Director6')
        self.add_fa_department('Branch L*','Director6')
        self.update_position()
        self.get_network()

    def add_department(self, name_of_department, list_of_worker):
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~:",name_of_department
        self.department[name_of_department] = Department(name_of_department, list_of_worker)
        self.proformance_of_department[name_of_department] = 0

    def add_fa_department(self, s1, s2):
        self.department[s1].fa = s2

    def cal_alp(self, k):
        ret = ct.alp[self.level_of_position[k]] \
        * (1-self.position[k].PN/100)
        l = len(self.position)
        s1 = 0
        s2 = self.position[k].PN+0.01
        for i in range(l):
            if self.position[i] != None:
                if self.matrix[k][i] == 1:
                    if self.position[i].EXP < 0:
                        s1 += self.position[i].PN
                    s2 += self.position[i].PN
        ret += s1/s2
        ret += self.position[k].cal_proformance() / (self.o * ct.salary[self.level_of_position[k]])
        return ret


    def update_position(self):
        self.position = list()
        for i in self.department:
            for j in self.department[i].list_of_worker:
                self.position.append(j)
        l = len(self.position)
        self.level_of_position = [-1 for i in range(l)]
        for i in range(l):
            if self.position[i] != None:
                self.level_of_position[i] = self.position[i].level
        self.department_of_position = ['' for i in range(l)]
        for i in range(l):
            if self.position[i] != None:
                self.department_of_position[i] = self.position[i].name_of_department

    def add_edge(self,u,v):
        self.matrix[u][v] = 1
        self.matrix[v][u] = 1

    def get_network(self):
        l = len(self.position)
        self.matrix = [[0 for i in range(l)] for j in range(l)]
        for i in range(l):
            for j in range(l):
                if i < j:
                    if self.position[i].name_of_department \
                        == self.position[j].name_of_department:
                        self.add_edge(i,j)
                    ni = self.position[i].name_of_department
                    nj = self.position[j].name_of_department
                    if self.department[ni].list_of_worker[len(self.department[ni].list_of_worker)-1].id == self.position[i].id \
                    and self.department[nj].list_of_worker[len(self.department[nj].list_of_worker)-1].id == self.position[j].id \
                    and ((self.department[ni].fa == nj) or (self.department[nj].fa == ni)):
                        self.add_edge(i,j)

    def init_draw(self):

        l = len(self.position)

        self.color = ['r' for i in range(l)]
        self.node_size = [100 for i in range(l)]
        self.g = nx.Graph()
        self.g.add_nodes_from(range(l))
        for i in range(l):
            for j in range(l):
                if self.matrix[i][j] == 1:
                    self.g.add_edge(i,j)
        self.draw_pos = nx.spring_layout(self.g)


    def draw(self,name):
        l = len(self.position)
        plt.cla()
        plt.figure(figsize=(20,20))
        for i in range(l):
            if self.position[i] == None or self.position[i].EXP < 0:
                self.color[i] = 'b'
                self.node_size[i] = 500

        nx.draw(self.g,pos=self.draw_pos,node_size=self.node_size,node_color=self.color)
        plt.savefig('d%d.png' % (name))

    def make_leave(self, k):
        l = len(self.position)
        for i in range(l):
            if self.position[i] != None and self.matrix[k][i] == 1:
                self.position[i].sum_leave += self.position[k].PN
        self.position[k] = None

    def invite(self, k):
        if self.level_of_position[k] <= 1:
            if self.number_of_invite > 370*0.1/12:
                return
            self.number_of_invite += 1
            self.position[k] = Worker(self.level_of_position[k], name_of_department = self.department_of_position[k], new=True)
            self.cost += ct.cost_of_recruitment[self.level_of_position[k]]
        else:
            max_of_proformance = 0
            max_of_position = -1
            l = len(self.position)
            for i in range(l):
                if self.position[i] != None \
                and self.level_of_position[i]+1 == self.level_of_position[k] \
                and self.position[i].EXP >= ct.EXP[self.level_of_position[i]] \
                and self.position[i].cal_proformance() > max_of_proformance:
                    max_of_proformance = self.position[i].cal_proformance()
                    max_of_position = i
            if max_of_position != -1:
                self.position[k] = self.position[max_of_position]
                self.position[k].level = self.level_of_position[k]
                self.position[max_of_position] = None
            else:
                if self.number_of_invite > 370*0.1/12:
                    return
                self.number_of_invite += 1
                self.position[k] = Worker(self.level_of_position[k], name_of_department = self.department_of_position[k], new=True)
                self.cost += ct.cost_of_recruitment[self.level_of_position[k]]*self.o

    def run(self, rate_of_leave):

        l = len(self.position)
        proformance = 0
        unhealthy = 0
        rate_of_leave = 4000/self.o * rate_of_leave
        self.number_of_invite = 0
        self.cost = 0
        tmp = [0 for i in range(l)]
        alp = [0 for i in range(l)]
        #print alp
        for i in range(l):
            if self.position[i] != None:
                 alp[i] = self.cal_alp(i)
        #print "alp:", alp
        s = sum(alp)
        for i in range(l):
            if alp[i] != 0:
                tmp[i] = alp[i] / s * rate_of_leave * l
        for i in range(l):
            if random.random() < tmp[i]:
                self.make_leave(i)
        for i in range(l):
            if self.position[i] == None:
                self.invite(i)
        for i in self.proformance_of_department:
            self.proformance_of_department[i] = 0
        for i in range(l):
            if self.position[i] != None and self.position[i].EXP >= 0:
                #print '!!!!:', self.position[i].name_of_department
                self.proformance_of_department[self.position[i].name_of_department] += (self.position[i].CA + self.position[i].EXP)/2 + self.position[i].PN * (self.position[i].level/7) #####wait
        ##cal team proformance
        for i in self.proformance_of_department:
            proformance += self.proformance_of_department[i]
        for i in range(l):
            if self.position[i] == None:
                unhealthy += ct.CA[self.level_of_position[i]] + ct.PN[self.level_of_position[i]]
                continue
            if self.position[i].CA < ct.CA[self.level_of_position[i]]:
                unhealthy += ct.CA[self.level_of_position[i]] - self.position[i].CA
            if self.position[i].PN < ct.PN[self.level_of_position[i]]:
                unhealthy += ct.PN[self.level_of_position[i]] - self.position[i].PN
        ##cal company proformance
        num = 0
        for i in range(l):
            if self.position[i] != None and self.position[i].EXP >= 0:
                num += 1
        for i in range(l):
            if self.position[i] != None and self.position[i].EXP >= 0:
                self.cost += (ct.salary[self.level_of_position[i]] + ct.training_cost[self.level_of_position[i]])*self.o
        print "o:",self.o
        for i in range(l):
            if self.position[i] != None:
                self.position[i].EXP = ct.check(self.position[i].EXP+1)
        return [unhealthy, proformance, num, self.cost]

hrn1 = Human_Capital_Network(3000)
hrn2 = copy.deepcopy(hrn1)
hrn2.o = 6000
hrn3 = copy.deepcopy(hrn1)
hrn3.o = 10000

l = 24
uh = [[0 for i in range(l)] for j in range(3)]
pro = [[0 for i in range(l)] for j in range(3)]
num = [[0 for i in range(l)] for j in range(3)]
cost = [[0 for i in range(l)] for j in range(3)]
for i in range(l):
    [uh[0][i], pro[0][i], num[0][i], cost[0][i]] = hrn1.run(0.18/12)
    [uh[1][i], pro[1][i], num[1][i], cost[1][i]] = hrn2.run(0.18/12)
    [uh[2][i], pro[2][i], num[2][i], cost[2][i]] = hrn3.run(0.18/12)
print num
#draw
plt.cla()
plt.figure(figsize=(8,4))
plt.plot(range(l),pro[0],label="sigma=3000",color="r")
plt.plot(range(l),pro[1],label="sigma=6000",color="b")
plt.plot(range(l),pro[2],label="sigma=10000",color="g")
plt.legend()
#plt.plot(range(l),num,label="number",color="yellow")
#plt.show()
plt.savefig("salary_pro.png")

plt.cla()
plt.figure(figsize=(8,4))
plt.plot(range(l),cost[0],label="sigma=3000",color="r")
plt.plot(range(l),cost[1],label="sigma=6000",color="b")
plt.plot(range(l),cost[2],label="sigma=10000",color="g")
plt.legend()
#plt.plot(range(l),num,label="number",color="yellow")
#plt.show()
plt.savefig("salary_cost.png")

plt.cla()
plt.figure(figsize=(8,4))
plt.plot(range(l),num[0],label="salary=3000",color="r")
plt.plot(range(l),num[1],label="salary=6000",color="b")
plt.plot(range(l),num[2],label="salary=10000",color="g")
plt.legend()
#plt.plot(range(l),num,label="number",color="yellow")
#plt.show()
plt.savefig("salary_num.png")
