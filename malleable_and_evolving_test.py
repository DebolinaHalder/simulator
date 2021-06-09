# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
from Class import Job, Event, System, Agreement, Phase
from typing import Dict
import operator
import random
import numpy as np
import sys
import math



max_no_of_phase = 4
min_no_of_phase = 2
max_time = 41
min_time = 40
exp_probability = 0.8

submission_event = 0
expansion_event = 1
shrinkage_event = 2
completion_event = 3



rigid = 1
malleable = 2
evolving = 3

max_expansion_percentage = 31
min_expansion_percentage = 30
max_shrinkage_percentage = 31
mim_shrinkage_percentage = 30


input_location = "workload/rigid"
output_location = "result/rigid"
#res_proc = open(r"result3/mal/mal10_2016_15k_40k.txt", "w")

random.seed(123)

def jobEntry(job_to_start_list, job, event, state, event_counter, event_list, sim_clock):
    print("job added in job to start list", job.id, "at time", sim_clock)
    job_to_start_list[job.id] = job
    state.update_cores(state.cores - job.current_resources)
    job.updateCompletion(sim_clock)
    job.updateStart(sim_clock)
    event_list.remove(event)
    return state, event_counter, event_list


def find_malleable(running_job_list, sim_clock):
    running_malleable_job = []
    for key, value in running_job_list.items():
        if value.type == 2:
            value.calculateRemaining()
            value.remaining_time = value.remaining_time - (sim_clock - value.s_time)
            running_malleable_job.append(value)
    running_malleable_job = sorted(running_malleable_job, key=operator.attrgetter('remaining_resources'), reverse=True)
    return running_malleable_job


def create_phases(job):
    no_of_phase = random.randint(min_no_of_phase, max_no_of_phase)
    phase = []
    for i in range(no_of_phase):
        s = np.random.binomial(1, exp_probability)
        time = random.randint(min_time, max_time)

        if s == 1:
            percentage = random.randint(min_expansion_percentage, max_expansion_percentage)
            cores = math.ceil(job.current_resources * percentage / 100)
            p = Phase(expansion_event, cores, time)
        else:
            percentage = random.randint(mim_shrinkage_percentage, max_shrinkage_percentage)
            cores = math.ceil(job.current_resources * percentage / 100)
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
                            pending_job_list, running_job_list, processor_df):
    job = event.job
    if job.current_resources <= state.cores:
        print("job allocation", job.id)
        state, event_counter, event_list = jobEntry(job_to_start_list, job, event, state, event_counter, event_list,
                                                    sim_clock)
        for key in job_to_start_list:
            if key in queued_job_list:
                queued_job_list.pop(key)
    else:
        if job.type == malleable:
            if job.min_resource <= state.cores:
                job.current_resources = job.min_resource
                print("job allocation with min resource", job.id)
                state, event_counter, event_list = jobEntry(job_to_start_list, job, event, state, event_counter,
                                                            event_list,
                                                            sim_clock)
                for key in job_to_start_list:
                    if key in queued_job_list:
                        queued_job_list.pop(key)
            else:
                queued_job_list[job.id] = job
                print("job queued malleable", job.id, job.type)
                event_counter = event_counter + 1

        else:
            queued_job_list[job.id] = job
            print("job queued", job.id, job.type, sim_clock)
            event_counter = event_counter + 1
    if len(event_list) == 0:
        agreement_list = []
        negotiation_overhead = 0
        event_list, processor_df = dispatcher(job_to_start_list, pending_job_list, running_job_list, event_list, agreement_list,
                                queued_job_list, sim_clock, negotiation_overhead, state, processor_df)
        event_counter = 0
    return state, event_counter, event_list


def find_agreement_evolving(running_malleable_job, sim_clock, event, state):
    negotiation_overhead = 0
    print("core needed", event.core)
    print("core existing", state.cores)
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
            state.cores = state.cores + i.modify_cores
        a = Agreement('e', event.core, event.job)
        agreement_list.append(a)
        state.cores = state.cores - event.core
        print("core current", state.cores)
    else:
        agreement_to_be.clear()
    negotiation_overhead = negotiation_overhead + getNegotiationCost()
    #running_malleable_job = sorted(running_malleable_job, key=operator.attrgetter('remaining_resources'))
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
        running_malleable_job = sorted(running_malleable_job, key=operator.attrgetter('remaining_resources'), reverse=True)
    for key in job_to_start_list:
        if key in queued_job_list:
            queued_job_list.pop(key)
    running_malleable_job = sorted(running_malleable_job, key=operator.attrgetter('no_of_shrinkage'), reverse=True)
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


