# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
from Class import Job, Event, System, Agreement
import queue as q
from typing import Dict
import operator
import random


def jobEntry(job_to_start_list, job, event, state, event_counter, event_list, sim_clock):
    print("job added in job to start list", job.id)
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
    running_malleable_job = sorted(running_malleable_job, key=operator.attrgetter('remaining_resources'))
    return running_malleable_job


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
    else:
        if job.type == 2:
            if job.min_resource <= state.cores:
                job.current_resources = job.min_resource
                print("job allocation", job.id)
                state, event_counter, event_list = jobEntry(job_to_start_list, job, event, state, event_counter,
                                                            event_list,
                                                            sim_clock)
            else:
                queued_job_list[job.id] = job
                print("job queued", job.id)
                event_counter = event_counter + 1

        else:
            queued_job_list[job.id] = job
            print("job queued", job.id)
            event_counter = event_counter + 1
    if len(event_list) == 0:
        agreement_list = []
        negotiation_overhead = 0
        event_list = dispatcher(job_to_start_list, pending_job_list, running_job_list, event_list, agreement_list,
                                queued_job_list, sim_clock, negotiation_overhead)
        event_counter = 0
    return state, event_counter, event_list


def find_agreement(queued_job_list, running_malleable_job, job_to_start_list, state, event_list, sim_clock):
    agreement_list = []
    agreement_to_be = []
    negotiation_overhead = 0
    for key, value in queued_job_list.items():
        needed = value.current_resources - state.cores
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
            e = find_event(event_list, value)
            event_counter = 0
            state, event_counter, event_list = jobEntry(job_to_start_list, value, e, state, event_counter, event_list,
                                                        sim_clock)
        else:
            agreement_to_be.clear()
        running_malleable_job = sorted(running_malleable_job, key=operator.attrgetter('remaining_resources'))
    sim_clock = sim_clock + negotiation_overhead
    if len(agreement_list) == 0:
        if state.cores != 0:
            for i in running_malleable_job:
                print("here", i.id)
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
    return agreement_list, job_to_start_list, sim_clock, negotiation_overhead


def scheduler(job_to_start_list, pending_job_list, running_job_list, event_list, queued_job_list, state, sim_clock):
    idle_processes = state.total - state.cores
    agreement_list = []
    negotiation_overhead = 0
    if idle_processes:
        running_malleable_job = []
        running_malleable_job = find_malleable(running_job_list)
        if len(running_malleable_job) != 0:
            agreement_list, job_to_start_list, sim_clock, negotiation_overhead = find_agreement(queued_job_list,
                                                                                                running_malleable_job,
                                                                                                job_to_start_list,
                                                                                                state, event_list,
                                                                                                sim_clock)

    event_list = dispatcher(job_to_start_list, pending_job_list, running_job_list, event_list, agreement_list,
                            queued_job_list, sim_clock, negotiation_overhead)
    return event_list, sim_clock


def find_event(event_list, job):
    for i in event_list:
        if i.job == job:
            return i


def dispatcher(job_to_start_list, pending_job_list, running_job_list, event_list, agreement_list, queued_job_list,
               sim_clock, negotiation_overhead):
    for i in agreement_list:
        id = i.job.id
        if i.type == 'e':
            time = running_job_list[id].updateExpansion(i.modify_cores, sim_clock, negotiation_overhead)
            event = find_event(event_list, i.job)
            index = event_list.index(event)
            event_list[index].job.c_time = time
            event_list[index].time = event_list[index].job.c_time
            print("job expansion", i.job.id)

        elif i.type == 's':
            time = running_job_list[id].updateSkrinkage(i.modify_cores, sim_clock, negotiation_overhead)
            event = find_event(event_list, i.job)
            index = event_list.index(event)
            event_list[index].job.c_time = time
            event_list[index].time = event_list[index].job.c_time
            print("job skrinked", i.job.id)

    for key, value in job_to_start_list.items():
        value.updateStatus("running")
        running_job_list[value.id] = value
        e = Event(value, value.c_time, 3)
        event_list.append(e)
        print("completion event created with id & time", e.job.id, e.job.c_time)
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


# Press the green button in the gutter to run the script.
def main():
    pending_job_list: Dict[int, Job] = {}
    event_list = []
    running_job_list: Dict[int, Job] = {}
    complete_job_list: Dict[int, Job] = {}
    queued_job_list: Dict[int, Job] = {}
    job_to_start_list: Dict[int, Job] = {}
    data = pd.read_csv("workload.csv")
    for index, row in data.iterrows():
        J = Job(row['type'], row['a_time'], row['cores'], row['exe_time'], row['id'], row['min_resource'],
                row['max_resource'])
        pending_job_list[J.id] = J
        e = Event(J, row['a_time'], 0)
        event_list.append(e)
    event_list = sorted(event_list, key=operator.attrgetter('time'))
    state = System(12)
    sim_clock = 0
    event_counter = 0
    event: Event

    while len(event_list) != 0:
        event = event_list[event_counter]
        if event.typ == 3:
            sim_clock = event.time
            running_job_list, complete_job_list = runningToComplete(running_job_list, complete_job_list, event)
            state.update_cores(state.cores + event.job.cores)
            event_list.remove(event)
            event_list = sorted(event_list, key=operator.attrgetter('time'))
            print("event finished", event.job.id)
            event_counter = 0
            if len(event_list) == 0 and len(job_to_start_list) != 0:
                agreement_list = []
                negotiation_overhead = 0
                event_list = dispatcher(job_to_start_list, pending_job_list, running_job_list, event_list,
                                        agreement_list, queued_job_list, sim_clock, negotiation_overhead)
        else:
            if sim_clock >= event.time:
                state, event_counter, event_list = create_initial_schedule(event, state, job_to_start_list, sim_clock,
                                                                           event_counter, event_list, queued_job_list,
                                                                           pending_job_list, running_job_list)
            elif sim_clock < event.time:
                event_list, sim_clock = scheduler(job_to_start_list, pending_job_list, running_job_list, event_list,
                                                  queued_job_list, state, sim_clock)
                sim_clock = event.time
                state, event_counter, event_list = create_initial_schedule(event, state, job_to_start_list, sim_clock,
                                                                           event_counter, event_list, queued_job_list,
                                                                           pending_job_list, running_job_list)
    for key, value in complete_job_list.items():
        print(value.id, value.a_time, value.s_time, value.c_time)


if __name__ == '__main__':
    main()
