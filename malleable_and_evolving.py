# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
from Class import Job, Event, System, Agreement, Phase
from typing import Dict
import operator
import random
import numpy as np


max_no_of_phase = 4
min_no_of_phase = 1
max_time = 80
min_time = 10
max_cores = 5
min_cores = 2
exp_probability = 0.7

submission_event = 0
expansion_event = 1
shrinkage_event = 2
completion_event = 3



rigid = 1
malleable = 2
evolving = 3

np.random.seed(12)

def jobEntry(job_to_start_list, job, event, state, event_counter, event_list, sim_clock):
    print("job added in job to start list", job.id, "at time", sim_clock)
    job_to_start_list[job.id] = job
    state.update_cores(state.cores - job.current_resources)
    job.updateCompletion(sim_clock)
    job.updateStart(sim_clock)
    event_list.remove(event)
    return state, event_counter, event_list


def find_malleable(running_job_list):
    running_malleable_job = []
    for key, value in running_job_list.items():
        if value.type == 2:
            value.calculateRemaining()
            running_malleable_job.append(value)
    running_malleable_job = sorted(running_malleable_job, key=operator.attrgetter('no_of_expansion'))
    return running_malleable_job


def create_phases(job):
    no_of_phase = random.randint(min_no_of_phase, max_no_of_phase)
    phase = []
    for i in range(no_of_phase):
        s = np.random.binomial(1, exp_probability)
        time = random.randint(min_time, max_time)
        cores = random.randint(job.min_resource, job.max_resource)
        if s == 1:
            p = Phase(expansion_event, cores, time)
        else:
            p = Phase(shrinkage_event, cores, time)
        phase.append(p)
    return phase


def create_phases_static():
    no_of_phase = 2
    phase = []
    p = Phase(shrinkage_event, 2, 35)
    phase.append(p)
    q = Phase(expansion_event, 4, 10)
    phase.append(q)
    return phase

def getNegotiationCost():
    min = 0.05
    max = 0.8
    k = random.uniform(min,max)
    return k


def create_initial_schedule(event, state, job_to_start_list, sim_clock, event_counter, event_list, queued_job_list,
                            pending_job_list, running_job_list):
    job = event.job
    if job.current_resources <= state.cores:
        print("job allocation", job.id)
        state, event_counter, event_list = jobEntry(job_to_start_list, job, event, state, event_counter, event_list,
                                                    sim_clock)
        for key in job_to_start_list:
            if key in queued_job_list:
                queued_job_list.pop(key)
    else:
        if job.type == 2:
            if job.min_resource <= state.cores:
                job.current_resources = job.min_resource
                print("job allocation", job.id)
                state, event_counter, event_list = jobEntry(job_to_start_list, job, event, state, event_counter,
                                                            event_list,
                                                            sim_clock)
                for key in job_to_start_list:
                    if key in queued_job_list:
                        queued_job_list.pop(key)
            else:
                queued_job_list[job.id] = job
                print("job queued", job.id, event.typ)
                event_counter = event_counter + 1

        else:
            queued_job_list[job.id] = job
            print("job queued", job.id, event.typ, sim_clock)
            event_counter = event_counter + 1
    if len(event_list) == 0:
        agreement_list = []
        negotiation_overhead = 0
        event_list = dispatcher(job_to_start_list, pending_job_list, running_job_list, event_list, agreement_list,
                                queued_job_list, sim_clock, negotiation_overhead)
        event_counter = 0
    return state, event_counter, event_list


def find_agreement_evolving(running_malleable_job, sim_clock, event, state):
    negotiation_overhead = 0
    agreement_list = []
    agreement_to_be = []
    needed = event.core - state.cores
    for i in running_malleable_job:
        if needed == 0:
            break
        if i.remaining_resources != 0:
            if i.remaining_resources >= needed:
                cores = needed
            else:
                cores = i.remaining_resources
            a = Agreement('s', cores, i)
            agreement_to_be.append(a)
            needed = needed - cores

    if needed == 0:
        for i in agreement_to_be:
            agreement_list.append(i)
            negotiation_overhead = negotiation_overhead + getNegotiationCost()
            index = running_malleable_job.index(i.job)
            running_malleable_job[index].remaining_resources = running_malleable_job[
                                                                   index].remaining_resources - i.modify_cores
        a = Agreement('e', needed, event.job)
        state.cores = 0
    else:
        agreement_to_be.clear()
    running_malleable_job = sorted(running_malleable_job, key=operator.attrgetter('remaining_resources'))
    return sim_clock, negotiation_overhead, agreement_list, state



