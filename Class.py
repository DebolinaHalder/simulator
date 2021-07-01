import random

max_adaptation_cost = 0.001
min_adaptation_cost = 0.0005
max_synchronization_cost = 0.05
min_synchronization_cost = 0.015
max_alpha = 0.05
min_alpha = 0.005
max_beta = 0.05
min_beta = 0.005
submission_event = 0
expansion_event = 1
shrinkage_event = 2
completion_event = 3

random.seed(123)



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
        self.current_resources = cores
        self.remaining_time = exe_time
        self.remaining_resources = self.current_resources - self.min_resource
        self.no_of_expansion = 0
        self.no_of_shrinkage = 0
        self.phase_list = []
        self.phase_req = []
        self.overheads = []
        self.requested_expansion = 0
        self.requested_shrinkage = 0
        self.priority = 0
        self.gain = 0
        self.adaptation = random.uniform(min_adaptation_cost, max_adaptation_cost)
        self.alpha = random.uniform(max_alpha, min_alpha)
        self.beta = random.uniform(max_beta, min_beta)
        self.synchronization = random.uniform(max_synchronization_cost, min_synchronization_cost)


    def updateStatus(self, status):
        self.status = status


    def updateCompletion(self,sim_clk):
        if self.current_resources == self.cores:
            self.c_time = self.exe_time + sim_clk
        elif self.current_resources < self.cores:
            if(self.current_resources == 0):
                print("divide by zero here", self.id)
            perc = self.adaptation
            overhead = self.exe_time * perc
            cost = self.exe_time - overhead
            overhead = overhead * self.current_resources / self.cores
            work_remaining = cost * self.cores
            remaining_cost = work_remaining/self.current_resources + overhead

            self.c_time = sim_clk + remaining_cost
            self.gain = self.current_resources - self.cores
            print(self.id, sim_clk, overhead)
        else:
            perc = random.uniform(min_adaptation_cost, max_adaptation_cost)
            overhead = self.exe_time * perc
            cost = self.exe_time - overhead
            overhead = overhead * self.current_resources / self.cores
            work_remaining = cost * self.cores
            remaining_cost = work_remaining / self.current_resources + overhead
            self.c_time = sim_clk + remaining_cost
            self.gain = self.cores - self.current_resources
            print(self.id, sim_clk, overhead)

    def updateStart(self, sim_clk):
        self.s_time = sim_clk

    def calculateRemaining(self):
        self.remaining_resources = self.current_resources - self.min_resource
        self.extra_resources = self.max_resource - self.remaining_resources

    def get_adaptationCost(self, typ, cost, cores):
        perc = random.uniform(min_adaptation_cost, max_adaptation_cost)
        overhead = cost * perc
        comp = cost - overhead
        print("computation", comp)
        work_remaining = comp * self.current_resources
        print(self.current_resources)
        if typ == 'e':
            overhead = (overhead/self.current_resources) * (self.current_resources + cores)
            new_time = work_remaining / (self.current_resources + cores)
        elif typ == 's':
            overhead = (overhead / self.current_resources) * (self.current_resources - cores)
            new_time = work_remaining / (self.current_resources - cores)
        return new_time,  overhead


    def get_dataRedistributionCost(self, cores) -> float:
        alpha = random.uniform(min_alpha, max_alpha)
        beta = random.uniform(min_beta, max_beta)
        difference = abs(self.current_resources - cores)
        total = self.current_resources + cores
        x = alpha*difference + beta/total
        return x




    def updateSkrinkage(self, cores, sim_clock, negotiation_overhead):
        time_rem = self.c_time - sim_clock - negotiation_overhead
        print("rem_time", time_rem)
        time, overhead = self.get_adaptationCost('s', time_rem, cores)
        time_required = time + overhead
        datadistribution_cost = self.get_dataRedistributionCost(cores)
        synchronization_cost = random.uniform(min_synchronization_cost, max_synchronization_cost)
        self.c_time = sim_clock + time_required + datadistribution_cost + synchronization_cost
        self.current_resources = self.current_resources - cores
        print("completion time", self.c_time)
        print(self.id, sim_clock, overhead+datadistribution_cost+synchronization_cost)
        self.gain = self.gain - cores
        return self.c_time




    def updateExpansion(self, cores, sim_clock, negotiation_overhead):
        time_rem = self.c_time - sim_clock - negotiation_overhead
        time, overhead = self.get_adaptationCost('e', time_rem, cores)
        time_required = time + overhead
        datadistribution_cost = self.get_dataRedistributionCost(cores)
        synchronization_cost = random.uniform(min_synchronization_cost, max_synchronization_cost)
        self.c_time = sim_clock + time_required + datadistribution_cost + synchronization_cost
        self.current_resources = self.current_resources + cores
        print(self.id, sim_clock, overhead, datadistribution_cost, synchronization_cost)
        self.gain = self.gain + cores
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
        self.adaptation_cost = 0

    def set_remaining(self, remaining_time):
        self.rem_time = remaining_time

    def get_adaptation_cost(self, cost):
        self.adaptation_cost = cost

class Phase_req:
    def __init__(self, type, cores, time):
        self.type = type
        self.cores = cores
        self.time = time
        self. rem_time = 0

class Overhead:
    def __init__(self, cost, time):
        self.cost = cost
        self.time = time