def scheduler(job_to_start_list, pending_job_list, running_job_list, event_list, queued_job_list, state, sim_clock, processor_df):
    idle_processes = state.total - state.cores
    agreement_list = []
    negotiation_overhead = 0
    if idle_processes:
        running_malleable_job = []
        running_malleable_job = find_malleable(running_job_list, sim_clock)
        if len(running_malleable_job) != 0:
            agreement_list, job_to_start_list, sim_clock, negotiation_overhead, state = find_agreement(queued_job_list,
                                                                                                running_malleable_job,
                                                                                                job_to_start_list,
                                                                                                state, event_list,
                                                                                                sim_clock)

    event_list, processor_df = dispatcher(job_to_start_list, pending_job_list, running_job_list, event_list, agreement_list,
                            queued_job_list, sim_clock, negotiation_overhead, state, processor_df)
    return event_list, sim_clock, state, processor_df


def find_event(event_list, job):
    for i in event_list:
        if i.job == job:
            return i


def expansion(cores, sim_clk, running_job_list, negotiation_overhead, job, event_list):
    id = job.id
    p = Phase(expansion_event, cores+job.current_resources, sim_clk)
    #running_job_list[id].phase_list.append(p)
    running_job_list[id].no_of_expansion = running_job_list[id].no_of_expansion + 1
    time = running_job_list[id].updateExpansion(cores, sim_clk, negotiation_overhead)
    p.set_remaining(time - sim_clk)
    print("remaining time", p.rem_time)
    running_job_list[id].phase_list.append(p)
    event = find_event(event_list, job)
    index = event_list.index(event)
    event_list[index].job.c_time = time
    event_list[index].job.phase_list = running_job_list[id].phase_list
    event_list[index].job.no_of_expansion = running_job_list[id].no_of_expansion
    event_list[index].time = event_list[index].job.c_time
    print("job expansion", job.id,"with cores", cores, "at time", sim_clk)
    print("new completion time", time)
    return event_list


def shrinkage(cores, sim_clk, running_job_list, negotiation_overhead, job, event_list):
    id = job.id
    #running_job_list[id].phase_list.append(p)
    p = Phase(shrinkage_event, job.current_resources - cores, sim_clk)
    running_job_list[id].no_of_shrinkage = running_job_list[id].no_of_shrinkage + 1
    time = running_job_list[id].updateSkrinkage(cores, sim_clk, negotiation_overhead)
    p.set_remaining(time - sim_clk)
    running_job_list[id].phase_list.append(p)
    event = find_event(event_list, job)
    index = event_list.index(event)
    event_list[index].job.c_time = time
    event_list[index].job.phase_list = running_job_list[id].phase_list
    event_list[index].job.no_of_expansion = running_job_list[id].no_of_expansion
    event_list[index].time = event_list[index].job.c_time
    print("job skrinked", job.id, "with cores", cores, "at time", sim_clk)
    print("new completion time", time)
    return event_list


def dispatcher(job_to_start_list, pending_job_list, running_job_list, event_list, agreement_list, queued_job_list,
               sim_clock, negotiation_overhead, state, processor_df):
    for i in agreement_list:
        id = i.job.id
        if i.type == 'e':
            event_list = expansion(i.modify_cores, sim_clock, running_job_list, negotiation_overhead, i.job, event_list)

        elif i.type == 's':
            event_list = shrinkage(i.modify_cores, sim_clock, running_job_list, negotiation_overhead, i.job, event_list)

    for key, value in job_to_start_list.items():
        value.updateStatus("running")
        running_job_list[value.id] = value
        print("here", value.id)
        e = Event(value, value.c_time, 3)
        event_list.append(e)
        p = Phase(submission_event, value.cores, sim_clock)
        p.set_remaining(value.c_time - sim_clock)
        running_job_list[value.id].phase_list.append(p)
        if value.type == evolving:
            event_list = create_evolving_events(event_list, value, sim_clock)
        print("completion event created with id & time", e.job.id, e.time, "with resource", value.current_resources)
        pending_job_list.pop(value.id)
        if value.id in queued_job_list:
            queued_job_list.pop(value.id)
    event_list = sorted(event_list, key=operator.attrgetter('time'))
    job_to_start_list.clear()
    value = (state.total - state.cores, sim_clock, len(running_job_list))
    processor_df = processor_df.append(
        {'cores': state.total - state.cores, 'time': sim_clock, 'running_job_len': len(running_job_list)}, ignore_index=True)
    #res_proc.write(str(value) + '\n')
    return event_list, processor_df


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
        if type == expansion_event:
            total_cores = cores + J.current_resources
        else:
            if cores == J.current_resources:
                return event_list
            total_cores = J.current_resources - cores
        if total_cores < J.min_resource:
            return event_list
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
    data = data.iloc[0:200:]
    for index, row in data.iterrows():
        J = Job(row['type'], row['S_ime'], row['Processors'], row['R_time'], row['id'], row['Min_resource'],
                row['Max_resource'])
        if J.type == evolving:
            phase_rq = create_phases(J)
            J.phase_req = phase_rq
        pending_job_list[J.id] = J
        e = Event(J, row['S_ime'], 0)
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


