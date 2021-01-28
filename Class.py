import random

class Job:
    def __init__(self, type, a_time, cores, exe_time, id, min_resource, max_resource):
        self.type = type
        self.a_time = a_time
        self.cores = cores
        self.exe_time = exe_time
        self.id = id
        self.status = "pending"
        self.min_resource = min_resource
        self.max_resource = max_resource
        self.current_resources = self.cores
        self.remaining_resources = self.current_resources - self.min_resource

    def updateStatus(self, status):
        self.status = status

    def updateCompletion(self,sim_clk):
        if(self.current_resources == self.cores):
            self.c_time = self.exe_time + sim_clk
        elif(self.current_resources < self.cores):
            self.c_time = self.exe_time + sim_clk + 20
        else:
            self.c_time = self.exe_time + sim_clk - 20

    def updateStart(self, sim_clk):
        self.s_time = sim_clk

    def calculateRemaining(self):
        self.remaining_resources = self.current_resources - self.min_resource
        self.extra_resources = self.max_resource - self.remaining_resources

    def get_adaptationCost(self, typ, cost) -> float:
        x = random.uniform(1.005, 1.05)
        if typ == 'e':
            return cost*x
        elif typ == 's':
            return cost/x

    def get_dataRedistributionCost(self, type) -> float:
        if type == 'e':
            x = random.uniform(1.25, 1.75)
            return x
        elif type == 's':
            x = random.uniform(0.5, 0.85)
            return x



    def updateSkrinkage(self, cores, sim_clock, negotiation_overhead):
        time_elasped = sim_clock - negotiation_overhead
        work_done = self.current_resources * time_elasped
        total_work = self.current_resources * self.c_time
        remaining_work = total_work - work_done
        time_required = remaining_work / (self.current_resources - cores)
        adaptation_cost = self.get_adaptationCost('s', time_required)
        print("time required, adaptation cost", time_required, adaptation_cost)
        datadistribution_cost = self.get_dataRedistributionCost('s')
        self.c_time = sim_clock+ adaptation_cost + datadistribution_cost
        self.current_resources = self.current_resources - cores
        return self.c_time




    def updateExpansion(self, cores, sim_clock, negotiation_overhead):
        time_elasped = sim_clock - negotiation_overhead
        work_done = self.current_resources*time_elasped
        total_work = self.current_resources*self.c_time
        remaining_work = total_work - work_done
        time_required = remaining_work/(self.current_resources + cores)
        adaptation_cost = self.get_adaptationCost('e', time_required)
        datadistribution_cost = self.get_dataRedistributionCost('e')
        self.c_time = sim_clock + adaptation_cost + datadistribution_cost
        self.current_resources = self.current_resources + cores
        return self.c_time


class Event:
    def __init__(self, job, time, typ):
        self.typ = typ
        self.job = job
        self.time = time

    def getTime(self):
        return self.time

    def setCore(self, core):
        self.core = core


class System:
    def __init__(self, cores):
        self.cores = cores
        self.total = cores
    def update_cores(self, cores):
        self.cores = cores

class Agreement:
    def __init__(self, type, cores, job):
        self.type = type
        self.modify_cores = cores
        self.job = job