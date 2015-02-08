im
import random
import math
//productive_capacity
//
"""
CEO(1,2,0,0,0,0,1)

"""
class CONST():
    def __init__(self):
        self.tot_of_work = 0
    def get_tot():
        ret = self.tot_of_work
        self.tot_of_work += 1
        return ret
Const = CONST()

class Worker():
    def __init__(self, lv=None,name_of_department=""):
        if (lv == None):
            self.administrative_ability = random.randint(0,100)
            self.professional_competence = random.randint(0,100)
        else:
            self.administrative_ability = rank_of_administrative_ability[lv] + random.randint(0,5)
            self.professional_competence = rank_of_professional_competence[lv] + random.randint(0,5)
            self.lv = lv
        self.name_of_department = name_of_department
        self.work_experience = 0
        self.loyalty = 0.0
        self.id = Const.get_tot()
    def get_level(self):
        return self.lv
    def set_level(self,lv):
        self.lv = lv
    def set_position(self, pos):
        self.position = pos
        self.level = level[pos]
    def check_loyalty(self):
        if self.loyalty < 0:
            self.loyalty = 0
        if self.loyalty > 100
            self.loyalty = 100
    def award_bonuses(self):
        self.loyalty *= 1.1
        self.check_loyalty()
    def promotion(self):
        self.loyalty *= 1.2
        self.check_loyalty()
    def resign_effect(self):
        self.loyalty *= 0.9
        self.check_loyalty()
    def get_id(self):
        return self.id
    def get_name_of_department(self):
        return self.name_of_department

#End_Worker

class Department(self, name_of_department, list_of_department, superior_department):
    def __init__(self):
        self.name_of_department = name_of_department
        self.list_of_worker = list()
        for i in range(len(list_of_worker)):
            for j in range(list_of_worker[i]):
                self.list_of_worker.append(Worker(lv=i))
        self.number_of_worker = len(self.list_of_worker)
        self.superior_department = superior_department
    def get_name(self):
        return self.name_of_department
    def get_superior_department(self):
        return self.superior_department
    def get_number_of_worker(self):
        return self.number_of_worker
    def get_ith_worker(self, i):
        return self.list_of_worker[i]
    def get_boss_of_department(self):
        return self.list_of_worker[self.number_of_department-1]
#End_Department


class Human_Capital_Network():
    def __init__(self, number_of_people, hierarchy):
        self.number_of_people = number_of_people
        self.hierarchy ＝ hierarchy
        self.number_of_department = number_of_department
        self.position ＝ list()
        self.department = list()
    def add_department(self, name_of_department, dpm):
        self.department.append(Department(name_of_department, dpm))
    def update_position(self):
        self.position = list()
        for i in self.department:
            for j in self.department[i]:
                self.position.append(j)
        l = len(self.position)
        for i in range(l):
            self.level_of_position = self.position[i].get_level()
        for i in range(l):
            self.department_of_position = slef.position[i].get_name_of_department()
    def get_network(self):
        l = len(self.position)
        self.matrix = [[0 for i in range(l)] for j in range(l)]
        for i in range(l):
            for j in range(l):
                if i < j:
                    if self.position[i].get_name_of_department() \
                        == self.position[j].get_name_of_department():
                        self.add_edge(i,j)
                    if self.department[self.position[i].get_name_of_department()].get_boss_of_department().get_id() \
                        == self.position[j].get_id():
                        self.add_edge(i,j)
                    if self.department[self.position[j],get_name_of_department()].get_boss_of_department().get_id() \
                        == self.postion[i].get_id():
                        self.add_edge(i,j)


    def KM(self):

    def run(self, rate_of_leave):
        l = len(self.position)
        leave = [self.func_loyalty(self.position[i].loyalty) for i in range(l)]
        s = sum(leave)
        for i in range(l):
            leave[i] = leave[i] * rate_of_leave
        for i in range(l):
            if random.random < leave[i]:
                self.leave(i)
        for i in range(l):
            if self.is_empty_position(i):
                self.take_up_the_job(i)
        """
        计算绩效与生产力
        """
    def leave(self, k):
        l = len(self.position)
        for i in range(l):
            if self.matrix[i][k]:
                self.position[i].resign_effect()

    def take_up_the_job(self, k):
        max_of_pf = 0
        p = -1
        for i in range(l):
            if self.position[i] != None and self.cal_performence(self.position[i],self.level_of_position[k]) > max_of_pf
                max_of_pf = self.cal_performence(self.position[i],self.level_of_position[k])
                p = i
        if p != -1:
            self.position[k] = self.position[p]
            self.position[p] = None
        else:
            self.position[k] = Worker(self.level_of_position[k], self.department_of_position[k])
            self.position[k].set_exp(-Const.exp_requier[self.leve_of_position])