def get_average_result(dataframe):
    W_time = dataframe['Wait_time']
    Turn_time = dataframe['Turn_around_time']
    C_time = dataframe['Completion']
    A_time = dataframe['Arrival']
    E_time = dataframe['Exe_time']
    avg_w_time = W_time.mean()
    avg_t_time = Turn_time.mean()
    avg_e_time = E_time.mean()
    span = C_time.max() - A_time.min()
    return avg_w_time, avg_t_time, span, avg_e_time


def calculate_utilization(complete_job_list, span, total_processor):
    total_cost = 0
    total_clk_cycle = span * total_processor
    for key, value in complete_job_list.items():
        cost = 0
        for i in range(0, len(value.phase_list)):
            if i == (len(value.phase_list) - 1):
                time = value.c_time - value.phase_list[i].time
            else:
                time = value.phase_list[i+1].time - value.phase_list[i].time
            cost = cost + value.phase_list[i].cores * time

        total_cost = total_cost + cost
    return total_cost/total_clk_cycle


def calculate_util2(processor_df, span, total_processors):
    cores = processor_df['cores'].values.tolist()
    time = processor_df['time'].values.tolist()
    cost = 0
    for i in range(len(time) - 1):
        cost += cores[i] * (time[i+1] - time[i])
    total = span * total_processors
    return cost/total


