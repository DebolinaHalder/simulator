from typing import Dict
import random
def modify(tel):
    tel['guido'] = 4127
    del tel['sape']
def main():
    x = random.uniform(0.5, 0.85)
    print(x)

def find_agreement(queued_job_list, running_malleable_job, job_to_start_list, state, event_list, sim_clock):
    agreement_list = []
    agreement_to_be = []
    for key, value in queued_job_list.items():
        needed = value.current_resources
        for i in running_malleable_job:
            if (needed == 0):
                break
            if (i.remaining_resources >= needed and needed != 0):
                a = Agreement('s', needed, i)
                agreement_to_be.append(a)
                i.remaining_resources = i.remaining_resources - needed
                needed = 0
                state.cores = state.cores + needed
                e = find_event(event_list, value)
                event_counter = 0
                state, event_counter = jobEntry(job_to_start_list, value, e, state, event_counter, event_list,
                                                sim_clock)
        running_malleable_job = sorted(running_malleable_job, key=operator.attrgetter('remaining_resources'))

    return agreement_list, job_to_start_list
main()