def find_agreement(queued_job_list, running_malleable_job, job_to_start_list, state, event_list, sim_clock):
    agreement_list = []
    agreement_to_be = []
    negotiation_overhead = 0
    for key, value in queued_job_list.items():
        if value.current_resources > state.cores:
            needed = value.current_resources - state.cores
        else:
            needed = 0
        for i in running_malleable_job:
            if needed == 0:
                break
            if i.remaining_resources != 0:
                if i.remaining_resources >= needed:
                    cores = needed
                else:
                    cores = i.remaining_resources
                a = Agreement('s', cores, i)
                agreement_to_be.append(a)
                needed = needed - cores
        if needed == 0:
            for i in agreement_to_be:
                agreement_list.append(i)
                negotiation_overhead = negotiation_overhead + getNegotiationCost()
                index = running_malleable_job.index(i.job)
                running_malleable_job[index].remaining_resources = running_malleable_job[
                                                                       index].remaining_resources - i.modify_cores
                state.cores = state.cores + i.modify_cores
            sim_clock = sim_clock + negotiation_overhead
            e = find_event(event_list, value)
            event_counter = 0
            state, event_counter, event_list = jobEntry(job_to_start_list, value, e, state, event_counter, event_list,
                                                        sim_clock)
            agreement_to_be.clear()
        else:
            agreement_to_be.clear()
        running_malleable_job = sorted(running_malleable_job, key=operator.attrgetter('remaining_resources'))
    for key in job_to_start_list:
        if key in queued_job_list:
            queued_job_list.pop(key)
    running_malleable_job = sorted(running_malleable_job, key=operator.attrgetter('no_of_shrinkage'))
    if state.cores != 0:
        for i in running_malleable_job:
            if i.extra_resources != 0:
                cores = i.extra_resources if i.extra_resources < state.cores else state.cores
                a = Agreement('e', cores, i)
                agreement_list.append(a)
                index = running_malleable_job.index(i)
                running_malleable_job[index].extra_resources = running_malleable_job[
                                                                   index].remaining_resources - a.modify_cores
                state.cores = state.cores - a.modify_cores
                if state.cores == 0:
                    break
    return agreement_list, job_to_start_list, sim_clock, negotiation_overhead, state


def scheduler(job_to_start_list, pending_job_list, running_job_list, event_list, queued_job_list, state, sim_clock):
    idle_processes = state.total - state.cores
    agreement_list = []
    negotiation_overhead = 0
    if idle_processes:
        running_malleable_job = []
        running_malleable_job = find_malleable(running_job_list)
        if len(running_malleable_job) != 0:
            agreement_list, job_to_start_list, sim_clock, negotiation_overhead, state = find_agreement(queued_job_list,
                                                                                                running_malleable_job,
                                                                                                job_to_start_list,
                                                                                                state, event_list,
                                                                                                sim_clock)

    event_list = dispatcher(job_to_start_list, pending_job_list, running_job_list, event_list, agreement_list,
                            queued_job_list, sim_clock, negotiation_overhead)
    return event_list, sim_clock, state


def find_event(event_list, job):
    for i in event_list:
        if i.job == job:
            return i


def expansion(cores, sim_clk, running_job_list, negotiation_overhead, job, event_list):
    id = job.id
    p = Phase(expansion_event, cores, sim_clk)
    running_job_list[id].phase_list.append(p)
    running_job_list[id].no_of_expansion = running_job_list[id].no_of_expansion + 1
    time = running_job_list[id].updateExpansion(cores, sim_clk, negotiation_overhead)
    event = find_event(event_list, job)
    index = event_list.index(event)
    event_list[index].job.c_time = time
    event_list[index].job.phase_list.append(p)
    event_list[index].job.no_of_expansion = running_job_list[id].no_of_expansion
    event_list[index].time = event_list[index].job.c_time
    print("job expansion", job.id,"with cores", cores, "at time", sim_clk)
    print("new completion time", time)
    return event_list


