import random

max_adaptation_cost = 1.15
min_adaptation_cost = 1.05
max_alpha = 0.1
min_alpha = 0.05
max_beta = 10.0
min_beta = 8.0
submission_event = 0
expansion_event = 1
shrinkage_event = 2
completion_event = 3



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
        self.no_of_expansion = 0
        self.no_of_shrinkage = 0
        self.phase_list = []
        self.phase_req = []
        self.requested_expansion = 0
        self.requested_shrinkage = 0


    def updateStatus(self, status):
        self.status = status


    def updateCompletion(self,sim_clk):
        if self.current_resources == self.cores:
            self.c_time = self.exe_time + sim_clk
        elif self.current_resources < self.cores:
            self.c_time = self.exe_time + sim_clk + 20
        else:
            self.c_time = self.exe_time + sim_clk - 20

    def updateStart(self, sim_clk):
        self.s_time = sim_clk

    def calculateRemaining(self):
        self.remaining_resources = self.current_resources - self.min_resource
        self.extra_resources = self.max_resource - self.remaining_resources

    def get_adaptationCost(self, typ, cost) -> float:
        x = random.uniform(min_adaptation_cost, max_adaptation_cost)
        if typ == 'e':
            return cost*x
        elif typ == 's':
            return cost/x

    def get_dataRedistributionCost(self, cores) -> float:
        alpha = random.uniform(min_alpha, max_alpha)
        beta = random.uniform(min_beta, max_beta)
        difference = abs(self.current_resources - cores)
        total = self.current_resources + cores
        x = alpha*difference + beta/total
        return x




    def updateSkrinkage(self, cores, sim_clock, negotiation_overhead):
        time_elasped = sim_clock - negotiation_overhead - self.phase_list[-1].time
        work_done = self.current_resources * time_elasped
        total_work = self.current_resources*self.phase_list[-1].rem_time
        remaining_work = total_work - work_done
        adaptation_cost = self.get_adaptationCost('s', remaining_work)
        #print("remaining work", remaining_work, "adaptation cost", adaptation_cost)
        time_required = adaptation_cost / (self.current_resources - cores)
        datadistribution_cost = self.get_dataRedistributionCost(cores)
        self.c_time = sim_clock + time_required + datadistribution_cost
        self.current_resources = self.current_resources - cores
        #print("completion time", self.c_time)
        return self.c_time




    def updateExpansion(self, cores, sim_clock, negotiation_overhead):
        time_elasped = sim_clock - negotiation_overhead - self.phase_list[-1].time
        work_done = self.current_resources*time_elasped
        total_work = self.current_resources*self.phase_list[-1].rem_time
        remaining_work = total_work - work_done
        adaptation_cost = self.get_adaptationCost('e', remaining_work)
        time_required = adaptation_cost / (self.current_resources + cores)
        datadistribution_cost = self.get_dataRedistributionCost(cores)
        self.c_time = sim_clock + time_required + datadistribution_cost
        self.current_resources = self.current_resources + cores
        return self.c_time


class Event:
    def __init__(self, job, time, typ):
        self.typ = typ
        self.job = job
        self.time = time
        self.core = 0

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


class Phase:
    def __init__(self, type, cores, time):
        self.type = type
        self.cores = cores
        self.time = time
        self.rem_time = 0

    def set_remaining(self, remaining_time):
        self.rem_time = remaining_time


class Phase_req:
    def __init__(self, type, cores, time):
        self.type = type
        self.cores = cores
        self.time = time
        self. rem_time = 0
