# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
from Class import Job, Event, System
import queue as q
from typing import Dict
import operator

def jobEntry(job_to_start_list, job, event, state, event_counter, event_list, sim_clock):
    job_to_start_list[job.id] = job
    state.update_cores(state.cores - job.current_resources)
    job.updateCompletion(sim_clock)
    job.updateStart(sim_clock)
    event_list.remove(event)
    return state, event_counter

def create_intitial_schedule(event, state, job_to_start_list, sim_clock, event_counter, event_list, queued_job_list, pending_job_list, running_job_list):
    job = event.job
    if (job.current_resources <= state.cores):
        print("job allocation", job.id)
        state, event_counter = jobEntry(job_to_start_list, job, event, state, event_counter, event_list, sim_clock)
    else:
        if (job.type == 2):
            if(job.min_resource <= state.cores):
                job.current_resources = job.min_resource
                print("job allocation", job.id)
                state, event_counter = jobEntry(job_to_start_list, job, event, state, event_counter, event_list,
                                                sim_clock)
            else:
                queued_job_list[job.id] = job
                print("job queued", job.id)
                event_counter = event_counter + 1

        else:
            queued_job_list[job.id] = job
            print("job queued", job.id)
            event_counter = event_counter + 1
    if(len(event_list) == 0):
        event_list = schedular(job_to_start_list, pending_job_list, running_job_list, event_list)
        event_counter = 0
    return state, event_counter, event_list



def schedular(job_to_start_list, pending_job_list, running_job_list, event_list):
    print("size of job to start list", len(job_to_start_list))
    for key, value in job_to_start_list.items():
        value.updateStatus("running")
        running_job_list[value.id] = value
        e = Event(value, value.c_time, 3)
        event_list.append(e)
        print("completion event created with id & time", e.job.id, e.job.c_time)
        pending_job_list.pop(value.id)
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
        J = Job(row['type'], row['a_time'], row['cores'], row['exe_time'], row['id'], row['min_resource'], row['max_resource'])
        pending_job_list[J.id] = J
        e = Event(J, row['a_time'], 0)
        event_list.append(e)
    event_list = sorted(event_list, key=operator.attrgetter('time'))
    state = System(12)
    sim_clock = 0
    event_counter = 0
    event: Event

    while(len(event_list) != 0):
        event = event_list[event_counter]
        if(event.typ == 3):
            sim_clock = event.time
            running_job_list, complete_job_list = runningToComplete(running_job_list, complete_job_list, event)
            state.update_cores(state.cores + event.job.cores)
            event_list.remove(event)
            event_list = sorted(event_list, key=operator.attrgetter('time'))
            print("event finished", event.job.id)
            event_counter = 0
            if(len(event_list) == 0 and len(job_to_start_list) != 0):
                event_list = schedular(job_to_start_list, pending_job_list, running_job_list, event_list)
        else:
            if(sim_clock >= event.time):
                state, event_counter, event_list = create_intitial_schedule(event, state, job_to_start_list, sim_clock, event_counter, event_list, queued_job_list,pending_job_list, running_job_list)
            elif(sim_clock < event.time):
                event_list = schedular(job_to_start_list, pending_job_list, running_job_list, event_list)
                sim_clock = event.time
                state, event_counter, event_list = create_intitial_schedule(event, state, job_to_start_list, sim_clock, event_counter, event_list, queued_job_list, pending_job_list, running_job_list)


    for key, value in complete_job_list.items():
        print(value.id, value.a_time, value.s_time, value.c_time)

if __name__ == '__main__':
    main()