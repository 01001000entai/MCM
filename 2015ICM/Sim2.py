
class CT():
    def __init__(self):
        self.tot = 0
        self.num = 0
        self.PN = [6,30,52,66,71,79,90] #wait
        self.CA = [6,30,52,66,71,79,90]
        self.EXP = [0,0,12,12,24,24,36]
        self.NEW_EXP = [2,1,3,4,5,6,7]
    def new_id(self):
        ret = self.tot
        self.tot += 1
        return ret
    def check(a):
        if (a < 0):
            return 0
        if (a > 100):
            return 100
        return a

ct = CT()
class Worker():
    def __init__(self, lv=0, new=False):
        self.PN = ct.check(random.guass(50,20))
        self.CA = ct.check(random.guass(50,20))
        self.EXP = random.randint(0,10)
        self.name_of_department = ""
        self.id = ct.new_id()
        self.level = lv
        self.sum_leave = 0
        if new == True:
            self.EXP = -ct.NEW_EXP[self.level]
    def cal_proformance(self):
        return 0.25 * self.CA + 0.25 * self.EX + 0.5 * self.PN

class Department():
    def __init__(self, name_of_department, list_of_worker):
        self.name = name_of_department
        self.list_of_worker = list()
        for i in range(7):
            for j in range(list_of_worker[i]):
                self.list_of_worker.append(Worker(i))

class Human_Capital_Network():
    def __init__(self):
        self.department = dict()
        self.position = list()
        self.level_of_position = list()
        self.department_of_position = list()
        self.month = 0

    def add_department(self, name_of_department, list_of_worker):
        self.department.append(Department(name_of_department, list_of_worker))

    def cal_alp(self, k):
        ret = ct.alp[self.level_of_position[k]] * (1-self.position[k].PN/100)
        l = len(self.position)
        s1 = 0
        s2 = self.position[k]
        for i in range(l):
            if self.position[i] != None:
                if self.mat[k][i] == 1:
                    if self.position[i].EXP < 0:
                        s1 += self.position[i].PN
                    else:
                        s2 += self.position[i].PN
        ret += s1/s2



    def update_position(self):
        self.position = list()
        for i in self.department:
            for j in self.department[i]:
                self.position.append(j)
        l = len(self.position)
        for i in range(l):
            self.level_of_position = self.position[i].level
        for i in range(l):
            self.department_of_position = self.position[i].name_of_department

    def get_network(self):
        l = len(self.position)
        self.matrix = [[0 for i in range(l)] for j in range(l)]
        for i in range(l):
            for j in range(l):
                if i < j:
                    if self.position[i].name_of_department \
                        == self.position[j].name_of_department:
                        self.add_edge(i,j)

    def make_leave(self, k):
        self.position[k] = None
        l = len(self.position)
        for i in range(l):
            if self.position[i] != None and self.mat[k][i] == 1:
                self.position[i].sum_leave += self.position[k]

    def invite(self, k):
        if self.level_of_position[k] <= 1:
            self.position[k] = Worker(self.level_of_position[k], new=True)
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
                self.position[k] = Worker(self.leve_of_position[k], new=True)

    def run(self, rate_of_leave):
        l = len(self.position)
        proformance = 0
        unhealthy = 0
        tmp = [0 for i in range(l)]
        s = sum([1/self.position[i].PN for i in range(l)])
        for i in range(l):
            tmp[i] = (1/self.position) / s * rate_of_leave
        for i in range(l):
            if random.random(0,1) < tmp[i]:
                self.make_leave(i)
        for i in range(l):
            if self.position[i] == None:
                self.invite(i)
        for i in range(l):
            if self.position[i] != None and self.position[i].EXP >= 0:
                self.proformance_of_department[self.position[i].name_of_department] += (self.position[i].CA + self.position[i].EXP)/2 + self.position[i].NP * (self.position[i].level/7) #####wait
        ##cal team proformance
        for i in range(self.proformance_of_department):
            proformance_of_company += self.proformance_of_department[i]
        for i in range(l):
            if self.position[i].CA < ct.CA[self.level_of_position[i]]:
                unhealthy += ct.CA[self.level_of_position[i]] - self.position[i].CA
            if self.position[i].PN < ct.PN[self.level_of_position[i]]:
                unhealthy += ct.PN[self.level_of_position[i]] - self.position[i].PN
        ##cal company proformance
        return [unhealthy, proformance_of_company]