def shrinkage(cores, sim_clk, running_job_list, negotiation_overhead, job, event_list):
    id = job.id
    p = Phase(shrinkage_event, cores, sim_clk)
    running_job_list[id].phase_list.append(p)
    running_job_list[id].no_of_shrinkage = running_job_list[id].no_of_shrinkage + 1
    time = running_job_list[id].updateSkrinkage(cores, sim_clk, negotiation_overhead)
    event = find_event(event_list, job)
    index = event_list.index(event)
    event_list[index].job.c_time = time
    event_list[index].job.phase_list.append(p)
    event_list[index].job.no_of_expansion = running_job_list[id].no_of_expansion
    event_list[index].time = event_list[index].job.c_time
    print("job skrinked", job.id, "with cores", cores, "at time", sim_clk)
    print("new completion time", time)
    return event_list


def dispatcher(job_to_start_list, pending_job_list, running_job_list, event_list, agreement_list, queued_job_list,
               sim_clock, negotiation_overhead):
    for i in agreement_list:
        id = i.job.id
        if i.type == 'e':
            event_list = expansion(i.modify_cores, sim_clock, running_job_list, negotiation_overhead, i.job, event_list)

        elif i.type == 's':
            event_list = shrinkage(i.modify_cores, sim_clock, running_job_list, negotiation_overhead, i.job, event_list)

    for key, value in job_to_start_list.items():
        value.updateStatus("running")
        running_job_list[value.id] = value
        e = Event(value, value.c_time, 3)
        event_list.append(e)
        if value.type == evolving:
            event_list = create_evolving_events(event_list, value, sim_clock)
        print("completion event created with id & time", e.job.id, e.time)
        pending_job_list.pop(value.id)
        if value.id in queued_job_list:
            queued_job_list.pop(value.id)
    event_list = sorted(event_list, key=operator.attrgetter('time'))
    job_to_start_list.clear()
    return event_list


def runningToComplete(running_job_list, complete_job_list, event):
    Job = event.job
    Job.updateStatus("completed")
    running_job_list.pop(Job.id)
    complete_job_list[Job.id] = Job
    return running_job_list, complete_job_list


def create_evolving_events(event_list, J, sim_clk):
    phase_rq = J.phase_req
    if len(phase_rq) != 0:
        phase = phase_rq[0]
        phase_rq.remove(phase)
        perc, type, cores = phase.time, phase.type, phase.cores
        rem_time = J.c_time - sim_clk
        time = rem_time * perc / 100
        time = sim_clk + time
        #if phase.type == shrinkage_event:
        #   cores = random.randint(1, J.current_resources - 1)
        e = Event(J, time, type)
        e.setCore(cores)
        event_list.append(e)
        event_list = sorted(event_list, key=operator.attrgetter('time'))
        if phase.type == expansion_event:
            print("expansion event created for", J.id, "at time", time)
        elif phase.type == shrinkage_event:
            print("shrinkage event created for", J.id, "at time", time)
    return event_list


def initialize_event(fileName, pending_job_list, event_list):
    data = pd.read_csv(fileName)
    for index, row in data.iterrows():
        J = Job(row['type'], row['S_time'], row['Processors'], row['R_time'], row['id'], row['Min_resource'],
                row['Max_resource'])
        if J.type == evolving:
            phase_rq = create_phases_static()
            J.phase_req = phase_rq
        pending_job_list[J.id] = J
        e = Event(J, row['S_time'], 0)
        event_list.append(e)
    event_list = sorted(event_list, key=operator.attrgetter('time'))
    return pending_job_list, event_list


def initialize_system(cores):
    state = System(cores)
    return state


def clear_list(event_list, job):
    for i in event_list:
        if i.job == job:
            event_list.remove(i)
    return event_list