def main():
    pending_job_list: Dict[int, Job] = {}
    event_list = []
    running_job_list: Dict[int, Job] = {}
    complete_job_list: Dict[int, Job] = {}
    queued_job_list: Dict[int, Job] = {}
    job_to_start_list: Dict[int, Job] = {}
    pending_job_list, event_list = initialize_event("synthetic/workload12/rigid/workload_synthetic_rigid.csv", pending_job_list, event_list)
    #pending_job_list, event_list = initialize_event("shrinked/workload/mal/mal20_2016_15k_40k.csv", pending_job_list, event_list)

    total_processor = 85
    state = initialize_system(total_processor)

    sim_clock = 0
    event_counter = 0
    event: Event

    #f = open('debug.txt', 'w')
    #sys.stdout = f

    processor_df = pd.DataFrame(columns=['cores', 'time', 'running_job_len'])

    while len(event_list) != 0:
        try:
            event = event_list[event_counter]
        except IndexError:
            if len(job_to_start_list) != 0:
                event_list, sim_clock, state, processor_df = scheduler(job_to_start_list, pending_job_list, running_job_list,
                                                         event_list,
                                                         queued_job_list, state, sim_clock, processor_df)
                event_counter = 0
            else:
                print("check what is wrong")
                break
        print("current time", sim_clock, "event time", event.time, "job", event.job.id)
        if event.typ == expansion_event or event.typ == shrinkage_event:
            print("evolving event")
            if len(job_to_start_list) != 0:
                event_list, sim_clock, state, processor_df = scheduler(job_to_start_list, pending_job_list, running_job_list, event_list,
                                            queued_job_list, state, sim_clock, processor_df)
                event_counter = 0
            sim_clock = event.time
            cores = event.core
            job = event.job
            event_list.remove(event)
            negotiation_overhead = getNegotiationCost()
            if event.typ == shrinkage_event:
                shrinkage(cores, sim_clock, running_job_list, negotiation_overhead, job, event_list)
                state.cores = state.cores + event.core

            elif event.typ == expansion_event:
                if event.core <= state.cores:
                    expansion(cores, sim_clock, running_job_list, negotiation_overhead, job, event_list)
                    state.cores = state.cores - event.core
                else:
                    running_malleable_job = find_malleable(running_job_list, sim_clock)
                    sim_clock, negotiation_overhead, agreement_list, state = find_agreement_evolving(running_malleable_job, sim_clock, event, state)
                    event_list, processor_df = dispatcher(job_to_start_list, pending_job_list, running_job_list, event_list,
                                            agreement_list, queued_job_list, sim_clock, negotiation_overhead, state, processor_df)
                    print("core current", state.cores)
            else:
                print("couldn't expand job", job.id, "at time", sim_clock)
            event_list = create_evolving_events(event_list, running_job_list[event.job.id], sim_clock)
            event_counter = 0

        elif event.typ == completion_event:
            if len(job_to_start_list) != 0:
                event_list, sim_clock, state, processor_df = scheduler(job_to_start_list, pending_job_list, running_job_list,
                                                         event_list,
                                                         queued_job_list, state, sim_clock, processor_df)
                event_list = sorted(event_list, key=operator.attrgetter('time'))
                event_counter = 0
            else:
                sim_clock = event.time
                running_job_list, complete_job_list = runningToComplete(running_job_list, complete_job_list, event)
                state.cores = state.cores + event.job.current_resources
                event_list.remove(event)
                event_list = clear_list(event_list, event.job)
                event_list = sorted(event_list, key=operator.attrgetter('time'))
                print("event finished", event.job.id, "at time", sim_clock)
                print("remaining cores", state.cores)
                event_counter = 0
                if len(event_list) == 0 and len(job_to_start_list) != 0:
                    agreement_list = []
                    event_list, processor_df = dispatcher(job_to_start_list, pending_job_list, running_job_list, event_list,
                                            agreement_list, queued_job_list, sim_clock, 0, state, processor_df)
                else:
                    processor_df = processor_df.append({'cores': state.total - state.cores, 'time': sim_clock,
                                                        'running_job_len': len(running_job_list)}, ignore_index=True)
        else:
            if sim_clock >= event.time:
                state, event_counter, event_list = create_initial_schedule(event, state, job_to_start_list, sim_clock,
                                                                           event_counter, event_list, queued_job_list,
                                                                           pending_job_list, running_job_list, processor_df)
            elif sim_clock < event.time:
                if len(job_to_start_list) != 0:
                    event_list, sim_clock, state, processor_df = scheduler(job_to_start_list, pending_job_list, running_job_list, event_list,
                                                  queued_job_list, state, sim_clock, processor_df)
                if sim_clock < event.time:
                    sim_clock = event.time
                event_counter = 0
        event_list = sorted(event_list, key=operator.attrgetter('time'))


    print("length of complete job list", len(complete_job_list))
    print("length of running job list", len(running_job_list))
    print("length of pending job list", len(pending_job_list))
    print("length of queued job list", len(queued_job_list))
    print("length of event list", len(event_list))
    processor_df_all = processor_df.drop_duplicates()
    processor_df = processor_df_all.drop_duplicates(subset='time', keep='last')
    result_df = pd.DataFrame(columns = ['id', 'Arrival', 'Start','Completion','No_of_expansion', 'No_of_shrinkage', 'Wait_time', 'Turn_around_time', 'Exe_time'])
    for key, value in complete_job_list.items():
        #print(value.id, value.a_time, value.s_time)
        result_df=result_df.append({'id': value.id, 'Arrival': value.a_time, 'Start': value.s_time, 'Completion': value.c_time, 'No_of_expansion': value.no_of_expansion, 'No_of_shrinkage': value.no_of_shrinkage, 'Wait_time': value.s_time - value.a_time, 'Turn_around_time': value.c_time - value.a_time, 'Exe_time':value.c_time - value.s_time}, ignore_index=True)
    #result_df.to_csv('shrinked/result/mal/mal20_2016_15k_40k.csv', index=False)
    #processor_df.to_csv('shrinked/result/mal/processor_mal20_2016_15k_40k.csv', index=False)
    #res_avg = open(r"shrinked/result/mal/average_mal20_2016_15k_40k.txt", "w")
    avg_wait_time, avg_turn_time, span, avg_run_time = get_average_result(result_df)
    utilization = calculate_util2(processor_df, span, total_processor)
    #res_avg.write(str(avg_wait_time)+'\n')
    #res_avg.write(str(avg_turn_time)+'\n')
    #res_avg.write(str(span)+'\n')
    #res_avg.write(str(utilization)+'\n')
    #res_avg.write(str(avg_run_time) + '\n')
    print(avg_wait_time, avg_turn_time, span, utilization, avg_run_time)
    #res_avg.close()
    #res_proc.close() hi I am Jento


if __name__ == '__main__':
    main()
