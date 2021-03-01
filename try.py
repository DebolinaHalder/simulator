def updateSkrinkage(self, cores, sim_clock, negotiation_overhead):
    time_elasped = sim_clock - negotiation_overhead - self.phase_list[-1].time
    if (time_elasped < 0):
        if self.phase_list[-1].type == expansion_event:
            cores = abs((self.phase_list[-1].cores - self.current_resources) - cores)
        cores = (self.current_resources - self.phase_list[-1].cores) + cores
        self.phase_list.pop()
        time_elasped = sim_clock - negotiation_overhead - self.phase_list[-1].time
    work_done = self.current_resources * time_elasped
    total_work = self.current_resources * self.phase_list[-1].rem_time
    remaining_work = total_work - work_done
    adaptation_cost = self.get_adaptationCost('s', remaining_work)
    print(time_elasped, work_done, total_work)
    # print("remaining work", remaining_work, "adaptation cost", adaptation_cost)
    time_required = adaptation_cost / (self.current_resources - cores)
    datadistribution_cost = self.get_dataRedistributionCost(cores)
    synchronization_cost = random.uniform(min_synchronization_cost, max_synchronization_cost)
    self.c_time = sim_clock + time_required + datadistribution_cost + synchronization_cost
    self.current_resources = self.current_resources - cores
    p = Phase(shrinkage_event, self.current_resources - cores, sim_clock)
    p.set_remaining(self.c_time - sim_clock)
    print("remaining time", p.rem_time)
    if (p.rem_time < 0):
        print("look here")
    self.phase_list.append(p)
    # print("completion time", self.c_time)
    return self.c_time


def updateExpansion(self, cores, sim_clock, negotiation_overhead):
    time_elasped = sim_clock - negotiation_overhead - self.phase_list[-1].time
    work_done = self.current_resources * time_elasped
    total_work = self.current_resources * self.phase_list[-1].rem_time
    remaining_work = total_work - work_done
    adaptation_cost = self.get_adaptationCost('e', remaining_work)
    print(time_elasped, work_done, total_work)
    time_required = adaptation_cost / (self.current_resources + cores)
    datadistribution_cost = self.get_dataRedistributionCost(cores)
    synchronization_cost = random.uniform(min_synchronization_cost, max_synchronization_cost)
    self.c_time = sim_clock + time_required + datadistribution_cost + synchronization_cost
    self.current_resources = self.current_resources + cores
    return self.c_time