def main():
    pending_job_list: Dict[int, Job] = {}
    event_list = []
    running_job_list: Dict[int, Job] = {}
    complete_job_list: Dict[int, Job] = {}
    queued_job_list: Dict[int, Job] = {}
    job_to_start_list: Dict[int, Job] = {}
    pending_job_list, event_list = initialize_event("workload_mal_evol.csv", pending_job_list, event_list)
    state = initialize_system(600)

    sim_clock = 0
    event_counter = 0
    event: Event

    while len(event_list) != 0:
        try:
            event = event_list[event_counter]
        except IndexError:
            if len(job_to_start_list) != 0:
                event_list, sim_clock, state = scheduler(job_to_start_list, pending_job_list, running_job_list,
                                                         event_list,
                                                         queued_job_list, state, sim_clock)
                event_counter = 0
            else:
                print("check what is wrong")
        print("current time", sim_clock, "time", event.time, "job", event.job.id)
        if event.typ == expansion_event or event.typ == shrinkage_event:
            if len(job_to_start_list) != 0:
                event_list, sim_clock, state = scheduler(job_to_start_list, pending_job_list, running_job_list, event_list,
                                            queued_job_list, state, sim_clock)
                event_counter = 0
            sim_clock = event.time
            cores = event.core
            job = event.job
            event_list.remove(event)
            if event.typ == shrinkage_event:
                shrinkage(cores, sim_clock, running_job_list, 0, job, event_list)
                state.cores = state.cores + event.core

            elif event.typ == expansion_event:
                if event.core <= state.cores:
                    expansion(cores, sim_clock, running_job_list, 0, job, event_list)
                    state.cores = state.cores - event.core
                else:
                    running_malleable_job = find_malleable(running_job_list)
                    sim_clock, negotiation_overhead, agreement_list, state = find_agreement_evolving(running_malleable_job, sim_clock, event, state)
                    event_list = dispatcher(job_to_start_list, pending_job_list, running_job_list, event_list,
                                            agreement_list, queued_job_list, sim_clock, negotiation_overhead)
            else:
                print("couldn't expand job", job.id, "at time", sim_clock)
            event_list = create_evolving_events(event_list, running_job_list[event.job.id], sim_clock)
            event_counter = 0

        elif event.typ == completion_event:
            if len(job_to_start_list) != 0:
                event_list, sim_clock, state = scheduler(job_to_start_list, pending_job_list, running_job_list,
                                                         event_list,
                                                         queued_job_list, state, sim_clock)
                event_list = sorted(event_list, key=operator.attrgetter('time'))
                event_counter = 0
            else:
                sim_clock = event.time
                running_job_list, complete_job_list = runningToComplete(running_job_list, complete_job_list, event)
                state.cores = state.cores + event.job.cores
                event_list.remove(event)
                event_list = clear_list(event_list, event.job)
                event_list = sorted(event_list, key=operator.attrgetter('time'))
                print("event finished", event.job.id, "at time", sim_clock)
                event_counter = 0
                if len(event_list) == 0 and len(job_to_start_list) != 0:
                    agreement_list = []
                    event_list = dispatcher(job_to_start_list, pending_job_list, running_job_list, event_list,
                                            agreement_list, queued_job_list, sim_clock, 0)
        else:
            if sim_clock >= event.time:
                state, event_counter, event_list = create_initial_schedule(event, state, job_to_start_list, sim_clock,
                                                                           event_counter, event_list, queued_job_list,
                                                                           pending_job_list, running_job_list)
            elif sim_clock < event.time:
                event_list, sim_clock, state = scheduler(job_to_start_list, pending_job_list, running_job_list, event_list,
                                                  queued_job_list, state, sim_clock)
                sim_clock = event.time
                event_counter = 0
    result_df = df = pd.DataFrame(columns = ['id', 'Arrival', 'Start','Completion','No_of_expansion', 'No_of_shrinkage'])
    for key, value in complete_job_list.items():
        result_df.append({'id':value.id, 'Arrival': value.a_time, 'Start': value.s_time, 'Completion': value.c_time, 'No_of_expansion': value.no_of_expansion, 'No_of_shrinkage': value.no_of_shrinkage}, ignore_index = True)
        result_df.to_csv('result_mal_evol.csv', index=False)


if __name__ == '__main__':
    main()
