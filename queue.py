# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
from Class import Job, Event, System
import queue as q
from typing import Dict
import operator

def sortClass(j):
    return



def schedular(pending_job_list, running_job_list, complete_job_list, event, sim_clock, state, event_counter, event_list):
    job : Job
    job = event.job
    if(job.cores <= state.cores):
        state.update_cores(state.cores - job.cores)
        job.updateStatus("running")
        job.updateCompletion(sim_clock)
        job.updateStart(sim_clock)
        running_job_list[job.id] = job
        e = Event(job, job.c_time,3)
        event_list.append(e)
        pending_job_list.pop(job.id)
        event_list.remove(event)
        event_list = sorted(event_list, key=operator.attrgetter('time'))
    else:
        event_counter = event_counter + 1
    return pending_job_list, running_job_list, complete_job_list, event, sim_clock, state, event_counter, event_list




def runningToComplete(running_job_list, complete_job_list, event):
    Job = event.job
    Job.updateStatus("completed")
    running_job_list.pop(Job.id)
    complete_job_list[Job.id] = Job
    return running_job_list, complete_job_list

def updateSystemUp(state, Job):
    state.update_cores(state.cores + Job.cores)
    return state





# Press the green button in the gutter to run the script.
def main():
    pending_job_list: Dict[int, Job] = {}
    event_list = []
    running_job_list: Dict[int, Job] = {}
    complete_job_list: Dict[int, Job] = {}
    data = pd.read_csv("workload.csv")
    for index, row in data.iterrows():
        J = Job(row['type'], row['a_time'], row['cores'], row['exe_time'], row['id'], row['min_resource'], row['max_resource'])
        pending_job_list[J.id] = J
        e = Event(J, row['a_time'], 0)
        event_list.append(e)
    event_list = sorted(event_list, key=operator.attrgetter('time'))
    print(len(event_list))
    state = System(12)
    sim_clock = 0
    event_counter = 0
    event: Event
    while(len(event_list) != 0):
        event = event_list[event_counter]
        if(event.typ == 3):
            sim_clock = event.time
            running_job_list, complete_job_list = runningToComplete(running_job_list, complete_job_list, event)
            state = updateSystemUp(state, event.job)
            event_list.remove(event)
            event_counter = 0
        else:

            if(sim_clock < event.time):
                sim_clock = event.time
            pending_job_list, running_job_list, complete_job_list, event, sim_clock, state, event_counter, event_list = schedular(pending_job_list, running_job_list, complete_job_list, event, sim_clock, state, event_counter, event_list)
    for key, value in complete_job_list.items():
        print(value.id, value.a_time, value.s_time, value.c_time)

if __name__ == '__main__':
    main()