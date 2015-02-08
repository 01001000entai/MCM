
class CT():
    def __init__(self):
        self.tot = 0
        self.num = 0
    def new_id(self):
        ret = self.tot
        self.tot += 1
        return ret
ct = CT()
class Worker():
    def __init__(self, lv=0):
        self.PN = random.guass(50,20)
        self.CA = random.guass(50,20)
        self.EXP = random.randint(0,10)
        self.name_of_department = ""
        self.id = ct.new_id
        self.level = lv

class Department():
    def __init__(self, name_of_department, list_of_worker):
        self.name = name_of_department
        self.list_of_worker = list()
        for i in range(7):
            for j in range(list_of_worker[i]):
                self.list_of_worker.append(Worker())

class Human_Capital_Network():
    def __init__(self):
        self.department = dict()
        self.position = list()
        self.level_of_position = list()
        self.department_of_position = list()

    def add_department(self, name_of_department, list_of_worker):
        self.department.append(Department(name_of_department, list_of_worker))

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

    def run(self, rate_of_leave):
        l = len(self.position)
        tmp = [0 for i in range(l)]
        s = sum([self.position[i].PN for i in range(l)])
        for i in range(l):
            tmp[i] =
